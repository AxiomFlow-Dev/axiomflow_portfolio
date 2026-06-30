import os
import glob
import logging
import pandas as pd
from datetime import datetime

# Configure professional logging to track execution metrics
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"excel_automation_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)

def secure_excel_lookup(master_file_path, lookup_folder_path, output_file_path):
    """
    Executes a secure, monitored row-by-row data cross-reference lookup
    between a master Excel configuration and a target reference directory.
    """
    logging.info("Initializing automated Excel cross-reference pipeline...")
    
    # Pre-flight structural checks
    if not os.path.exists(master_file_path):
        logging.error(f"Execution halted: Master file '{master_file_path}' not found.")
        return False
        
    if not os.path.exists(lookup_folder_path):
        logging.warning(f"Target directory '{lookup_folder_path}' missing. Creating directory...")
        os.makedirs(lookup_folder_path)
        logging.info(f"Directory created. Please populate '{lookup_folder_path}' with target reference sheets.")
        return False

    try:
        logging.info(f"Reading master data core: {master_file_path}")
        master_df = pd.read_excel(master_file_path, dtype=str)
    except Exception as e:
        logging.error(f"Failed to parse master Excel file structural integrity: {e}")
        return False

    # Check for target mapping validation rules
    if 'Lookup_ID' not in master_df.columns:
        logging.error("Missing required index column: 'Lookup_ID' must be present in the master sheet.")
        return False

    # Ensure placeholder target output column exists cleanly
    if 'Master_Target_Column' not in master_df.columns:
        master_df['Master_Target_Column'] = None

    rows_updated = 0
    rows_skipped = 0

    logging.info(f"Processing database records ({len(master_df)} entries found)...")
    
    for idx, row in master_df.iterrows():
        lookup_id = str(row['Lookup_ID']).strip()
        
        # Guard clause against empty or NaN keys
        if not lookup_id or lookup_id == 'nan':
            rows_skipped += 1
            continue
            
        target_pattern = os.path.join(lookup_folder_path, f"*{lookup_id}*.xlsx")
        matching_files = glob.glob(target_pattern)
        
        if matching_files:
            sub_file = matching_files[0]
            try:
                # Open reference file read-only to avoid file locks
                sub_df = pd.read_excel(sub_file, dtype=str)
                
                if not sub_df.empty and 'Target_Value' in sub_df.columns:
                    extracted_val = sub_df.iloc[0]['Target_Value']
                    
                    # Core atomic update mapping
                    master_df.at[idx, 'Master_Target_Column'] = extracted_val
                    rows_updated += 1
                else:
                    logging.warning(f"Skipping empty or invalid schema file: {os.path.basename(sub_file)}")
                    rows_skipped += 1
                    
            except Exception as e:
                logging.error(f"Error reading sub-file structural stream [{os.path.basename(sub_file)}]: {e}")
                rows_skipped += 1
        else:
            rows_skipped += 1

    try:
        # Atomic file write back to secondary output file
        logging.info(f"Writing parsed datasets out to memory cache target: {output_file_path}")
        master_df.to_excel(output_file_path, index=False)
        logging.info(f"[SUCCESS] Script executed cleanly. Rows updated: {rows_updated} | Rows unmapped/skipped: {rows_skipped}")
        return True
    except Exception as e:
        logging.error(f"Failed to export compilation data to target path: {e}")
        return False

if __name__ == "__main__":
    # Runtime Configurations
    CONFIG_MASTER = "master_sheet.xlsx"
    CONFIG_LOOKUP_DIR = "./reference_files"
    CONFIG_OUTPUT = "final_output_master.xlsx"
    
    secure_excel_lookup(CONFIG_MASTER, CONFIG_LOOKUP_DIR, CONFIG_OUTPUT)