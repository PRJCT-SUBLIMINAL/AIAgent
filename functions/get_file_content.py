import os
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    combined_path = os.path.join(abs_working_dir, file_path)
    norm_file_path = os.path.normpath(combined_path)
    common_path = os.path.commonpath([abs_working_dir, norm_file_path])
    try:
        if common_path != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(norm_file_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(norm_file_path, "r") as f:
            file_content_string = f.read(10000)
            content = file_content_string

            if f.read(1):
                content += f'[...File "{file_path}" truncated at 10000 characters]'

            return content
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a specified file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to get the file content from.",
            ),
        },
        required=["file_path"],
    ),
)