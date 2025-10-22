import os
from google.genai import types

def write_file(working_directory, file_path, content):
    fullpath = os.path.abspath(os.path.join(working_directory, file_path))
    if not fullpath.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        if not os.path.exists(os.path.dirname(fullpath)):
            os.makedirs(os.path.dirname(fullpath))
        
        with open(fullpath, "w") as f:
            f.write(content)

    except Exception as e:
        return f"Error: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content into the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the specific file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The exact content to be written into the file.",
            )
        },
    ),
)