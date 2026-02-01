import asyncio
import os
import pandas as pd
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler

# LLM and Structured Output Libraries
import instructor
from litellm import completion
from pydantic import BaseModel, Field

# 1. SETUP: Load environment variables
load_dotenv()

# --- CONFIGURATION ---
USE_FREE_MODEL = True 

# --- SCHEMA ---
class CompanyIntel(BaseModel):
    company_name: str = Field(..., description="Full name of the company")
    short_summary: str = Field(..., description="2-sentence summary of what the company does")
    key_products: list[str] = Field(..., description="List of key products or services offered by the company")
    target_audience: str = Field(..., description="Who are these products for? (e.g., Developers, Enterprise, Students)")
    hiring_status: bool = Field(..., description="Is the company currently hiring? (Infer from careers page)")

# --- THE BRAIN (LLM Analysis) ---
def analyze_with_llm(markdown_content: str) -> CompanyIntel:
    print(f"🧠 [AuraSight] Analyzing intelligence (Free Mode: {USE_FREE_MODEL})...")
    
    if USE_FREE_MODEL:
        # Manual Mode (Required for Free models that don't support native Tool Use)
        client = instructor.from_litellm(completion, mode=instructor.Mode.MD_JSON)
        
        # STRONG & FREE MODEL SELECTION
        # We need a capable model for complex sites like NVIDIA.
               
        model_name = "openrouter/arcee-ai/trinity-large-preview:free"
        
    else:
        # Premium Mode (Production)
        client = instructor.from_litellm(completion)
        model_name = "openrouter/anthropic/claude-3.5-sonnet"

    try:
        resp = client.chat.completions.create(
            model=model_name,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            response_model=CompanyIntel,
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert tech analyst. You MUST return valid JSON matching the schema."
                },
                {
                    "role": "user", 
                    "content": f"Analyze this content:\n\n{markdown_content}"
                }
            ],
        )
        return resp
    except Exception as e:
        print(f"⚠️ Model Error ({model_name}): {e}")
        # Return None to prevent the pipeline from crashing
        return None

# --- THE SCOUT (Web Scraper) ---
async def scout_website(url: str):
    print(f"🕵️  [AuraSight] Scouting target: {url}...")
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun(url=url)
        if result.success:
            return result.markdown
        print(f"❌ Failed to scout {url}: {result.error_message}")
        return None

# --- MAIN FLOW (Pipeline) ---
async def main():
    target_urls = [
       
        "https://openai.com",
        "https://www.google.com",
        "https://www.spacex.com",
        "https://www.apple.com",
        "https://www.amazon.com",
        "https://www.aboutamazon.com",
        "https://about.netflix.com/en"
    ]
    
    file_name = "strategic_report.xlsx"
    
    # 1. CHECK EXISTING DATABASE (Prevent Duplicates)
    existing_urls = []
    if os.path.exists(file_name):
        try:
            existing_df = pd.read_excel(file_name)
            if "source_url" in existing_df.columns:
                existing_urls = existing_df["source_url"].tolist()
            print(f"📂 Database loaded. {len(existing_urls)} sites already recorded.")
        except Exception as e:
            print(f"⚠️ Error reading Excel, creating a new file: {e}")

    new_intel_list = []
    print(f"🚀 AuraSight Batch Pipeline Started...")

    for url in target_urls:
        # CHECK: Is this URL already in our database?
        if url in existing_urls:
            print(f"⏭️  Already recorded, skipping: {url}")
            continue

        # If not, start processing
        raw_data = await scout_website(url)
        
        if raw_data:
            intel = analyze_with_llm(raw_data)
            
            if intel: # If analysis was successful
                intel_dict = intel.model_dump()
                intel_dict["source_url"] = url
                # Convert list to string for Excel compatibility
                intel_dict["key_products"] = ", ".join(intel_dict["key_products"])
                
                new_intel_list.append(intel_dict)
                print(f"✅ Analyzed & Added: {intel.company_name}")
            else:
                print(f"❌ Analysis failed for {url} (JSON error or Rate Limit)")
        else:
            print(f"⚠️ Skip: {url}")

    # 3. SAVE TO EXCEL
    if new_intel_list:
        new_df = pd.DataFrame(new_intel_list)
        
        if os.path.exists(file_name):
            # Load existing data and append new data
            existing_df = pd.read_excel(file_name)
            final_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            # Create new file
            final_df = new_df
            
        final_df.to_excel(file_name, index=False)
        print("="*50)
        print(f"💾 {len(new_intel_list)} new records added. Total records: {len(final_df)}")
        print("="*50)
        print(new_df[["company_name", "hiring_status"]])
    else:
        print("\n✨ No new data to add (All targets are already recorded).")

if __name__ == "__main__":
    asyncio.run(main())