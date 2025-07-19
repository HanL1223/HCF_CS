import os
import zipfile
from abc import ABC, abstractmethod
import pandas as pd

class DataIngestor(ABC):
    @abstractmethod
    def ingest(self, file_path: str) -> pd.DataFrame:  # Changed parameter name
        """Abstract method to ingest data from a given file"""
        pass

class CSVIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:  # Changed parameter name
        """Read directly from CSV file path"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found at {file_path}")
        return pd.read_csv(file_path)
    
class XlsxIngester(DataIngestor):
    def ingest(self, file_path: str,has_header= None) -> pd.DataFrame:
        """Extract .xlsx file and return the content as a Pandas DataFrame"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Xlsx file not found at {file_path}")

         # Auto-detect header if not specified
        if has_header is None:
            preview = pd.read_excel(file_path, header=None, nrows=2)
            first_row = preview.iloc[0]
            has_header = all(isinstance(val, str) or pd.isnull(val) for val in first_row)

        # Read full file based on header detection
        return pd.read_excel(file_path, header=0 if has_header else None)

class ZIPIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:  # Changed parameter name
        """Extracts a .zip file and returns the content as a pandas DataFrame."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"ZIP file not found at {file_path}")
            
        # Extract to same directory as ZIP file
        extract_dir = os.path.dirname(file_path)
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find the extracted CSV
        extracted_files = os.listdir(extract_dir)
        csv_files = [f for f in extracted_files if f.endswith('.csv')]
        
        if len(csv_files) == 0:
            raise FileNotFoundError("No CSV file found in the extracted files")
        if len(csv_files) > 1:
            raise ValueError("Multiple CSV files found in the extracted files")
        
        return pd.read_csv(os.path.join(extract_dir, csv_files[0]))

class DataIngestorFactory:
    @staticmethod
    def get_data_ingestor(file_extension: str) -> DataIngestor:
        """Returns the appropriate DataIngestor based on file extension."""
        if file_extension == ".zip":
            return ZIPIngestor()
        elif file_extension == ".csv":
            return CSVIngestor()  # Fixed: now returns instance instead of class
        elif file_extension =='.xlsx':
            return XlsxIngester()
        else:
            raise ValueError(f"No ingestor available for file extension: {file_extension}")

# Keep the original if __name__ block untouched
if __name__ == "__main__":
    pass