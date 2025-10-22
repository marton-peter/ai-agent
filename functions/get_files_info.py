import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    fullpath = os.path.abspath(os.path.join(working_directory, directory))
    if not fullpath.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(fullpath):
        return f'Error: "{directory}" is not a directory'
    
    try:
        contents = os.listdir(fullpath)
        results = []

        for item in contents:
            results.append(f" - {item}: file_size={os.path.getsize(os.path.join(fullpath, item))}, is_dir={os.path.isdir(os.path.join(fullpath, item))}")
    
    except Exception as e:
        return f"Error: {e}"

    return "\n".join(results)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)