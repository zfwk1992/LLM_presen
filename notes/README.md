# LLM 与 AI Agent 演讲 · 学习笔记

这套笔记和 [../llm_agent_animations_single_page/](../llm_agent_animations_single_page/) 里的 28 个 GIF 一一对应。每篇笔记讲清楚一页动画：画面每一步在演示什么、背后的概念、容易讲错的地方、听众可能问什么。

## 整体故事线

整场演讲只有一条主线：**LLM 只会做一件事——根据已有的 token 预测下一个 token。后面所有的能力，都是在"往上下文里放什么"上做文章。**

| 章节 | 回答的问题 | 页面 |
|---|---|---|
| LLM Fundamentals | 模型本身到底在做什么？ | 01 → 02a → 02b → 02c → 02d → 02e → 02f → 03 |
| From LLM to AI Agent | 只会写字的模型怎么"做事"？ | 04a → 04b → 04c → 04d → 04e → 04f → 05 |
| Extending Capabilities | 怎么让它知道更多、连上更多系统、又不被信息淹没？ | 06 → 07a → 07b → 08 → 09 |
| Claude Code | 用的时候有哪两个旋钮？ | 10a → 10b → 10c → 10d → 10e |

每一章都建立在上一章之上，讲的时候可以反复回扣这三句话：

1. 模型看到的只有 **token**（01、02）。
2. 模型做的只有 **预测下一个 token，然后循环**（03）。
3. Agent、工具、RAG、MCP、Skills 都是在决定 **哪些 token 进入上下文**（04–09），模型选择和 effort 决定 **这个循环跑多贵、跑多久**（10）。

## 页面与笔记对照

