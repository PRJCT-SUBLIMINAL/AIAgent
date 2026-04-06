import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    combined_path = os.path.join(abs_working_dir, file_path)
    norm_file_path = os.path.normpath(combined_path)
    common_path = os.path.commonpath([abs_working_dir, norm_file_path])
    try:
        if common_path != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
        if os.path.isdir(norm_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(norm_file_path), exist_ok=True)

        with open(norm_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a text file based on the input.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to create.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content you wish to write",
            ),
        },
        required=["file_path", "content"],
    ),
)