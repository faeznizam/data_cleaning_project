import re
import os

def clean_name(folder_path):

    file_names = os.listdir(folder_path)

    for file_name in file_names:

        original_path = os.path.join(folder_path, file_name)

        pattern = r'-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}'
        cleaned_name = re.sub(pattern, '', file_name)

        new_path = os.path.join(folder_path, cleaned_name)

        os.rename(original_path, new_path)

        print(f'Renamed: {file_name} to {cleaned_name}')