| # | GIF | 时长 | 笔记 | 一句话 |
|---|---|---|---|---|
| 1 | `01_tokenization.gif` | 15.4 s | [01_tokenization.md](01_tokenization.md) | 文本先被切成 token，再变成整数 ID |
| 2 | `02a_embedding_lookup.gif` | 8.0 s | [02_embedding.md](02_embedding.md) | 每个 ID 查表得到一个向量 |
| 3 | `02b_embedding_space.gif` | 8.8 s | [02_embedding.md](02_embedding.md) | 意思相近的向量方向相近 |
| 4 | `02c_whole_path.gif` | 23.5 s | [02c_whole_path.md](02c_whole_path.md) | 全程总览：向量进，概率出，选一个 token，放回输入 |
| 5 | `02d_vectors_into_transformer.gif` | 23.0 s | [02_embedding.md](02_embedding.md) | 网络内部：逐层变换，最后一个向量得到分数 |
| 6 | `02e_one_network_per_token.gif` | 22.5 s | [02e_02f_network_structure.md](02e_02f_network_structure.md) | 同一套权重用在每个 token 上，attention 把各列连起来 |
| 7 | `02f_new_token_adds_column.gif` | 22.5 s | [02e_02f_network_structure.md](02e_02f_network_structure.md) | 每个新 token 加一列，前面的列复用，权重不变 |
| 8 | `03_generation_loop.gif` | 23.4 s | [03_generation_loop.md](03_generation_loop.md) | 一次只生成一个 token，然后重复 |
| 9 | `04a_one_big_prompt.gif` | 22.5 s | [04_agent_example.md](04_agent_example.md) | 例子 1/5：第 1 次调用，LLM 收到的是一个大提示词 |
| 10 | `04b_tool_call_is_text.gif` | 24.0 s | [04_agent_example.md](04_agent_example.md) | 例子 2/5：LLM 返回一段文字，harness 去执行 |
| 11 | `04c_second_call.gif` | 23.0 s | [04_agent_example.md](04_agent_example.md) | 例子 3/5：第 2 次调用全部重发，模型读到你的流程 |
| 12 | `04d_agent_at_work.gif` | 24.0 s | [04_agent_example.md](04_agent_example.md) | 例子 4/5：完整过程，6 次 LLM 调用，5 次工具执行 |
| 13 | `04e_two_loops.gif` | 23.5 s | [04_agent_example.md](04_agent_example.md) | 例子 5/5：两层循环，harness 套着 LLM |
| 14 | `04f_agent_loop.gif` | 21.4 s | [04_agent_loop.md](04_agent_loop.md) | 抽象总结：Think → Act → Observe |
| 15 | `05_tool_calling.gif` | 21.4 s | [05_tool_calling.md](05_tool_calling.md) | 模型只写结构化文本，执行的是 harness |
| 16 | `06_rag.gif` | 21.4 s | [06_rag.md](06_rag.md) | 先检索，再把检索结果放进 prompt |
| 17 | `06a_rag_pdf_to_chunks.gif` | 22.0 s | [06abc_rag_in_detail.md](06abc_rag_in_detail.md) | RAG 细节 1/3：PDF 提取文字，切成带元数据的 chunk |
| 18 | `06b_rag_chunks_to_vectors.gif` | 24.0 s | [06abc_rag_in_detail.md](06abc_rag_in_detail.md) | RAG 细节 2/3：每个 chunk 一个向量；和 LLM 的 embedding 层不是一回事 |
| 19 | `06c_rag_agent_uses_it.gif` | 23.0 s | [06abc_rag_in_detail.md](06abc_rag_in_detail.md) | RAG 细节 3/3：工具调用 → 向量比较 → 返回原文 |
| 20 | `07a_mcp_why.gif` | 6.7 s | [07_mcp.md](07_mcp.md) | M×N 个集成变成 M+N 个 |
| 21 | `07b_mcp_how.gif` | 16.1 s | [07_mcp.md](07_mcp.md) | 连接、发现、调用三步 |
| 22 | `08_skills.gif` | 19.4 s | [08_skills.md](08_skills.md) | 三级按需加载，装很多也不占上下文 |
| 23 | `09_context_engineering.gif` | 23.4 s | [09_context_engineering.md](09_context_engineering.md) | 上下文是有限资源，要管理 |
| 24 | `10a_model.gif` | 10.7 s | [10_model_vs_effort.md](10_model_vs_effort.md) | 模型 = 用哪套权重 |
| 25 | `10b_effort.gif` | 10.6 s | [10_model_vs_effort.md](10_model_vs_effort.md) | Effort = 同一个模型干多少活 |
| 26 | `10c_cost_formula.gif` | 5.7 s | [10_model_vs_effort.md](10_model_vs_effort.md) | 两个旋钮相乘 |
| 27 | `10d_same_task_models.gif` | 22.5 s | [10_model_vs_effort.md](10_model_vs_effort.md) | 同一个 DCM 请求换三个模型：速度、单价、判断质量不同 |
| 28 | `10e_same_task_effort.gif` | 23.0 s | [10_model_vs_effort.md](10_model_vs_effort.md) | 同一个 DCM 请求换四档 effort：轮数和思考量不同 |

另有 [glossary.md](glossary.md)：中英文术语对照，备查；[captions.md](captions.md)：每页动画底部说明文字的原文和翻译，可直接贴到 PPT。

`02c` 到 `02f`、`04a` 到 `04e` 是后来新增的九页，`02b` 末尾加了一个说明框，原始循环版文件夹里没有这些内容。原来的 `04_agent_loop.gif` 改名为 `04f_agent_loop.gif`，内容没变。生成脚本在 [../tools/anim/](../tools/anim/)，以后要改文字或节奏可以直接改脚本重新生成。

动画总时长约 9 分钟。

`06a` 到 `06c` 把 RAG 拆成三步细讲，用的是 DCM 例子里的那次规范检索。它们和 `06` 的总览内容重叠：只想点到为止放 `06`；想讲清楚放 `06a`–`06c`，可以不放 `06`。其中 `06b` 专门澄清了"RAG 的 embedding 模型"和"LLM 内部的 embedding 层"不是一回事。

`10d` 和 `10e` 沿用 04a–04e 的例子，展示换模型和换 effort 各自改变了什么。里面的时间、成本倍数和结果都是示意值。如果时间有限，可以用这两页代替 `10a`、`10b`，再用 `10c` 的公式收尾。

