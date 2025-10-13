import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


if len(sys.argv) < 2:
    sys.stderr.write("no prompt provided\n")
    sys.exit(1)

user_prompt = sys.argv[1]
if user_prompt == "":
    sys.stderr.write("empty prompt provided\n")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

verbose = False
if "--verbose" in sys.argv:
    verbose = True

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)
if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

print(response.text)

