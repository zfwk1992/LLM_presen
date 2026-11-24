# 02e、02f · 网络的结构：每个 token 一列

这两页把 02c 里那个 "Transformer" 黑盒打开，回答一个具体的问题：**网络是怎么同时处理 5 个 token 的？提示词长短不同，网络会变吗？**

![One network per token](../llm_agent_animations_single_page/02e_one_network_per_token.gif)

![A new token adds a column](../llm_agent_animations_single_page/02f_new_token_adds_column.gif)

> **一句话**：网络的宽度是 d（一个向量的大小）。有几个 token，就把同一套权重用几次，形成几"列"；列与列之间靠 attention 连接。新增一个 token 就新增一列，权重始终是同一套。

## 先纠正一个常见的想象

很多人（包括学过传统神经网络的人）会这样想象：

> 网络有固定数量的输入口，比如 20 万个。我的提示词只有 10 个 token，就占 10 个口，其余填零。所以无论提示词多长，计算量都一样。

**这个想象不对。** 实际情况是：

| | 错误的想象 | 实际情况 |
|---|---|---|
| 固定的是什么 | token 的个数（输入口数量） | 每个向量的维数 d |
| 短提示词 | 空位填零，照样全算 | 只有几列，算得少 |
| 长提示词 | 计算量不变 | 列数多，算得多 |
| 权重和位置的关系 | 每个输入口有自己专属的权重 | 所有位置共用同一套权重 |

"上下文窗口 200K"是最多能有多少列，不是固定有多少列。

## 第一页：一个网络，复制给每个 token（02e，22.5 s）

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0.8 s | ① One token: its vector of d numbers goes through one small network | 只有一个 token `The`，它的向量向下进入一个标着 MLP 的方块，出来一个新向量；旁边标注 "d numbers wide" | "先看一个 token。它的向量有 d 个数，进入一个小网络，出来还是 d 个数。网络的宽度就是 d" |
| 5.0 s | ② Five tokens: the same network is used five times, at the same time | 另外 4 个 token 依次出现，每个下面都"盖"出一个一模一样的 MLP；一条虚线把 5 个 MLP 串到右边的 "one set of weights" | "5 个 token，就把同一个网络用 5 次。权重只存一份，5 个位置同时计算" |
| 9.6 s | ③ Attention links the copies: each token reads the ones before it | MLP 上方出现连线，全部从左边的列指向右边的列；外面出现 Layer 1 的框 | "光是复制还不够，它们彼此看不见。attention 把它们连起来：每个 token 读取它前面的 token" |
| 14.6 s | ④ Attention + MLP is one layer. All columns pass layer after layer | 省略号、Layer N、最后一行向量；一条亮带从上到下扫过所有列 | "attention 加 MLP 是一层。这样的层有 N 层，所有列一起一层一层往下走" |
| 18.2 s | ⑤ The last column has seen everything: its output gives the next token | 最后一列的输出被橙色框出，向下得到 `·bus` | "最后一列读到了前面所有 token，所以用它的输出来得到下一个 token" |

画面右侧依次出现四段说明，可以直接照着讲：

- **Width = d**：the size of one vector, not the number of tokens
- **Attention = the links**：each token reads the tokens before it; earlier tokens never read later ones
- **one set of weights (for this layer)**：stored once, used in every column · 5 tokens → 5 columns, no extra weights
- **Layer by layer**：every column passes layer 1, then every column passes layer 2, …

结尾的深色框：**One set of weights. One column per token.**

### 这一页要讲清楚的四件事

**1. 宽度是 d，不是 token 数。** 每一层的权重规定的是"d 个数怎样变成新的 d 个数"。这个规则可以用在任意多个 token 上。

**2. "复制"是同一套权重用多次。** 画面里 5 个 MLP 方块下面都写着 "same weights"，一条虚线把它们连到右边同一个权重框。内存里权重只有一份，token 再多，参数量也不增加。好比一个印章在 5 个位置各盖一次。

**3. 连接只发生在 attention，而且是单向的。** MLP 之间没有连线，每一列各算各的。列与列的信息交换全在 attention 那一步，并且只能"往前读"：第 5 列读第 1–4 列，第 1 列读不到任何别的列。原因很简单：生成的时候，后面的 token 还不存在。

**4. 同时算，按层推进。** 5 列是并行计算的，不排队。顺序是：所有列过第 1 层，再所有列过第 2 层……每一层有自己的一套权重（画面上 "N layers, each with its own weights"），在这一层里同样被所有列共用。

### 用一张表理解"为什么能同时算"

输入是一张 5 行 × d 列的数字表，每一层的权重相当于一个公式。把公式应用到整张表，5 行同时得到结果。表有 1000 行，就同时算 1000 行。公式不变，行数随意。

## 第二页：新 token 加一列（02f，22.5 s）

这一页把每个 token 画成一根竖着的"柱子"，里面是 Layer 1、Layer 2 … Layer N。

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0.8 s | ① The prompt: 5 tokens, 5 columns, all computed in one pass | 5 根柱子同时出现，一条亮带同时从上到下扫过 5 根；顶部标签 "forward pass #1 · 5 columns computed together" | "提示词的 5 个 token，5 列，一次全部算完" |
| 4.6 s | ② The last column gives the next token | 最后一根柱子下方的输出被框出，得到 `·bus` | "最后一列给出下一个 token" |
| 7.4 s | ③ The new token becomes column 6: only this column is new work | `·bus` 飞到右上方成为第 6 个 token；前 5 根柱子变灰，底部出现 "saved"；第 6 根柱子出现，亮带只扫这一根 | "新 token 成为第 6 列。前 5 列算过了，不用重算，只算新的这一列" |
| 11.0 s | ④ It reads the saved results of the columns before it | 每一层都有橙色横线从前面的柱子通到新柱子 | "新的一列在每一层都要读取前面各列保存下来的结果" |
| 14.6 s | ⑤ Every new token adds one column: more to read, same weights | `·every` 成为第 7 列，同样的过程；标签变成 "forward pass #3" | "再来一个 token，再加一列。要读的列更多了，权重还是那一套" |
| 18.6 s | ⑥ Longer context costs more per step; the network never changes | 右侧出现 "Longer context" 的说明和深色框 | "上下文越长，每一步越贵；但网络本身从来没有变过" |

