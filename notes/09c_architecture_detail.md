# 09c · Harness 内部：一轮循环，以及它怎么停下来

![Architecture in detail](../llm_agent_animations_single_page/09c_architecture_detail.gif)

> **一句话**：Harness 每一轮做同样的八步。第四步是一个检查："回复里有工具调用吗？"有就继续，没有就结束。决定结束的是 LLM，harness 只是检查。

这一页是 09b 的放大版：09b 画的是"谁连着谁"，这一页画的是 harness **内部**一轮是怎么走的，并且正面回答一个问题：**Agent 怎么知道自己做完了？**

## 先回答这个问题

### 是谁判断任务结束的？

**是 LLM，不是 harness。**

要分清两个层次的"结束"：

| | 一次回复结束 | 整个任务结束 |
|---|---|---|
| 标志 | LLM 输出结束 token | LLM 的回复里没有工具调用 |
| 多久发生一次 | 每次 LLM 调用都发生 | 整个任务只发生一次 |
| 谁决定 | LLM | LLM |
| harness 做什么 | 收下这次回复 | 检查回复里有没有工具调用，没有就停 |

每一次回复都以结束 token 收尾，不管回复的内容是"请帮我读这个文件"还是"答案是这样"。所以结束 token 本身不能说明任务做完了。能说明任务做完的是回复的**内容**：模型没有再提任何要求。

Harness 的检查是机械的，可以写成一行：

```python
if not reply.tool_calls: break
```

它不理解任务，也不评估答案好不好。

### LLM 怎么"知道"该停了？

它每一轮都读到完整的提示词，里面有：

- 你最初的请求
- 它做过的每一步
- 每一步拿回来的结果
- 如果加载了 skill，还有那份流程清单

读完之后，它做的还是 03 讲的那件事：预测接下来最可能的内容。这时有两种可能的续写：

- "还缺信息，再调用一个工具"
- "信息够了，写答案"

当需要的东西都已经在提示词里了，后者就成了最可能的续写。DCM 例子里，第 6 次调用时模型的思考是 "Step 5: I have enough. Write the plan."，流程清单的前四步都有了结果，于是它写出方案，没有再请求工具。

这种判断是模型在训练中学会的，不是一条写死的规则。

### 这个判断会出错吗？

会。两种方向都可能：

- **停得太早**：信息其实不够，但它认为够了，给出一个不完整的答案。
- **停不下来**：在一个问题上反复尝试，或者不断去查不必要的东西。

应对的办法：

| 办法 | 作用 |
|---|---|
| 在 skill 或提示词里写清"做到什么程度算完成" | 帮模型判断 |
| 提高 effort | 让它多核对一遍再下结论（10e） |
| 要求它在回答前自行验证，比如跑一遍测试 | 用客观结果代替主观判断 |
| harness 的安全停止条件 | 防止无限循环 |

### Harness 自己的停止条件

除了"没有工具调用"这一条，harness 还有几个兜底，这些才是 harness 自己做的决定：

- 你手动中断
- 达到最大轮数
- 上下文窗口满了
- 权限被拒绝

画面右下角的黄色框列的就是这些。

## 画面布局

| 区域 | 内容 |
|---|---|
| 上方中间 | **Model provider**：LLM 在网络另一端，旁边是提示缓存 |
| 中间的大框 | **Harness**：你机器上的一个程序，里面是八个编号的步骤 |
| 右上 | 第 2 步往提示词里放了什么 |
| 右中 | NO 分支的出口：任务完成 |
| 右下 | MCP server：spec、jira、bitbucket |
| 底部 | 两个结论框：谁决定结束；harness 的安全停止条件 |

## 八个步骤

| 步骤 | 名称 | 做什么 |
|---|---|---|
| ① | Conversation store | 保存到目前为止的每一条消息。你的请求从这里进入 |
| ② | Prompt builder | 把系统提示、工具定义、CLAUDE.md、skill 列表和整段对话拼成一条序列 |
| — | LLM | 提示词通过网络发给模型，回来一个回复。前缀没变的部分走缓存 |
| ③ | Reply parser | 解析回复：里面是文字，还是工具调用 |
| ④ | **Stop check** | **回复里有工具调用吗？** |
| ⑤ | Permissions | 这个操作允许执行吗，需要先问用户吗 |
| ⑥ | Tool router | 这个调用该交给谁 |
| — | 四种执行者 | 内置工具、Skill loader、子 Agent、MCP client |
| ⑦ | Result as text | 把结果变成文字，作为 tool_result 追加到对话里 |
| ⑧ | Next round | 回到第 ① 步 |

第 ④ 步是整张图的关键：它是唯一的分叉点。

