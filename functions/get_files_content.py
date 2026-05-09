import os

from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: file not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content

    except Exception as e:
        return f"Error: {e}"


schema_get_files_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Reads the contents of a file in the relevant working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Reads the content of a file from the given file path, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