右侧的面板随着每一次前向传播更新，这是这一页最有说服力的部分：

| This forward pass | #1 | #2 | #3 |
|---|---|---|---|
| tokens in context | 5 | 6 | 7 |
| columns computed now | 5 | 1 | 1 |
| columns read from memory | 0 | 5 | 6 |
| weights | same | same | same |

结尾的深色框：**New token = new column. The weights stay the same.**

### 这一页要讲清楚的三件事

**1. 提示词是一次算完的，生成是一列一列加的。** 第一次前向传播同时算 5 列。之后每生成一个 token，只新算 1 列。

**2. 前面的列被保存下来复用。** 因为每一列只依赖它自己和它前面的列，所以新 token 加进来之后，前面各列的结果完全不变，没有必要重算。画面里变灰并标着 "saved" 的柱子就是这个意思。

**3. 长度影响的是每一步的代价，不是网络。** 看面板的最后两行："columns read from memory" 从 0 涨到 5 再到 6，"weights" 一直是 same。上下文越长，新的一列要读的东西越多，所以每一步越慢、越贵。这就是 09 那页上下文工程在成本上的意义。

## 这两页和你之前的理解怎么对应

把前面几轮讨论的结论和画面对上：

| 你的理解 | 是否正确 | 画面上的对应 |
|---|---|---|
| 第一层的宽度由向量维度 d 决定 | 正确 | 02e 第 ① 步的 "d numbers wide" 和右侧的 "Width = d" |
| 5 个 token 的输入是 5 × d 的矩阵 | 正确 | 02e 的 5 条向量 |
| 把处理一个 token 的网络复制成 5 份 | 正确，但是同一套权重用 5 次 | 02e 第 ② 步，5 个标着 "same weights" 的 MLP |
| 这 5 份之间互相连接 | 正确，连接在 attention，方向只能往前读 | 02e 第 ③ 步的连线 |
| 结果会被缓存 | 正确 | 02f 里变灰、标着 "saved" 的柱子 |
| 所有输入口都参与计算，空的填零 | 不正确 | 02f 的面板：token 数是几，列数就是几 |
| 无论提示词长短，计算量一样 | 不正确 | 02f 的面板：要读的列数随长度增加 |

## 画面上的简化

- **MLP 上方的连线粗细相同**：真实的 attention 对不同的 token 读取的多少不同（02d 用线的粗细表示了这一点）。这里为了突出"谁连着谁"，画成一样粗。
- **位置信息没有画**：02d 里有 "+ pos" 那一步，这两页省略了。
- **02f 里每层写的是 "attn + MLP"**：就是 02e 里 attention 和 MLP 的合称。
- **"saved" 保存的内容**：实际保存的是每一列在每一层供后面读取的那部分中间结果，业内叫 KV cache。讲的时候说"保存下来的结果"就够了。

## 和其他页的关系

| 页面 | 角度 | 能不能跳过 |
|---|---|---|
| 02c 全程总览 | 把网络当黑盒，看数据怎么流 | 不建议跳 |
| 02d 向量进入 Transformer | 网络内部的完整流程，含位置信息、attention 权重、输出打分 | 可以跳 |
| **02e 一个网络复制给每个 token** | 网络的结构：共享权重、列、attention 连接 | 听众有传统神经网络背景时建议保留 |
| **02f 新 token 加一列** | 生成时的增量计算和成本 | 想讲清楚"为什么长上下文更贵"时保留 |
| 03 生成循环 | 连续多轮、采样、结束条件 | 核心页 |

02d 和 02e 有重叠：两页都画了列、attention 和 MLP。02d 更完整，02e 更聚焦在"共享权重"这一点上。时间有限时二选一即可；如果听众和你一样是从"固定输入口"的想象出发的，选 02e。

## 自测

<details>
<summary>1. 网络里固定不变的尺寸是什么？随输入变化的是什么？</summary>

固定的是向量的维数 d 和权重。变化的是列数，也就是 token 的个数。
</details>

<details>
<summary>2. 5 个 token 对应 5 个 MLP，参数量是 1 个 MLP 的 5 倍吗？</summary>

不是。是同一套权重被用了 5 次，参数只有一份。
</details>

<details>
<summary>3. 列与列之间在哪里连接？方向是怎样的？</summary>

在 attention 那一步。每一列只读取它前面的列，前面的列读不到后面的。
</details>

<details>
<summary>4. 生成第 2 个 token 时，前 5 列需要重新计算吗？为什么？</summary>

不需要。每一列只依赖它自己和它前面的列，新 token 加入不会改变前面各列的结果，所以直接复用保存的结果。
</details>

<details>
<summary>5. 提示词从 10 个 token 变成 10000 个 token，什么变了，什么没变？</summary>

变了：列数，以及每一步要读取和计算的量，所以更慢、更贵。没变：网络的权重和结构。
</details>
