import os

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