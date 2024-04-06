def check_email(email):
    if email == 'noemail@unicef.org':
        return ''
    else:
        return email
    

def rename_column(df):
    df.rename(columns = {'Email' : 'Original Email'}, inplace=True)

    return df

