import os

def get_files_info(working_directory, directory="."):
    absolute_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_path, directory))
    is_valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

    if is_valid_target_dir == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    is_dir = os.path.isdir(target_dir)

    if is_dir == False:
        return f'Error: "{directory}" is not a directory'

    string = ""
    try:
        items = os.listdir(target_dir)
    except:
        return "Error: No permission to view contents of this directory."

    for item in items:
        item_path = os.path.join(target_dir, item)

        try:
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
        except:
            return f"Error: coudn't get size of file/directory {item_path}"
        
        string += f"- {item}: file_size={size} bytes, is_dir={is_dir}\n"
    
    return string