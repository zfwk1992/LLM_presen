# 09 · Context Engineering（上下文工程）

![Context engineering](../llm_agent_animations_single_page/09_context_engineering.gif)

> **一句话**：上下文窗口是有限的，而且不是越满越好。上下文工程就是想办法让模型在每一步看到的都是**数量最少、信息量最高**的那些 token。

## 在演讲里的位置

第三章的收尾，也是对前面所有内容的总结。回头看：04 的上下文只增不减；05、07 的工具说明占空间；06 往 prompt 里贴段落；08 小心翼翼地按需加载。这一页把这些归结成一个问题，并给出四个通用的应对办法。

## 画面布局

- **顶部长条**：MAIN AGENT CONTEXT WINDOW · e.g. 200K tokens。右上角是占用百分比。
- **图例**（长条下方）：每种颜色代表一类内容。

| 颜色块 | 内容 | 特点 |
|---|---|---|
| System prompt | 系统提示 | 固定，一开始就在 |
| Tools / MCP schemas | 工具说明 | 固定，连的 server 越多越大 |
| CLAUDE.md | 项目记忆文件 | 固定 |
| User msgs | 用户消息 | 通常很小 |
| Assistant msgs | 模型的回复 | 中等 |
| Tool results | 工具结果 | **最大**，增长最快 |
| Summary | 压缩后的摘要 | 压缩后才出现 |

- **下半部分**：先后展示问题、两种解法、四个策略。

## 动画逐步解读

这一页画面内容换了四次，建议按四段来讲。

### 第一段：窗口被填满（0–10 s）

| 时间 | 画面 | 这时候讲什么 |
|---|---|---|
| 0–2 s | 长条里先出现三块固定内容，15% used | "对话还没开始，已经用掉一部分" |
| 2–8 s | 依次加入 file read、build log、test output、grep results，53% → 80% → 92% | "每调用一次工具，结果就占一大块" |
| 约 8 s | 长条边框变红，92% used | "快满了" |
| 8–10 s | 红色箭头指向很靠前的一小块：*the original task gets lost in the noise* | "用户最初的要求，现在只是一长串内容里很小的一段" |

字幕：*"Everything the model sees competes for one finite window"*，然后是 *"More tokens ≠ better: irrelevant tokens dilute attention"*。

注意看黄色的 Tool results 块有多大。占满上下文的通常不是对话，而是工具返回的内容。

### 第二段：压缩（10–14 s）

| 时间 | 画面 | 这时候讲什么 |
|---|---|---|
| 10–12 s | 中间的块收缩，72% → 20% | "把旧的对话总结成一小段" |
| 12–14 s | 只剩固定三块加一块绿色的 Summary；绿色箭头：*decisions, open tasks and key facts kept: details dropped* | "保留决定、待办和关键事实，丢掉细节" |

字幕：*"Compaction: summarise old turns, free the space"*

### 第三段：子 Agent（14.5–19 s）

| 时间 | 画面 | 这时候讲什么 |
|---|---|---|
| 14.5–16 s | 下方出现第二个长条：SUB-AGENT CONTEXT · fresh & isolated | "另开一个全新的、独立的上下文" |
| 16–18 s | 子 Agent 的长条里出现 grep ×12、read ×6、read ×5 | "脏活在那边干，消耗的是它自己的上下文" |
| 18–19 s | 一个小标签 "7 call sites (summary)" 飞回主上下文，20% → 22% | "回到主上下文的只有一句结论" |

字幕：*"Sub-agents: explore in a separate context, return only the result"*

这里的数字对比很有说服力：子 Agent 做了 23 次工具调用，主上下文只增加了 2%。

### 第四段：四个策略（19–22 s）

四张卡片依次出现，字幕：*"Goal: the smallest set of high-signal tokens for the task"*

| 策略 | 画面上的说明 | 前面哪一页讲过 |
|---|---|---|
| **Select** 选择 | load only what is relevant, just in time (tools, skills, RAG) | 06 RAG、08 Skills |
| **Compress** 压缩 | summarise / compact long histories | 本页第二段 |
| **Isolate** 隔离 | delegate noisy exploration to sub-agents | 本页第三段 |
| **Persist** 持久化 | notes & CLAUDE.md live outside the window | 08 提到的 CLAUDE.md |

## 需要真正搞懂的概念

### 上下文窗口里到底有什么

