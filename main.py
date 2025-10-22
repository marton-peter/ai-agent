import os
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from config import model_name
from config import system_prompt
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

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
)

if verbose: # Print metadata if the verbose argument is present
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if len(response.function_calls) > 0: # Check for called functions and print them
    for call in response.function_calls:
        print(f"Calling function: {call.name}({call.args})")
else:
    print(response.text)

