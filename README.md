# 冰块和饮料冷却模型

这个项目用一个简化的热力学模型，模拟常温可乐加入不同质量冰块后的降温、融冰、稀释和口感权衡。它可以用来回答一个很适合做科普内容的问题：少冰真的更浓吗？

模型的核心结论是：少冰不一定更好。冰太少时，冰会更快融完，但饮料可能仍然不够冷；冰足够多时，饮料能更快进入低温区，而融化量不会随加入冰块总量线性增加。

## 项目内容

```text
.
├── cola_ice_model.py              # 批量模拟、生成 CSV、图表和 Markdown 报告
├── visual_model_matplotlib.py     # Matplotlib 交互式滑块模型
├── generate_visual_model.py       # 生成独立 HTML 可视化页面
├── cola_ice_visual_model.html     # 由 generate_visual_model.py 生成的浏览器页面
├── cola_ice_report.md             # 由 cola_ice_model.py 生成的分析报告
├── templates/report.md            # 报告正文模板
├── requirements.txt               # Python 依赖
└── outputs/
    ├── cooling_curves.png         # 不同冰量下的降温曲线
    ├── ice_amount_tradeoff.png    # 冰量、温度、稀释之间的关系
    ├── taste_score.png            # 示例口感分数曲线
    └── simulation_summary.csv     # 批量模拟结果
```

## 模型假设

默认参数位于 `cola_ice_model.py` 的 `Params` 数据类中：

- 可乐质量：250 g
- 可乐初温：25 deg C
- 环境温度：25 deg C
- 冰块初温：-18 deg C
- 模拟时长：15 min
- 时间步长：0.5 s

模型把可乐近似为水溶液，并模拟三类主要过程：

- 饮料向冰块传热，冰块先升温到 0 deg C，再继续融化。
- 杯中液体质量随融冰增加，因此稀释比例会上升。
- 饮料也会从环境空气中吸热，出现回温趋势。

这里的口感分数只是为了比较方案而设定的示意指标，不是严格的感官科学模型。

## 安装依赖

建议使用 Python 3.10 或更新版本。

```bash
pip install -r requirements.txt
```

## 使用方法

运行批量模拟并重新生成输出文件：

```bash
python cola_ice_model.py
```

运行后会更新：

- `outputs/simulation_summary.csv`
- `outputs/cooling_curves.png`
- `outputs/ice_amount_tradeoff.png`
- `outputs/taste_score.png`
- `cola_ice_report.md`

打开 Matplotlib 交互式模型：

```bash
python visual_model_matplotlib.py
```

它会弹出一个带滑块的窗口，可以调整饮料质量、冰块质量、初始温度、环境温度、饮用时间等参数。

重新生成独立 HTML 可视化页面：

```bash
python generate_visual_model.py
```

然后直接用浏览器打开 `cola_ice_visual_model.html`。

## 生成物和发布

`cola_ice_visual_model.html` 和 `cola_ice_report.md` 是仓库中保留的生成物，方便 GitHub Pages 和读者直接打开。修改模型、页面文案或报告模板后，建议重新运行：

```bash
python cola_ice_model.py
python generate_visual_model.py
```

`outputs/` 目录包含本地生成的 CSV 和图片，默认被 `.gitignore` 忽略。如果需要把报告里的图片一并发布到 GitHub Pages，可以临时移除这条忽略规则，或改用单独的发布流程拷贝这些图片。

## 输出结果怎么读

`simulation_summary.csv` 按不同初始冰量和不同时间点记录模拟结果，主要字段包括：

- `initial_ice_g`：初始冰块质量
- `minute`：观察时间点
- `temperature_c`：饮料温度
- `ice_melted_g`：已经融化的冰质量
- `ice_remaining_g`：剩余冰块质量
- `dilution_pct`：相对于初始饮料质量的稀释比例
- `taste_score`：示意口感分数

三张图分别展示：

- `cooling_curves.png`：不同冰量随时间的降温曲线。
- `ice_amount_tradeoff.png`：冰量增加时，温度和稀释比例如何变化。
- `taste_score.png`：在简化口感指标下，不同冰量的综合表现。

## 典型结论

在默认参数下，25 g 到 50 g 的冰量往往不足以让 250 g 常温可乐快速变冷；100 g 到 150 g 左右的冰量通常能在几分钟内把温度压到较低区间，同时保留一定冰块。继续增加冰量会让饮料更冷，但也会占据杯中空间，实际饮用体验未必继续提升。

## 局限性

这个模型适合做趋势解释和实验设计起点，但不能替代真实测量。它没有精细模拟：

- 冰块形状和表面积差异
- 搅拌带来的传热变化
- 杯壁材质和杯子热容量
- 二氧化碳逸出对口感的影响
- 真实消费者对甜度、冰爽感和水感的主观偏好

如果要做视频或文章，建议把模型结果和实际称重、温度记录实验结合起来使用。
