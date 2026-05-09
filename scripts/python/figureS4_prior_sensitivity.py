#!/usr/bin/env python3
"""
Generate Supplementary Figure S4: Prior Sensitivity Analysis

Reads Table_B4_Prior_Sensitivity.csv (produced by
scripts/R/bayesian/09_manuscript_tables.R) and renders a grouped bar chart of
posterior medians under three prior specifications. Per project style, the
figure carries no on-image title; descriptive text lives in the SI caption.

Output: figures/supplementary/FigureS4_Prior_Sensitivity.{png,pdf}
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent.parent
TABLE = REPO / "results" / "bayesian" / "manuscript_tables" / "Table_B4_Prior_Sensitivity.csv"
OUT_DIR = REPO / "figures" / "supplementary"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PARAM_LABELS = {
    "elsevier_pct_z": "Elsevier %",
    "books_pct_z": "Books %",
    "field_type_fmixed": "Mixed vs Journal",
    "field_type_fbook_heavy": "Book-heavy vs Journal",
    "log_works_z": "Log Works",
}

PRIOR_COLORS = {
    "Default Prior\nNormal(0, 1)":   "#1f77b4",
    "Skeptical Prior\nNormal(0, 0.5)": "#ff7f0e",
    "Diffuse Prior\nNormal(0, 2)":   "#2ca02c",
}
COL_TO_PRIOR = {
    "Default Prior":   "Default Prior\nNormal(0, 1)",
    "Skeptical Prior": "Skeptical Prior\nNormal(0, 0.5)",
    "Diffuse Prior":   "Diffuse Prior\nNormal(0, 2)",
}


_NUM_RE = re.compile(r"-?\d+\.\d+")


def parse_median(cell: str) -> float:
    """Extract the median (first number) from cells like '0.156 [0.081, 0.231]'."""
    m = _NUM_RE.match(cell.strip())
    if m is None:
        raise ValueError(f"Could not parse median from {cell!r}")
    return float(m.group(0))


def main() -> None:
    df = pd.read_csv(TABLE)
    df = df[df["Parameter"].isin(PARAM_LABELS)].copy()
    df["Parameter"] = df["Parameter"].map(PARAM_LABELS)
    for col in ("Default Prior", "Skeptical Prior", "Diffuse Prior"):
        df[col] = df[col].map(parse_median)

    params = list(PARAM_LABELS.values())
    n_params = len(params)
    prior_cols = ["Default Prior", "Skeptical Prior", "Diffuse Prior"]
    n_priors = len(prior_cols)
    bar_w = 0.25
    x = np.arange(n_params)

    fig, ax = plt.subplots(figsize=(10, 6))
    for i, col in enumerate(prior_cols):
        legend_label = COL_TO_PRIOR[col]
        offsets = (i - (n_priors - 1) / 2) * bar_w
        bars = ax.bar(
            x + offsets,
            df[col].values,
            width=bar_w,
            label=legend_label,
            color=PRIOR_COLORS[legend_label],
            edgecolor="black",
            linewidth=0.4,
        )
        for bar, val in zip(bars, df[col].values):
            va = "bottom" if val >= 0 else "top"
            offset = 0.015 if val >= 0 else -0.015
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                val + offset,
                f"{val:.2f}",
                ha="center",
                va=va,
                fontsize=8,
            )

    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(params)
    ax.set_ylabel("Effect Size (β, logit scale)")
    ax.set_xlabel("")
    ax.legend(loc="lower left", frameon=True, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.4)
    plt.tight_layout()

    png_path = OUT_DIR / "FigureS4_Prior_Sensitivity.png"
    pdf_path = OUT_DIR / "FigureS4_Prior_Sensitivity.pdf"
    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Figure S4 saved: {png_path}")
    print(f"  Also: {pdf_path}")


if __name__ == "__main__":
    main()
