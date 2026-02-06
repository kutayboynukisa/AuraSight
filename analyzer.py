import os
import instructor
from litellm import completion
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# --- SCHEMA DEFINITION ---
class CompanyIntel(BaseModel):
    company_name: str = Field(..., description="Full name of the company")
    short_summary: str = Field(..., description="2-sentence summary of what they do")
    key_products: list[str] = Field(..., description="List of key products or services")
    target_audience: str = Field(..., description="Who are they selling to?")
    hiring_status: bool = Field(..., description="True if they are hiring, else False")

# --- AI LOGIC ---
def analyze_with_llm(markdown_content: str, use_free_model: bool = True) -> CompanyIntel | None:
    """
    Takes Markdown content, analyzes it with LLM, and 
    returns a structured CompanyIntel object (or None).
    """
    print(f"🧠 [AuraSight] Analyzing intelligence (Free Mode: {use_free_model})...")
    
    model_name: str
    if use_free_model:
        client = instructor.from_litellm(completion, mode=instructor.Mode.MD_JSON)
        model_name = "openrouter/arcee-ai/trinity-large-preview:free"
    else:
        client = instructor.from_litellm(completion)
        model_name = "openrouter/anthropic/claude-3.5-sonnet"

    try:
        resp = client.chat.completions.create(
            model=model_name,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            response_model=CompanyIntel, 
            messages=[
                {"role": "system", "content": "You are a strategic business analyst."},
                {"role": "user", "content": f"Analyze this website content:\n\n{markdown_content}"}
            ],
        )
        return resp
        
    except Exception as e:
        print(f"⚠️ Model Error ({model_name}): {e}")
        return None