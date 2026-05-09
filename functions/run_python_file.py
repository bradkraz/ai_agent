import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        python_command = ["python", target_file]
        if args:
            python_command.extend(args)
        python_result = subprocess.run(
            python_command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )
        python_output = []
        if python_result.returncode != 0:
            python_output.append(f"Process exited with code {python_result.returncode}")
        if not python_result.stderr and not python_result.stdout:
            python_output.append("No output produced")
        if python_result.stdout:
            python_output.append(f"STDOUT: {python_result.stdout}")
        if python_result.stderr:
            python_output.append(f"STDERR: {python_result.stderr}")
        return "\n".join(python_output)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"],
    ),
)
