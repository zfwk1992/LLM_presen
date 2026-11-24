# 05 · Tool Calling（工具调用）

![Tool calling](../llm_agent_animations_single_page/05_tool_calling.gif)

> **一句话**：模型从不执行任何东西。它只是写出一段结构化的文本说"我想调用这个工具"，真正去执行的是 harness。

## 在演讲里的位置

这一页把 04 里的 "Act → Observe" 放大成慢动作。它澄清整场演讲里最常见的误解：模型"能运行代码""能访问文件"。准确的说法是：模型能**请求**，程序来**执行**。这一页讲清楚了，后面的 MCP（07）才讲得通，因为 MCP 只是给 harness 提供更多可执行的工具。

## 画面布局

- **左边**：Context window，标题旁写着 "what the model sees"（模型看到的东西）。所有消息按顺序堆在这里。
- **右边**：三个角色。
  - **LLM**：reads the context · predicts next tokens
  - **Harness (Claude Code)**：parses tool_use · runs the tool · returns result
  - **Tool: run_tests**：e.g. ctest -R Com on your machine

## 动画逐步解读

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0–3 s | ① Tool definitions sit in the context | 上下文里出现工具定义 | "模型知道有什么工具，是因为说明书就写在上下文里" |
| 3–5 s | The user asks a question | 用户消息：Why does the Com unit test fail? | "用户问了一个模型自己答不了的问题" |
| 5–9 s | ② The model answers with a structured tool_use block | LLM 亮起，一段 JSON 被逐字打出 | "模型的回答不是一句话，而是一段固定格式的 JSON" |
| 9.5–13 s | ③ The harness parses it and actually runs the tool | Harness 亮起，再到 Tool，出现转圈 | "程序读懂这段 JSON，在你的机器上真的运行测试" |
| 13.5–16 s | ④ The result is appended to the context as a new message | 结果作为新消息出现在上下文里 | "运行结果写回上下文" |
| 17–20 s | ⑤ The model continues, now with real data | LLM 再次亮起，给出回答 | "模型再读一遍上下文，这次有了真实数据" |
| 约 20 s | 深色框 | The model never executes anything, it only writes structured text. | **这一页的结论，停一下再说** |

## 上下文里的四段内容

### ① 工具定义

```json
tools: [{"name": "run_tests",
  "description": "Run unit tests of a module",
  "input_schema": {"type": "object",
    "properties": {"module": {"type": "string"}}}
}]
```

一个工具由三部分描述：

- **name**：工具名。
- **description**：用自然语言说明这个工具是干什么的。模型靠这段话判断什么时候该用它。
- **input_schema**：参数的格式，用 JSON Schema 描述。这里是"一个对象，有一个字符串类型的 `module` 字段"。

### ② 模型的回复

```json
{"type": "tool_use",
 "name": "run_tests",
 "input": {"module": "Com"}}
```

这段文字和普通回答一样，是用 03 的循环一个 token 一个 token 生成出来的。模型根据问题里的 "Com unit test" 和工具说明，自己填出了 `"module": "Com"`。

### ④ 工具结果

```json
{"type": "tool_result",
 "content": "FAILED test_Com_SendSignal:
   expected 0x12, got 0x00"}
```

注意画面上这条消息的标签是 **USER · TOOL_RESULT**。在 API 里，工具结果是以用户这一方的身份发回给模型的。从模型的角度看，对话只有两方：它自己，和"外面的世界"。

### ⑤ 最终回答

```
The signal is packed at the wrong byte offset …
```

这个回答里的事实（期望 0x12，实际 0x00）来自真实的测试输出，不是模型猜的。

## 需要真正搞懂的概念

### 三个角色的分工

| 角色 | 做什么 | 不做什么 |
|---|---|---|
| LLM | 读上下文，决定是否需要工具，写出调用请求 | 不执行任何东西 |
| Harness | 解析请求，检查权限，执行工具，把结果写回上下文 | 不做判断，不决定调用哪个工具 |
| Tool | 真正干活的程序或命令 | 不知道 LLM 的存在 |

一个好记的说法：**模型负责"想要"，harness 负责"去做"**。

### 为什么这样设计

- **安全**：执行权在 harness 手里。它可以拒绝、可以先问用户、可以限制范围。模型写出 `rm -rf /` 并不会发生任何事，除非 harness 决定执行它。
- **通用**：任何能用"名字 + 说明 + 参数格式"描述的东西都可以变成工具：运行命令、读文件、查数据库、调用内部系统。
- **模型无需改动**：增加新工具不需要重新训练模型，只需要在上下文里多放一段说明。

### 工具说明的质量很重要

模型选不选这个工具、参数填得对不对，完全取决于 `description` 和 `input_schema` 写得清不清楚。给模型写工具说明，和给新同事写接口文档是同一件事。

### 工具定义也占上下文

每个工具的说明都是 token，每一轮都要发给模型。工具装得越多，固定开销越大。这是 08（Skills 的按需加载）和 09（上下文管理）要解决的问题之一。

### 动画里省略的细节

- **调用 ID**：真实的 `tool_use` 带一个 `id`，`tool_result` 里用 `tool_use_id` 指回它，这样一次回复里同时调用多个工具时，结果能对得上。动画里省略了。
- **并行调用**：模型可以在一次回复里请求多个工具，harness 可以同时执行。

## 常见误解

- **"模型可以访问我的文件系统"**：模型不能。是 harness 在你的机器上读了文件，把内容作为文本交给模型。
- **"工具调用是一种特殊的模型能力"**：从机制上说，它就是生成特定格式的文本。模型在训练中学会了在合适的时候输出这种格式。
- **"模型看到的是工具的代码"**：看不到。它只看到名字、说明和参数格式，以及执行后返回的结果。

## 听众可能会问

**Q：模型写出的 JSON 格式错了怎么办？**
harness 会校验。不合格的话，把错误信息作为结果返回，模型下一轮通常会改正。

**Q：工具返回的内容里如果有恶意指令呢？**
这是真实的风险，叫提示注入（prompt injection）。工具结果对模型来说也是文本，可能被其中的内容误导。所以 harness 的权限控制很重要，高风险操作要有人确认。

**Q：这和 MCP 是什么关系？**
这一页讲的是模型和 harness 之间怎么交互。MCP 讲的是 harness 和外部系统之间怎么交互。07 展开。

**Q：这里的 harness 具体是什么？**
任何调用模型 API 并负责执行工具的程序。Claude Code 是一个，你自己用 SDK 写的脚本也可以是一个。

## 承上启下

- **上一页**：04 展示了循环，把工具调用当成一个黑盒。
- **这一页**：打开黑盒。
- **下一章**：模型现在能做事了，但它只知道训练数据里的东西和上下文里的东西。下一章讲怎样把更多知识和更多系统接进来。
- **过渡句**："到这里，我们有了一个能动手的 Agent。但它不了解我们公司的文档，也连不上我们的内部系统。接下来三页解决这两个问题。"

## 自测

<details>
<summary>1. 模型怎么知道有哪些工具可用？</summary>

工具的名字、说明和参数格式写在上下文里，模型每一轮都能读到。
</details>

<details>
<summary>2. 当模型"调用工具"时，模型实际输出的是什么？</summary>

一段结构化文本（`tool_use` 块），包含工具名和参数。它本身不产生任何副作用。
</details>

<details>
<summary>3. 工具结果以什么身份回到上下文？为什么？</summary>

以用户一方的消息（`tool_result`）。对模型来说，凡是不是它自己生成的内容，都来自对话的另一方。
</details>
