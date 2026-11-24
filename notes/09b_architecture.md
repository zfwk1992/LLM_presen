# 09b · 整体架构：一切都经过 Harness

![Architecture](../llm_agent_animations_single_page/09b_architecture.gif)

> **一句话**：LLM 只连着一样东西，就是 harness。文件、skill、MCP server、RAG 检索，全都由 harness 去访问，结果都以文字的形式放回提示词。

## 在演讲里的位置

这是第三章的最后一页，把这一章讲的东西和第二章的 Agent loop 拼成一张图。前面每一页讲的都是一个部件，这一页回答"它们是怎么连在一起的"。例子仍然是 "How do we integrate DCM into this project?"。

## 画面布局

| 位置 | 内容 |
|---|---|
| 左 | **You**：你，只发了一句请求 |
| 中上 | **LLM**：tokens in, tokens out |
| 中 | **Harness (Claude Code)**：*the only program the LLM is connected to*。里面四个部件：Prompt builder、Agent loop、Permissions、Tool router |
| 右 | 五种能力，从上到下：Built-in tools、Skills、MCP server "spec"、MCP server "jira"、Sub-agents |
| 下 | **The prompt**：每次调用时 LLM 收到的内容 |

Harness 里的四个部件：

| 部件 | 做什么 | 在哪页讲过 |
|---|---|---|
| Prompt builder | 把系统提示、工具定义、CLAUDE.md、skill 列表、对话记录拼成一条序列 | 04a、04c |
| Agent loop | 调用 LLM，检查回复里有没有工具调用，有就继续 | 04e |
| Permissions | 这个操作允许执行吗，要不要先问用户 | 05 |
| Tool router | 这个工具调用该交给谁：内置工具、skill，还是哪个 MCP server | 07c |

右边五种能力里，这次任务用到了上面三种；"jira" 这个 MCP server 和子 Agent 画成灰色，标着 *not needed this time*。它们一直连着、一直可用，只是模型这次没有请求。

## 动画逐步解读

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0.8 s | ① The LLM talks to one thing only: the harness | You、LLM、Harness 和它的四个部件出现 | "LLM 上下两个箭头只连着 harness：提示词上去，回复下来" |
| 3.6 s | ② At startup the harness collects what exists: tools, MCP servers, skills | 右边五个框依次出现；底部提示词里"工具定义"和"skills"两段亮一下 | "启动时 harness 把能用的东西收集起来，它们的说明进入提示词" |
| 7.0 s | ③ Call 1: the model asks for a skill; the harness reads it from disk | 小圆点：上到 LLM，下回 harness，向右到 Skills，返回，落入提示词 | "模型要求加载 skill，harness 从磁盘读出来" |
| 10.4 s | ④ Call 2: a built-in tool runs your script on your machine | 圆点走向 Built-in tools | "跑脚本用的是内置的 Bash 工具，在你的机器上执行" |
| 13.4 s | ⑤ Call 3: an MCP server does the RAG search and returns text | 圆点走向 MCP server "spec"，这个框亮起 | "查规范走的是 MCP，RAG 检索在这个 server 里面完成" |
| 16.6 s | ⑥ Every result comes back as text in the prompt, until the model answers | 又一次内置工具；最后模型不再请求工具，答案回到 You | "每个结果都变成提示词里的一段文字，直到模型给出答案" |

每一轮小圆点走的路线都一样，值得指给听众看：

1. 从 harness **向上**到 LLM（提示词）
2. 从 LLM **向下**回 harness（回复，里面是一个工具调用）
3. 从 harness **向右**到某一种能力
4. **原路返回** harness
5. **向下**落入提示词，底部的长条多出一段

五种请求走的是同一条路，只有第 3 步的目的地不同。

## 这一页把前面的内容都串起来了

| 画面上的部分 | 对应的页 |
|---|---|
| LLM 的两个箭头 | 03 生成循环、04b 回复是逐个 token 生成的 |
| Prompt builder 和底部的长条 | 04a 第 1 次调用收到了什么、04c 每次全部重发 |
| Agent loop | 04e 两层循环 |
| Built-in tools | 05 工具调用 |
| Skills | 08 三级加载 |
| MCP server "spec" | 07c MCP 的通信过程、06a–06c RAG 的细节 |
| MCP server "jira" | 07a、07b |
| Sub-agents | 09 上下文工程里的隔离 |
| 长条越来越长 | 09 上下文是有限的 |