`04a` 到 `04e` 是一个连续的系列，用同一句请求 "How do we integrate DCM into this project?" 从头讲到尾：第 1 次调用发了什么、LLM 回了什么、第 2 次调用发了什么、完整过程、两层循环。每页右上角显示这句请求，左上角标着 PART 1–5 OF 5。这五页建议连着放。

`04f` 和 `05` 是更抽象的总结，用的是另一个例子（修复 Com 模块的测试）。时间紧时可以只留一页，或者都不放。

第 4 页（`04d`）同时用到了 skill、脚本、规范检索和上下文增长，可以作为第三章的引子：先看到一次完整的过程，再逐个展开 RAG、MCP、Skills 和上下文管理。

`02c` 到 `02f` 都在讲 embedding 和生成循环之间的那一段，四页全放会偏长。建议的取舍：

- **必放**：`02c`，它是连接前后的总览。
- **三选一或二**：`02d`（网络内部的完整流程）、`02e`（共享权重和列的结构）、`02f`（生成时加一列、为什么长上下文更贵）。`02d` 和 `02e` 内容有重叠，一般二选一。
- **听众有传统神经网络背景**时优先 `02e`，它正面纠正"固定输入口、空位填零"的想象。如果每页在动画之外再讲 1–2 分钟，全场大约 20–30 分钟；这只是按页数估的，请按你实际拿到的时间调整。

## 建议的学习顺序

1. 先按顺序把 01–03 读透。后面所有内容都依赖"token → 向量 → 预测下一个 token"这三步，这里不牢，后面讲起来会虚。
2. 再读 04、05。重点是分清 **模型** 和 **harness** 各自负责什么。
3. 06–09 可以当成同一个问题的四种答案来读：怎样把正确的信息在正确的时刻放进上下文。
4. 最后读 10，把成本和速度联系回 03 的循环。
5. 每篇末尾有自测题，合上笔记能答出来再往下。

## 放映注意事项

- **GIF 只播一遍**，播完停在完整画面上。翻到这一页时动画自动开始，所以先翻页、再开口。
- **翻回上一页会重播**。如果只是想回看某个画面，等它播完再讲。
- **编辑视图里这些页是空白的**（GIF 第一帧是白底），放映时正常。导出 PDF 发给别人时这些页也是空白，需要另外截最后一帧。
- **节奏由动画定**。每篇笔记里有时间轴表格，排练时对着表格练，确认你说的话和画面出现的内容同步。

## 讲的时候要主动说明的简化

这些地方动画为了清晰做了简化，如果听众里有熟悉细节的人，主动说一句比被问到更好：

| 页面 | 简化之处 | 一句话说明 |
|---|---|---|
| 01 | token ID 是编的 | "数字只是示意，不同模型的词表不一样" |
| 02b | 画成二维 | "真实是几千维，这里投影到二维方便看" |
| 03 | 只列了 4 个候选 | "实际是对词表里每一个 token 都给出概率" |
| 05 | `tool_use` 没有 `id` | "真实 API 里调用和结果靠 id 配对" |
| 07b | 工具名写成 `jira.get_issue` | "Claude Code 里显示为 `mcp__jira__get_issue`" |
| 10a | 神经网络画成全连接层 | "只是表示大小不同，真实结构是 Transformer" |
| 10a | Opus 标注 "most capable" | 目前产品线里 Opus 之上还有 Fable，见 [10 的笔记](10_model_vs_effort.md) |
| 10b | ≈1× 到 ≈5× | "倍数是示意，不是实测" |

## 排练清单

- [ ] 每一页能不看笔记说出"这一页的一句话"
- [ ] 01–03 的三个自测题全部答对
- [ ] 能说清模型和 harness 的分工（05）
- [ ] 能说清 MCP 和 Skills 的区别（08）
- [ ] 能用 03 的循环解释为什么大模型更慢、高 effort 更贵（10）
- [ ] 在 PowerPoint 里完整放映过一遍，确认每个 GIF 都停在最后一帧
- [ ] 计时：全程用时是否在限定时间内
