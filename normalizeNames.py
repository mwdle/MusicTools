import os
import argparse

illegal_chars = {'?', ':', '"', '*', '!'}

def rename_item(root, old_path, new_name):
    new_path = os.path.join(root, new_name)
    if old_path != new_path:
        os.rename(old_path, new_path)
        print(f'Renamed item: {old_path} -> {new_path}')

def replace_colon(old_name, illegal_char):
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

# You can implement custom logic here for handling specific illegal characters.
def repair_illegal_name(old_name, illegal_chars):
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

def rename_folders(root_folder):
    for root, dirnames, _ in os.walk(root_folder):
        for dirname in dirnames:
            if any(illegal_char in dirname for illegal_char in illegal_chars) or dirname.endswith('.'):
                new_dirname = repair_illegal_name(dirname, illegal_chars)
                rename_item(root, os.path.join(root, dirname), new_dirname)

def rename_files(root_folder):
    for root, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if any(illegal_char in filename for illegal_char in illegal_chars) or filename.endswith('.'):
                new_name = repair_illegal_name(filename, illegal_chars)
                rename_item(root, os.path.join(root, filename), new_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script allows you to quickly and easily replace or remove 'illegal' characters from filenames and foldernames in a specific a folder and subfolders that break sync compatibility between devices using different filesystem conventions. A practical use of this application is bulk renaming stored music folders/files to enable portability and syncing of a music library across devices without file system compatibility issues. This program does *NOT* modify music metadata, just filenames/foldernames. By default, this application will intelligently replace colons ':' with dashes '-' and proper surrounding spacing, replace quotation marks '\"' with single quotes ', remove trailing periods '.', and remove any other characters defined in the illegal characters list at the top of the normalizeNames.py file. All of the aforementioned behavior can be easily overridden/modified in the repair_illegal_name() method and illegal characters list. All renames will be printed to the console.")
    parser.add_argument('root_folder', type=str, help="Path to folder containing music/subfolders to repair names in.")
    args = parser.parse_args()
    rename_files(args.root_folder)
    rename_folders(args.root_folder)
    print("Finished! Exiting . . .")