import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

def plot_correlation(data, x_col, y_col, x_label, y_label, title, filename):
    r, p = pearsonr(
        data[x_col],
        data[y_col]
    )

    slope, intercept = np.polyfit(
        data[x_col],
        data[y_col],
        1
    )

    x_line = np.linspace(
        data[x_col].min(),
        data[x_col].max(),
        100
    )

    y_line = slope * x_line + intercept

    plt.figure(figsize=(8, 6))

    plt.scatter(
        data[x_col],
        data[y_col],
        color="#cc5a5a"
    )

    plt.plot(
        x_line,
        y_line,
        color="#cc5a5a"
    )

    plt.xlabel(
        x_label,
        fontfamily="serif"
    )

    plt.ylabel(
        y_label,
        fontfamily="serif"
    )

    plt.title(
        title,
        fontfamily="serif",
        fontweight="bold",
        color="#cc5a5a"
    )

    plt.xlim(0.03, 0.50)
    plt.ylim(0, 1)

    plt.xticks(
        np.arange(0.05, 0.51, 0.05),
        fontfamily="serif"
    )

    plt.yticks(fontfamily="serif")

    plt.grid(
        alpha=0.3
    )

    plt.text(
        0.05,
        0.08,
        f"r = {r:.3f}\np = {p:.3f}\nn = {len(data)}",
        transform=plt.gca().transAxes,
        fontfamily="serif"
    )

    plt.tight_layout()

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

pain_physical = pd.read_csv(
    "Pain_Physical_user_means.csv"
)

pain_emotional = pd.read_csv(
    "Pain_Emotional_user_means.csv"
)

gi_physical = pd.read_csv(
    "GI_Physical_user_means.csv"
)

gi_emotional = pd.read_csv(
    "GI_Emotional_user_means.csv"
)

plot_correlation(
    pain_physical,
    "Pain_mean",
    "Physical_mean",
    "Average normalized pain burden",
    "Average normalized general physical state",
    "Pain burden vs. general physical state",
    "Pain_Physical_correlation.png"
)

plot_correlation(
    pain_emotional,
    "Pain_mean",
    "Emotional_mean",
    "Average normalized pain burden",
    "Average normalized general emotional state",
    "Pain burden vs. general emotional state",
    "Pain_Emotional_correlation.png"
)

plot_correlation(
    gi_physical,
    "GI_mean",
    "Physical_mean",
    "Average normalized GI burden",
    "Average normalized general physical state",
    "GI burden vs. general physical state",
    "GI_Physical_correlation.png"
)

plot_correlation(
    gi_emotional,
    "GI_mean",
    "Emotional_mean",
    "Average normalized GI burden",
    "Average normalized general emotional state",
    "GI burden vs. general emotional state",
    "GI_Emotional_correlation.png"
)