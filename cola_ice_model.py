from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


OUT = Path("outputs")
OUT.mkdir(exist_ok=True)


@dataclass(frozen=True)
class Params:
    cola_mass_g: float = 250.0
    cola_initial_c: float = 25.0
    ambient_c: float = 25.0
    ice_initial_c: float = -18.0
    cola_cp_j_gk: float = 4.0
    water_cp_j_gk: float = 4.18
    ice_cp_j_gk: float = 2.1
    ice_fusion_j_g: float = 334.0
    ice_transfer_w_per_gk: float = 0.08
    env_transfer_w_per_k: float = 0.25
    dt_s: float = 0.5
    total_time_s: float = 15 * 60


def theoretical_melt_for_target(
    target_c: float, ice_mass_g: float, p: Params
) -> tuple[float, bool]:
    """Return melt mass needed to reach target_c in an isolated system.

    The calculation assumes some ice is still present at the target temperature.
    The ice starts below zero, warms to 0 C, then the melted part warms to target_c.
    """
    heat_removed = p.cola_mass_g * p.cola_cp_j_gk * (p.cola_initial_c - target_c)
    sensible_by_all_ice = ice_mass_g * p.ice_cp_j_gk * (0 - p.ice_initial_c)
    heat_per_g_melt = p.ice_fusion_j_g + p.water_cp_j_gk * target_c
    melt_g = max(0.0, (heat_removed - sensible_by_all_ice) / heat_per_g_melt)
    return min(melt_g, ice_mass_g), melt_g <= ice_mass_g


def simulate(ice_initial_g: float, p: Params) -> pd.DataFrame:
    steps = int(p.total_time_s / p.dt_s) + 1

    t = np.zeros(steps)
    temp = np.zeros(steps)
    ice = np.zeros(steps)
    melted = np.zeros(steps)
    liquid_mass = np.zeros(steps)

    temp[0] = p.cola_initial_c
    ice[0] = ice_initial_g
    melted[0] = 0.0
    liquid_mass[0] = p.cola_mass_g

    # Ice is treated as a single thermal reservoir before it reaches 0 C.
    # After that, incoming heat melts ice. This keeps the model compact enough
    # for a blog post while preserving the important energy scales.
    ice_temp = p.ice_initial_c

    for i in range(1, steps):
        t[i] = i * p.dt_s
        T = temp[i - 1]
        m_ice = ice[i - 1]
        m_liq = liquid_mass[i - 1]

        q_env = p.env_transfer_w_per_k * (p.ambient_c - T) * p.dt_s
        q_to_ice = 0.0
        dm = 0.0

        if m_ice > 1e-9 and T > 0:
            heat_transfer = p.ice_transfer_w_per_gk * m_ice * max(T - max(ice_temp, 0.0), 0.0)
            q_available = heat_transfer * p.dt_s

            if ice_temp < 0:
                q_warm_needed = m_ice * p.ice_cp_j_gk * (0 - ice_temp)
                q_warm = min(q_available, q_warm_needed)
                ice_temp += q_warm / (m_ice * p.ice_cp_j_gk)
                q_to_ice += q_warm
                q_available -= q_warm

            if q_available > 0 and ice_temp >= -1e-9 and m_ice > 0:
                heat_per_g_melt = p.ice_fusion_j_g + p.water_cp_j_gk * max(T, 0.0)
                dm = min(m_ice, q_available / heat_per_g_melt)
                q_to_ice += dm * heat_per_g_melt

        heat_capacity = m_liq * p.cola_cp_j_gk
        T_next = T + (q_env - q_to_ice) / heat_capacity
        T_next = max(T_next, 0.0 if m_ice - dm > 1e-9 else -5.0)

        temp[i] = T_next
        ice[i] = max(0.0, m_ice - dm)
        melted[i] = melted[i - 1] + dm
        liquid_mass[i] = m_liq + dm

        if ice[i] <= 1e-9:
            ice_temp = 0.0

    return pd.DataFrame(
        {
            "time_s": t,
            "time_min": t / 60,
            "temperature_c": temp,
            "ice_remaining_g": ice,
            "ice_melted_g": melted,
            "dilution_pct": melted / p.cola_mass_g * 100,
            "initial_ice_g": ice_initial_g,
        }
    )


