# 04a–04e · 用一个例子讲清 Agent 是怎么工作的

这五页用同一句请求贯穿到底：

```
How do we integrate DCM into this project?
```

每一页右上角都显示这句请求，左上角标着 PART 1 OF 5 到 PART 5 OF 5，可以连着放。

![Part 1](../llm_agent_animations_single_page/04a_one_big_prompt.gif)

![Part 2](../llm_agent_animations_single_page/04b_tool_call_is_text.gif)

![Part 3](../llm_agent_animations_single_page/04c_second_call.gif)

![Part 4](../llm_agent_animations_single_page/04d_agent_at_work.gif)

![Part 5](../llm_agent_animations_single_page/04e_two_loops.gif)

> **一句话**：LLM 还是那个只会预测下一个 token 的网络。Agent 是它外面的一个程序（harness），反复做三件事：把所有内容拼成一个提示词发给 LLM；LLM 写出一个回复；如果回复是工具调用，harness 就执行它，把结果拼回提示词，再发一次。

## 五页分别回答什么

| 页 | 标题 | 回答的问题 | 时长 |
|---|---|---|---|
| 04a | Call 1: What the LLM Receives | 第一次传给 LLM 的到底是什么？ | 22.5 s |
| 04b | Call 1: What the LLM Returns | LLM 返回了什么？harness 怎么处理？ | 24.0 s |
| 04c | Call 2: Everything Is Sent Again | 第二次传的是什么？我写的流程是怎么生效的？ | 23.0 s |
| 04d | The Whole Session, Call by Call | 整个任务从头到尾是什么样的？ | 24.0 s |
| 04e | Two Loops: the Harness Around the LLM | 抽象一下，Agent 和 LLM 是什么关系？ | 23.5 s |

之后的 04f（Think → Act → Observe 的环）和 05（工具调用）是更抽象的总结，时间紧时可以只留一页或都不放。

## 先建立一个画面：专家和助理

把 LLM 想成**关在房间里的专家**：很聪明，但出不了门，看不到你的电脑，只能通过门缝递纸条。Harness 是**门外的助理**。

1. 你把任务交给助理。助理把任务、项目说明、可用工具的清单一起写在纸上，塞进门缝。
2. 专家看完，递出一张纸条："请帮我做某件事"。
3. 助理去做，把结果抄在纸上，**连同之前所有的纸**一起再塞进去。
4. 重复，直到专家递出来的不是请求，而是答案。

两个要点：专家没有记忆，每次都要把之前的纸全部重新给他；专家从不亲自动手。

| | LLM（专家） | Harness（助理，如 Claude Code） |
|---|---|---|
| 决定下一步做什么 | ✔ | |
| 决定任务是否完成 | ✔ | |
| 读文件、跑命令、搜索 | | ✔ |
| 保存对话记录、拼提示词 | | ✔ |
| 检查权限 | | ✔ |
| 运行循环 | | ✔ |

## 例子里的项目

| 文件 | 是什么 | 一开始在不在提示词里 |
|---|---|---|
| `CLAUDE.md` | 项目说明 | 全文在 |
| `skills/dcm-integration/SKILL.md` | 你写的 Dcm 集成流程 | 只有一行简介 |
| `skills/misra-check/SKILL.md` | MISRA 检查 | 只有一行简介 |
| `docs/AUTOSAR_SWS_Dcm.pdf` | Dcm 规范，600 页 | 不在 |
| `config/EcuC.arxml` | ECU 配置值 | 不在 |
| `docs/architecture.md` | 本仓库的分层规则 | 不在 |
| `config/Os.arxml`、`rte/` | Os 任务和 Rte 端口 | 不在 |
| `bsw/Dcm/` 和其余 214 个文件 | 模块源码等 | 不在 |

SKILL.md 里写的流程（这就是你自己定义的工作流）：

```
1. Run scripts/extract_dcm_config.py on the EcuC ARXML
2. Look up the requirements in the Dcm specification
3. Read docs/architecture.md
4. Check the Os and Rte definitions
5. Then propose the changes
```

## 04a · 第 1 次调用：LLM 收到了什么

你打的那句话只有 10 个 token。Harness 把下面这些按固定顺序拼成一条序列，一次性送进网络：

| 顺序 | 部分 | 谁写的 | 大小（示意） |
|---|---|---|---|
| 1 | System prompt | Claude Code | 3,200 |
| 2 | Tool definitions | Claude Code 和各 MCP server | 9,500 |
| 3 | CLAUDE.md | 你 | 1,400 |
| 4 | Skill list（每个 skill 一行） | 各 skill 的作者 | 600 |
| 5 | **你的输入** | **你** | **10** |

