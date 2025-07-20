# Hospital Casemix Protocol Data Analysis Case Study - XXX Healthcare

## Exclusive Summary

An analysis of the Hospital Casemix Protocol (HCP) dataset was conducted to identify key trends and patterns. 

The findings reveal significant opportunities to enhance commercial outcomes, improve patient care, optimise resource allocation, and increase operational efficiency.

Key recommendations including:

- Protecting and growing core high-revenue services
- Introducing fixed-price packages to manage patient out-of-pocket costs, 
- Implementing targeted programs to reduce the length of stay for mental health patients
- Realigning staffing models to match weekly admission patterns.

---

## Project Background

Hospital Casemix Protocol(HCP) is a national program in Australia to collect de-identified patient data from public and private hospitals.
HCP data includes de-identified clinical, demographic, and financial information related to privately insured patients

## Analysis Objective

To analyze the HCP dataset to identify trends, insights, and patterns that lead to tangible improvements across four critical domains:

- **Commercial Outcomes:** Enhancing financial sustainability.
- **Patient Care:** Improving clinical quality and patient experience.
- **Resource Allocation:** Optimising the use of staff, facilities, and beds.
- **Operational Efficiency:** Streamlining patient flow and internal processes.

---

## Analytical Approach

### Data Quality

Initial automated checks did not detect empty columns or duplicate records. 

```
Null Value Exist
False               162
------------------------------------------
Duplicate Value Exist
False                    30615
```

However, manual inspection revealed that some fields contained spaces, indicating missing data. 

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

#### Script can be fine in [Github]() under `src/HCPDataPrepare.py` 

----

### Key Finding and Insight Deep Dive

#### Commercial Outcomes

**KPI to Track:** Total Hospital Charges by Principal Diagnosis Code.

**Why:** To identify the hospital's primary revenue streams, informing strategic decisions on investment and resource allocation.

![image-20250720122947413](reports\figures\Top 10 totalcharge.png)

![Top10 outofpocket category](reports\figures\Top10 totalcharge category.png)



**Observation:** The top three diagnosis codes by total hospital charges are **Gonarthrosis (M171)**, **Extracorporeal Dialysis (Z491)**, and **Coxarthrosis (M161)**. The corresponding categories—**Category M (Musculoskeletal System)** and **Category Z (Factors influencing health status)**—account for **38%** and **20%** of total charges, respectively.

**Recommendation:** **Protect and grow these core services.** Prioritise capital investment, specialist recruitment, and operational support for musculoskeletal and health services contact-related care to strengthen the hospital's primary revenue drivers.

------

**KPI to Track:** Total Patient Out-of-Pocket by Principal Diagnosis Code.

**Why:**  To identify procedures creating the greatest financial burden on patients. This is crucial for managing patient satisfaction, mitigating bad debt risk, and ensuring transparent, competitive pricing

![Top10 outofpocket](reports\figures\Top10 outofpocket.png)

![Top10 outofpocket by category](reports\figures\Top10 outofpocket by category.png)

**Observation:** Align with total revenue, categories **M (Musculoskeletal)** and **Z (Health Services Contact)** also represent the highest out-of-pocket costs for patients. Conversely, categories **G (Nervous System)** and **A (Infectious Diseases)** show negative values, suggesting bundled payments may exceed actual charges. This could reflect efficient service delivery or potential revenue leakage.

Categories **G (Nervous System)** and **A (Infectious Diseases)** show **negative values**, suggesting **bundled payments exceed actual charges** for these groups. This may reflect **over-compensation**, **low-charge service utilisation**, or **coding allocation patterns**.

**Recommendation: ** 

**For High-Cost Areas (M & Z):** Introduce **fixed-price packages** and a **financial navigation service** . This provides patients with price certainty and reduces the hospital's bad debt risk.

**For Negative-Cost Areas (G & A):** Launch a **profitability review** for nervous system and infectious disease services. Determine if the negative gap is due to efficient care (a positive outcome) or potential revenue loss from missed charges.

------

####  **Patient Care:** 

**KPI to Track:** Average Length of Stay (LOS) by Principal Diagnosis Code

**Why:** Understanding which diagnoses lead to the longest hospital stays allows the hospital to **Prioritise high-impact conditions** for care pathway improvements. By targeting these areas, leadership can improve **clinical efficiency, discharge planning**, and ultimately **patient flow**, while reducing avoidable inpatient costs.

![top10 LOS by code](reports\figures\top10 LOS by code.png)

**Observation:** 

This visual reveals a clear outlier

- Patients admitted with **Diagnosis Code ‘F’** (*Mental and Behavioural Disorders*) have an average LOS of approximately **13 days** — **more than triple** that of the next-highest group.
- In contrast, the LOS for **Diagnosis Code ‘P’** (*Perinatal Conditions*) is under **4 days**, with most other top diagnoses falling between **2 and 4 days**.
- This stark difference indicates that **Diagnosis Code ‘F’ is a major contributor to extended hospitalisations**, standing apart from all other diagnostic groups.

