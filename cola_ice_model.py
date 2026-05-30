from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from string import Template

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

    context = {
        "cola_mass_g": f"{p.cola_mass_g:.0f}",
        "cola_initial_c": f"{p.cola_initial_c:.0f}",
        "ambient_c": f"{p.ambient_c:.0f}",
        "ice_initial_c": f"{p.ice_initial_c:.0f}",
        "cola_cp": f"{p.cola_cp_j_gk:.2f}",
        "cola_cp_short": f"{p.cola_cp_j_gk:.1f}",
        "ice_cp": f"{p.ice_cp_j_gk:.2f}",
        "ice_fusion": f"{p.ice_fusion_j_g:.0f}",
        "heat_removed": f"{p.cola_mass_g * p.cola_cp_j_gk * (p.cola_initial_c - 4):.0f}",
        "theory_table": chr(10).join(theory_table),
        "table_rows": chr(10).join(table_rows),
        "best5_ice_g": f"{best5.initial_ice_g:.0f}",
        "best10_ice_g": f"{best10.initial_ice_g:.0f}",
    }
    template = Template(Path("templates/report.md").read_text(encoding="utf-8"))
    report = template.safe_substitute(context)
    Path("cola_ice_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    p = Params()
    summary = summarize_cases(p)
    summary.to_csv(OUT / "simulation_summary.csv", index=False)
    make_plots(summary, p)
    write_report(summary, p)


if __name__ == "__main__":
    main()
