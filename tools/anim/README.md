# 动画生成脚本

这里的脚本生成后来新增或修改的几页动画，输出到 `llm_agent_animations_single_page/`。

| 脚本 | 生成 |
|---|---|
| `whole_path.py` | `02c_whole_path.gif` |
| `inside_transformer.py` | `02d_vectors_into_transformer.gif` |
| `copies.py` | `02e_one_network_per_token.gif` |
| `add_column.py` | `02f_new_token_adds_column.gif` |
| `one_big_prompt.py` | `04a_one_big_prompt.gif` |
| `tool_call_is_text.py` | `04b_tool_call_is_text.gif` |
| `second_call.py` | `04c_second_call.gif` |
| `agent_at_work.py` | `04d_agent_at_work.gif` |
| `two_loops.py` | `04e_two_loops.gif` |
| `rag_pdf_to_chunks.py` | `06a_rag_pdf_to_chunks.gif` |
| `rag_chunks_to_vectors.py` | `06b_rag_chunks_to_vectors.gif` |
| `rag_agent_uses_it.py` | `06c_rag_agent_uses_it.gif` |
| `mcp_in_detail.py` | `07c_mcp_in_detail.gif` |
| `architecture.py` | `09b_architecture.gif` |
| `architecture_detail.py` | `09c_architecture_detail.gif` |
| `same_task_models.py` | `10d_same_task_models.gif` |
| `same_task_effort.py` | `10e_same_task_effort.gif` |
| `note_02b.py` | 给 `02b_embedding_space.gif` 加右下角的说明框 |
| `gifout.py` | 公用部分：标题、底部说明条、token 方块、GIF 输出 |

## 依赖

- Python 3，`pillow`、`numpy`、`matplotlib`（只用到它自带的 DejaVu Sans Mono 字体）
- Inter 字体：仓库里没有包含。从 Google Fonts 下载 Inter 的可变字体文件，保存为 `fonts/Inter-var.ttf`

## 用法

在本目录下运行：

```
python whole_path.py ../../llm_agent_animations_single_page/02c_whole_path.gif
python inside_transformer.py ../../llm_agent_animations_single_page/02d_vectors_into_transformer.gif
python note_02b.py ../../llm_agent_animations ../../llm_agent_animations_single_page <预览图目录> write
```

只想看某几个时刻的画面而不生成整个 GIF：

```
python whole_path.py <预览图目录> preview 8.2 14.0 23.5
```

文字、时间点和布局都在各脚本顶部和 `render()` 函数里，改完重新运行即可。