## 这一页要讲清楚的四件事

**1. LLM 只有一个连接。** 它不能读文件，不能访问网络，不知道 MCP 的存在，也不知道向量数据库的存在。它只收到提示词，只输出回复。

**2. 所有能力对 LLM 来说长得一样。** 读文件、加载 skill、调用 MCP、检索规范，在 LLM 这边都是"写一个工具调用，下一次在提示词里看到一段结果文字"。区别全部被 harness 挡在了外面。

**3. 分工很清楚。**

| | 负责 |
|---|---|
| LLM | 决定下一步要什么，以及任务是否完成 |
| Harness | 拼提示词、执行请求、检查权限、把结果放回去 |
| 内置工具 | 操作你的项目文件和命令行 |
| Skills | 提供做事的方法（文档加脚本） |
| MCP server | 连接外部系统；RAG 检索可以作为其中一个 server |

**4. RAG 和 MCP 不是并列的两条路。** 这是容易混淆的地方：

- **MCP** 是一种**连接方式**：harness 怎样和外部程序通信。
- **RAG** 是一种**做法**：先检索、再把结果放进提示词。

在这个例子里，RAG 检索被包装成了一个 MCP server 提供的工具。所以它们是"RAG 这件事，通过 MCP 这条通道，被 Agent 用上了"的关系。RAG 也可以不走 MCP（比如做成内置工具），MCP server 也可以和 RAG 无关（比如查 Jira）。

结尾的结论框：*The LLM sees only the prompt. The harness is its only door to files, skills, MCP servers and RAG. Everything returns as text.*

## 可以用来收尾第三章的一段话

"这一章我们讲了四样东西：RAG 让它读到我们的文档，MCP 让它连上我们的系统，Skills 把我们的做法交给它，上下文工程让这一切不至于把它淹没。现在看这张图：它们在结构上其实是一回事。模型提出要求，harness 去取，结果变成提示词里的一段文字。模型从头到尾只做了一件事：读提示词，预测下一个 token。"

## 画面上的简化

- **只画了 6 次调用中的 4 次工具执行**。第 5 次调用（一次 Grep）和前面走的路线相同，画面上用一行小字说明。
- **Harness 内部的四个部件是为了讲解划分的**，真实程序里不一定是这样四个模块。
- **Skill 的加载画成了一种独立的能力**。实际上它也是通过一个工具调用触发的，读取的是磁盘上的文件。
- **子 Agent 画成了右边的一种能力**。它实际上是 harness 再启动一个带独立上下文的循环，结束后只把结论返回。
- **"jira" 这个 server 是为了说明"连着但没用到"而加的**，前面的例子里没有出现。

## 自测

<details>
<summary>1. LLM 直接连接着哪些东西？</summary>

只有 harness。提示词从 harness 来，回复交给 harness。
</details>

<details>
<summary>2. 读文件、加载 skill、调用 MCP server，在 LLM 看来有什么不同？</summary>

没有不同。都是写出一个工具调用，然后在下一次的提示词里看到结果文字。
</details>

<details>
<summary>3. 这个例子里，RAG 检索是在哪里完成的？它是怎么被 Agent 用上的？</summary>

在名为 "spec" 的 MCP server 内部完成（embedding 模型加向量数据库）。模型写出工具调用，harness 通过 MCP 转发给 server，server 返回 3 段文字，harness 把它们放进提示词。
</details>

<details>
<summary>4. RAG 和 MCP 是什么关系？</summary>

MCP 是 harness 与外部程序通信的方式；RAG 是先检索再把结果放进提示词的做法。RAG 可以通过 MCP 提供，也可以不通过；MCP server 也可以和 RAG 无关。
</details>

<details>
<summary>5. 每一轮里，信息走过的五段路是什么？</summary>

提示词从 harness 到 LLM；回复从 LLM 回 harness；请求从 harness 到某种能力；结果返回 harness；结果被追加进提示词。
</details>
