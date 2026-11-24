# 08 · Skills（技能）与渐进式加载

![Skills](../llm_agent_animations_single_page/08_skills.gif)

> **一句话**：Skill 是一个文件夹，里面装着"某类任务该怎么做"的说明和脚本。平时只有一行简介在上下文里，用到的时候才加载正文，脚本只运行、不加载。

## 在演讲里的位置

RAG 给了 Agent 知识，MCP 给了它系统访问，Skills 给它**做事的方法**。这一页的标题重点其实是副标题 "Progressive Disclosure"（渐进式加载）：它展示了一种节省上下文的设计思路，直接引出下一页的上下文管理。

## 画面布局

- **左边 · CONTEXT WINDOW**：一个竖条，表示模型的上下文。内容从底部往上堆。
- **右边 · INSTALLED SKILLS (on disk)**：磁盘上安装的三个 skill，每个分成三层：

| Skill | 简介（L1） | 正文（L2） | 资源（L3） |
|---|---|---|---|
| `misra-check/` | Check C code against MISRA C rules | SKILL.md | `scripts/check_misra.py`、`rules/misra_c2012.json` |
| `arxml-editor/` | Read & edit AUTOSAR ARXML files | SKILL.md | `scripts/arxml_tool.py`、`reference/schema.md` |
| `pptx/` | Create PowerPoint presentations | SKILL.md | `scripts/build.py`、`templates/` |

整页动画的看点是：**右边的东西很多，左边进去的很少**。

## 动画逐步解读

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0–4 s | Level 1: at startup only each skill's name + description is loaded | 三个 skill 的顶部一行各飞出一个小条，落入上下文 | "启动时，每个 skill 只有名字和一句简介进入上下文" |
| 5–7.5 s | The model matches the task against the skill descriptions | 用户消息 "check Com_Send.c …" 进入；`misra-check` 亮起，其余两个变淡，出现 "description matches the task ✓" | "模型拿任务和简介比对，发现 misra-check 对得上" |
| 8–10 s | Level 2: the full SKILL.md is read only when it is needed | misra-check 的 SKILL.md 作为一大块进入上下文 | "这时才读取这一个 skill 的完整说明" |
| 10.5–15 s | Level 3: scripts run via tools; only their output enters the context | 弹出终端窗口运行脚本；之后只有 "script output: 3 violations" 一小条进入上下文 | "脚本被执行，进入上下文的只有结果" |
| 15.5 s 起 | Many skills installed, minimal context cost | 右下角出现三级的总结表 | 收尾 |

终端窗口里的内容：

```
$ python scripts/check_misra.py Com_Send.c
3 violations:
  Rule 10.3  line 218
  Rule 11.5  line 301   · Rule 15.7  line 377
```

下方的红字是这一步的要点：*"the script's code never enters the context, only its output"*。

结束时上下文里（从下到上）：System prompt → 三条简介 → 用户消息 → misra-check 的 SKILL.md → 脚本输出。另外两个 skill 的正文和所有脚本代码都**没有**进来。

## 三级加载

画面右下角的总结表：

| 级别 | 内容 | 什么时候进入上下文 |
|---|---|---|
| **L1** | name + description | 始终加载（每个约 100 token） |
| **L2** | SKILL.md 正文 | 任务匹配时加载 |
| **L3** | 脚本和资源文件 | 需要时才运行或读取 |

## 需要真正搞懂的概念

### 一个 skill 是什么

就是一个文件夹。核心是一个 `SKILL.md` 文件：开头是名字和简介，后面是给模型看的操作说明（什么情况下用、分几步做、注意什么）。旁边可以放脚本、模板、参考资料。没有特殊的格式或编译步骤，会写文档就会写 skill。

### 为什么不把所有说明都放进系统提示

算一笔账就明白了。假设装了 50 个 skill，每个正文几千 token：

- **全部预先加载**：几十万 token，上下文直接占满，而一次任务通常只用到其中一两个。
- **渐进式加载**：50 × 约 100 token ≈ 5000 token 的固定开销，其余按需付费。

