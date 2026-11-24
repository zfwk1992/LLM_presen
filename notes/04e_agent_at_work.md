# 04e · 一个 Agent 的实际工作过程

![An agent at work](../llm_agent_animations_single_page/04e_agent_at_work.gif)

> **一句话**：你只发了一句话。Agent 用了 6 次 LLM 调用、5 次工具执行，自己决定去读哪些文件、查规范的哪一段，最后给出答案。模型本身从头到尾没有打开过任何文件。

## 场景

你对 Agent 说：

```
Analyze how DCM is integrated in this project.
```

项目里有这些东西：

| 文件 | 是什么 | 一开始在不在提示词里 |
|---|---|---|
| `CLAUDE.md` | 项目说明 | **全文在** |
| `skills/dcm-guide/SKILL.md` | 分析 Dcm 的方法 | 只有一行简介 |
| `skills/misra-check/SKILL.md` | MISRA 规则检查 | 只有一行简介 |
| `docs/AUTOSAR_SWS_Dcm.pdf` | DCM 规范，600 页 | 不在 |
| `config/Dcm.arxml` | Dcm 的配置 | 不在 |
| `src/Dcm/Dcm_Dsl.c`、`Dcm_Dsp.c` | Dcm 的源码 | 不在 |
| `src/PduR/PduR_Cfg.c` | PDU 路由配置 | 不在 |
| 其余 214 个文件 | 项目的其他部分 | 不在 |

这张表本身就是一个重点：**项目里的大部分内容一开始都不在提示词里。** Agent 需要什么，就通过工具去取什么。

## 画面布局

- **左边 · YOUR PROJECT (on disk)**：磁盘上的文件。被工具访问到的那一行会闪一下橙色，并留下一个标记（loaded、read、searched、3 passages）。
- **中间 · WHAT THE AGENT DOES**：每一次 LLM 调用一张卡片。卡片里三行：
  - 引号里的话：模型的思考
  - **asks for**（橙色）：模型写出的工具调用
  - **harness ran it**（绿色）：harness 执行后拿回的结果
- **右边 · THE PROMPT (context window)**：提示词的长条，每执行一次工具就长一截。

## 逐步解读

| 时间 | 字幕 | 发生了什么 |
|---|---|---|
| 0.8 s | ① One request. Project notes and skill descriptions are already in the prompt | 你的请求出现。左边 CLAUDE.md 标着 "in the prompt"，两个 skill 标着 "1 line in prompt"。右边的长条已有 14.7k |
| 2.6 s | ② Call 1: the model sees a matching skill and asks to load it | 模型看到 dcm-guide 的简介与任务相关，要求加载它 |
| 6.0 s | ③ Call 2: following the skill, it asks to read the Dcm configuration | 模型按 skill 里的清单，要求读取 Dcm 的配置 |
| 9.2 s | ④ Calls 3 and 4: it asks to search the routing, then to read the code | 模型要求搜索 PduR 的路由，然后读取会话层的代码 |
| 15.6 s | ⑤ Call 5: it asks the spec. Only 3 passages of 600 pages come back | 模型要求查规范；600 页里只有 3 段进入提示词 |
| 18.8 s | ⑥ Call 6: no tool call this time. It writes the answer and the loop ends | 模型不再要求工具，直接写出答案 |

六次调用的详细内容：

| 调用 | 模型的思考 | 模型写出的工具调用 | harness 执行的结果 | 提示词 |
|---|---|---|---|---|
| 1 | A skill matches this task. Load it first. | `Skill("dcm-guide")` | SKILL.md 载入：一份 4 步的检查清单 | 14.7k → 16.8k |
| 2 | Checklist step 1: find the Dcm configuration. | `Read("config/Dcm.arxml")` | 3 个协议，配置了 14 个 UDS 服务 | → 23.1k |
| 3 | How do requests reach Dcm? Check the routing. | `Grep("Dcm", "src/PduR/")` | PduR_Cfg.c：2 个 PDU 路由到 Dcm | → 23.9k |
| 4 | Now the session handling code. | `Read("src/Dcm/Dcm_Dsl.c")` | 612 行 | → 33.3k |
| 5 | Compare with what the standard requires. | `search_spec("Dcm PduR interface")` | SWS_Dcm 里的 3 段，共 600 页 | → 35.1k |
| 6 | I have enough. Write the answer. | 无 | — | 结束 |

