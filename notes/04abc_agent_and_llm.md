# 04a、04b、04c · Agent 和 LLM 到底是什么关系

这三页用同一个例子（你输入"调查 DCM 怎么工作"）把 Agent loop 和前面讲的 LLM 接起来。

![What the LLM actually receives](../llm_agent_animations_single_page/04a_one_big_prompt.gif)

![A tool call is just generated text](../llm_agent_animations_single_page/04b_tool_call_is_text.gif)

![Two loops](../llm_agent_animations_single_page/04c_two_loops.gif)

> **一句话**：LLM 还是那个只会预测下一个 token 的网络，一点没变。Agent 是它外面的一个普通程序（harness），反复做三件事：把所有内容拼成一个大提示词，调用 LLM，执行 LLM 写出来的工具调用并把结果拼回去。

## 先回答你的两个问题

### 问题一：context window 是不是就是一个一次性传入的大提示词？

**是的。**

你输入"调查 DCM 怎么工作"之后，Claude Code 不是只把这一句发给模型。它会把下面这些东西按顺序拼成**一条很长的 token 序列**，一次性送进网络：

| 部分 | 谁写的 | 大小（示意） |
|---|---|---|
| System prompt | Claude Code | 3,200 token |
| Tool definitions（Read、Grep、Bash、Skill、MCP 工具 …） | Claude Code 和各个 MCP server | 9,500 token |
| CLAUDE.md | 你，事先写好的项目说明 | 1,400 token |
| Skill list（每个 skill 一行简介） | 各个 skill 的作者 | 600 token |
| 之前的对话（如果有） | 你和模型 | — |
| **你这次输入的话** | **你** | **9 token** |

对模型来说，这就是一个提示词。它看到的是一串 token，并不知道哪一段是你打的、哪一段是系统加的（靠序列里的标记 token 区分角色）。所以可以这样理解：

**"context window" 就是提示词。你手打的只是其中很小的一部分，其余是 harness 自动拼上去的。**

然后按 02c 讲的那样：全部 token 变成向量，一起进入网络，做一次前向传播，得到第一个输出 token。

### 一处需要修正：skill 不是一开始就全文放进去的

你设想的是"DCM 相关的 skill 都会放进提示词"。实际分两步：

1. **一开始**：提示词里只有每个 skill 的**一行简介**，比如 `dcm-guide: how the Dcm module is structured in this project`。全文不在里面。
2. **模型决定要用之后**：模型读到你的问题和这行简介，认为相关，于是写出一个工具调用"使用 dcm-guide 这个 skill"。harness 执行这个调用，从磁盘读出 SKILL.md 的全文，作为工具结果**追加**到提示词里。
3. **下一次调用 LLM 时**，SKILL.md 的全文才在提示词里。

这就是 08 那页讲的三级加载。04a 画面下方的绿色框写的就是这件事，04b 则把第 2 步完整演示了一遍。

### 问题二：Agent loop 和 LLM 是什么关系？

**LLM 是被调用的那个东西，Agent loop 是调用它的那个程序。**

| | LLM | Harness（Agent loop 的执行者） |
|---|---|---|
| 是什么 | 一个神经网络 | 一个普通程序，例如 Claude Code |
| 会做什么 | 给定一串 token，预测下一个 token | 拼提示词、调用 LLM、解析回复、执行工具、管理权限 |
| 能不能读文件、跑命令 | 不能 | 能 |
| 有没有记忆 | 没有，每次只看到这一次的提示词 | 有，它保存着完整的对话记录 |
| 循环的单位 | 一圈生成一个 token | 一圈是一次 LLM 调用加一次工具执行 |

两层循环是嵌套的：harness 每调用一次 LLM，LLM 内部就跑一遍 03 讲的生成循环，一个 token 一个 token 地把回复写出来。

## 04a：LLM 实际收到了什么（22.5 s）

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0.8 s | ① You type one short message | 左下角只有一张蓝色卡片 "Your message" | "你只打了一句话" |
| 3.6 s | ② The harness adds the rest: system prompt, tools, CLAUDE.md, skill list | 上方依次出现四张卡片 | "Claude Code 在前面加了这些东西，你平时看不到" |
| 7.0 s | ③ Everything is joined into one long token sequence | 五张卡片飞到中间，按 token 数量的比例叠成一根长条 | "它们被拼成一条长长的 token 序列。注意比例" |
| 11.6 s | ④ That whole sequence goes into the LLM at once | 长条右边的括号指向 LLM | "这一整条一次性进入网络，就是 02c 讲的那次前向传播" |
| 15.0 s | ⑤ Skills: only the one-line descriptions are in it, not the full text | 下方出现绿色说明框 | "skill 这时只有一行简介，全文还没进来" |
| 18.6 s | ⑥ The context window is the prompt: you typed a tiny part of it | 深色框：You typed 9 of its 14,709 tokens | 结论 |

