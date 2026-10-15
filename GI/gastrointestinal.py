import pandas as pd
import glob
import re

######################################################
# GI symptoms higher = better or higher = worse ★
######################################################
GI_HIGHER_BETTER = [
    "Appetite",
    "Appetite / no appetite"
]

GI_HIGHER_WORSE = [
    "Painful bowel movement",
    "Endo belly",
    "Pain before bowel movement",
    "Bloating",
    "Rectal bleeding",
    "Nausea",
    "No appetite",
    "Gas",
    "Nausea / vomiting",
    "Stomach flare / abdominal flare",
    "Heartburn",
    "Rectum pain",
    "Diarrhea",
    "Stomach discomfort",
    "Stomach stiffness",
    "Vomiting",
    "Pain before / during bowel movement"
]

GI_SYMPTOMS = GI_HIGHER_BETTER + GI_HIGHER_WORSE

######################################################
# Normalizing scores ★
######################################################
def normalize_gi(series, column_name):
    symptom = column_name.split(" (")[0].strip()
    scale_match = re.search(r",\s*(\d+)\s*-", column_name)

    if scale_match is None:
        raise ValueError(
            f"Could not determine scale for: {column_name}"
        )
    maximum = float(scale_match.group(1))
    values = pd.to_numeric(series, errors="coerce")

    if symptom in GI_HIGHER_BETTER:
        normalized = 1 - (values / maximum)
    elif symptom in GI_HIGHER_WORSE:

        normalized = values / maximum
    else:
        raise ValueError(
            f"Unknown GI symptom: {symptom}"
        )

    return normalized

######################################################
# Find files (hard-coded directory) ★
######################################################
files = glob.glob("project/User*.csv")

######################################################
# Storage for phase results ★
######################################################
menstrual_results = []
follicular_results = []
ovulation_results = []
luteal_results = []

gi_daily_results = [] # for correlation 

######################################################
# Calculating GI phase mean ★
######################################################
def calculate_gi_phase_mean(data, user, cycle_number, phase):
    gi_mean = data["GI_daily_mean"].mean()
    gi_days = data["GI_daily_mean"].notna().sum()

    return {
        "User": user,
        "Cycle": cycle_number,
        "Phase": phase,
        "GI_mean": gi_mean,
        "GI_days": gi_days
    }

######################################################
# Normalize and calculate phase mean ★
######################################################
for file in files:
    df = pd.read_csv(file)
    user = re.search(r"User\d+", file).group()
    normalized_gi_columns = []

    for col in df.columns:
        symptom = col.split(" (")[0].strip()
        if symptom in GI_SYMPTOMS:
            normalized_col = col + "_normalized"
            df[normalized_col] = normalize_gi(
                df[col],
                col
            )
            normalized_gi_columns.append(normalized_col)

######################################################
# Daily mean ★
######################################################

    if len(normalized_gi_columns) > 0:
        df["GI_daily_n"] = (
            df[normalized_gi_columns]
            .notna()
            .sum(axis=1)
        )

        df["GI_daily_mean"] = (
            df[normalized_gi_columns]
            .mean(axis=1, skipna=True)
        )
    else:
        df["GI_daily_n"] = 0
        df["GI_daily_mean"] = float("nan")

    daily_gi = pd.DataFrame({
        "User": user,
        "Day_index": df.index,
        "GI_daily_mean": df["GI_daily_mean"]
    })

    gi_daily_results.append(daily_gi)

    period_col = next(
        col for col in df.columns
        if col.startswith("Period")
    )

######################################################
# Find complete cycles ★
######################################################
    cycle_starts = df.index[
        (df["Cycle day"] == 1) &
        (df[period_col] == 1)
    ].tolist()

    for i in range(len(cycle_starts) - 1):
        start = cycle_starts[i]
        next_start = cycle_starts[i + 1]
        cycle = df.loc[start:next_start - 1].copy()
        cycle_number = i + 1
        last_cycle_day = int(cycle["Cycle day"].max())

