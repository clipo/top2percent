#!/usr/bin/env python3
"""
Generate Figure 4: University adoption of Stanford/Elsevier "Top 2%" rankings.

STANDALONE VERSION for reproducibility package.
This script does not require the main project package installation.

Creates visualizations showing temporal, geographic, and institutional patterns
of university adoption of the rankings for marketing purposes (2022-2024).

Usage:
    python generate_figure4_adoption_standalone.py

    # Or with custom output directory:
    python generate_figure4_adoption_standalone.py --output-dir figures/

Requirements:
    - pandas
    - numpy
    - matplotlib
    - seaborn

Data files (must be in ../../data/university_adoption/):
    - university_adoption_data.csv
    - university_details.csv
"""

import argparse
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def load_adoption_data(data_dir: Path) -> tuple:
    """
    Load university adoption datasets.

    Args:
        data_dir: Directory containing data files

    Returns:
        Tuple of (adoption_data, university_details) DataFrames
    """
    adoption_data = pd.read_csv(data_dir / "university_adoption_data.csv")
    university_details = pd.read_csv(data_dir / "university_details.csv")

    print(f"Loaded {len(adoption_data)} adoption metrics")
    print(f"Loaded {len(university_details)} university records")

    return adoption_data, university_details


def prepare_data(adoption_data: pd.DataFrame) -> dict:
    """Prepare data for plotting."""
    # Yearly totals
    yearly_totals = (
        adoption_data[adoption_data["metric"] == "total_universities"][["year", "value"]]
        .rename(columns={"value": "total"})
    )

    # Cumulative data
    cumulative_data = (
        adoption_data[adoption_data["metric"] == "cumulative_total"][["year", "value"]]
        .rename(columns={"value": "cumulative"})
    )

    # Geographic data
    geographic_data = adoption_data[
        adoption_data["metric"].isin(["north_america", "asia", "europe"])
    ].copy()
    geographic_data["region"] = geographic_data["metric"].map(
        {"north_america": "North America", "asia": "Asia", "europe": "Europe"}
    )
    geographic_data = geographic_data[["year", "region", "value"]].rename(
        columns={"value": "count"}
    )

    # Institution data
    institution_data = adoption_data[
        adoption_data["metric"].isin(["r1_research", "regional", "international"])
    ].copy()
    institution_data["type"] = institution_data["metric"].map(
        {"r1_research": "R1 Research", "regional": "Regional", "international": "International"}
    )
    institution_data = institution_data[["year", "type", "value"]].rename(
        columns={"value": "count"}
    )

    return {
        "yearly_totals": yearly_totals,
        "cumulative_data": cumulative_data,
        "geographic_data": geographic_data,
        "institution_data": institution_data,
    }