| 时间 | 字幕 | 这时候讲什么 |
|---|---|---|
| 0.8 s | ① You type one short message | "你只打了一句话" |
| 3.6 s | ② The harness adds the rest: system prompt, tools, CLAUDE.md, skill list | "Claude Code 在前面加了这些，你平时看不到" |
| 7.0 s | ③ Everything is joined into one long token sequence | "拼成一条长序列。注意比例" |
| 11.6 s | ④ That whole sequence goes into the LLM at once | "整条一次性进入网络，一次前向传播" |
| 15.0 s | ⑤ Skills: only the one-line descriptions are in it, not the full text | "skill 这时只有一行简介" |
| 18.6 s | ⑥ The context window is the prompt: you typed a tiny part of it | 结论：You typed 10 of its 14,710 tokens |

三个要讲清楚的点：

- **Harness 在这里不做选择。** 不管你问什么，它放进去的都是这几样，全部 skill 的简介都列出，不挑。
- **顺序的规律是：固定不变的在前，最新的在后。** 前面那一大段每次都一样，可以走缓存。
- **你的流程此时还不在里面。** 模型只看到 `dcm-integration` 的一行简介。

## 04b · 第 1 次调用：LLM 返回了什么

| 时间 | 字幕 | 这时候讲什么 |
|---|---|---|
| 0.8 s | ① The whole prompt goes into the LLM | "上一页的整个提示词进入 LLM" |
| 3.2 s | ② The reply comes out one token at a time: one forward pass each | "回复一个 token 一个 token 出来，计数从 #1 到 #24" |
| 8.2 s | ③ The tokens spell a tool call. To the LLM it is just text | "拼起来是一个工具调用。对 LLM 来说只是文字" |
| 11.2 s | ④ The LLM stops at \<end\>. Nothing has been executed yet | **停一下**："LLM 到这里结束了。什么都没执行" |
| 14.0 s | ⑤ The harness reads the text and runs the tool on your machine | "接下来是程序的事：解析、检查权限、执行" |
| 18.0 s | ⑥ The result is added to the prompt, ready for the next LLM call | "结果加回提示词，从 14,734 变成 16,834" |

模型写出的 24 个 token 连起来是：

```json
{"type": "tool_use", "name": "Skill", "input": {"skill": "dcm-integration"}}
```

这一页回答了"谁选的 skill"：**模型选的。** 它在 30 行简介里读到 `dcm-integration` 这一行，判断和你的问题相关，于是写出这个调用。Harness 只是照做，从磁盘读出 SKILL.md 的全文。

结尾的深色框：**The LLM writes. The harness acts.**

## 04c · 第 2 次调用：全部重新发送

这一页是新加的，它回答两个问题：第二次发的是什么？你写的流程是怎么生效的？

画面左边是第 2 次调用的提示词，从上到下：

| 段 | 内容 | 状态 |
|---|---|---|
| SYSTEM | 系统提示、工具定义、CLAUDE.md、skill 列表 | 和第 1 次完全相同 |
| USER | How do we integrate DCM into this project? | 和第 1 次完全相同 |
| ASSISTANT | `tool_use Skill("dcm-integration")` | 新增：模型上次写的 |
| USER · TOOL_RESULT | SKILL.md 全文，含 5 步流程 | 新增：harness 读回来的 |

| 时间 | 字幕 | 这时候讲什么 |
|---|---|---|
| 0.8 s | ① Call 2 starts: the harness sends everything again, from the top | "第二次调用，harness 从头把所有内容再发一遍" |
| 3.6 s | ② New at the end: what the LLM wrote, and the full SKILL.md text | "末尾多了两段：模型上次写的，和 skill 的全文" |
| 7.6 s | ③ Now the LLM can read your workflow. It starts with step 1 | "现在模型才看到你的流程。第一步那一行亮起来" |
| 11.0 s | ④ Again it only writes a request: run the extraction script | "它还是只写了一个请求" |
| 13.6 s | ⑤ The harness runs the script; the result joins the prompt | "harness 跑脚本，结果加进提示词" |
| 16.8 s | ⑥ Call 3 will receive all of this: the prompt only ever grows | "左边又多了两段，第 3 次调用会带上它们" |

这一页最重要的一句话在结尾的深色框里：

**Your workflow is followed because the LLM reads it in the prompt, not because the harness executes it.**

也就是说：你在 SKILL.md 里写"先跑提取脚本，再查规范……"，harness 并不理解这些步骤，它只是把这段文字放进提示词。是**模型读到之后照着做**，每一步都通过"写一个工具调用"来完成。

