import pandas as pd
import matplotlib.pyplot as plt

pain_data = pd.read_csv("Pain_group_summary.csv")
print(pain_data)

phase_order = [
    "Menstrual",
    "Follicular",
    "Ovulation",
    "Luteal"
]

pain_data["Phase"] = pd.Categorical(
    pain_data["Phase"],
    categories=phase_order,
    ordered=True
)

pain_data = pain_data.sort_values("Phase")

plt.figure(figsize=(10, 6))

plt.errorbar(
    pain_data["Phase"],
    pain_data["Pain_group_mean"],
    yerr=pain_data["Pain_group_SD"],
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
    "Normalized pain burden intensity",
    fontfamily="serif"
)

plt.title(
    "Average pain burden intensity across the menstrual cycle",
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
    "Pain_burden.png",
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

pain_diff = pd.read_csv("Pain_phase_comparisons.csv")

print(pain_diff)

plt.figure(figsize=(11, 6))

plt.errorbar(
    comparison_labels,
    pain_diff["Pain_mean_difference"],
    yerr=pain_diff["Pain_SD_difference"],
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
    "Difference in normalized pain burden intensity",
    fontfamily="serif"
)

plt.title(
    "Differences in pain burden intensity between cycle phases",
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
    "Pain_burden_differences.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()