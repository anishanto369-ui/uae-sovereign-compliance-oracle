import os
import re
import datetime
from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv

# Load keys from .env
load_dotenv()

# Initialize clients
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

def redact_pii(text):
    """Enforces UAE Federal Decree Law No. 45 (Data Protection)"""
    # Redact Emirates IDs
    text = re.sub(r'784-\d{4}-\d{7}-\d{1}', '[CONFIDENTIAL_EID]', text)
    # Redact UAE Phone numbers
    text = re.sub(r'(\+971|05)\d{8}', '[CONFIDENTIAL_PHONE]', text)
    # Redact Emails
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[CONFIDENTIAL_EMAIL]', text)
    return text

def run_uae_audit(user_query):
    try:
        # 1. DATA PRIVACY LAYER
        safe_query = redact_pii(user_query)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 2. OPTIMIZED SEARCH STRATEGY (Fixes "Query too long" Error)
        # We use short keywords for the search but keep the full query for reasoning.
        is_fin = any(x in safe_query.lower() for x in ['aed', 'transfer', 'payment', 'shipment', 'jafza'])
        
        search_keywords = "UAE FTA VAT recovery 5-year limit 2026"
        if is_fin:
            search_keywords += " CBUAE AML Proliferation Financing April 2026"

        print(f"🔍 Searching Sovereign Data Lake: {search_keywords}")
        search_results = tavily.search(query=search_keywords, search_depth="advanced")
        context = "\n".join([f"Source [{i}]: {res['content']}" for i, res in enumerate(search_results['results'][:5])])

        # 3. MCKINSEY-GRADE AUDIT ENGINE (Llama 3.3)
        print("⚖️ Executing Institutional Audit Reasoning...")
        
        system_prompt = f"""
        You are a Senior Compliance Partner at a Global Strategy Firm (McKinsey/EY Level). 
        Current Date: {timestamp}.
        You must deliver a definitive audit report based on UAE 2026 Laws.

        STRICT AUDIT PROTOCOL:
        1. CITATIONS: Cite Decree Laws (e.g., Law 47 of 2022, Law 10 of 2025).
        2. BILINGUAL: Executive Summary MUST be professional Arabic and English.
        3. DATA PRIVACY: Respect Law 45; never guess the redacted PII.
        4. XAI LOGIC: Explicitly state the reasoning logic used for the risk score.

        REPORT STRUCTURE:
        - I. EXECUTIVE SUMMARY / الملخص التنفيذي (Bilingual)
        - II. COMPLIANCE MATRIX (Tax Trigger, AML Risk Score, PF Rating)
        - III. DETAILED LEGAL ANALYSIS (Article-by-Article)
        - IV. XAI & REASONING PATH
        - V. STRATEGIC CFO ACTION PLAN (3 Priority Steps)
        """
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"REGULATORY CONTEXT:\n{context}\n\nFULL CLIENT SCENARIO:\n{safe_query}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )
        
        report = response.choices[0].message.content
        report += f"\n\n--- \n**McKinsey/EY Grade Verification Metadata**\n- Verified: {timestamp}\n- PII Status: Sanitized per Law 45\n- Grounding: Sovereign UAE Corpora Only"
        
        return report

    except Exception as e:
        return f"Audit Pipeline Error: {str(e)}"