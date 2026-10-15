import pandas as pd
from scipy.stats import pearsonr

######################################################
# Data files for wellbeing, GI, and pain ★
######################################################
wellbeing = pd.read_csv("wellbeing_daily.csv")
gi = pd.read_csv("GI_daily_means.csv")
pain = pd.read_csv("Pain_daily_means.csv")

######################################################
# Merge pain and physical ★
######################################################
pain_physical = pd.merge(
    pain,
    wellbeing[["User", "Day_index", "Physical_daily"]],
    on=["User", "Day_index"],
    how="inner"
)

######################################################
# Only days when both pain and physical reported ★
######################################################
pain_physical = pain_physical.dropna(
    subset=["Pain_daily_mean", "Physical_daily"]
)

print("\nNumber of matched daily observations:")
print(len(pain_physical))

######################################################
# Mean pain-physical per user ★
######################################################
pain_physical_users = (
    pain_physical
    .groupby("User")
    .agg(
        Pain_mean=("Pain_daily_mean", "mean"),
        Physical_mean=("Physical_daily", "mean"),
        Matched_days=("Pain_daily_mean", "count")
    )
    .reset_index()
)

print("\nParticipant means:")
print(pain_physical_users)

pain_physical_users.to_csv(
    "Pain_Physical_user_means.csv",
    index=False
)

######################################################
# Pearson pain-physical correlation ★
######################################################
r, p = pearsonr(
    pain_physical_users["Pain_mean"],
    pain_physical_users["Physical_mean"]
)


print("\nPain burden vs. physical well-being:")
print("r =", r)
print("p =", p)
print("n =", len(pain_physical_users))

######################################################
# Merge pain and emotional ★
######################################################
pain_emotional = pd.merge(
    pain,
    wellbeing[["User", "Day_index", "Emotional_daily"]],
    on=["User", "Day_index"],
    how="inner"
)

######################################################
# Only days when both pain and emotional reported ★
######################################################
pain_emotional = pain_emotional.dropna(
    subset=["Pain_daily_mean", "Emotional_daily"]
)

print("\nNumber of matched daily observations:")
print(len(pain_emotional))

######################################################
# Mean pain-physical per user ★
######################################################
pain_emotional_users = (
    pain_emotional
    .groupby("User")
    .agg(
        Pain_mean=("Pain_daily_mean", "mean"),
        Emotional_mean=("Emotional_daily", "mean"),
        Matched_days=("Pain_daily_mean", "count")
    )
    .reset_index()
)

print("\nParticipant means:")
print(pain_emotional_users)

pain_emotional_users.to_csv(
    "Pain_Emotional_user_means.csv",
    index=False
)

######################################################
# Pearson pain-emotional correlation ★
######################################################
r, p = pearsonr(
    pain_emotional_users["Pain_mean"],
    pain_emotional_users["Emotional_mean"]
)

print("\nPain burden vs. emotional well-being:")
print("r =", r)
print("p =", p)
print("n =", len(pain_emotional_users))

######################################################
# Merge GI and physical ★
######################################################
gi_physical = pd.merge(
    gi,
    wellbeing[["User", "Day_index", "Physical_daily"]],
    on=["User", "Day_index"],
    how="inner"
)

######################################################
# Only days when both GI and physical reported ★
######################################################
gi_physical = gi_physical.dropna(
    subset=["GI_daily_mean", "Physical_daily"]
)

print("\nNumber of matched daily observations:")
print(len(gi_physical))

######################################################
# Mean GI-physical per user ★
######################################################
gi_physical_users = (
    gi_physical
    .groupby("User")
    .agg(
        GI_mean=("GI_daily_mean", "mean"),
        Physical_mean=("Physical_daily", "mean"),
        Matched_days=("GI_daily_mean", "count")
    )
    .reset_index()
)

print("\nGI vs physical participant means:")
print(gi_physical_users)

gi_physical_users.to_csv(
    "GI_Physical_user_means.csv",
    index=False
)

######################################################
# Pearson GI-physical correlation ★
######################################################
r, p = pearsonr(
    gi_physical_users["GI_mean"],
    gi_physical_users["Physical_mean"]
)

print("\nGI burden vs. physical well-being:")
print("r =", r)
print("p =", p)
print("n =", len(gi_physical_users))

######################################################
# Merge GI and emotional ★
######################################################
gi_emotional = pd.merge(
    gi,
    wellbeing[["User", "Day_index", "Emotional_daily"]],
    on=["User", "Day_index"],
    how="inner"
)

######################################################
# Only days when both GI and emotional reported ★
######################################################
gi_emotional = gi_emotional.dropna(
    subset=["GI_daily_mean", "Emotional_daily"]
)

print("\nNumber of matched daily observations:")
print(len(gi_emotional))

######################################################
# Mean GI-emotional per user ★
######################################################
gi_emotional_users = (
    gi_emotional
    .groupby("User")
    .agg(
        GI_mean=("GI_daily_mean", "mean"),
        Emotional_mean=("Emotional_daily", "mean"),
        Matched_days=("GI_daily_mean", "count")
    )
    .reset_index()
)

print("\nGI vs emotional participant means:")
print(gi_emotional_users)

gi_emotional_users.to_csv(
    "GI_Emotional_user_means.csv",
    index=False
)

######################################################
# Pearson GI-emotional correlation ★
######################################################
r, p = pearsonr(
    gi_emotional_users["GI_mean"],
    gi_emotional_users["Emotional_mean"]
)

print("\nGI burden vs. emotional well-being:")
print("r =", r)
print("p =", p)
print("n =", len(gi_emotional_users))