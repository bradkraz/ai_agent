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


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
<<<<<<< HEAD
    description="Reads the contents of a file in the relevant working directory",
=======
    description=f"Retrieves the content (at most {MAX_CHARS} characters) of a specified file within the working directory",
>>>>>>> e100a72 (add all declarations, ammend get_file_content name)
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
<<<<<<< HEAD
                description="File path of the given file to read, relative to the working directory (default is the working directory itself)",
=======
                description="Path to the file to read, relative to the working directory",
>>>>>>> e100a72 (add all declarations, ammend get_file_content name)
            ),
        },
        required=["file_path"],
    ),
)