还有一个值得指出的细节：标着 "identical to call 1 (read from the cache)" 的那两段。它们每次都原样重发，所以可以走提示缓存，计费便宜很多，但仍然占着上下文窗口。

## 04d · 完整过程，逐次调用

三栏同步推进：左边是磁盘上的文件，中间是每次 LLM 调用的卡片，右边是提示词的长条。

| 调用 | 模型的思考 | 模型要求的工具 | harness 执行的结果 | 提示词 |
|---|---|---|---|---|
| 1 | A skill matches this task. Load it first. | `Skill("dcm-integration")` | 载入你的 5 步流程 | 14.7k → 16.8k |
| 2 | Workflow step 1: get the EcuC values. | `Bash("scripts/extract_dcm_config.py config/EcuC.arxml")` | 3 个协议，14 个 UDS 服务，2 个 PDU | → 17.7k |
| 3 | Step 2: what does the standard require? | `search_spec("Dcm integration PduR ComM")` | 600 页里取回 3 段 | → 19.5k |
| 4 | Step 3: the rules of this repository. | `Read("docs/architecture.md")` | 180 行 | → 21.9k |
| 5 | Step 4: is Dcm already scheduled and connected? | `Grep("Dcm_MainFunction", "config/ rte/")` | 没有匹配：还没有 Os 任务，也没有 Rte 端口 | → 22.5k |
| 6 | Step 5: I have enough. Write the plan. | 无 | 输出方案，循环结束 | — |

最终答案：

```
1. Add Dcm_MainFunction to the 10 ms Os task   2. Route the 2 PDUs in PduR
3. Connect the Dcm ports in the Rte   4. Regenerate   (sources: EcuC, SWS_Dcm §7)
```

| 时间 | 字幕 |
|---|---|
| 0.8 s | ① One request. Project notes and skill descriptions are already in the prompt |
| 2.6 s | ② Call 1: the model sees a matching skill and asks to load it |
| 6.0 s | ③ Call 2: following your workflow, it asks to run the extraction script |
| 9.2 s | ④ Calls 3 and 4: it asks the spec, then reads the repo's own rules |
| 15.6 s | ⑤ Call 5: it checks Os and Rte and finds Dcm is not connected yet |
| 18.8 s | ⑥ Call 6: no tool call this time. It writes the plan and the loop ends |

值得指给听众看的四个细节：

- **模型的每一步都对着你流程里的一步**（卡片里写着 Workflow step 1、Step 2 …）。这就是 skill 的作用：把团队的做法交给模型。
- **EcuC.arxml 没有被整个读进来**，而是用脚本提取，只有 900 token 进入提示词。大文件应该这样处理。
- **600 页的规范只进来了 3 段**，这是检索（06 那页）。
- **有些东西始终没被打开**：`bsw/Dcm/` 和其余 214 个文件标着 "never opened"，`misra-check` 一直只有一行简介。

结尾的深色框：**6 LLM calls · 5 tool runs by the harness · the model never opened a file itself**

## 04e · 两层循环

泳道图：上面一条是 harness，下面一条是 LLM，时间从左到右。画了第 1、2、3、6 次调用，第 4、5 次省略（画面上有说明）。

| 时间 | 字幕 | 这时候讲什么 |
|---|---|---|
| 0.8 s | ① The harness builds the prompt and calls the LLM | "程序拼好提示词，调用 LLM" |
| 3.4 s | ② Inside the call, the generation loop writes a tool call token by token | "这个框里就是 04b 的全部内容" |
| 5.6 s | ③ The harness runs the tool and adds the result to the prompt | "程序执行工具，结果加进提示词" |
| 8.0 s | ④ Then it calls the LLM again, sending everything so far | "再调用一次，全部重发" |
| 11.6 s | ⑤ This repeats until the reply contains no tool call | "一直重复，直到回复里没有工具调用" |
| 18.4 s | ⑥ Two loops: the harness loops over LLM calls, the LLM loops over tokens | 结论 |

两层循环：

| | 外层循环 | 内层循环 |
|---|---|---|
| 谁执行 | Harness | LLM |
| 一圈产出 | 一次 LLM 调用加一次工具执行 | 一个 token |
| 这个例子里跑了几圈 | 6 | 每次调用几十到几百 |
| 讲解在哪页 | 04c、04d | 03、04b |

画面下方四根横条是每次调用收到的提示词，灰色是起始部分，彩色是途中加进来的工具结果。每根都比上一根长，而且每次都是全部重发。

结尾的深色框：**Agent = a program calling the LLM in a loop. The LLM never changes and never acts. It only receives a longer prompt each time.**

## 它怎么知道任务结束了

有两个不同层次的"结束"：

