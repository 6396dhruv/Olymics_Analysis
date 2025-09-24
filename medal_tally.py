import pandas as pd


def preprocess(events_df, region_df):
    # filter for summer olympic
    events_df[events_df['Season'] == 'Summer']
    #merge with region
    events_df= events_df.merge(region_df, on='NOC', how= 'left')
    #dropping duplicates
    events_df.drop_duplicates(inplace = True)
    # one hot encoding models
    events_df = pd.concat([events_df, pd.get_dummies(events_df['Medal']).astype(int)], axis=1)
    
    return events_df
