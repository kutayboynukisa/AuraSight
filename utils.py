import os
import pandas as pd
from typing import Any # Since Pandas types are complex, sometimes Any may be required.

FILE_NAME = "strategic_report.xlsx"

def load_existing_urls() -> list[str]:
    """
    Checks the Excel file and returns a list of previously scanned URLs.
    """
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_excel(FILE_NAME)
            if "source_url" in df.columns:
                print(f"📂 Database loaded. {len(df)} sites already recorded.")
                return df["source_url"].astype(str).tolist()
        except Exception as e:
            print(f"⚠️ Error reading Excel: {e}")
    
    return []

def save_to_excel(new_data: list[dict[str, Any]]) -> None:
    """
    Appends new data (dictionary list) to the Excel database.
    Returns nothing (None).
    """
    if not new_data:
        print("\n✨ No new data to add.")
        return

    new_df = pd.DataFrame(new_data)
    
    if os.path.exists(FILE_NAME):
        existing_df = pd.read_excel(FILE_NAME)
        final_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        final_df = new_df
        
    final_df.to_excel(FILE_NAME, index=False)
    print("="*50)
    print(f"💾 {len(new_data)} new records added. Total: {len(final_df)}")
    print("="*50)