from __future__ import annotations

from dataclasses import dataclass, replace

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider


@dataclass(frozen=True)
class Params:
    cola_mass_g: float = 250.0
    ice_mass_g: float = 120.0
    cola_initial_c: float = 25.0
    ice_initial_c: float = -18.0
    ambient_c: float = 25.0
    drink_time_min: float = 5.0
    ice_transfer_w_per_gk: float = 0.08
    env_transfer_w_per_k: float = 0.25
    cola_cp_j_gk: float = 4.0
    water_cp_j_gk: float = 4.18
    ice_cp_j_gk: float = 2.1
    ice_fusion_j_g: float = 334.0
    dt_s: float = 0.5
    total_time_s: float = 15 * 60


def simulate(p: Params) -> dict[str, np.ndarray]:
    steps = int(p.total_time_s / p.dt_s) + 1
    time_s = np.arange(steps) * p.dt_s
    temp = np.zeros(steps)
    ice = np.zeros(steps)
    melted = np.zeros(steps)

    temp[0] = p.cola_initial_c
    ice[0] = p.ice_mass_g
    liquid_mass = p.cola_mass_g
    ice_temp = p.ice_initial_c

    for i in range(1, steps):
        T = temp[i - 1]
        m_ice = ice[i - 1]
        q_env = p.env_transfer_w_per_k * (p.ambient_c - T) * p.dt_s
        q_to_ice = 0.0
        dm = 0.0

        if m_ice > 1e-9 and T > 0:
            surface_t = max(ice_temp, 0.0)
            q_available = (
                p.ice_transfer_w_per_gk * m_ice * max(T - surface_t, 0.0) * p.dt_s
            )
            if ice_temp < 0:
                q_warm_needed = m_ice * p.ice_cp_j_gk * (0 - ice_temp)
                q_warm = min(q_available, q_warm_needed)
                ice_temp += q_warm / (m_ice * p.ice_cp_j_gk)
                q_to_ice += q_warm
                q_available -= q_warm

            if q_available > 0 and ice_temp >= -1e-9:
                heat_per_g_melt = p.ice_fusion_j_g + p.water_cp_j_gk * max(T, 0.0)
                dm = min(m_ice, q_available / heat_per_g_melt)
                q_to_ice += dm * heat_per_g_melt

        heat_capacity = liquid_mass * p.cola_cp_j_gk
        temp[i] = max(T + (q_env - q_to_ice) / heat_capacity, 0.0 if m_ice - dm > 1e-9 else -5.0)
        ice[i] = max(0.0, m_ice - dm)
        melted[i] = melted[i - 1] + dm
        liquid_mass += dm
        if ice[i] <= 1e-9:
            ice_temp = 0.0

    return {
        "time_min": time_s / 60,
        "temperature_c": temp,
        "ice_remaining_g": ice,
        "ice_melted_g": melted,
        "dilution_pct": melted / p.cola_mass_g * 100,
    }


def row_at(data: dict[str, np.ndarray], minute: float) -> int:
    return int(np.argmin(np.abs(data["time_min"] - minute)))


def taste_score(temp_c: float, dilution_pct: float, ice_remaining_g: float, initial_ice_g: float, cola_mass_g: float) -> float:
    cold_score = 88 / (1 + np.exp((temp_c - 8.0) / 1.8))
    overcold_penalty = 1.2 * max(0.0, 2.0 - temp_c)
    watery_penalty = 1.6 * dilution_pct
    crowding_penalty = 0.22 * max(0.0, initial_ice_g - 0.6 * cola_mass_g)
    no_ice_penalty = 8.0 if ice_remaining_g <= 0 and temp_c > 6 else 0.0
    return float(
        np.clip(
            cold_score - overcold_penalty - watery_penalty - crowding_penalty - no_ice_penalty,
            0,
            100,
        )
    )


def scan_ice(p: Params) -> dict[str, np.ndarray | float]:
    ice_grid = np.arange(0, 301, 5)
    temps, dilutions, melts, scores = [], [], [], []
    for ice_g in ice_grid:
        test_p = replace(p, ice_mass_g=float(ice_g))
        data = simulate(test_p)
        idx = row_at(data, p.drink_time_min)
        temp = data["temperature_c"][idx]
        dilution = data["dilution_pct"][idx]
        remaining = data["ice_remaining_g"][idx]
        temps.append(temp)
        dilutions.append(dilution)
        melts.append(data["ice_melted_g"][idx])
        scores.append(taste_score(temp, dilution, remaining, ice_g, p.cola_mass_g))

    scores_arr = np.array(scores)
    return {
        "ice_grid": ice_grid,
        "temperature_c": np.array(temps),
        "dilution_pct": np.array(dilutions),
        "ice_melted_g": np.array(melts),
        "taste_score": scores_arr,
        "best_ice_g": float(ice_grid[int(np.argmax(scores_arr))]),
    }