def taste_score(
    temp_c: float, dilution_pct: float, ice_remaining_g: float, initial_ice_g: float
) -> float:
    """Illustrative score for comparing scenarios, not a universal taste law."""
    cold_score = 88 / (1 + np.exp((temp_c - 8.0) / 1.8))
    overcold_penalty = 1.2 * max(0.0, 2.0 - temp_c)
    watery_penalty = 1.6 * dilution_pct
    crowding_penalty = 0.22 * max(0.0, initial_ice_g - 150.0)
    no_ice_penalty = 8.0 if ice_remaining_g <= 0 and temp_c > 6 else 0.0
    return float(
        np.clip(
            cold_score
            - overcold_penalty
            - watery_penalty
            - crowding_penalty
            - no_ice_penalty,
            0,
            100,
        )
    )


def summarize_cases(p: Params) -> pd.DataFrame:
    cases = []
    for ice_g in np.arange(0, 251, 5):
        df = simulate(float(ice_g), p)
        for minute in (2, 5, 10, 15):
            row = df.iloc[(df["time_min"] - minute).abs().argmin()]
            cases.append(
                {
                    "initial_ice_g": ice_g,
                    "minute": minute,
                    "temperature_c": row.temperature_c,
                    "ice_melted_g": row.ice_melted_g,
                    "ice_remaining_g": row.ice_remaining_g,
                    "dilution_pct": row.dilution_pct,
                    "taste_score": taste_score(
                        row.temperature_c,
                        row.dilution_pct,
                        row.ice_remaining_g,
                        ice_g,
                    ),
                }
            )
    return pd.DataFrame(cases)


def make_plots(summary: pd.DataFrame, p: Params) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")

    selected = [25, 50, 75, 100, 150, 200]
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    for ice_g in selected:
        df = simulate(ice_g, p)
        ax.plot(df["time_min"], df["temperature_c"], label=f"{ice_g} g ice")
    ax.axhspan(0, 6, color="#8fd3ff", alpha=0.16, label="very cold zone")
    ax.set_xlabel("Time after adding ice (min)")
    ax.set_ylabel("Cola temperature (deg C)")
    ax.set_title("Cooling curves for a 250 g cola at 25 deg C")
    ax.legend(ncol=2)
    fig.tight_layout()
    fig.savefig(OUT / "cooling_curves.png", dpi=180)
    plt.close(fig)

    five = summary[summary["minute"] == 5].copy()
    ten = summary[summary["minute"] == 10].copy()

    fig, ax1 = plt.subplots(figsize=(8.5, 5.2))
    ax1.plot(five["initial_ice_g"], five["temperature_c"], color="#0b6fa4", label="5 min temp")
    ax1.plot(ten["initial_ice_g"], ten["temperature_c"], color="#75aadb", label="10 min temp")
    ax1.set_xlabel("Initial ice mass (g)")
    ax1.set_ylabel("Temperature (deg C)")
    ax1.set_ylim(0, p.cola_initial_c + 1)
    ax2 = ax1.twinx()
    ax2.plot(five["initial_ice_g"], five["dilution_pct"], color="#c44e52", label="5 min dilution")
    ax2.plot(ten["initial_ice_g"], ten["dilution_pct"], color="#e49a9d", label="10 min dilution")
    ax2.set_ylabel("Dilution from melted ice (%)")
    lines = ax1.get_lines() + ax2.get_lines()
    ax1.legend(lines, [line.get_label() for line in lines], loc="center right")
    ax1.set_title("More ice cools faster; dilution does not rise linearly")
    fig.tight_layout()
    fig.savefig(OUT / "ice_amount_tradeoff.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    for minute, color in [(2, "#7a5195"), (5, "#ef5675"), (10, "#ffa600")]:
        sub = summary[summary["minute"] == minute]
        ax.plot(sub["initial_ice_g"], sub["taste_score"], color=color, label=f"{minute} min")
    ax.set_xlabel("Initial ice mass (g)")
    ax.set_ylabel("Illustrative taste score")
    ax.set_title("A simple taste index favors enough ice, not minimal ice")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "taste_score.png", dpi=180)
    plt.close(fig)