**Recommendation:**

Implement a Targeted Intervention Strategy for Diagnosis 'F'

**1. Conduct a Deep-Dive Diagnostic Review:**

- Launch an immediate analysis of **Diagnosis Code 'F'** cases to clarify the most common underlying conditions (e.g., schizophrenia, severe depression, substance use disorders).
- Identify clinical, social, and systemic factors contributing to prolonged stays.

**2. Form a Multidisciplinary Optimization Taskforce:**

- Include psychiatry, nursing, social work, allied health, discharge planners, and hospital operations.
- Evaluate current care pathways, coordination gaps, and barriers to discharge (e.g., rehab waitlists, lack of community support).

**3. Design a Proactive Mental Health Care Management Program:**

- Standardise early psychiatric assessments and discharge planning on Day 1.
- Improve handoffs to outpatient or community-based mental health services.
- Explore transitional care options, including partnerships with step-down or supported accommodation facilities.

---

**KPI to Track:** Average Length of Stay (LOS) by Patient Age Group and Comorbidity Count.

**Why:** To create a "risk matrix" that visually identifies which patient segments are most vulnerable to prolonged hospital stays based on their intrinsic health factors, allowing for proactive care management.

![Top10 outofpocket by category](reports\figures\LOS matrix by age group.png)

**Observation:** The heatmap effectively visualizes this risk matrix. Moving **down the y-axis** (higher comorbidity counts) and **across the x-axis** (older age groups), the color intensifies, signaling longer average LOS.

- The **“red zone”** in the bottom-right corner highlights patients aged **65+ with multiple comorbidities** as the highest risk group, experiencing significantly extended hospital stays compared to others. 

### Recommendation:

**Implement a Proactive Geriatric Care Model focused on the red zone:**

- Automatically trigger **comprehensive geriatric assessments** within 24 hours for all admitted patients aged **65+ with 3 or more comorbidities**.
- This early intervention supports tailored care plans, anticipates complications, and promotes safer, more timely discharges.

------

#### Resource Allocation and Operational Efficiency: Matching Resources to Demand

**KPI to Track:** Admission Volume by Day of the Week, segmented by Urgency of Admission (Emergency, Elective, Unassigned)

### Why: 

Understanding the daily volume and urgency mix of patient admissions is critical for effective resource planning and operational efficiency. By knowing when and what type of admissions occur, hospitals can better align staffing, bed availability, and clinical services to patient demand, improving care quality, reducing waiting times, and optimising costs 

![Admission by week and emgergency](reports\figures\Admission by week and emgergency.png)

### **Observation:**

- **Weekdays (Monday to Friday)** are dominated by **elective admissions**, with counts consistently above 5,000 per day. Emergency admissions during weekdays remain relatively low and stable, ranging from 120 to 187 daily.
- **Saturday** shows a significant drop in elective admissions (1,701), but emergency admissions (153) remain steady, increasing the relative proportion of emergencies.
- **Sunday** presents a dramatic shift where elective admissions down  to just 136, while emergency admissions remain comparatively raise to 169. This results in **emergency admissions constituting over 40% of total admissions on Sundays**, indicating that the weekend admission profile is heavily skewed towards emergency cases.
- The volume of unassigned urgency codes remains relatively small and stable across all days, suggesting good data quality and triage assignment.

### **Recommendation:**

#### **1. Resource Allocation:**

- **Weekdays:** Given the high **total patient volume (~5,000+ per day)** dominated by elective admissions, staffing and resource planning should prioritise **high throughput for elective cases** — including surgical teams, bed managers, discharge coordinators, and administrative staff to optimise patient flow and minimize delays. Emergency teams can operate with standard coverage due to the relatively low emergency volume.
- **Saturday:** Despite lower total volume, maintain a **balanced staffing model** that supports elective procedures but is flexible to handle a relatively higher share of emergency admissions. Consider slightly reduced elective resources but maintain robust emergency care capacity.
- **Sunday:** Focus operational resources on **emergency and acute care**, as emergency admissions comprise nearly half of a much smaller total volume. Elective services and associated staffing can be scaled back accordingly. Emergency departments and critical care units should be staffed to meet this demand.

#### **2. Operational Efficiency:**

- **Weekdays:** Streamline discharge planning and elective care pathways to manage large patient numbers efficiently and reduce bed occupancy times.
- **Weekends:** Implement expedited triage and care protocols for emergencies and consider cross-training staff to cover essential functions with fewer elective cases.
- Track and minimize unassigned urgency cases to improve triage accuracy, helping optimise allocation decisions.

---

### Reference Link

Script for analysis,visulisation,reuse are in this [Github Repository](https://github.com/HanL1223/HCF_CS)

Diagnosis Code Mapping from [ICD-10-AM-12th Edition](https://www.ihacpa.gov.au/sites/default/files/2022-12/ICD-10-AM%20Chronicle_Twelfth%20Edition_Part%201_A00%20to%20T98%20and%20Z00%20to%20Z99.PDF)



