# Endometriosis Across the Menstrual Cycle 🩸
Cycle-tracking data-based investigating of phase-related symptom variation in women with endometriosis.

## Table of Contents
- [Overview](#overview)
- [Research Questions](#research-questions)
- [Dataset](#dataset)
- [Methods](#methods)
- [Key Findings](#key-findings)
- [Repository Structure](repository-structure)
- [Usage Instructions](#usage-instructions)
- [Limitations](#limitations)
- [References](#references)

## Overview
The menstrual cycle comprises four phases: menstrual, follicular, ovulatory, and luteal. Endometriosis is a chronic inflammatory gynecological disease marked by the presence of endometrial-like tissue outside of the uterus, accompanied by painful symptoms such as dysmenorrhea, dyspareunia, dyschezia, or dysuria. This project aimed to investigate how general physical state together with gastrointestinal (GI) issues and pain level change across the menstrual cycle phases.

## Research Questions
1. Does the general physical state differ significantly across the menstrual cycle phases?

*All participants recorded their daily general physical state. This part of analysis checks whether the general physical state changes across the menstrual cycle phases.*

2. Do gastrointestinal (GI) and pain burden intensities differ significantly across the menstrual cycle phases?

*Endometriosis symptoms may intensify during certain phases. This part of analysis checks whether GI issues and pain levels vary across the menstrual cycle phases.*

3. Is the general physical state associated with GI and pain burden intensities?

*The final part of the analysis checks whether the general physical state is correlated with GI and pain burden intensities.*
 

## Dataset
The cycle tracking data came from the published [KI EndoLIST: Endometriosis Longitudinal Individualized Symptoms Tracking Dataset](https://physionet.org/content/ki-endolist/1.0.0/). 
The dataset contains daily symptom-tracking records from 34 women diagnosed with endometriosis. Only the individual participant CSV files are required for this project (approximately 0.5 MB in total). Each CSV file contains rows representing tracking days and columns representing diverse symptoms.

**Note:** The original dataset is not redistributed in this repository due to its restricted-access license. Sign the required data use agreement on the PhysioNet website to access the files.


<details>
<summary>👤 See all participant CSV files</summary>

**Required files:**

- `User38.csv`
- `User39.csv`
- `User41.csv`
- `User42.csv`
- `User44.csv`
- `User48.csv`
- `User49.csv`
- `User51.csv`
- `User52.csv`
- `User53.csv`
- `User59.csv`
- `User61.csv`
- `User62.csv`
- `User63.csv`
- `User64.csv`
- `User65.csv`
- `User66.csv`
- `User67.csv`
- `User71.csv`
- `User72.csv`
- `User73.csv`
- `User75.csv`
- `User77.csv`
- `User79.csv`
- `User82.csv`
- `User84.csv`
- `User87.csv`

**Excluded participants (less than 2 full cycles tracked):**

- `User47.csv` 
- `User49.csv` 
- `User69.csv` 
- `User74.csv` 
- `User79.csv`
- `User80.csv` 

</details>

## Methods
### Score Normalization
The scripts normalize symptom intensity scores to a common **0–1 scale**, allowing comparison between participants who used different rating scales.
<details>
<summary>📊 See normalization </summary>

The original symptom intensity scales were normalized to a common **0–1 range** using the following transformations:

| Original scale | Normalization |
|:---:|:---:|
| 0–4 | `x / 4` |
| 0–10 | `x / 10` |
| 1–4 | `(x - 1) / 3` |
| 1–10 | `(x - 1) / 9` |
| 0/1 | Already normalized |

Here, `x` represents the original recorded score.

</details>

The full list of symptom classifications is available in [`burdens.csv`](./burdens.csv). The scripts can be adapted to investigate additional burden associations.

### Differences between Cycle Phases (RQ1 & RQ2)
1. **Daily scores:** Calculate normalized daily scores for general physical state (RQ1) and daily GI and pain burdens (RQ2).

   For GI and pain, daily burden is calculated as the mean intensity of the symptoms reported in that category on a given day. Missing symptom values are excluded rather than treated as zero.

   $$
   \text{Daily burden} =
   \frac{\sum \text{normalized intensities of reported symptoms}}
   {\text{number of symptoms reported that day}}
   $$

2. **Cycle-phase means:** Calculate the mean daily score for each menstrual cycle phase within each individual cycle.

   $$
   \text{Cycle-phase mean} =
   \frac{\sum \text{normalized daily scores}}
   {\text{number of recorded days}}
   $$

3. **Participant means:** Average the cycle-phase means across all available cycles for each participant, producing one mean per participant per phase.

4. **Group means:** Average the participant means for the same phase across all participants.

5. **Paired differences:** Calculate differences between menstrual cycle phases using participant-level paired observations. Differences are calculated as the second phase minus the first phase.

### Correlation (RQ3)
1. **Match observations:** Match daily physical state and burden scores by participant and day, retaining only days with both values available.
2. **Calculate participant means:** For each participant, calculate the mean physical state and mean burden intensity across the matched days.
3. **Calculate correlations:** Find Pearson's correlation for the participant-level pairs.

## Key Findings
The analysis revealed a moderate negative correlation between pain burden intensity and general physical state (r = −0.447, p = 0.019, n = 27). All differences between menstrual cycle phases remained below the 2σ threshold. For detailed results and discussion, see the [final report](./report.pdf).

## Repository Structure
The repository is organized into four folders, each containing Python scripts for data analysis, scripts for plot generation, and the resulting figures (.png).

<details>
<summary>📂 Click to expand repository structure</summary>

| Folder / File | Description |
|---|---|
| `GI/` | Python scripts for GI burden analysis and plotting, alongside generated figures. |
| `pain/` | Python scripts for pain burden analysis and plotting, alongside generated figures. |
| `wellbeing/` | Python scripts for general physical and emotional state analysis and plotting, alongside generated figures. |
| `correlation/` | Python scripts for Pearson correlation analysis and plotting, alongside generated figures. |
| `burdens.csv` | Classification of symptoms into burdens. |
| `report.pdf` | Final report, including methodology, results, discussion, and conclusions. |

</details>


**Note:** Emotional-state analyses are available in the repository but are not included in the final report.

## Usage Instructions
### Requirements
Python 3 and the following libraries: `pandas`, `Matplotlib`, `SciPy`, `glob`, and `re`.

**Installation:**

**macOS**
```bash
python3 -m pip install numpy pandas matplotlib scipy
```

**Windows**
```bash
py -m pip install numpy pandas matplotlib scipy
```

**Linux**
```bash
sudo apt-get install python3-tk
python3 -m pip install numpy pandas matplotlib scipy
```

### Running the Code
The analysis is organized by research questions. Download the relevant Python scripts and run them in the order indicated below.

***RQ1: Does general physical state differ significantly across menstrual cycle phases?***

Folder: [`wellbeing/`](./wellbeing/)
1. Run `general_wellbeing.py` to perform the analysis.
2. Run `general_wellbeing_plots.py` to generate the plots.

***RQ2: Do gastrointestinal (GI) and pain burden intensities differ significantly across menstrual cycle phases?***

Folder: [`GI/`](./GI/)
1. Run `gastrointestinal.py` to perform the GI burden analysis.
2. Run `giplots.py` to generate the plots.

Folder: [`pain/`](./pain/)
1. Run `pain.py` to perform the pain burden analysis.
2. Run `painplots.py` to generate the plots.

***RQ3: Is general physical state associated with GI and pain burden intensities?***

Folder: [`correlation/`](./correlation/)
1. Run `correlation.py` to calculate Pearson correlations.
2. Run `correlationplots.py` to generate the plots.

## Limitations
- **Inconsistent symptom tracking.** Participants did not record symptoms every day.
- **Small sample size.** Of the 34 participants, only 27 met the inclusion criteria.
- **Cycle phase estimates.** Cycle estimates potentially overlooked individual variation in cycle length and ovulation timing.
- **Artifical burden clustering.** These categories may overlap (e.g., bloating and abdominal pain). 

## References
**Dataset:** Zelovich, T., et al. (2026). KI EndoLIST: Endometriosis Longitudinal Individualized Symptoms Tracking Dataset (Version 1.0.0). PhysioNet. https://doi.org/10.13026/k99q-fm63

For the complete list of references, see the [final report](./report.pdf).