最终答案：

```
Dcm is reached through PduR (2 routed PDUs). Dsl handles sessions,
Dsp the 14 UDS services. Configured in Dcm.arxml. Matches SWS_Dcm §7.2.
```

结尾的深色框：**6 LLM calls · 5 tool runs by the harness · the model never opened a file itself**

## 这一页把前面哪些内容串起来了

| 画面上的现象 | 对应的概念 | 讲解在哪一页 |
|---|---|---|
| CLAUDE.md 一开始就在提示词里 | 每次会话都加载的项目记忆 | 04a、08 |
| skill 一开始只有一行，调用 1 之后才载入全文 | 三级按需加载 | 08 |
| 每张卡片是一次 LLM 调用 | 外层循环 | 04c |
| 卡片里的工具调用是模型"写"出来的 | 工具调用只是文字 | 04b、05 |
| 橙色箭头从卡片指向文件 | harness 执行工具 | 05 |
| 600 页规范只进来 3 段 | 检索，只取相关的部分 | 06 |
| `search_spec` 这样的工具从哪来 | 可以由 MCP server 提供 | 07 |
| 右边的长条越来越长 | 上下文只增不减 | 09 |
| 有些文件始终没被打开 | Agent 自己决定需要什么 | 04d |

所以这一页适合作为第二章的收尾，或者作为第三章（RAG、MCP、Skills、上下文工程）的开场：先让听众看到一次完整的过程，再逐个展开其中的机制。

## 值得指给听众看的四个细节

**1. 模型的第一步是加载 skill，而不是直接去翻代码。** 它在提示词里看到 `dcm-guide` 的一行简介，判断和任务相关，于是先要求加载。之后的步骤是照着 skill 里的清单走的（调用 2 的思考是 "Checklist step 1"）。这就是 skill 的作用：把团队的做事方法交给模型。

**2. 没有人规定这六步。** 先读配置、再查路由、再读代码、最后对照规范，这个顺序是模型每一轮根据上一轮的结果自己决定的。

**3. 600 页的规范只进来了 3 段。** 整份规范放不进上下文，也没有必要。`search_spec` 背后是 06 讲的检索：只把最相关的段落取回来。

**4. 有些文件始终没有被打开。** 画面结束时，`Dcm_Dsp.c` 和其余 214 个文件标着 "never opened"，`misra-check` 这个 skill 也始终只有一行简介。Agent 只取了它认为需要的东西。

## 一个容易被问到的问题

**Q：它没读 Dcm_Dsp.c，怎么知道 Dsp 处理 14 个 UDS 服务？**
这个信息来自 `Dcm.arxml`（配置里列出了服务）和 skill 的说明。这也提醒我们：Agent 的结论只建立在它实际读到的内容上。如果答案需要更可靠，可以要求它把相关文件都读一遍，或者提高 effort（见 10b）。

## 画面上的简化

- **token 数量是示意值**，画面上有标注。
- **`search_spec` 是为了举例虚构的工具名**。实际项目里它可以是一个 MCP server 提供的检索工具，也可以是 Agent 直接用 Grep 在文档里搜索。
- **每次调用只画了一个工具**，实际上模型可以在一次回复里同时请求多个。
- **模型的"思考"只画了一句话**，实际可能更长。
- **文件名和内容是为了例子编的**，但结构（Dsl 负责会话、Dsp 负责服务处理、经 PduR 路由）符合 AUTOSAR 的 Dcm 架构。

## 自测

<details>
<summary>1. 开始时，CLAUDE.md、dcm-guide 的 SKILL.md、DCM 规范，各自有多少内容在提示词里？</summary>

CLAUDE.md 全文在；SKILL.md 只有一行简介；规范完全不在。
</details>

<details>
<summary>2. 这次任务一共调用了几次 LLM？执行了几次工具？为什么差一次？</summary>

6 次 LLM 调用，5 次工具执行。最后一次调用模型没有请求工具，直接写出了答案，循环因此结束。
</details>

<details>
<summary>3. 600 页的规范是怎么被用上的？</summary>

模型请求了一个检索工具，harness 执行后只把最相关的 3 段放进提示词。
</details>

<details>
<summary>4. 是谁决定先读配置、再查路由的？</summary>

模型。它每一轮根据提示词里已有的内容（包括 skill 的清单和上一步的结果）决定下一步。
</details>
