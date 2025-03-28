import os
import sys

import numpy as np

from ethopy.core.logger import stimulus


def list_files(folder_path: str = "objs", file_extension: str = ".egg") -> list:
    """Returns a list of file_extension filenames in the specified folder."""
    try:
        return [f for f in os.listdir(folder_path) if f.endswith(".egg")]
    except FileNotFoundError:
        print("Error: Folder not found.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def store(obj_id, file_path, file_name, description=""):
    """Uploads an object to the stimulus database."""
    tuple = dict(
        obj_id=obj_id,
        description=description,
        object=np.fromfile(file_path + "/" + file_name, dtype=np.int8),
        file_name=file_name,
    )
    stimulus.Objects.insert1(tuple)


def table_exist(table_name, schema=stimulus):
    """Checks if a table exists in the stimulus schema."""
    if table_name not in dir(schema):
        print(f"Table '{table_name}' does not exist in the stimulus schema.")
        return False
    return True


if __name__ == "__main__":
    table_name = "Objects"
    if not table_exist("Objects", schema=stimulus):
        sys.exit(1)

    # Example usage
    folder_path = "objs"
    egg_files = list_files(folder_path)
    print(egg_files)

    obj_ids = stimulus.Objects.fetch("obj_id")
    if len(obj_ids) == 0:
        max_obj_id = 0
    else:
        max_obj_id = max(obj_ids)
        print(f"Max obj_id: {max_obj_id}")

    for i, file in enumerate(egg_files):
        store(max_obj_id + 1 + i, folder_path, file)
