# 🔍 Inventory Obsolescence Risk Dashboard
## 📌 Project Overview

In this project I created a tool for determining inventory at risk of becoming short-dated and eventually expiring. The insights and data presented in this dashboard will help Supply Chain, QA and Commercial Teams collaborate on eliminating inventory waste and reduce costly destructions. The project uses a **synthetic SKU master dataset**; no real data was used in this project.

The inventory snapshot data was generated using AI an Python. I then loaded the data into a PostgreSQL database to serve as the source of truth. I used Power Query to extract the data using SQL, and add conditional values based on expiration dates and an assummed 365 day aging profile across all SKUs.

This project closely reflects my day-to-day work in inventory analytics in a pharmaceutical environment.

**Note:** This project is an oversimplification of a real inventory data.

---

## 🧠 Problem Statement

Raw inventory data is often stored in complex ERP systems or static spreadsheets. While the data exists, it isn't actionable. Stakeholders need a way to transform thousands of rows of lot-level data into a prioritized "hit list" that identifies exactly which products need immediate attention to save their value. This will reduce or eliminate costly write-offs and product destructions.

---

## 🏗️ Workflow and Tools Overview

ChatGPT & Python (Synthetic Data Generation)

  ⬇️
  
PostgreSQL (Relational Database Storage)

  ⬇️
  
PowerBI (Ingestion, Rule Validation, Visualization)

---

### 🛠️ Data Generation (Python)

-  Leveraged AI to create a [Python script](python/synth_sku_generator.py) used to generate a synthetic SKU master dataset with over 5,000 SKUs. The script allowed me to customize output, including the # of SKUs to generate and the percentage of errors to insert in the dataset.
-  Included fields such as:
    -  SKU Number/Material Number
    -  Description with dosage form and strength
    -  Commercial Classification
    -  Brand/Label Type
-  Errors introduced
    -  Missing values
    -  Inconsistent SKU Numbers
    -  Conflicting values
 ---


### 🗄️ Data Storage (PostgreSQL)

Loaded the synthetic dataset of Pharma and OTC products (csv format) into a local PostgreSQL database using the pgAdmin 4 admin tool. The table design resembled that of the csv dataset. No cleansing was performed, only verification that all data was loaded properly.

**First 10 rows**

![SKU Master First 10 Rows](screenshots/postgresql_check_10_rows.png) 

**Column Names and Data Types**

![Column Names and Data Types](screenshots/postgresql_column_names_types.png)

**Count of Records**

![Count of Records](screenshots/postgresql_check_total_records.png)

### 🔍 Data Ingestion and Data Quality Rules (Power BI)

-  I used PowerQuery to conenct to the local PostgreSQL database, and then loaded the data using using Import Mode so I could add Custom Columns.
-  Added Custom Columns to apply data rules to generate a boolean value. True = exception, False = no exception (data follows rule).
    -  SKU number must follow a ######ABC naming format (6 numeric characters, 3 alphabetic characters)
    -  Description must contain commercial classification ('General Market', 'Sample', 'Private Label') and, conversely, Commercial Classification must match this description
    -  Product Type must be 'OTC' or 'Pharma' with no blanks
    -  Lot Control has to be set to 'Yes' for all products with no blanks
    -  Primary Distribution Center must be one of five valid DCs with no blanks
    -  ABC Code (used accounting and cycle counting) must be populated with A, B, or C

**Initial Load into PowerQuery** [M code](powerquery/m_code.txt)

![PowerQuery Initial Load](screenshots/powerquery_db_connection.png)



### 📊 Dashboard Features, Insights, and Action Plan

The design of the PowerBI dashboard includes:
-  Overall data quality score (card)
-  Count of SKUs failing one or more rules (card)
-  Count of rule failures across the entire dataset (card)
-  Count of SKUs being considered in the analysis (card)
-  Breakdown of rule failures by type (stacked bar chart)
-  Breakdown of SKUs failing one or more rules by Product Type and Commercial Classification (clustered column chart)
-  Table of all SKUs failing one or more rules, with the option to filter/search by SKU

**Dashoard**

![Dashboard](screenshots/dashboard.png)

**The dashboard is reporting a 51% data quality level**, or 2673 out of 5489 SKUs not meeting all data quality rules. While there is significannt work to be done, the dashboard enables the work to be broken down into **manageabe, actionable tasks.**

Several **actionables** can be determined by using this dashboard

**Quick Wins**
  -  SKU naming conventions can be easily resolved. This only affects 29 SKUs but it is low-hanging fruit. This would be a quick win.
  -  Lot Control flag should be set as YES to on all SKUs. This update should be quick using SQL and it would correct 363 SKUs. This is also a quick win.
      ```
      UPDATE table
      SET lot_control_flag = 'Yes';
      ```     
  **Long Term Actionables**
  -  Incorrect Primary DC or blank values would require input from Supply Chain and Logistics teams, but this only affects 330 of SKUs.
  -  SKU Description and Commercial Classification. SKU description should include the Commercial Classification for 'Samples' and 'Private Label'. Determining and confirming these values would require input from commercial teams.
  -  ABC code updates would require Inventory Control or Finance/Accounting input. These are critical for cycle-counts at the DC and for audit purposes. Financial Reporting Group can also be considered in these discussions.

**Proposed Action Plan**

-  Tackle the quick wins first. These may only take a day or two to complete. Mass updates to SQL tables should still be performed with caution and be done in a Quality environment first.
-  Set time with subject matter experts to verify values (Description vs Commercial Classification, Incorrect/Missing DC, ABC Codes)

Long term actionables will require input for validation and verification of planned corrections, but this can happen in tandem with enforcement of rules for all new SKUs and SKU updates, along with additional training in best data entry and data stewardship practices.

### Realistic Two Week Progress Report

After two weeks, the following realistic improvements were achieved, increasing data from **51% to 78%**:
- 29 SKU numbers updated following naming rules. Root cause: 6th and 7th character had been switched
 
  ![SKU Corrections Verification](screenshots/postgresql_sku_corrections_verification.png)
  
- 363 Lot Control Flags updated to 'Yes'

  ![SKU Corrections Verification](screenshots/postgresql_lot_control_update.png)

- 1,427 SKU descripions updated to match Commercial Classification. These required the Commercial Classification to be added to the description
  
  ![SKU Corrections Verification](screenshots/postgresql_description_comm_class_update.png)
  
- ABC codes updated (**note:** A virtually equal distribution of ABC codes is highly unlikely)

  ![SKU Corrections Verification](screenshots/postgresql_abc_codes_corrected.png)

**Dashboard Present State**

![Dashboard Present State](screenshots/dashboard_post_data_cleanse.png)


---

## 🗂️ Repository Structure

```text
/
├── powerquery/           # Power Query (M) scripts for PostgreSQL ingestion and ETL
├── powerbi/              # Power BI dashboard file
├── docs/                 # Screenshots 
├── python/               # Python script 
└── README.md
