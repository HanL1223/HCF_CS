import os
import pandas as pd
import numpy as np
import logging
from src.ingest_data import DataIngestorFactory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class HCPDataPreparer:
    def __init__(self, df_raw: pd.DataFrame):
        self.df = df_raw.copy()

    def _convert_date_columns(self):
        """Convert specified columns from day-month-year integer format to datetime; add _dt and _yyyymmdd columns."""
        date_cols = ['AdmissionDate', 'DischargeDate', 'DateOfBirth']

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

        diag_cols = [f'AdditionalDiagnosis{i}' for i in range(1, 11)]
        present_cols = [col for col in diag_cols if col in self.df.columns]
        self.df['ComorbidityCount'] = self.df[present_cols].notna().sum(axis=1)

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

    def _final_cleaning(self):
        if 'LengthOfStay' in self.df.columns:
            self.df = self.df[self.df['LengthOfStay'].isna() | (self.df['LengthOfStay'] >= 0)]

    def _clean_column_names(self):
        self.df.columns = [
            col.strip().lower().replace(' ', '_').replace('(', '').replace(')', '')
            for col in self.df.columns
        ]

    def prepare_data(self) -> pd.DataFrame:
        logging.info("1. Convert Dates")
        self._convert_date_columns()

        logging.info("2. Engineer Commercial Outcomes")
        self._engineer_commercial_outcomes_features()

        logging.info("3. Engineer Patient Care Metrics")
        self._engineer_patient_care_features()

        logging.info("4. Engineer Resource Allocation Metrics")
        self._engineer_resource_allocation_features()

        logging.info("5. Engineer Operational Efficiency Metrics")
        self._engineer_operational_efficiency_features()

        logging.info("6. Final Cleaning")
        self._final_cleaning()

        logging.info("7. Standardize Column Names")
        self._clean_column_names()

        return self.df


if __name__ == "__main__":
    file_path = 'HCP_Dataset_for_Case_Study_CSV.csv'
    file_extension = os.path.splitext(file_path)[1].lower()

    try:
        ingestor = DataIngestorFactory.get_data_ingestor(file_extension)
        df_raw = ingestor.ingest(file_path)

        data_preparer = HCPDataPreparer(df_raw)
        df_prepared = data_preparer.prepare_data()

        print("\n--- Final Dataset Ready for Analysis ---")
        print("DataFrame Info:")
        df_prepared.info()

        print("\nSample of Prepared Data:")
        print(df_prepared[[
            'primarydiagnosis', 'insurerid', 'totalhospitalcharges', 'benefitpaid',
            'outofpocketexpense', 'outofpocketpct', 'lengthofstay', 'comorbiditycount',
            'admissionmonth', 'dischargehour'
        ]].head())

        output_filename = 'hcp_data_prepared_for_kpi_analysis.csv'
        df_prepared.to_csv(output_filename, index=False)
        print(f"\nSaved to '{output_filename}'")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
