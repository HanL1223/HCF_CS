import os
import pandas as pd
import numpy as np
import logging
from src.ingest_data import DataIngestorFactory
from datetime import date

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class HCPDataPreparer:
    def __init__(self, df_raw: pd.DataFrame):
        self.df = df_raw.copy()

    def _clean_blank_strings_as_na(self):
        """Replace blank or space-only strings in all columns with np.nan."""
        for col in self.df.columns:
            # Only apply to object or string-like columns
            if self.df[col].dtype == 'object':
                self.df[col] = self.df[col].apply(lambda x: np.nan if isinstance(x, str) and x.strip() == '' else x)

    def _convert_date_columns(self):
        """Convert specified columns from day-month-year integer format to datetime; add _dt and _yyyymmdd columns."""
        date_cols = ['AdmissionDate', 'DischargeDate', 'DateOfBirth','SeparationDate']

        def parse_dmy(val):
            if pd.isna(val):
                return pd.NaT
            try:
                # Convert to string, zero pad to 8 chars for DDMMYYYY format
                s = str(int(val)).zfill(8)
                # Parse assuming day=0:2, month=2:4, year=4:8
                return pd.to_datetime(f"{s[4:8]}-{s[2:4]}-{s[0:2]}", format="%Y-%m-%d")
            except Exception:
                return pd.NaT

        for col in date_cols:
            if col in self.df.columns:
                self.df[f"{col}_dt"] = self.df[col].apply(parse_dmy)
                self.df[f"{col}_yyyymmdd"] = self.df[f"{col}_dt"].dt.strftime('%Y%m%d')
        

    def _engineer_commercial_outcomes_features(self):
        charge_cols =  [
    'AccommodationCharge',
    'TheatreCharge',
    'MedicalDevicesCharge',
    'NonMedicalCharge',
    'LabourWardCharge',
    'ICU_Charge',
    'ProsthesisCharge',
    'PharmacyCharge',
    'OtherCharges',
    'SCN_Charges',
    'CCU_Charges'
]
        available = [col for col in charge_cols if col in self.df.columns]
        if not available:
            raise ValueError("No hospital charge columns found.")
        
        self.df['TotalHospitalCharges'] = self.df[available].sum(axis=1)

        if 'BundledCharges' in self.df.columns:
            self.df['BenefitPaid'] = self.df['BundledCharges']
        else:
            self.df['BenefitPaid'] = 0

        self.df['OutOfPocketExpense'] = self.df['TotalHospitalCharges'] - self.df['BenefitPaid']
        self.df['OutOfPocketPct'] = np.where(
            self.df['TotalHospitalCharges'] > 0,
            (self.df['OutOfPocketExpense'] / self.df['TotalHospitalCharges']) * 100,
            0
        )
        

    def _engineer_patient_care_features(self):
        # Use *_dt columns for date calculations
        if 'AdmissionDate_dt' in self.df.columns and 'DischargeDate_dt' in self.df.columns:
            self.df['LengthOfStay'] = (self.df['DischargeDate_dt'] - self.df['AdmissionDate_dt']).dt.days

        diag_cols = [f'AdditionalDiagnosis{i}' for i in range(1, 50)]
        present_cols = [col for col in diag_cols if col in self.df.columns]
        self.df['ComorbidityCount'] = self.df[present_cols].apply(
    lambda row: sum((str(x).strip() not in ['', '0', 'nan','  ','NaN']) for x in row), axis=1
)

    def _engineer_resource_allocation_features(self):
        if 'AdmissionDate_dt' in self.df.columns:
            self.df['AdmissionYear'] = self.df['AdmissionDate_dt'].dt.year
            self.df['AdmissionMonth'] = self.df['AdmissionDate_dt'].dt.month
            self.df['AdmissionDayOfWeek'] = self.df['AdmissionDate_dt'].dt.day_name()

    def _engineer_operational_efficiency_features(self):
        if 'DischargeDate_dt' in self.df.columns:
            self.df['DischargeHour'] = self.df['DischargeDate_dt'].dt.hour
        if 'AdmissionDate_dt' in self.df.columns:
            self.df['AdmissionDateOnly'] = self.df['AdmissionDate_dt'].dt.date

    def _clean_column_names(self):
        self.df.columns = [
            col.strip().lower().replace(' ', '_').replace('(', '').replace(')', '')
            for col in self.df.columns
        ]
    def _final_cleaning(self):
        self.df['lengthofstay'] = (self.df['separationdate_dt'] - self.df['admissiondate_dt']).dt.days
        today = pd.to_datetime('today').normalize() #Standarlised to 0:00
        self.df['age'] = self.df['dateofbirth_dt'].apply(
    lambda dob: today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
)
        self.df['principaldiagnosiscode'] = self.df['principaldiagnosis'].str[1]
        urgency_map = {
            1: 'Emergency',
            2: 'Elective',
            3: 'Unassigned',
            9: 'Unknown' 
        } #12th edition
        self.df['urgency_mapped'] = self.df['urgencyofadmission'].map(urgency_map)
        self.df['admission_day_name'] = self.df['admissiondate_dt'].dt.day_name()
        self.df['separation_day_name'] = self.df['separationdate_dt'].dt.day_name()

    def prepare_data(self) -> pd.DataFrame:
        logging.info("1. Convert Dates and removing empty space value")
        self._convert_date_columns()
        self._clean_blank_strings_as_na

        logging.info("2. Engineer Commercial Outcomes")
        self._engineer_commercial_outcomes_features()

        logging.info("3. Engineer Patient Care Metrics")
        self._engineer_patient_care_features()

        logging.info("4. Engineer Resource Allocation Metrics")
        self._engineer_resource_allocation_features()

        logging.info("5. Engineer Operational Efficiency Metrics")
        self._engineer_operational_efficiency_features()

        logging.info("6. Standardize Column Names")
        self._clean_column_names()

        logging.info("7. Final Cleaning")
        self._final_cleaning()

        

        return self.df


if __name__ == "__main__":
    pass
