# import from sub files
from script import clean_gender
from script import clean_icnumber
from script import clean_birthdate
from script import clean_email
from script import clean_ethnic
from script import clean_phone_number
from script import clean_file_name

# import from module
import pandas as pd
import os
import warnings
from datetime import datetime


def create_file_path(folder_path, file):
    return os.path.join(folder_path, file)

def create_date_format():
    current_date = datetime.now()
    date_format = current_date.strftime('%Y-%m-%d')
    return date_format

def rename_file(file, date_format):
    extract_filename = file[:-5]
    new_file_name = f'{extract_filename}_{date_format}.xlsx'
    return new_file_name

def save_file(folder_path, new_file_name, df):
    file_path = os.path.join(folder_path, new_file_name)
    df.to_excel(file_path, index=False)
    print(f'{new_file_name} has been saved in the folder!')

def convert_date_format(df):
    df['Created Date'] = pd.to_datetime(df['Created Date'], format='%d/%m/%Y')
    df['Created Date'] = df['Created Date'].dt.strftime('%Y-%m-%d')

    return df

def main():
    # filter warning 
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    year = '2024'
    month = 'Apr'
    day = '01'

    # folder path
    folder_path = rf'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Data Cleaning\{year}\{month}\{day}'

    clean_file_name.clean_name(folder_path)

    date_format = create_date_format()

    for file in os.listdir(folder_path):

        if 'Donor With Invalid Email.xlsx' in file:
            file_path = create_file_path(folder_path, file)
            df = pd.read_excel(file_path)

            df = clean_email.rename_column(df)
            df['Email'] = df['Original Email'].apply(clean_email.check_email)
            df['npe01__HomeEmail__c'] = df['Original Email'].apply(clean_email.check_email)
            df['npe01__Preferred_Email__c'] = df['Original Email'].apply(clean_email.check_email)
            df['npe01__WorkEmail__c'] = df['Original Email'].apply(clean_email.check_email)
            df['Date'] = create_date_format()

            date_format = create_date_format()
            df = convert_date_format(df)
            new_file_name = rename_file(file, date_format)
            save_file(folder_path, new_file_name, df)

        elif 'Donor With Invalid IC.xlsx' in file:
            file_path = create_file_path(folder_path, file)
            df = pd.read_excel(file_path, dtype = {'National ID': str})

            df['Updated National ID'] = df['National ID'].apply(clean_icnumber.validate_nat_id)
            df = clean_icnumber.blank_invalid_ic(df)
            df = clean_icnumber.rename_column(df)
            df['Date'] = create_date_format()

            date_format = create_date_format()
            df = convert_date_format(df)
            new_file_name = rename_file(file, date_format)
            save_file(folder_path, new_file_name, df)

        elif 'Donor With Invalid Phone Number.xlsx' in file:
            file_path = create_file_path(folder_path, file)
            df = pd.read_excel(file_path)

            df = clean_phone_number.process_mobile_numbers(df)
            df = clean_phone_number.rename_column(df)
            df['Date'] = create_date_format()

            date_format = create_date_format()
            df = convert_date_format(df)
            new_file_name = rename_file(file, date_format)
            save_file(folder_path, new_file_name, df)

        elif 'Donor Without Age and Birthdate.xlsx' in file:
            file_path = create_file_path(folder_path, file)
            df = pd.read_excel(file_path, dtype = {'National ID': str})

            df['National ID'] = df['National ID'].apply(clean_birthdate.validate_nat_id)
            df['Birthdate'] = df['National ID'].apply(clean_birthdate.calculate_birthdate)
            df['Age'] = df['Birthdate'].apply(clean_birthdate.calculate_age)
            df['Date'] = create_date_format()

            date_format = create_date_format()
            df = convert_date_format(df)
            new_file_name = rename_file(file, date_format)
            save_file(folder_path, new_file_name, df)
            
        elif 'Donor Without Ethnic.xlsx' in file:
            file_path = create_file_path(folder_path, file)
            df = pd.read_excel(file_path)

            df['Ethnic'] = df['Full Name'].apply(clean_ethnic.categorize_ethnic)
            df = clean_ethnic.rename_column(df)
            df['Date'] = create_date_format()
            
            date_format = create_date_format()
            df = convert_date_format(df)
            new_file_name = rename_file(file, date_format)
            save_file(folder_path, new_file_name, df)

        elif 'Donor Without Gender.xlsx' in file:
            file_path = create_file_path(folder_path, file)
            df = pd.read_excel(file_path, dtype = {'National ID': str})

            df['National ID'] = df['National ID'].apply(clean_icnumber.validate_nat_id)
            df = clean_gender.gender_by_national_id(df)
            df = clean_gender.rename_column(df)
            df['Date'] = create_date_format()

            date_format = create_date_format()
            df = convert_date_format(df)
            new_file_name = rename_file(file, date_format)
            save_file(folder_path, new_file_name, df)

        else:
            pass

if __name__ == '__main__':
    main()





