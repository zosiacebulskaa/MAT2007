import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("group_phase_summary.csv")
phase_order = [
    "Menstrual",
    "Follicular",
    "Ovulation",
    "Luteal"
]

df["Phase"] = pd.Categorical(
    df["Phase"],
    categories=phase_order,
    ordered=True
)

df = df.sort_values("Phase")

plt.figure(figsize=(8, 5))

plt.errorbar(
    df["Phase"],
    df["Physical_group_mean"],
    yerr=df["Physical_group_SD"],
    fmt="o",
    capsize=5,
    color="#cc5a5a"
)

plt.ylim(0, 1)
plt.xticks(fontfamily="serif")
plt.yticks(fontfamily="serif")

plt.ylabel("Normalized general physical state", fontfamily="serif")
plt.xlabel("Menstrual cycle phase", fontfamily="serif")
plt.title("Average general physical state across the menstrual cycle", fontfamily="serif", fontweight="bold", color="#cc5a5a")

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    "physical_wellbeing.png",
    dpi=300
)

plt.show()

plt.figure(figsize=(8, 5))

plt.errorbar(
    df["Phase"],
    df["Emotional_group_mean"],
    yerr=df["Emotional_group_SD"],
    fmt="o",
    capsize=5,
    color="#cc5a5a"
)

plt.ylim(0, 1)
plt.xticks(fontfamily="serif")
plt.yticks(fontfamily="serif")

plt.ylabel("Normalized general emotional state", fontfamily="serif")
plt.xlabel("Menstrual cycle phase", fontfamily="serif")
plt.title("Average general emotional state across the menstrual cycle", fontfamily="serif", fontweight="bold", color="#cc5a5a")

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    "emotional_wellbeing.png",
    dpi=300
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

df = pd.read_csv("phase_comparisons.csv")

plt.figure(figsize=(10, 6))

plt.errorbar(
    comparison_labels,
    df["Physical_mean_difference"],
    yerr=df["Physical_SD_difference"],
    fmt="o",
    color="#cc5a5a",
    capsize=6,
    markersize=8,
    linewidth=2
)

plt.axhline(
    y=0,
    linestyle="--",
    linewidth=1.5,
    color="#cc5a5a"
)

plt.ylabel("Difference in normalized physical state", fontfamily="serif")
plt.xlabel("Phase comparison", fontfamily="serif")

plt.xticks(fontfamily="serif")
plt.yticks(fontfamily="serif")

plt.title(
    "Differences in general physical state between cycle phases",
     color="#cc5a5a",
    fontfamily="serif",
    fontweight="bold"
    )

plt.grid(axis="y", alpha=0.3)

plt.xticks(
    rotation=25,
    ha="right"
)

plt.savefig(
    "physicaldifferences.png",
    dpi=300,
    bbox_inches="tight"
)

plt.tight_layout()
plt.show()
plt.figure(figsize=(10, 6))

plt.errorbar(
    comparison_labels,
    df["Emotional_mean_difference"],
    yerr=df["Emotional_SD_difference"],
    fmt="o",
    color="#cc5a5a",
    capsize=6,
    markersize=8,
    linewidth=2
)

plt.axhline(
    y=0,
    linestyle="--",
    linewidth=1.5,
    color="#cc5a5a"
)

plt.ylabel("Paired difference in normalized emotional state", fontfamily="serif")
plt.xlabel("Phase comparison", fontfamily="serif")

plt.title(
    "Differences in general emotional state between cycle phases",
    color="#cc5a5a",
    fontfamily="serif",
    fontweight="bold"
)

plt.grid(axis="y", alpha=0.3)

plt.xticks(fontfamily="serif")
plt.yticks(fontfamily="serif")

plt.xticks(
    rotation=25,
    ha="right"
)

plt.savefig(
    "emotionaldifferences.png",
    dpi=300,
    bbox_inches="tight"
)

plt.tight_layout()
plt.show()
