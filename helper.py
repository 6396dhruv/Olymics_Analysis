import numpy as np

def fetch_medal_tally(events_df,year, country):
    medadl_df = events_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag =0
    if year == 'Overall' and country == 'Overall':
        temp_df = medadl_df
    if year == 'Overall' and country != 'Overall':
        flag =1
        temp_df = medadl_df[medadl_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medadl_df[medadl_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medadl_df[(medadl_df['Year'] == year) & (medadl_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending= False).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending= False).reset_index()
        
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x



def medal_tally(events_df):
    medal_tally = events_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally=medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending= False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally

def country_year_list(events_df):
    years = events_df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(events_df['region'].dropna()).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country



def data_over_time(events_df, col):
    nations_participants= events_df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('count')
    nations_participants.rename(columns={'count': col, 'Year': 'country_counts'}, inplace=True)
    return nations_participants


def most_successful(events_df, sport):
    tempdf = events_df.dropna(subset= ['Medal'])

    if sport != 'Overall':
        tempdf = tempdf[tempdf['Sport'] == sport]

    x= tempdf['Name'].value_counts().reset_index().merge(events_df)[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns= {'count': 'Medals'}, inplace= True)
    return x

def yearwise_medal(events_df, country):
    temp_df =events_df.dropna(subset= ['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df= temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    # fig = px.line(final_df, x= 'Year', y= 'Medal')
    # fig.show()
    return final_df

def yearwise_heatmap(events_df, country):
    temp_df = events_df.dropna(subset= ['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index= 'Sport', columns= 'Year', values= 'Medal', aggfunc= 'count').fillna(0)
    return pt

def most_successful_countrywise(events_df, country):
    tempdf = events_df.dropna(subset= ['Medal'])
    tempdf = tempdf[tempdf['region'] == country]

    x= tempdf['Name'].value_counts().reset_index().head(10).merge(events_df)[['Name', 'count', 'Sport']].drop_duplicates('Name')
    x.rename(columns= {'count': 'Medals'}, inplace= True)
    return x