def build_app() -> None:
    p = Params()
    fig, (ax_curve, ax_scan) = plt.subplots(1, 2, figsize=(13, 7))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.86, bottom=0.31, wspace=0.28)
    fig.suptitle("Cola + Ice visual model", fontsize=16, fontweight="bold")

    slider_axes = {
        "cola_mass_g": fig.add_axes([0.10, 0.22, 0.30, 0.025]),
        "ice_mass_g": fig.add_axes([0.10, 0.17, 0.30, 0.025]),
        "cola_initial_c": fig.add_axes([0.10, 0.12, 0.30, 0.025]),
        "ice_initial_c": fig.add_axes([0.10, 0.07, 0.30, 0.025]),
        "ambient_c": fig.add_axes([0.58, 0.22, 0.30, 0.025]),
        "drink_time_min": fig.add_axes([0.58, 0.17, 0.30, 0.025]),
        "ice_transfer_w_per_gk": fig.add_axes([0.58, 0.12, 0.30, 0.025]),
    }

    sliders = {
        "cola_mass_g": Slider(slider_axes["cola_mass_g"], "cola g", 150, 500, valinit=p.cola_mass_g, valstep=10),
        "ice_mass_g": Slider(slider_axes["ice_mass_g"], "ice g", 0, 300, valinit=p.ice_mass_g, valstep=5),
        "cola_initial_c": Slider(slider_axes["cola_initial_c"], "cola C", 4, 35, valinit=p.cola_initial_c, valstep=1),
        "ice_initial_c": Slider(slider_axes["ice_initial_c"], "ice C", -25, 0, valinit=p.ice_initial_c, valstep=1),
        "ambient_c": Slider(slider_axes["ambient_c"], "air C", 10, 35, valinit=p.ambient_c, valstep=1),
        "drink_time_min": Slider(slider_axes["drink_time_min"], "time min", 1, 15, valinit=p.drink_time_min, valstep=1),
        "ice_transfer_w_per_gk": Slider(slider_axes["ice_transfer_w_per_gk"], "transfer", 0.02, 0.16, valinit=p.ice_transfer_w_per_gk, valstep=0.005),
    }

    info = fig.text(0.5, 0.91, "", ha="center", va="center", fontsize=11)

    def current_params() -> Params:
        return Params(
            cola_mass_g=sliders["cola_mass_g"].val,
            ice_mass_g=sliders["ice_mass_g"].val,
            cola_initial_c=sliders["cola_initial_c"].val,
            ice_initial_c=sliders["ice_initial_c"].val,
            ambient_c=sliders["ambient_c"].val,
            drink_time_min=sliders["drink_time_min"].val,
            ice_transfer_w_per_gk=sliders["ice_transfer_w_per_gk"].val,
        )

    def redraw(_=None) -> None:
        cp = current_params()
        data = simulate(cp)
        scan = scan_ice(cp)
        best_p = replace(cp, ice_mass_g=scan["best_ice_g"])
        best_data = simulate(best_p)
        idx = row_at(data, cp.drink_time_min)

        ax_curve.clear()
        ax_curve.axhspan(0, 6, color="#7fbf9b", alpha=0.16, label="cold zone")
        ax_curve.plot(data["time_min"], data["temperature_c"], color="#1674a6", lw=2.8, label=f"current {cp.ice_mass_g:.0f} g")
        ax_curve.plot(best_data["time_min"], best_data["temperature_c"], color="#c7473f", lw=2.2, ls="--", label=f"recommended {scan['best_ice_g']:.0f} g")
        ax_curve.axvline(cp.drink_time_min, color="#777", lw=1, ls=":")
        ax_curve.set_title("Cooling curve")
        ax_curve.set_xlabel("time (min)")
        ax_curve.set_ylabel("temperature (deg C)")
        ax_curve.set_xlim(0, 15)
        ax_curve.set_ylim(0, max(35, cp.cola_initial_c + 2))
        ax_curve.grid(True, alpha=0.25)
        ax_curve.legend(loc="upper right")

        ax_scan.clear()
        ax2 = ax_scan.twinx()
        ax_scan.plot(scan["ice_grid"], scan["temperature_c"], color="#1674a6", lw=2.6, label="temperature")
        ax2.plot(scan["ice_grid"], scan["dilution_pct"], color="#c7473f", lw=2.3, label="dilution")
        ax2.plot(scan["ice_grid"], scan["taste_score"], color="#b87918", lw=2.3, label="taste score")
        ax_scan.axvline(cp.ice_mass_g, color="#222", lw=1.2, ls=":", label="current")
        ax_scan.axvline(scan["best_ice_g"], color="#c7473f", lw=1.2, ls="--", label="recommended")
        ax_scan.set_title(f"Tradeoff at {cp.drink_time_min:.0f} min")
        ax_scan.set_xlabel("initial ice (g)")
        ax_scan.set_ylabel("temperature (deg C)")
        ax2.set_ylabel("dilution (%) / score")
        ax_scan.set_xlim(0, 300)
        ax_scan.set_ylim(0, max(35, cp.cola_initial_c + 2))
        ax2.set_ylim(0, 100)
        ax_scan.grid(True, alpha=0.25)
        lines = ax_scan.get_lines() + ax2.get_lines()
        ax_scan.legend(lines, [line.get_label() for line in lines], loc="upper right", fontsize=8)

        info.set_text(
            f"At {cp.drink_time_min:.0f} min: T={data['temperature_c'][idx]:.1f} deg C, "
            f"melted={data['ice_melted_g'][idx]:.1f} g, "
            f"dilution={data['dilution_pct'][idx]:.1f}%, "
            f"recommended ice={scan['best_ice_g']:.0f} g"
        )
        fig.canvas.draw_idle()

    for slider in sliders.values():
        slider.on_changed(redraw)

    redraw()
    plt.show()


if __name__ == "__main__":
    build_app()
