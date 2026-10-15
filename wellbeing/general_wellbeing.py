import pandas as pd
import glob
import re

######################################################
# Find files (hardcoded directory) ★
######################################################
files = glob.glob("project/User*.csv")

def get_user_number(filename):
    return int(re.search(r"User(\d+)", filename).group(1))

files.sort(key=get_user_number)

######################################################
# Normalize scores ★
######################################################
def normalize_scores(series, column_name):

    # Scale 1-10
    if "1-bad, 10-amazing" in column_name:
        return (series - 1) / 9

    # Scale 1-4
    elif "1-bad, 4-amazing" in column_name:
        return (series - 1) / 3

    else:
        raise ValueError(
            f"Unknown scale: {column_name}"
        )

######################################################
# Store cycle data ★
######################################################
menstrual_results = []
follicular_results = []
ovulation_results = []
luteal_results = []

######################################################
# Calculating phase means ★
######################################################
def calculate_phase_mean(data, user, cycle_number, phase):

    physical_mean = data["Physical_normalized"].mean()
    emotional_mean = data["Emotional_normalized"].mean()

    physical_n = data["Physical_normalized"].notna().sum()
    emotional_n = data["Emotional_normalized"].notna().sum()

    return {
        "User": user,
        "Cycle": cycle_number,
        "Phase": phase,
        "Physical_mean": physical_mean,
        "Emotional_mean": emotional_mean,
        "Physical_n": physical_n,
        "Emotional_n": emotional_n
    }

wellbeing_daily_results = []

######################################################
# Analyze each user ★
######################################################
for file in files:
    df = pd.read_csv(file)
    user = re.search(r"User\d+", file).group()
    physical_col = next(
        col for col in df.columns
        if col.startswith("General physical condition")
    )

    emotional_col = next(
        col for col in df.columns
        if col.startswith("General emotional condition")
    )

    period_col = next(
        col for col in df.columns
        if col.startswith("Period")
    )

######################################################
# Normalize and save wellbeing scores ★
######################################################
    df["Physical_normalized"] = normalize_scores(
        df[physical_col],
        physical_col
    )

    df["Emotional_normalized"] = normalize_scores(
        df[emotional_col],
        emotional_col
    )

    daily_wellbeing = pd.DataFrame({
        "User": user,
        "Day_index": df.index,
        "Physical_daily": df["Physical_normalized"],
        "Emotional_daily": df["Emotional_normalized"]
    })

    wellbeing_daily_results.append(daily_wellbeing)

######################################################
# Find complete cycles ★
######################################################
    cycle_starts = df.index[
        (df["Cycle day"] == 1) &
        (df[period_col] == 1)
    ].tolist()

    # Each pair of cycle starts defines one full cycle
    for i in range(len(cycle_starts) - 1):

        start = cycle_starts[i]
        next_start = cycle_starts[i + 1]

        cycle = df.loc[start:next_start - 1].copy()

        cycle_number = i + 1

        # Last day before next menstruation
        last_cycle_day = int(cycle["Cycle day"].max())

######################################################
# Determine phase boundaries ★
######################################################
        # Luteal = final 14 days
        luteal_start = last_cycle_day - 13

        # Ovulation window = 2 days before luteal
        ovulation_start = luteal_start - 2

        ovulation_days = [
            ovulation_start,
            ovulation_start + 1
        ]

        menstruation = cycle[
            cycle[period_col] == 1
        ]

        menstrual_results.append(
            calculate_phase_mean(
                menstruation,
                user,
                cycle_number,
                "Menstrual"
            )
        )

        follicular = cycle[
            (cycle[period_col] == 0) &
            (cycle["Cycle day"] < ovulation_start)
        ]

        follicular_results.append(
            calculate_phase_mean(
                follicular,
                user,
                cycle_number,
                "Follicular"
            )
        )

        ovulation = cycle[
            cycle["Cycle day"].isin(ovulation_days)
        ]

        ovulation_results.append(
            calculate_phase_mean(
                ovulation,
                user,
                cycle_number,
                "Ovulation"
            )
        )

        luteal = cycle[
            cycle["Cycle day"] >= luteal_start
        ]

        luteal_results.append(
            calculate_phase_mean(
                luteal,
                user,
                cycle_number,
                "Luteal"
            )
        )

######################################################
# Combine and save wellbeing scores ★
######################################################
wellbeing_daily_results = pd.concat(
    wellbeing_daily_results,
    ignore_index=True
)

