import pandas as pd
import matplotlib.pyplot as plt

gi_data = pd.read_csv("GI_group_summary.csv")
print(gi_data)

phase_order = [
    "Menstrual",
    "Follicular",
    "Ovulation",
    "Luteal"
]

gi_data["Phase"] = pd.Categorical(
    gi_data["Phase"],
    categories=phase_order,
    ordered=True
)

gi_data = gi_data.sort_values("Phase")

plt.figure(figsize=(10, 6))

plt.errorbar(
    gi_data["Phase"],
    gi_data["GI_group_mean"],
    yerr=gi_data["GI_group_SD"],
    fmt="o",
    capsize=6,
    markersize=8,
    color="#cc5a5a"
)

plt.ylim(0, 1)

plt.xlabel(
    "Menstrual cycle phase",
    fontfamily="serif"
)

plt.ylabel(
    "Normalized GI burden intensity",
    fontfamily="serif"
)

plt.title(
    "Average GI burden intensity across the menstrual cycle",
    fontfamily="serif",
    fontweight="bold",
    color="#cc5a5a"
)

plt.xticks(
    fontfamily="serif"
)

plt.yticks(
    fontfamily="serif"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "GI_burden.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

comparison_labels = [
    "Menstrual vs. Follicular",
    "Menstrual vs. Ovulation",
    "Menstrual vs. Luteal",
    "Follicular vs. Ovulation",
    "Follicular vs. Luteal",
    "Ovulation vs. Luteal"
]

gi_diff = pd.read_csv("GI_phase_comparisons.csv")

print(gi_diff)

plt.figure(figsize=(11, 6))

plt.errorbar(
    comparison_labels,
    gi_diff["GI_mean_difference"],
    yerr=gi_diff["GI_SD_difference"],
    fmt="o",
    capsize=6,
    markersize=8,
    color="#cc5a5a",
    ecolor="#cc5a5a"
)

plt.axhline(
    y=0,
    linestyle="--",
    color="#cc5a5a"
)

plt.xlabel(
    "Phase comparison",
    fontfamily="serif"
)

plt.ylabel(
    "Difference in normalized GI burden intensity",
    fontfamily="serif"
)

plt.title(
    "Differences in GI burden intensity between cycle phases",
    fontfamily="serif",
    fontweight="bold",
    color="#cc5a5a"
)

plt.xticks(
    rotation=25,
    ha="right",
    fontfamily="serif"
)

plt.yticks(
    fontfamily="serif"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "GI_burden_differences.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()