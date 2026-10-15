import pandas as pd
import glob
import re

######################################################
# Pain symptoms ★
######################################################
PAIN_SYMPTOMS = [
    "Migraines",
    "Breast tenderness",
    "Lower back pain and pelvic pain",
    "Lower abdominal stabbing pain / abdominal cramps",
    "Knee pain",
    "Pain in ankle",
    "Headache",
    "Ovaries pain",
    "Lower back pain",
    "Pain in tailbone",
    "Upper abdominal pain",
    "Lower abdominal pain",
    "Pelvic pain",
    "Scapula pain",
    "Abdominal cramps",
    "Endo flare up",
    "Vaginal pain",
    "Right pelvic pain",
    "Upper back pain",
    "Sciatic pain - right side / pain radiating down the leg",
    "Pain radiating down the leg",
    "Sciatic pain - right side",
    "Uterine cramps",
    "Left pelvic pain",
    "Rectal stabbing",
    "Painful right feet",
    "Abdominal dull-aching pain",
    "Vulval / groin pain",
    "Lower abdominal dull-aching pain",
    "Lower abdominal stabbing pain",
    "Uterine cervix pain",
    "Pelvic pain / pain in tailbone",
    "Shoulder pain",
    "Chest pain",
    "Pelvic pressure",
    "Navel pain",
    "Groin pain - right",
    "Pain radiating down the front leg",
    "Pain radiating down the back leg",
    "Rib / chest pain right side",
    "Shoulder / neck / scapula pain right side",
    "Waist pain",
    "Rib pain",
    "Pain in R knee",
    "Pain in L knee",
    "Rectum pain",
    "Sore feet",
    "Neck and scapula pain",
    "Pain radiating to the buttock",
    "Leg cramps",
    "Eye pain / pressure",
    "Groin pain",
    "Vulval pain",
    "Neck pain",
    "Joint pain",
    "Scapula pain right side",
    "Scapula pain left side",
    "Abdominal stabbing pain",
    "Pelvic pain / groin pain / pain radiating down the leg",
    "Sciatic pain - left side",
    "Lower abdominal stabbing / dull-aching pain",
    "General pain",
    "Buttock pain left",
    "Hands weakness / wrist pain",
    "Thigh and pelvic pain",
    "Pain in thigh",
    "Stabbing pain in the chest",
    "Stabbing pain in the sides of the abdomen",
    "Leg pain",
    "Upper abdominal pain L",
    "Abdominal pain",
    "Thigh stabs",
    "Ear pain",
    "Lower abdominal cramps",
    "Shoulder / neck / scapula pain",
    "Pain - right side",
    "Pain - left side",
    "Pelvic pain / stomach flare / abdominal flare",
    "Buttock pain / pain radiating down the leg",
    "Lower abdominal stabbing / persistent pain R",
    "Lower abdominal stabbing / persistent pain L",
    "Leg pain R",
    "Wrist pain",
    "Neck muscles cramps",
    "Lower abdominal stabbing pain / ovaries pain",
    "Joint pain R",
    "Right pelvic / buttock / knee / feet pain",
    "Lower abdominal stabbing pain R",
    "Abdominal dull-aching pain / abdominal cramps",
    "Leg pain L",
    "Rib pain R",
    "Stabbing pain in ovaries",
    "Neck muscles cramps L",
    "Muscle tightness"
]

######################################################
# Storage for phase results ★
######################################################
menstrual_results = []
follicular_results = []
ovulation_results = []
luteal_results = []

######################################################
# Find files (hard-coded directory) ★
######################################################
files = glob.glob("project/User*.csv")

######################################################
# Normalize scores ★
######################################################
def normalize_pain(series, column_name):
    symptom = column_name.split(" (")[0].strip()
    scale_match = re.search(r",\s*(\d+)\s*-", column_name)

    if scale_match is None:
        raise ValueError(
            f"Could not determine scale for: {column_name}"
        )

    maximum = float(scale_match.group(1))
    values = pd.to_numeric(series, errors="coerce")
    normalized = values / maximum

    return normalized

######################################################
# Calculating pain phase mean ★
######################################################
def calculate_pain_phase_mean(data, user, cycle_number, phase):

    pain_mean = data["Pain_daily_mean"].mean()
    pain_days = data["Pain_daily_mean"].notna().sum()

    return {
        "User": user,
        "Cycle": cycle_number,
        "Phase": phase,
        "Pain_mean": pain_mean,
        "Pain_days": pain_days
    }

pain_daily_results = [] 

