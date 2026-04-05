from google import genai
from dotenv import load_dotenv
import os
import json

# Load API key from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if API key loaded
if not GEMINI_API_KEY:
    print("❌ API Key not loaded! Check .env file.")
else:
    print("✅ API Key loaded successfully")


def analyze_transcript(transcript_text):
    """
    Reads the transcript and extracts:
    - Pain Points
    - Current Tech Stack
    - Desired Outcome
    """

    # Configure Gemini client
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Prompt for Gemini
    prompt = f"""
You are a Technical Sales Engineer.

Read this client meeting transcript carefully.

Extract ONLY the following information in JSON format:

{{
    "pain_points": ["list each pain point as a separate item"],
    "current_tech_stack": ["list each tool or system separately"],
    "desired_outcome": "one clear sentence describing what they want"
}}

IMPORTANT RULES:
- Return ONLY JSON
- No markdown
- No extra text
- No backticks

Transcript:
{transcript_text}
"""

    print("Analyzing transcript with Gemini...")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",   # ✅ Stable model
            contents=prompt
        )

        # Clean response
        raw = response.text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        # Convert JSON text to dictionary
        client_info = json.loads(raw)

        print("✅ Transcript analyzed successfully!")
        print(f"Pain Points found: {len(client_info['pain_points'])}")
        print(f"Tech Stack found: {len(client_info['current_tech_stack'])}")

        return client_info

    except Exception as e:
        print("❌ Error occurred:")
        print(e)
        return None


# TEST RUN
if __name__ == "__main__":

    try:
        # Read transcript file
        with open("transcripts/sample_transcript.txt", "r") as f:
            transcript = f.read()

        # Run analyzer
        result = analyze_transcript(transcript)

        # Print result
        if result:
            print("\n--- EXTRACTED INFO ---")
            print(json.dumps(result, indent=2))

    except FileNotFoundError:
        print("❌ transcript file not found!")