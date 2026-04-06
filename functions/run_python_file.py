import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:

        abs_working_dir = os.path.abspath(working_directory)
        combined_path = os.path.join(abs_working_dir, file_path)
        norm_file_path = os.path.normpath(combined_path)
        common_path = os.path.commonpath([abs_working_dir, norm_file_path])

        if common_path != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isfile(norm_file_path) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        is_python_file = file_path.endswith(".py")
        if not is_python_file:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", norm_file_path]

        if args is not None:
            command.extend(args)

        result = subprocess.run(command, cwd=abs_working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        returncode = result.returncode
        stdout = result.stdout
        stderr = result.stderr

        output = []
        if returncode != 0:
            output.append(f"Process exited with code {returncode}")

        if stdout == "" and stderr == "":
            output.append("No output produced")
        
        if stdout != "":
            output.append(f"STDOUT: {stdout}")

        if stderr != "":
            output.append(f"STDERR: {stderr}")

        return "\n".join(output)

    except Exception as e:
        return f'Error: executing Python file: {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specific python file based on the input.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to get the file content from.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments to pass to the Python script.",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
        required=["file_path"],
    ),
)