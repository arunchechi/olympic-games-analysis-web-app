import pandas as pd

def preprocess(df,region_df):
    
    # filtering for the summer olympics
    df = df[df['Season'] == 'Summer']

    # fetching the country names
    df = df.merge(region_df,on='NOC',how='left')

    # dropping the duplicate rows
    df.drop_duplicates(inplace=True)

    # one-hot encoding the medals column
    df = pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    
    return df