def write_report(summary: pd.DataFrame, p: Params) -> None:
    five = summary[summary["minute"] == 5].copy()
    ten = summary[summary["minute"] == 10].copy()
    best5 = five.loc[five["taste_score"].idxmax()]
    best10 = ten.loc[ten["taste_score"].idxmax()]

    target_rows = []
    for ice_g in [25, 50, 75, 100, 150, 200]:
        melt, enough = theoretical_melt_for_target(4.0, ice_g, p)
        target_rows.append((ice_g, melt, enough))

    table_rows = []
    for ice_g in [25, 50, 75, 100, 150, 200]:
        row5 = five[five["initial_ice_g"] == ice_g].iloc[0]
        row10 = ten[ten["initial_ice_g"] == ice_g].iloc[0]
        table_rows.append(
            f"| {ice_g:.0f} | {row5.temperature_c:.1f} | {row5.ice_melted_g:.1f} | "
            f"{row5.dilution_pct:.1f}% | {row10.temperature_c:.1f} | "
            f"{row10.ice_melted_g:.1f} | {row10.dilution_pct:.1f}% |"
        )

    theory_table = [
        f"| {ice_g:.0f} | {melt:.1f} | {'yes' if enough else 'no'} |"
        for ice_g, melt, enough in target_rows
    ]

    report = f"""# 一杯可乐应该加多少冰？一个简化数学模型

## 摘要

本文研究的问题是：向一杯常温可乐中加入冰块时，怎样在“快速降温”和“少融化、少稀释”之间取得平衡。

模型给出的核心结论是：**少冰并不等于少稀释**。当冰量不足时，冰会很快全部融化，但饮料仍然可能不够冷；当冰量足够时，可乐能更快进入低温区，而融化量不会随加冰量线性增加。以 250 g、25 deg C 的可乐为例，若希望在几分钟内获得接近冰镇的口感，模型建议使用约 **100-150 g 大冰块**，而不是只放一两小块。

## 1. 问题与假设

我们把一杯可乐简化为近似水溶液，并采用以下基准参数：

- 可乐质量：{p.cola_mass_g:.0f} g
- 可乐初温：{p.cola_initial_c:.0f} deg C
- 环境温度：{p.ambient_c:.0f} deg C
- 冰块初温：{p.ice_initial_c:.0f} deg C
- 可乐比热容：{p.cola_cp_j_gk:.2f} J/(g K)
- 冰的比热容：{p.ice_cp_j_gk:.2f} J/(g K)
- 冰的熔化潜热：{p.ice_fusion_j_g:.0f} J/g

这个模型忽略了可乐中糖、酸、二氧化碳对热容的细小修正，也没有直接模拟气泡逸出。它的目标不是给出唯一真理，而是解释主要趋势。

## 2. 封闭体系热量守恒

如果只考虑热量守恒，把 {p.cola_mass_g:.0f} g 可乐从 {p.cola_initial_c:.0f} deg C 降到 4 deg C，需要移走的热量约为：

```text
Q = m c Delta T = {p.cola_mass_g:.0f} x {p.cola_cp_j_gk:.1f} x ({p.cola_initial_c:.0f} - 4)
  = {p.cola_mass_g * p.cola_cp_j_gk * (p.cola_initial_c - 4):.0f} J
```

1 g、0 deg C 的冰融化为水并升到 4 deg C，大约吸收：

```text
334 + 4.18 x 4 = 351 J
```

因此，如果冰已经是 0 deg C，理论上需要融化大约 60 g 冰。若冰从 -18 deg C 冰箱中取出，冰块本身先升温到 0 deg C 也会吸热，所以所需融化量会略低。

| 初始冰量 (g) | 达到 4 deg C 理论融化量 (g) | 冰量是否足够 |
|---:|---:|:---:|
{chr(10).join(theory_table)}

这张表说明了一个关键点：只放 25 g 或 50 g 冰，理论上连把可乐降到 4 deg C 都不够；冰可能全融了，但可乐仍然不够冷。

## 3. 动态模型：降温速度、融化和回温

现实中，可乐不是瞬间达到热平衡。冰块和可乐之间的传热需要时间，杯子也会从空气中吸热。因此脚本中进一步使用了一个动态模型：

```text
环境给可乐的热量 = k_env (T_air - T_cola)
可乐传给冰的热量 = k_ice m_ice (T_cola - T_ice_surface)
冰未到 0 deg C 时，热量先用于升温
冰到 0 deg C 后，热量用于融化冰
```

这里把冰块表面积的影响简化进了 `k_ice m_ice`。这意味着冰越多，整体接触面积越大，降温越快。这个近似适合解释趋势，但不适合替代真实实验。

## 4. 模拟结果

| 初始冰量 (g) | 5 min 温度 (deg C) | 5 min 融冰 (g) | 5 min 稀释 | 10 min 温度 (deg C) | 10 min 融冰 (g) | 10 min 稀释 |
|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(table_rows)}

从结果看：

- 25 g 冰会全部融化，饮料仍然偏暖。
- 50-75 g 冰开始接近可接受区间，但冰量余量很小。
- 100-150 g 冰能在几分钟内把温度压到较低，同时保留部分冰块。
- 继续增加到 200 g，温度更低、冰更多，但杯中有效饮料空间变小，实际喝起来不一定更方便。

![Cooling curves](outputs/cooling_curves.png)

![Ice amount tradeoff](outputs/ice_amount_tradeoff.png)

## 5. 一个口感指标

为了把“冷”和“淡”放到同一张图中，脚本定义了一个示意性的口感分数：

```text
口感分数 = 冷感收益 - 稀释惩罚 - 冰已融尽且仍偏暖的惩罚
```

这个分数不是心理物理学定律，只是为了帮助比较方案。在基准参数下，5 分钟饮用窗口的最高分出现在约 **{best5.initial_ice_g:.0f} g** 冰，10 分钟窗口的最高分出现在约 **{best10.initial_ice_g:.0f} g** 冰。

![Taste score](outputs/taste_score.png)

## 6. 对博客或视频的主结论

这个选题最有传播力的结论是：

> 少冰不一定更浓。冰太少时，它会全部融化，却还不能把可乐快速降到好喝的温度；冰足够多时，饮料更快变冷，而融化量不会按冰块总量同比增加。

对于一杯 250 mL、常温 25 deg C 的可乐，比较合理的实用建议是：

> 如果想在 5-10 分钟内喝到明显冰爽、又不过度水感的可乐，优先选择 **100-150 g 较大冰块**。如果只放 25-50 g 小冰块，往往会得到“冰全化了但还不够冰”的结果。

## 7. 如何做真实验证

建议拍摄一个简单实验：

1. 准备 6 杯各 250 mL 可乐，初温统一到 25 deg C。
2. 分别加入 25、50、75、100、150、200 g 冰。
3. 每 30 秒记录温度，持续 10-15 分钟。
4. 到 5 分钟和 10 分钟时捞出剩余冰块称重。
5. 记录稀释量、温度曲线，并做盲品评分。

如果实验结果和模型趋势一致，就可以把视频结构设计成：先提出“少冰真的更浓吗”，再用热量守恒解释，再用实验曲线展示反直觉结果。

## 8. 局限性

本模型仍有几个局限：

- 没有模拟不同冰块形状和碎冰表面附着水。
- 没有模拟搅拌导致的二氧化碳逸出。
- 没有把杯子热容量单独建模。
- 口感分数是人为设定的示意指标。

因此，报告中的数值适合作为内容策划和实验设计起点，最终结论最好由实际测量校准。
"""

    Path("cola_ice_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    p = Params()
    summary = summarize_cases(p)
    summary.to_csv(OUT / "simulation_summary.csv", index=False)
    make_plots(summary, p)
    write_report(summary, p)


if __name__ == "__main__":
    main()