这一页最有冲击力的是那根长条的比例：最下面那条细得几乎看不见的蓝线，是你打的那句话。

## 04b：工具调用只是生成出来的文字（24.0 s）

这一页把**一次** LLM 调用放慢来看。

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0.8 s | ① The whole prompt goes into the LLM | 左边是上一页那根长条，箭头指向 LLM | "上一页的整个提示词进入 LLM" |
| 3.2 s | ② The reply comes out one token at a time: one forward pass each | 深色框里 token 一个一个出现，LLM 框里的计数从 #1 涨到 #24；下方有一个回环箭头 | "回复是一个 token 一个 token 出来的。每出一个，就接回去再跑一遍" |
| 8.2 s | ③ The tokens spell a tool call. To the LLM it is just text | 下方橙色框把这串 token 翻译成人话 | "这些 token 拼起来是一个工具调用。对 LLM 来说它只是文字" |
| 11.2 s | ④ The LLM stops at \<end\>. Nothing has been executed yet | 出现红色的 `<end>`；下方两行字 | **停一下**："LLM 到这里就结束了。没有读任何文件，没有跑任何命令" |
| 14.0 s | ⑤ The harness reads the text and runs the tool on your machine | 右边依次出现 Harness、Tool: Skill、tool_result | "接下来是程序的事：解析这段文字，检查权限，执行" |
| 18.0 s | ⑥ The result is added to the prompt, ready for the next LLM call | 绿线从右下绕回左边的长条，长条变长，数字从 14,733 变成 16,833 | "结果被加回提示词。提示词变长了，准备下一次调用" |

模型生成的 24 个 token 是：

```
{"  type  ":  ·"  tool  _use  ",  ·"  name  ":  ·"  Skill  ",  ·"  input  ":  ·{"  skill  ":  ·"  dcm  -guide  "}}  <end>
```

连起来读就是：`{"type": "tool_use", "name": "Skill", "input": {"skill": "dcm-guide"}}`

左边长条下方的数字变化值得指给听众看：

| 时刻 | 提示词大小 | 多了什么 |
|---|---|---|
| 调用前 | 14,709 | — |
| LLM 写完回复 | 14,733 | 它自己写的 24 个 token |
| 工具执行完 | 16,833 | SKILL.md 的全文，约 2,100 token |

结尾的深色框：**The LLM writes. The harness acts.**

## 04c：两层循环（23.5 s）

这一页用泳道图把整个任务画出来。上面一条是 harness，下面一条是 LLM，时间从左往右。

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0.8 s | ① The harness builds the prompt and calls the LLM | "build prompt" → 箭头向下（14.7k）→ "LLM call #1" | "程序拼好提示词，调用 LLM" |
| 3.4 s | ② Inside the call, the generation loop writes a tool call token by token | LLM call #1 的框里亮带扫过，出现 `Skill("dcm-guide")` 和 "24 tokens, one by one" | "这个框里面就是上一页的全部内容" |
| 5.6 s | ③ The harness runs the tool and adds the result to the prompt | 箭头向上（tool_use）→ "run Skill" | "程序执行工具，结果加进提示词" |
| 8.0 s | ④ Then it calls the LLM again, sending everything so far | 箭头向下（16.8k）→ "LLM call #2" | "再调用一次 LLM，把到目前为止的所有内容都发过去" |
| 11.6 s | ⑤ This repeats until the reply contains no tool call | 第 3、第 4 次调用；最后一次的回复是文字，harness 显示答案 | "一直重复，直到回复里没有工具调用" |
| 18.4 s | ⑥ Two loops: the harness loops over LLM calls, the LLM loops over tokens | 上下各出现一行标注：OUTER LOOP、INNER LOOP；右下深色框 | 结论 |

四次调用的内容：