######################################################
# Normalize scores ★
######################################################
for file in files:
    df = pd.read_csv(file)
    user = re.search(r"User\d+", file).group()
    normalized_pain_columns = []

    for col in df.columns:
        symptom = col.split(" (")[0].strip()

        if symptom in PAIN_SYMPTOMS:
            normalized_col = col + "_normalized"
            df[normalized_col] = normalize_pain(
                df[col],
                col
            )
            normalized_pain_columns.append(normalized_col)

######################################################
# Daily pain mean ★
######################################################
    if len(normalized_pain_columns) > 0:

        # Number of pain symptoms reported on each day
        df["Pain_daily_n"] = (
            df[normalized_pain_columns]
            .notna()
            .sum(axis=1)
        )

        # Mean normalized pain intensity for each day
        df["Pain_daily_mean"] = (
            df[normalized_pain_columns]
            .mean(axis=1, skipna=True)
        )

    else:

        # User has no pain variables
        df["Pain_daily_n"] = 0
        df["Pain_daily_mean"] = float("nan")

    daily_pain = pd.DataFrame({
        "User": user,
        "Day_index": df.index,
        "Pain_daily_mean": df["Pain_daily_mean"]
    })

    pain_daily_results.append(daily_pain)

######################################################
# Estimating cycle phases ★
######################################################
    period_col = next(
        col for col in df.columns
        if col.startswith("Period")
    )

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

        # Luteal = final 14 days
        luteal_start = last_cycle_day - 13

        # Ovulation = 2 days before luteal
        ovulation_start = luteal_start - 2

        ovulation_days = [
            ovulation_start,
            ovulation_start + 1
        ]

        menstruation = cycle[
            cycle[period_col] == 1
        ]

        menstrual_results.append(
            calculate_pain_phase_mean(
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
            calculate_pain_phase_mean(
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
            calculate_pain_phase_mean(
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
            calculate_pain_phase_mean(
                luteal,
                user,
                cycle_number,
                "Luteal"
            )
        )

pain_daily_results = pd.concat(
    pain_daily_results,
    ignore_index=True
)

pain_daily_results.to_csv(
    "Pain_daily_means.csv",
    index=False
)

print("\nDaily pain means saved!")
print(pain_daily_results.head(20))

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
all_phases_pain = pd.concat(
    [
        menstrual_results,
        follicular_results,
        ovulation_results,
        luteal_results
    ],
    ignore_index=True
)

all_phases_pain.to_csv(
    "all_phases_Pain.csv",
    index=False
)

print("\nPain phase analysis complete!")
print(all_phases_pain)
print("\nResults saved to all_phases_Pain.csv")

######################################################
# User mean and standard deviation across cycles ★
######################################################
user_pain_summary = (
    all_phases_pain
    .groupby(["User", "Phase"])
    .agg(
        Pain_mean=("Pain_mean", "mean"),
        Pain_SD=("Pain_mean", "std"),
        Pain_cycles=("Pain_mean", "count")
    )
    .reset_index()
)

user_pain_summary.to_csv(
    "user_Pain_summary.csv",
    index=False
)

print("\nUser Pain summary:")
print(user_pain_summary)
print("\nResults saved to user_Pain_summary.csv")

######################################################
# Group mean and standard deviation ★
######################################################
pain_group_summary = (
    user_pain_summary
    .groupby("Phase")
    .agg(
        Pain_group_mean=("Pain_mean", "mean"),
        Pain_group_SD=("Pain_mean", "std"),
        Pain_users=("Pain_mean", "count")
    )
    .reset_index()
)

pain_group_summary.to_csv(
    "Pain_group_summary.csv",
    index=False
)

print("\nPain group summary:")
print(pain_group_summary)
print("\nResults saved to Pain_group_summary.csv")

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

pain_table = user_pain_summary.pivot(
    index="User",
    columns="Phase",
    values="Pain_mean"
)

pain_comparison_results = []

for phase1, phase2 in comparisons:

    # Difference = second phase - first phase
    pain_difference = (
        pain_table[phase2] -
        pain_table[phase1]
    )

    # Mean of participant differences
    pain_mean_difference = pain_difference.mean()

    # Sample SD of participant differences
    pain_SD_difference = pain_difference.std()

    # Number of participants with both phases available
    pain_n = pain_difference.count()

    pain_comparison_results.append({
        "Comparison": f"{phase2} - {phase1}",
        "Pain_mean_difference": pain_mean_difference,
        "Pain_SD_difference": pain_SD_difference,
        "Pain_n": pain_n
    })

pain_phase_comparisons = pd.DataFrame(
    pain_comparison_results
)

pain_phase_comparisons.to_csv(
    "Pain_phase_comparisons.csv",
    index=False
)

print("\nPain phase comparisons:")
print(pain_phase_comparisons)
print("\nResults saved to Pain_phase_comparisons.csv")