- **YES**：往左走，经过 ⑤ ⑥ ⑦ ⑧，再来一轮。
- **NO**：往右走，回复就是答案，交给你，循环结束。

## 动画逐步解读

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0.8 s | ① The harness keeps the whole conversation and builds the prompt from it | ① ② 依次亮起，右上出现提示词内容的清单 | "harness 保存着完整的对话，每一轮都从它重新拼出提示词" |
| 3.8 s | ② The prompt goes to the model provider; one reply comes back | 箭头向上到 LLM，LLM 亮起，箭头向下到 ③ | "提示词发出去，回来一个回复。这一轮的回复是一个工具调用" |
| 6.8 s | ③ The harness parses the reply and asks one question: is there a tool call? | 菱形出现并亮起 | **停一下**："harness 只问一个问题" |
| 9.6 s | ④ Yes: check permission, then route it to the right executor | YES 箭头，⑤ ⑥ 亮起，四个执行者出现，MCP clients 亮起，右边出现 MCP server | "有。检查权限，然后交给对应的执行者。这次是 MCP" |
| 13.2 s | ⑤ The result becomes text, is appended, and the next round starts | ⑦ 亮起，左侧绿线绕回 ① | "结果变成文字，追加进对话，回到第一步" |
| 15.8 s | ⑥ Same path every round. One day the reply contains no tool call | ① ② LLM ③ 快速再亮一遍；③ 里的文字从 tool_use 变成 text；菱形变成绿色 | "每一轮都是这条路。直到有一次，回复里没有工具调用" |
| 18.6 s | ⑦ Then the loop ends. The LLM decided; the harness only checked | NO 箭头指向右边的绿色框；底部两个结论框出现 | 结论 |

注意第 ③ 步那个框里的一行小字在两轮之间的变化：

- 前面的轮次：`tool_use mcp__spec__search_spec`（橙色）
- 最后一轮：`text: the integration plan`（绿色）

菱形的颜色也跟着从橙色变成绿色。这就是"任务结束"在画面上的全部体现：回复的类型变了。

## 这一页要讲清楚的三件事

**1. 循环只有一个出口。** 就是第 ④ 步的 NO。不存在"harness 认为做得差不多了"这种情况。

**2. Harness 不做判断，只做检查。** 它不知道任务是什么，不知道答案对不对。它只看回复的格式：有工具调用，还是没有。

**3. LLM 的每一次决定都基于完整的提示词。** 它没有记忆，但 harness 每一轮都把全部历史重新给它。它读到"该做的都做了"，就写出答案。

## 和 09b 的关系

| | 09b | 09c |
|---|---|---|
| 视角 | 从外面看：谁连着谁 | 从里面看：一轮怎么走 |
| 重点 | 一切都经过 harness，都以文字返回 | 循环的步骤，以及唯一的出口 |
| 适合回答 | "RAG、MCP、Skills 是怎么接进来的？" | "它怎么知道该停了？" |

两页都放的话，先 09b 后 09c。时间有限时，按听众最可能问的问题选一页。

## 画面上的简化

- **八个步骤是为讲解划分的**，真实程序里的模块划分不一定是这样。
- **"Skill loader"画成了一种独立的执行者**。实际上加载 skill 也是通过一个工具调用触发的。
- **一次回复只画了一个工具调用**，实际上可以有多个，harness 会都执行完再进入下一轮。
- **"bitbucket" 这个 server 是为了举例加的**，前面的例子里没有用到。
- **提示缓存画在模型提供方那一侧**，它的具体行为和计费以官方文档为准。

## 自测

<details>
<summary>1. 结束 token 和"任务结束"是一回事吗？</summary>

不是。每次回复都以结束 token 收尾。任务结束的标志是某一次回复里没有工具调用。
</details>

<details>
<summary>2. 是谁决定任务做完了？harness 在其中做了什么？</summary>

LLM 决定：它写出答案而不是工具调用。Harness 只检查回复里有没有工具调用，没有就停止循环。
</details>

<details>
<summary>3. LLM 没有记忆，它凭什么判断"该做的都做了"？</summary>

Harness 每一轮都把完整的对话重新发给它。它读到自己做过的每一步和结果，据此预测下一段内容应该是答案。
</details>

<details>
<summary>4. 说出 harness 自己会强制停止的几种情况。</summary>

用户中断、达到最大轮数、上下文窗口满了、权限被拒绝。
</details>

<details>
<summary>5. 第 ④ 步的 YES 和 NO 分别通向哪里？</summary>

YES：权限检查 → 工具路由 → 执行 → 结果追加 → 回到第一步。NO：回复就是答案，交给用户，循环结束。
</details>