**所有东西。** 模型在某一步能看到的全部内容，就是这个窗口里的内容，没有别的"记忆"（03：权重是固定的）。系统提示、工具说明、历史对话、每一次工具的返回，都在里面，都算 token。

### 为什么"越多越好"不成立

两个层面的原因：

- **硬限制**：窗口有上限，满了就放不进新内容。
- **软限制**：还没满的时候效果就已经在下降。上下文越长、无关内容越多，模型越难抓住重点，越容易遗漏早先的指令或混淆细节。画面上把这个现象叫 "context rot"（上下文腐化），说明文字是 *long, noisy context → attention spread thin*。

再加上成本：04 讲过，Agent 的每一轮都要把全部上下文重新交给模型。上下文越长，每一轮越贵、越慢。

一个好用的类比：**上下文像工作台，不像仓库**。仓库越大越好，工作台上东西堆多了反而没法干活。

### 四个策略的含义

- **Select（选择）**：一开始就不要把用不上的东西放进来。RAG 只取最相关的几段，Skills 只加载匹配的那一个，工具只连用得上的 server。
- **Compress（压缩）**：已经进来的旧内容，总结成更短的形式。代价是丢失细节，所以画面里强调保留的是"决定、待办、关键事实"。
- **Isolate（隔离）**：会产生大量中间结果的任务，交给一个独立的上下文去做，只把结论拿回来。
- **Persist（持久化）**：需要长期记住的东西写到窗口之外（笔记文件、CLAUDE.md），需要时再读。这样即使上下文被压缩或清空，信息也不会丢。

### 在 Claude Code 里对应什么

| 策略 | 对应的功能 |
|---|---|
| Select | Skills 按需加载；只启用需要的 MCP server |
| Compress | `/compact` 手动压缩；接近上限时自动压缩 |
| Isolate | 子 Agent（subagent） |
| Persist | CLAUDE.md、记忆文件 |
| 查看占用 | `/context` |
| 重新开始 | `/clear`：换任务时清空上下文 |

### 从"提示工程"到"上下文工程"

- **提示工程（prompt engineering）**：琢磨一条指令怎么写。
- **上下文工程（context engineering）**：管理模型在每一步看到的**全部**内容。

对于只问一句答一句的聊天，前者够用。对于会跑几十轮、调用几十次工具的 Agent，后者才是决定成败的地方。

## 常见误解

- **"上下文窗口越大，问题就不存在了"**：窗口变大缓解的是硬限制。噪声干扰和成本问题仍然存在。
- **"把所有相关文件都给它，总没错"**：给得多不等于给得对。无关内容是有代价的。
- **"压缩是无损的"**：不是。它是有损的总结，被丢掉的细节之后就看不到了。重要的东西应该先持久化。

## 听众可能会问

**Q：日常使用里我该怎么做？**
三条最实用的：换任务时用 `/clear` 开新会话；长期有效的约定写进 CLAUDE.md；需要大范围搜索时让它用子 Agent。

**Q：子 Agent 不也要消耗 token 吗？**
要。它没有省总量，省的是**主上下文**的空间。主上下文保持干净，后面每一轮都更便宜、更准确。

**Q：自动压缩会不会把重要的东西丢掉？**
有可能。所以关键的决定和约束应该写进文件，而不是只留在对话里。

**Q：200K 是固定的吗？**
画面上写的是 "e.g. 200K"，是举例。不同模型和配置的窗口大小不同。

## 承上启下

- **这一章**：RAG、MCP、Skills 都是往上下文里加东西，这一页讲怎么管住它。
- **下一章**：最后回到使用层面，Claude Code 里有两个直接影响成本和速度的选项。
- **过渡句**："到这里，原理部分讲完了。最后三页回到每天都会碰到的两个选择：用哪个模型，用多大的 effort。"

## 自测

<details>
<summary>1. 上下文里通常哪一类内容占得最多？</summary>

工具结果（读文件、日志、测试输出、搜索结果）。
</details>

<details>
<summary>2. 说出四个策略，并各举一个例子。</summary>

Select：RAG 只取最相关的几段、Skills 按需加载。Compress：把旧对话总结成摘要。Isolate：让子 Agent 在独立上下文里搜索，只返回结论。Persist：把约定写进 CLAUDE.md。
</details>

<details>
<summary>3. 为什么上下文没满的时候也要控制它的大小？</summary>

无关内容会分散模型的注意力，降低效果；而且 Agent 每一轮都要重新处理全部上下文，越长越贵、越慢。
</details>
