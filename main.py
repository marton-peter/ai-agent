import os
import sys
from dotenv import load_dotenv
from google import genai

if len(sys.argv) < 2:
    sys.stderr.write("no prompt provided\n")
    sys.exit(1)

if sys.argv[1] == "":
    sys.stderr.write("empty prompt provided\n")
    sys.exit(1)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=sys.argv[1]
)
print(response.text)
print(
    f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
    f"Response tokens: {response.usage_metadata.candidates_token_count}"
)