- **一次回复写完了**：每次 LLM 调用，模型写到最后都会输出结束 token（04b 里红色的 `<end>`）。这个每次都发生。
- **整个任务做完了**：每次回复写完后，harness 检查里面有没有工具调用。有，就执行并再调用一次；没有，就把回复交给你，循环结束。

所以"做完了没有"是模型决定的，它通过**不再请求工具**来表达。04d 的第 6 张卡片上写的 "no tool call" 就是这个时刻。

另外 harness 还有兜底的停止条件：你手动中断、达到最大轮数、上下文快满了。

## 你能怎样影响这个过程

你不需要自己写 harness，Claude Code 就是一个现成的。你做的是**配置**它：

| 机制 | 放什么 | 谁来执行 | 约束力 |
|---|---|---|---|
| CLAUDE.md | 始终适用的项目信息 | 模型读后遵守 | 软 |
| Skill | 某类任务的做法，可带脚本 | 模型判断相关时加载并遵守 | 软 |
| MCP server | 额外的工具，例如规范检索 | 模型决定何时调用 | 软 |
| 权限设置 | 允许或禁止哪些操作 | Harness 强制 | 硬 |
| Hooks | 特定时刻必定运行的脚本 | Harness 强制 | 硬 |

判断标准：希望它这样做的，写成文字；必须每次都发生的，交给 hooks、权限或脚本。

写的时候注意三点：

- **CLAUDE.md 要短**：它每次全文加载。项目里没有这个文件也能工作，只是每次都要重新摸索；可以用 `/init` 生成初稿。
- **Skill 可以多，简介要准**：每多一个只多一行，但模型选不选它完全看那一行。
- **长流程放 skill，不放 CLAUDE.md**：这样只有相关任务才加载。

## 容易想错的地方

- **"Agent 是一种更高级的模型"**：不是，模型完全一样，区别在外面那层程序。
- **"Harness 是指挥官"**：反了。做决定的是模型，harness 是执行者。
- **"模型在执行工具"**：不是，模型写完一段文字就结束了。
- **"模型记得之前做过什么"**：不记得，是 harness 每次把完整记录重新发给它。
- **"Harness 按我写的流程去读文件"**：不是，harness 只把流程的文字放进提示词，照着做的是模型。
- **"Harness 会挑选相关的 skill"**：不会，它把所有简介都列出来，挑选的是模型。
- **"每一轮只发新增的内容"**：概念上每一轮都是全部重发，只是不变的部分可以走缓存。

## 画面上的简化

- **token 数量是示意值**，画面上有标注。
- **文件名、脚本名和内容是为例子编的**；`search_spec` 是虚构的工具名，实际可由 MCP server 提供。Dcm 需要调度 `Dcm_MainFunction`、经 PduR 路由、通过 Rte 连接端口，这些符合 AUTOSAR 的集成方式。
- **04b 的分词是示意的**。
- **工具调用的格式做了简化**：真实的 `tool_use` 还带一个 `id`。
- **每次调用只画了一个工具**，实际上一次回复可以请求多个。
- **提示词各段的精确顺序属于实现细节**，可能随版本变化，但"固定的在前、最新的在后"这个结构是稳定的。

## 自测

<details>
<summary>1. 你输入 10 个 token，第 1 次调用 LLM 实际收到了什么？</summary>

系统提示、工具定义、CLAUDE.md 全文、所有 skill 的一行简介，加上你的输入，拼成一条序列，示意值约 14,710 token。
</details>

<details>
<summary>2. 谁决定使用 dcm-integration 这个 skill？它的全文什么时候进入提示词？</summary>

模型决定。它在第 1 次调用里写出加载请求，harness 读回全文并追加，第 2 次调用时全文才在提示词里。
</details>

<details>
<summary>3. 你在 SKILL.md 里写的 5 步流程，是谁在执行？</summary>

模型读到后一步一步照做，每一步写出一个工具调用。Harness 只负责执行这些调用，它并不理解流程本身。
</details>

<details>
<summary>4. 第 5 次调用时，模型怎么知道前 4 次做了什么？</summary>

它不记得。Harness 把前面所有的回复和工具结果都保留在提示词里，每次全部重发。
</details>

<details>
<summary>5. 循环在什么条件下结束？</summary>

模型的回复里不包含工具调用时。Harness 检查到这一点就把回复交给用户并停止。
</details>

<details>
<summary>6. 说出两层循环各自由谁执行、每一圈产出什么。</summary>

外层由 harness 执行，每圈是一次 LLM 调用加一次工具执行。内层由 LLM 执行，每圈是一次前向传播，产出一个 token。
</details>
