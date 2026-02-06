import asyncio
from dotenv import load_dotenv
from typing import Any

# Import custom modules
from scraper import scout_website
from analyzer import analyze_with_llm
from utils import load_existing_urls, save_to_excel

load_dotenv()

USE_FREE_MODEL: bool = True 

async def main() -> None:
    target_urls: list[str] = [
        "https://openai.com",
        "https://www.anthropic.com",
        "https://www.spacex.com",
        "https://huggingface.co",
        "https://www.bostondynamics.com", 
        "https://www.nvidia.com"
    ]
    
    # Get old records from the database
    existing_urls: list[str] = load_existing_urls()
    
    # We will store the new collected data here (Dictionary List)
    new_intel_list: list[dict[str, Any]] = []

    print(f"🚀 AuraSight Batch Pipeline Started...")

    for url in target_urls:
        # Duplicate Check 
        if url in existing_urls:
            print(f"⏭️  Already recorded, skipping: {url}")
            continue

        # STEP 1: SCRAPING
        raw_data: str | None = await scout_website(url)
        
        if raw_data:
            # STEP 2: ANALYZING
            intel = analyze_with_llm(raw_data, use_free_model=USE_FREE_MODEL)
            
            if intel: # If the analysis is successful (not None)
                # Convert Pydantic object to dictionary (dict)
                intel_dict = intel.model_dump()
                
                # Extra fields for Excel
                intel_dict["source_url"] = url
                # Convert list to string (to fit in Excel cell)
                intel_dict["key_products"] = ", ".join(intel_dict["key_products"])
                
                new_intel_list.append(intel_dict)
                print(f"✅ Analyzed: {intel.company_name}")
            else:
                print(f"❌ Analysis failed for {url}")
        else:
            print(f"⚠️ Skip (No data): {url}")

    # STEP 3: SAVING
    save_to_excel(new_intel_list)

if __name__ == "__main__":
    asyncio.run(main())