wellbeing_daily_results.to_csv(
    "wellbeing_daily.csv",
    index=False
)

print("\nDaily well-being scores saved!")
print(wellbeing_daily_results.head(20))

######################################################
# Convert into dataframes ★
######################################################
menstrual_results = pd.DataFrame(menstrual_results)
follicular_results = pd.DataFrame(follicular_results)
ovulation_results = pd.DataFrame(ovulation_results)
luteal_results = pd.DataFrame(luteal_results)

all_phases_results = pd.concat(
    [
        menstrual_results,
        follicular_results,
        ovulation_results,
        luteal_results
    ],
    ignore_index=True
)

######################################################
# User mean and standard deviation across cycles ★
######################################################
user_phase_summary = (
    all_phases_results
    .groupby(["User", "Phase"])
    .agg(
        Physical_mean=("Physical_mean", "mean"),
        Physical_SD=("Physical_mean", "std"),
        Physical_cycles=("Physical_mean", "count"),

        Emotional_mean=("Emotional_mean", "mean"),
        Emotional_SD=("Emotional_mean", "std"),
        Emotional_cycles=("Emotional_mean", "count")
    )
    .reset_index()
)

user_phase_summary.to_csv(
    "user_phase_summary.csv",
    index=False
)

print("\nUser phase summary:")
print(user_phase_summary)
print("\nResults saved to user_phase_summary.csv")

######################################################
# Group mean and standard deviation ★
######################################################
group_phase_summary = (
    user_phase_summary
    .groupby("Phase")
    .agg(
        Physical_group_mean=("Physical_mean", "mean"),
        Physical_group_SD=("Physical_mean", "std"),
        Physical_users=("Physical_mean", "count"),

        Emotional_group_mean=("Emotional_mean", "mean"),
        Emotional_group_SD=("Emotional_mean", "std"),
        Emotional_users=("Emotional_mean", "count")
    )
    .reset_index()
)

group_phase_summary.to_csv(
    "group_phase_summary.csv",
    index=False
)

print("\nGroup phase summary:")
print(group_phase_summary)
print("\nResults saved to group_phase_summary.csv")

######################################################
# Pairwise phase comparisons ★
######################################################
physical_table = user_phase_summary.pivot(
    index="User",
    columns="Phase",
    values="Physical_mean"
)

emotional_table = user_phase_summary.pivot(
    index="User",
    columns="Phase",
    values="Emotional_mean"
)

comparisons = [
    ("Menstrual", "Follicular"),
    ("Menstrual", "Ovulation"),
    ("Menstrual", "Luteal"),
    ("Follicular", "Ovulation"),
    ("Follicular", "Luteal"),
    ("Ovulation", "Luteal")
]

comparison_results = []

for phase1, phase2 in comparisons:
    physical_difference = (
        physical_table[phase2] -
        physical_table[phase1]
    )
    physical_mean_difference = physical_difference.mean()
    physical_SD_difference = physical_difference.std()
    physical_n = physical_difference.count()

    emotional_difference = (
        emotional_table[phase2] -
        emotional_table[phase1]
    )
    emotional_mean_difference = emotional_difference.mean()
    emotional_SD_difference = emotional_difference.std()
    emotional_n = emotional_difference.count()

    comparison_results.append({
        "Comparison": f"{phase2} - {phase1}",

        "Physical_mean_difference":
            physical_mean_difference,

        "Physical_SD_difference":
            physical_SD_difference,

        "Physical_n":
            physical_n,

        "Emotional_mean_difference":
            emotional_mean_difference,

        "Emotional_SD_difference":
            emotional_SD_difference,

        "Emotional_n":
            emotional_n
    })

phase_comparisons = pd.DataFrame(comparison_results)
phase_comparisons.to_csv(
    "phase_comparisons.csv",
    index=False
)

print("\nPhase comparisons:")
print(phase_comparisons)
print("\nResults saved to phase_comparisons.csv")

######################################################
# Save results ★
######################################################
menstrual_results.to_csv(
    "menstrual_wellbeing.csv",
    index=False
)

follicular_results.to_csv(
    "follicular_wellbeing.csv",
    index=False
)

ovulation_results.to_csv(
    "ovulation_wellbeing.csv",
    index=False
)

luteal_results.to_csv(
    "luteal_wellbeing.csv",
    index=False
)

all_phases_results.to_csv(
    "all_phases_wellbeing.csv",
    index=False
)

print("Analysis complete!")
print(all_phases_results)