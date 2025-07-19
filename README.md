## Hospital Casemix Protocol Data Analysis Case Study - St John Of Gods Healthcare

### Exclusive Summary



---

### Project Background

Hospital Casemix Protocol(HCP) is a national program in Australia to collect de-identified patient data from public and private hospitals.
HCP data includes de-identified clinical, demographic, and financial information related to privately insured patients

#### Analysis Objective

To analyze the HCP dataset to identify trends, insights, and patterns that lead to tangible improvements across four critical domains:

- **Commercial Outcomes:** Enhancing financial sustainability.
- **Patient Care:** Improving clinical quality and patient experience.
- **Resource Allocation:** Optimising the use of staff, facilities, and beds.
- **Operational Efficiency:** Streamlining patient flow and internal processes.

---

### Analytical Approach

#### Data Quality

No empty columns or duplicate records detected

```
Null Value Exist
False               162
------------------------------------------
Duplicate Value Exist
False                    30615
```

By inspect data, we can see empty columns containing space

![image-20250719202621446](C:\Users\laaro\AppData\Roaming\Typora\typora-user-images\image-20250719202621446.png)

Given this is a medical dataset, is likely Missing Not At Random and should not be filled.

A decision is leave label it as **NA** at **Data preparation** stage

#### Data Understanding 

HCP Dataset contains 162 attributes which can be briefly break into different groups:

```markdown
🔹 Demographics (3 columns):
['Postcode', 'Sex','DateOfBirth']

🔹 Clinical (100 columns):
['PrincipalDiagnosis', 'AdditionalDiagnosis1', 'AdditionalDiagnosis2', 'AdditionalDiagnosis3', 'AdditionalDiagnosis4']...

🔹 Financial (12 columns):
['DischargeIntention', 'AccommodationCharge', 'TheatreCharge', 'LabourWardCharge', 'ICU_Charge']...

🔹 Provider (6 columns):
['InsurerIdentifier', 'EpisodeIdentifier', 'HospitalType', 'TransferInProviderNumber', 'InterHospitalContracted']...

🔹 Care Metrics (13 columns):
['ICU_Days', 'ICU_Hours', 'TotalPyschCareDays', 'PalliativeCareStatus', 'Readmission28Days']...
```



#### Data Preparation and Enrichment

#### Exploratory Data Analysis

#### Insight Generation

----

### Key Finding and Insight Deep Dive

#### Commercial Outcomes: Following the Money

####  Patient Care: Uncovering the Patient Journey

#### Resource Allocation: Matching Resources to Demand

#### Operational Efficiency: Pinpointing the Bottlenecks

----

### Strategic Recommendations: From Insight to Action

#### For Commercial Outcomes:

#### For Patient Care:

#### For Resource Allocation:

#### For Operational Efficiency:

---

### Reference Link

Script for analysis,visulisation,reuse are in this [Github Repository](https://github.com/HanL1223/HCF_CS)