def create_main_figure(data: dict, output_path: Path):
    """Create main 4-panel figure for manuscript."""
    # Set style
    plt.style.use("seaborn-v0_8-whitegrid")
    sns.set_palette("husl")

    # Create figure
    fig = plt.figure(figsize=(15, 12))
    fig.suptitle(
        'University Adoption of Stanford/Elsevier "Top 2% Scientists" List for Marketing\n(2022-2024)',
        fontsize=16,
        fontweight="bold",
    )

    # Panel A: Yearly totals
    ax1 = plt.subplot(2, 2, 1)
    colors1 = ["#2E86AB", "#A23B72", "#F18F01"]
    bars1 = ax1.bar(
        data["yearly_totals"]["year"], data["yearly_totals"]["total"], color=colors1, width=0.6
    )
    for bar, value in zip(bars1, data["yearly_totals"]["total"]):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            str(int(value)),
            ha="center",
            fontweight="bold",
        )
    ax1.set_ylim(0, 25)
    ax1.set_xlabel("Year", fontsize=11)
    ax1.set_ylabel("Number of Universities", fontsize=11)
    ax1.set_title("(a) Documented Universities Using the Metric", fontweight="bold", fontsize=12, loc="left")
    ax1.text(
        2023,
        23,
        "*Numbers represent minimum documented cases\nActual adoption likely much higher",
        ha="center",
        fontsize=9,
        style="italic",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    # Panel B: Geographic distribution
    ax2 = plt.subplot(2, 2, 2)
    pivot_geo = data["geographic_data"].pivot(index="year", columns="region", values="count")
    pivot_geo.plot(
        kind="bar", stacked=True, ax=ax2, width=0.6, color=["#4A90E2", "#E24A4A", "#4AE290"]
    )
    ax2.set_xlabel("Year", fontsize=11)
    ax2.set_ylabel("Number of Universities", fontsize=11)
    ax2.set_title("(b) Geographic Distribution of Adoption", fontweight="bold", fontsize=12, loc="left")
    ax2.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)

    # Panel C: Cumulative growth
    ax3 = plt.subplot(2, 2, 3)
    ax3.fill_between(
        data["cumulative_data"]["year"],
        0,
        data["cumulative_data"]["cumulative"],
        alpha=0.3,
        color="#D32F2F",
    )
    ax3.plot(
        data["cumulative_data"]["year"],
        data["cumulative_data"]["cumulative"],
        marker="o",
        linewidth=2.5,
        markersize=8,
        color="#D32F2F",
    )
    for x, y in zip(data["cumulative_data"]["year"], data["cumulative_data"]["cumulative"]):
        ax3.text(x, y + 2, str(int(y)), ha="center", fontweight="bold")
    ax3.set_ylim(0, 65)
    ax3.set_xlabel("Year", fontsize=11)
    ax3.set_ylabel("Cumulative Universities", fontsize=11)
    ax3.set_title("(c) Cumulative Growth in Documented Adoption", fontweight="bold", fontsize=12, loc="left")
    ax3.set_xticks([2022, 2023, 2024])
    note_text = (
        "Note: Year represents documented examples from press releases and official announcements. "
        "Actual adoption rates are likely significantly higher as many universities include "
        "the metric without public announcements."
    )
    ax3.text(
        0.5,
        -0.25,
        note_text,
        transform=ax3.transAxes,
        ha="center",
        va="top",
        fontsize=8,
        style="italic",
        wrap=True,
    )

    # Panel D: Institution type
    ax4 = plt.subplot(2, 2, 4)
    x = np.arange(len([2022, 2023, 2024]))
    width = 0.25
    types = ["R1 Research", "Regional", "International"]
    colors4 = ["#7B68EE", "#FF6B6B", "#4ECDC4"]

    for i, inst_type in enumerate(types):
        values = data["institution_data"][data["institution_data"]["type"] == inst_type][
            "count"
        ].values
        ax4.bar(x + i * width - width, values, width, label=inst_type, color=colors4[i])

    ax4.set_xlabel("Year", fontsize=11)
    ax4.set_ylabel("Number of Universities", fontsize=11)
    ax4.set_title("(d) Adoption by Institution Type", fontweight="bold", fontsize=12, loc="left")
    ax4.set_xticks(x)
    ax4.set_xticklabels([2022, 2023, 2024])
    ax4.legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    # Also save PDF version
    pdf_path = output_path.with_suffix('.pdf')
    plt.savefig(pdf_path, bbox_inches="tight")
    print(f"Main figure saved to: {output_path} and {pdf_path}")

    return fig


def print_summary_statistics(data: dict, university_details: pd.DataFrame):
    """Print summary statistics about the adoption data."""
    print("\n" + "=" * 70)
    print("UNIVERSITY ADOPTION SUMMARY STATISTICS")
    print("=" * 70)

    print("\n1. Yearly Totals:")
    print(data["yearly_totals"].to_string(index=False))

    print("\n2. Total by Region (2022-2024):")
    regional_totals = data["geographic_data"].groupby("region")["count"].sum().sort_values(
        ascending=False
    )
    print(regional_totals)

    print("\n3. Total by Institution Type (2022-2024):")
    institution_totals = data["institution_data"].groupby("type")["count"].sum().sort_values(
        ascending=False
    )
    print(institution_totals)

    print("\n4. Top 5 Countries:")
    country_summary = (
        university_details.groupby("country").size().reset_index(name="universities")
    )
    print(country_summary.sort_values("universities", ascending=False).head().to_string(index=False))

    print("\n5. Total Unique Universities: {}".format(len(university_details)))

    print("\n" + "=" * 70)


def main():
    """Generate Figure 4."""
    parser = argparse.ArgumentParser(
        description="Generate university adoption figures"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        help="Directory containing data files (default: ../../data/university_adoption/)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for figures (default: ../../figures/)",
    )

    args = parser.parse_args()

    try:
        # Set paths relative to script location
        script_dir = Path(__file__).parent

        if args.data_dir:
            data_dir = Path(args.data_dir)
        else:
            data_dir = script_dir / ".." / ".." / "data" / "university_adoption"

        if args.output_dir:
            output_dir = Path(args.output_dir)
        else:
            output_dir = script_dir / ".." / ".." / "figures"

        # Ensure directories exist
        if not data_dir.exists():
            print(f"Error: Data directory not found: {data_dir}")
            print("Expected files:")
            print("  - university_adoption_data.csv")
            print("  - university_details.csv")
            return 1

        output_dir.mkdir(parents=True, exist_ok=True)

        print("Loading adoption data...")
        adoption_data, university_details = load_adoption_data(data_dir)

        print("\nPreparing data for visualization...")
        data = prepare_data(adoption_data)

        print("\nGenerating Figure 1...")
        output_path = output_dir / "Figure1_University_Adoption.png"
        create_main_figure(data, output_path)

        print_summary_statistics(data, university_details)

        print(f"\n✓ Figure generated successfully: {output_path}")
        return 0

    except Exception as e:
        print(f"Error generating figure: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
