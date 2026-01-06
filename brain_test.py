import os
from dotenv import load_dotenv
from google import genai

# 1. Load the secret key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Initialize the client
client = genai.Client(api_key=api_key)
# Try this model from your list - it's fast and usually has open quota
model_id = "models/gemma-3-27b-it"


try:
    print("--- Jeeves is waking up... ---")
    response = client.models.generate_content(
        model=model_id,
        contents="Give me a 1-sentence sarcastic but helpful tip for a student who wants to save money but just bought 4 pairs of luxury sneakers."
    )
    print("\n--- Jeeves says: ---")
    print(response.text)
    
except Exception as e:
    print(f"\n❌ Error: {e}")