import os
from config import char_limit
from google.genai import types

def get_file_content(working_directory, file_path):
    fullpath = os.path.abspath(os.path.join(working_directory, file_path))
    if not fullpath.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(fullpath):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(fullpath, "r") as f:
            file_content_string = f.read(char_limit)
            if len(file_content_string) == char_limit:
                truncation = f'[...File "{file_path}" truncated at {char_limit} characters]'
                file_content_string += truncation

    except Exception as e:
        return f"Error: {e}"
    
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of the specified file up to the preset character limit, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the specific file, relative to the working directory.",
            ),
        },
    ),
)