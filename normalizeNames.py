import os
import argparse

ILLEGAL_CHARS = {'?', ':', '"', '*', '!'}
"""
Characters that must be replaced / removed from file/folder names in the given directory.
"""

def rename_item(root, old_path, new_name):
    """
    Renames a file or folder and prints the change to the console.
    """
    new_path = os.path.join(root, new_name)
    if old_path != new_path:
        os.rename(old_path, new_path)
        print(f'Renamed item: {old_path} -> {new_path}')

def replace_colon(old_name, illegal_char):
    """
    Custom logic for replacing a colon ':' with a dash '-' in a file/folder name. 
    If the colon is next to a space on only one side, when it is replaced with a dash a space is added to the opposite side for a more natural look.
    If there are already spaces on both sides of the colon, no spaces are added or removed.
    If there are no spaces on either side of the colon, no spaces are added.
    """
    new_name = old_name
    preceding_char = old_name.index(illegal_char)-1
    succeeding_char = old_name.index(illegal_char)+1
    if preceding_char < len(old_name) and preceding_char >= 0 and old_name[preceding_char] != ' ':
        if succeeding_char < len(old_name) and succeeding_char >= 0 and old_name[succeeding_char] != ' ':
            new_name = new_name.replace(illegal_char, '-')
        else: new_name = new_name.replace(illegal_char, ' -')
    elif succeeding_char < len(old_name) and succeeding_char >= 0 and old_name[succeeding_char] != ' ':
        new_name = new_name.replace(illegal_char, '- ')
    else: new_name = new_name.replace(illegal_char, '-')
    return new_name

def repair_illegal_name(old_name, illegal_chars):
    """
    Given a name and a list of illegal characters, each character found in the name is replaced or removed according to the logic below.
    Custom logic for a specific character can be added below.
    """
    new_name = old_name
    for illegal_char in illegal_chars:
        if illegal_char in old_name:
            if illegal_char == ':':
                new_name = replace_colon(old_name, illegal_char)
            elif illegal_char == '"':
                new_name = new_name.replace(illegal_char, "'")
            else:
                new_name = new_name.replace(illegal_char, '')
    if new_name.endswith("..."):
        new_name = new_name[:-3]
    if new_name.endswith('.'):
        new_name = new_name[:-1]
    return new_name

def repair_folder_names(root_folder):
    """
    Repair all folders with 'illegal' names found in the given folder and subfolders. Replaces names according to the logic in repair_illegal_name().
    """
    for root, dirnames, _ in os.walk(root_folder):
        for dirname in dirnames:
            if any(illegal_char in dirname for illegal_char in ILLEGAL_CHARS) or dirname.endswith('.'):
                new_dirname = repair_illegal_name(dirname, ILLEGAL_CHARS)
                rename_item(root, os.path.join(root, dirname), new_dirname)

def repair_file_names(root_folder):
    """
    Repair all filenames with 'illegal' names found in the given folder and subfolders. Replaces names according to the logic in repair_illegal_name().
    """
    for root, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if any(illegal_char in filename for illegal_char in ILLEGAL_CHARS) or filename.endswith('.'):
                new_name = repair_illegal_name(filename, ILLEGAL_CHARS)
                rename_item(root, os.path.join(root, filename), new_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script allows you to quickly and easily replace or remove 'illegal' characters from filenames and foldernames in a given folder and subfolders that break sync compatibility between devices using different filesystem conventions. A practical use of this application is bulk renaming stored music folders/files to enable portability and syncing of a music library across devices. This program does *NOT* modify music metadata, just filenames/foldernames. By default, this application will intelligently replace colons ':' with dashes '-' and proper surrounding spacing, replace quotation marks '\"' with single quotes ', remove trailing periods '.', and remove any other characters defined in the illegal characters list at the top of the normalizeNames.py file. All of the aforementioned behavior can be easily overridden/modified in the repair_illegal_name() method and illegal characters list. All changes are printed to the console.")
    parser.add_argument('root_folder', type=str, help="Path to folder containing music/subfolders to repair names in.")
    args = parser.parse_args()
    repair_file_names(args.root_folder)
    repair_folder_names(args.root_folder)
    print("Finished! Exiting . . .")