######################################################
# Determining phase boundaries ★
######################################################
        # Luteal = final 14 days
        luteal_start = last_cycle_day - 13

        # Ovulation = 2 days before luteal
        ovulation_start = luteal_start - 2

        ovulation_days = [
            ovulation_start,
            ovulation_start + 1
        ]

        # Menstruation = period yes
        menstruation = cycle[
            cycle[period_col] == 1
        ]

        menstrual_results.append(
            calculate_gi_phase_mean(
                menstruation,
                user,
                cycle_number,
                "Menstrual"
            )
        )

        # Follicular
        follicular = cycle[
            (cycle[period_col] == 0) &
            (cycle["Cycle day"] < ovulation_start)
        ]

        follicular_results.append(
            calculate_gi_phase_mean(
                follicular,
                user,
                cycle_number,
                "Follicular"
            )
        )

        # Ovulation
        ovulation = cycle[
            cycle["Cycle day"].isin(ovulation_days)
        ]

        ovulation_results.append(
            calculate_gi_phase_mean(
                ovulation,
                user,
                cycle_number,
                "Ovulation"
            )
        )

        # Ovulation
        luteal = cycle[
            cycle["Cycle day"] >= luteal_start
        ]

        luteal_results.append(
            calculate_gi_phase_mean(
                luteal,
                user,
                cycle_number,
                "Luteal"
            )
        )

######################################################
# Combine and save daily means ★
######################################################
gi_daily_results = pd.concat(
    gi_daily_results,
    ignore_index=True
)

gi_daily_results.to_csv(
    "GI_daily_means.csv",
    index=False
)

print("\nDaily GI means saved!")
print(gi_daily_results.head(20))

######################################################
# Convert to dataframes ★
######################################################
menstrual_results = pd.DataFrame(menstrual_results)
follicular_results = pd.DataFrame(follicular_results)
ovulation_results = pd.DataFrame(ovulation_results)
luteal_results = pd.DataFrame(luteal_results)

######################################################
# Combine all phases ★
######################################################
all_phases_gi = pd.concat(
    [
        menstrual_results,
        follicular_results,
        ovulation_results,
        luteal_results
    ],
    ignore_index=True
)

all_phases_gi.to_csv(
    "all_phases_GI.csv",
    index=False
)

print("\nGI phase analysis complete!")
print(all_phases_gi)

print("\nResults saved to all_phases_GI.csv")

######################################################
# Means and standard deviation per user ★
######################################################
user_gi_summary = (
    all_phases_gi
    .groupby(["User", "Phase"])
    .agg(
        GI_mean=("GI_mean", "mean"),
        GI_SD=("GI_mean", "std"),
        GI_cycles=("GI_mean", "count")
    )
    .reset_index()
)

user_gi_summary.to_csv(
    "user_GI_summary.csv",
    index=False
)

print("\nUser GI summary:")
print(user_gi_summary)
print("\nResults saved to user_GI_summary.csv")

######################################################
# Mean and standard deviation per group ★
######################################################
gi_group_summary = (
    user_gi_summary
    .groupby("Phase")
    .agg(
        GI_group_mean=("GI_mean", "mean"),
        GI_group_SD=("GI_mean", "std"),
        GI_users=("GI_mean", "count")
    )
    .reset_index()
)

gi_group_summary.to_csv(
    "GI_group_summary.csv",
    index=False
)

print("\nGI group summary:")
print(gi_group_summary)
print("\nResults saved to GI_group_summary.csv")

######################################################
# Formatting ★
######################################################
gi_wide = user_gi_summary.pivot(
    index="User",
    columns="Phase",
    values="GI_mean"
)

print("\nGI means by user:")
print(gi_wide)

######################################################
# Pairwise comparisons ★
######################################################
comparisons = [
    ("Menstrual", "Follicular"),
    ("Menstrual", "Ovulation"),
    ("Menstrual", "Luteal"),
    ("Follicular", "Ovulation"),
    ("Follicular", "Luteal"),
    ("Ovulation", "Luteal")
]

######################################################
# Formatting ★
######################################################
gi_table = user_gi_summary.pivot(
    index="User",
    columns="Phase",
    values="GI_mean"
)

######################################################
# Calculating paired differences ★
######################################################
gi_comparison_results = []

for phase1, phase2 in comparisons:

    # Difference = second phase - first phase
    gi_difference = (
        gi_table[phase2] -
        gi_table[phase1]
    )

    gi_mean_difference = gi_difference.mean()
    gi_SD_difference = gi_difference.std()
    gi_n = gi_difference.count()

    gi_comparison_results.append({
        "Comparison": f"{phase2} - {phase1}",
        "GI_mean_difference": gi_mean_difference,
        "GI_SD_difference": gi_SD_difference,
        "GI_n": gi_n
    })

gi_phase_comparisons = pd.DataFrame(
    gi_comparison_results
)

gi_phase_comparisons.to_csv(
    "GI_phase_comparisons.csv",
    index=False
)

print("\nGI phase comparisons:")
print(gi_phase_comparisons)
print("\nResults saved to GI_phase_comparisons.csv")