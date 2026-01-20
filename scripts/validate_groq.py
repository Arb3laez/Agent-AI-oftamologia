
import os
import time
import json
import sys
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

def validate_groq():
    """
    Validates Groq API connectivity, response, and latency.
    """
    print("="*60)
    print(" GROQ API VALIDATION SCRIPT")
    print("="*60)

    # 1. Check API Key
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print(" ERROR: GROQ_API_KEY not found in environment variables.")
        print("Please ensure .env file exists and contains GROQ_API_KEY.")
        sys.exit(1)
    
    print(f"✓ API Key found: {api_key[:8]}...{api_key[-4:]}")

    # 2. Initialize Client
    try:
        client = Groq(api_key=api_key)
        print("✓ Groq Client initialized")
    except Exception as e:
        print(f" ERROR: Failed to initialize Groq client: {e}")
        sys.exit(1)

    # 3. Make Test Call
    model = "llama-3.3-70b-versatile"
    prompt = "Responde con un JSON que tenga el campo 'status'='ok' y 'message'='Groq conected'."
    
    print(f"Testing connectivity with model: {model}...")
    
    start_time = time.time()
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful API validator. Output JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=100,
            response_format={"type": "json_object"}
        )
        end_time = time.time()
        
        latency_ms = (end_time - start_time) * 1000
        content = completion.choices[0].message.content
        
        print(f"✓ Response received in {latency_ms:.2f}ms")
        
        # 4. Validate Response
        try:
            data = json.loads(content)
            print("✓ Response is valid JSON")
            print(f"  Response content: {json.dumps(data, indent=2)}")
            
            result = {
                "status": "PASS",
                "latency_ms": round(latency_ms, 2),
                "model": model,
                "api_check": "OK"
            }
            
        except json.JSONDecodeError:
            print(" WARNING: Response is not valid JSON, but connection worked.")
            print(f"  Raw content: {content}")
            result = {
                "status": "PASS_WITH_WARNING",
                "latency_ms": round(latency_ms, 2),
                "model": model,
                "api_check": "JSON_PARSE_ERROR"
            }

    except Exception as e:
        print(f" ERROR: API Call failed: {e}")
        result = {
            "status": "FAIL",
            "error": str(e)
        }
        sys.exit(1)

    print("-" * 60)
    print("  VALIDATION REPORT")
    print("-" * 60)
    print(json.dumps(result, indent=2))
    print("=" * 60)

if __name__ == "__main__":
    validate_groq()
