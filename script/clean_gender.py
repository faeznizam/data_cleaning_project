import re

def gender_by_national_id(df):
  # match pattern
  national_id_pattern = re.compile(r'^\d{6}-\d{2}-\d{4}$')

  # function to determine gender by last digit in national id
  def determine_gender(national_id):
    return 'Female' if int(national_id[-1]) % 2 == 0 else 'Male'

  df['Gender'] = df['National ID'].apply(lambda x: determine_gender(x) if x and national_id_pattern.match(x) else '')

  return df

def rename_column(df):
    df.rename(columns = {'Gender' : 'sescore__Gender__c'}, inplace=True)

    return df