| LLM 调用 | 收到的提示词 | LLM 写了什么 | harness 做了什么 | 结果 |
|---|---|---|---|---|
| #1 | 14.7k | `Skill("dcm-guide")` | 读取 SKILL.md | +2.1k |
| #2 | 16.8k | `Grep("Dcm_")` | 在代码里搜索 | 38 处匹配，+1.2k |
| #3 | 18.0k | `Read("Dcm_Dsl.c")` | 读文件 | 612 行，+9.4k |
| #4 | 27.4k | 最终答案（文字） | 显示给你，循环结束 | — |

画面下半部分是四根横条，表示每次调用收到的提示词：灰色是起始的那部分，绿色和黄色是途中加进来的工具结果。每根都比上一根长，而且**每次都是从头全部重发**。

结尾的深色框：**Agent = a program calling the LLM in a loop. The LLM never changes and never acts. It only receives a longer prompt each time.**

## 把三页连起来讲

建议按 04a → 04b → 04c → 04d 的顺序：

1. **04a**："先看 LLM 到底收到了什么。"（一个大提示词）
2. **04b**："再看它回复了什么。"（一段文字，恰好是工具调用的格式）
3. **04c**："把这个过程重复几遍，就是 Agent。"（两层循环）
4. **04d**（原来的 Agent Loop 页）："抽象一下，就是 Think → Act → Observe 这个环。"

04d 和 05 是这三页的抽象版。先看具体的，再看抽象的，会容易得多。

## 几个容易想错的地方

- **"Agent 是一种更高级的模型"**：不是。模型完全一样，区别在外面那层程序。
- **"模型在执行工具"**：不是。模型写出一段文字就结束了，执行是 harness 的事。
- **"模型记得之前做过什么"**：不记得。它之所以知道，是因为 harness 每次都把完整记录重新发给它。
- **"我的提示词就是我打的那句话"**：不是。那句话通常只占提示词的不到千分之一。
- **"skill 的内容一直在上下文里"**：只有一行简介一直在。全文是模型主动要、harness 才加进去的。
- **"每一轮只发新增的内容"**：概念上每一轮都是全部重发。实际计费时，前面没变的部分可以走提示缓存，便宜很多，但它们仍然占着上下文窗口。

## 和成本的关系

04c 下方那四根越来越长的横条，直接解释了三件事：

- **为什么 Agent 任务的输入 token 这么多**：四次调用一共发送了 14.7k + 16.8k + 18.0k + 27.4k ≈ 77k token，而最后的提示词本身只有 27.4k。
- **为什么工具结果要节制**：一次 `Read` 加进来 9.4k，之后每一轮都要带着它。
- **为什么需要上下文工程（09）**：任务再长一些，这根横条就会顶到窗口上限。

## 画面上的简化

- **token 数量都是示意值**，画面上有标注。实际数字取决于装了多少工具和 skill。
- **04b 的分词是示意的**，真实分词器切出来的片段可能不同。
- **工具调用的格式做了简化**：真实的 `tool_use` 还带一个 `id`，并且模型通常会在调用前后写一些说明文字。
- **04c 里每次调用只画了一个工具**：实际上模型可以在一次回复里请求多个工具。

## 自测

<details>
<summary>1. 你输入一句 9 个 token 的话，LLM 实际收到多少？多出来的是什么？</summary>

收到的是完整的提示词，示意值是一万多 token。多出来的是系统提示、工具定义、CLAUDE.md 和 skill 简介列表，由 harness 自动拼接。
</details>

<details>
<summary>2. dcm-guide 这个 skill 的全文是什么时候进入提示词的？</summary>

模型先根据一行简介判断相关，写出一个调用 Skill 工具的回复；harness 执行后把 SKILL.md 全文作为工具结果追加到提示词；下一次调用 LLM 时全文才在里面。
</details>

<details>
<summary>3. 模型"调用工具"的那一刻，实际发生了什么？</summary>

模型用生成循环一个 token 一个 token 写出了一段特定格式的文字，然后输出结束 token。没有任何东西被执行。
</details>

<details>
<summary>4. 说出两层循环各自由谁执行、每一圈产出什么。</summary>

外层由 harness 执行，每一圈是一次 LLM 调用加一次工具执行。内层由 LLM 执行，每一圈是一次前向传播，产出一个 token。
</details>

<details>
<summary>5. 第 4 次调用 LLM 时，它怎么知道前 3 次做了什么？</summary>

它不记得。harness 把前 3 次的回复和工具结果都保留在提示词里，第 4 次全部重新发给它。
</details>
