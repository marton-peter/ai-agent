import os
from config import char_limit

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