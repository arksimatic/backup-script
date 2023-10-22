import shutil
import os
import filecmp
import win32com.client

original_path = r'C:\Projects\!Sandbox\from'
destination_path = r'C:\Projects\!Sandbox\to'

def get_dirs_and_files(path):
    dirs = set()
    files = set()
    for file in os.listdir(path):
        full_file_path = os.path.join(path, file)
        if(len(file) > 3 and file[-4:] == '.lnk'): # checking whether file is shortcut
            shell = win32com.client.Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(full_file_path)
            full_file_path = shortcut.Targetpath # replacing .lnk (shortcut) file with original file
        if(os.path.isdir(full_file_path)): # separating files and folders
            dirs.add(full_file_path)
        else:
            files.add(full_file_path)
    return dirs, files

def get_files(path):
    all_files = set()
    dirs, files = get_dirs_and_files(path)
    all_files.update(files)
    for d in dirs:
        files_from_dirs = get_files(d)
        for file in files_from_dirs:
            all_files.add(file)
    return all_files

def copy_file(file_original, file_destination):
    os.makedirs(os.path.dirname(file_destination), exist_ok=True)
    shutil.copy(file_original, file_destination)

def copy_files(from_path, to_path):
    all_files = get_files(from_path)
    for file_original in all_files:
        file_destination = os.path.join(to_path, file_original[0] + file_original[2:]) # cutting ':' from path
        print('file: ' + file_original)
        if(os.path.isfile(file_destination)): # checking if file exists
            if not filecmp.cmp(file_original, file_destination): # checking if files are the same
                print('-COPY (files different)')
                copy_file(file_original, file_destination)
        else:
            print('-COPY (file does not exists)')
            copy_file(file_original, file_destination)

copy_files(original_path, destination_path)