这就是字幕说的 "Many skills installed, minimal context cost"。

### 简介是触发条件

模型是否启用一个 skill，只看 L1 的那句简介。简介写得含糊，skill 就不会在该用的时候被用上；写得太宽，又会在不该用的时候被触发。**写好简介是写 skill 最重要的一步**，这和 05 里工具说明的道理一样。

### 为什么脚本代码不进上下文

- 模型不需要读懂 `check_misra.py` 的几百行代码，它只需要知道"运行它，看输出"。
- 脚本是确定性的：同样的输入永远得到同样的结果，比让模型自己逐条检查规则更可靠，也更便宜。
- 运行脚本用的是 05 讲的工具调用（画面里终端窗口右上角标着 "Bash tool"）。

可以总结成一个分工：**需要判断的交给模型，可以写成确定程序的交给脚本**。

### Skills 和 MCP 的区别

这是最容易被问到的问题，建议准备好这张表：

| | MCP | Skills |
|---|---|---|
| 提供的是 | 对外部系统的**访问** | 做某类事的**方法** |
| 形式 | 一个运行着的 server 程序 | 一个文件夹（文档 + 脚本） |
| 进入上下文的 | 工具的说明 | 简介，按需加载正文 |
| 例子 | 查 Jira issue、看 Git 记录 | 按 MISRA 规则检查代码、按公司模板做 PPT |
| 类比 | 给新同事开通系统账号 | 给新同事一本操作手册 |

两者可以配合：一个 skill 的说明里可以写"先用 Jira 的工具查到 issue，再按以下步骤处理"。

### Skills 和 CLAUDE.md 的区别

- **CLAUDE.md**：每次会话都**全部**加载。适合放始终适用的内容：项目约定、常用命令、目录结构。
- **Skill**：按需加载。适合放只在特定任务中才用得上的内容。

判断标准：这段说明是不是每次都用得上？是，放 CLAUDE.md；不是，做成 skill。

## 常见误解

- **"Skill 是一种插件代码"**：主体是文档。脚本是可选的。
- **"装的 skill 越多上下文越满"**：只增加每个约 100 token 的简介。
- **"模型会读脚本的源码然后模仿着做"**：不会。脚本是被执行的，模型看到的只有输出。

## 听众可能会问

**Q：谁来决定用哪个 skill？**
模型，根据任务和简介的匹配程度。用户也可以直接点名要求使用某个 skill。

**Q：我们团队的规范能做成 skill 吗？**
这正是它的典型用途。把规范写成 SKILL.md，把检查工具作为脚本放在旁边。

**Q：skill 放在哪里？**
可以放在个人目录（只对自己生效），也可以放在项目仓库里（随代码一起共享给团队）。

**Q：模型会不会该用的时候没用？**
会，通常是简介写得不够清楚。改进简介是首选的修复办法。

## 承上启下

- **前两页**：RAG 给知识，MCP 给访问。
- **这一页**：Skills 给方法，同时演示了"按需加载"的思路。
- **下一页**：把这个思路推广开。上下文是有限的，所有东西都在争这块空间。
- **过渡句**："这一页反复出现一个词：上下文。我们一直在小心翼翼地控制什么东西进去。为什么要这么小心？下一页专门讲。"

## 自测

<details>
<summary>1. 说出三级加载各自的内容和加载时机。</summary>

L1：名字和简介，始终加载。L2：SKILL.md 正文，任务匹配时加载。L3：脚本和资源，需要时运行或读取，脚本只有输出进入上下文。
</details>

<details>
<summary>2. 模型凭什么决定启用某个 skill？</summary>

凭 L1 的简介与当前任务是否匹配。
</details>

<details>
<summary>3. 用一句话区分 MCP 和 Skills。</summary>

MCP 让 Agent 能访问外部系统；Skills 告诉 Agent 某类任务该怎么做。
</details>
