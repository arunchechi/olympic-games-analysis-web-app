import numpy as np
import pandas as pd


# Function 1
# fetching the lists required for the drop-down menus
def country_year_list(df):

    # list of years
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    # list of countries
    country = np.unique(df["region"].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


# Function 2
# fetching the medal tally required in diff cases
def fetch_medal_tally(df, year, country):

    # considering a single medal for team games like hockey
    medal_df = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    # preparing the required tables for diff cases
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) &
                           (medal_df['region'] == country)]

    # performing groupby to find the number of medals
    if flag == 1:
        x = temp_df.groupby('Year').sum()[
            ['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    # finding the total number of medals
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    # removing the unnecessary decimal part
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


# Function 3
# fetching the number of participating nations or events or athletes over time
def data_over_time(df, col):

    # calculating the number of nations or events or athletes in each edition
    nations_over_time = df.drop_duplicates(
        ['Year', col])['Year'].value_counts().reset_index().sort_values('Year')

    # renaming col names appropriately for graphs
    nations_over_time.rename(
        columns={'Year': 'Edition', 'count': col}, inplace=True)

    return nations_over_time


# Function 4
# fetching the most successful player in each sport
def most_successful(df, sport):

    # removing players with no medals
    temp_df = df.dropna(subset=['Medal'])

    # filtering for specific sports if selected by the user
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # finding the athletes with most number of medals
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')

    # renaming col names appropriately
    x.rename(columns={'count': 'No of Medals',
             'region': 'Country'}, inplace=True)

    return x

# Function 5
# fetching the count of medals by a country over the years
def yearwise_medal_tally(df, country):

    # removing players with no medal
    temp_df = df.dropna(subset=['Medal'])

    # considering a single medal for team games like hockey
    temp_df.drop_duplicates(subset=[
                            'Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    # caculating the number of medals over the years
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


# Function 6
# fetching the required pivot table for a heatmap
def country_event_heatmap(df, country):

    # removing players with no medal
    temp_df = df.dropna(subset=['Medal'])

    # considering a single medal for team games like hockey
    temp_df.drop_duplicates(subset=[
                            'Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    # creating the required pivot table
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year',
                            values='Medal', aggfunc='count').fillna(0)

    return pt


# Function 7
# fetching the most successful players in a country
def most_successful_countrywise(df, country):

    # removing players with no medal
    temp_df = df.dropna(subset=['Medal'])

    # filtering for the selected country
    temp_df = temp_df[temp_df['region'] == country]

    # finding the athletes with most number of medals
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(
        df, on='Name', how='left')[['Name', 'count', 'Sport']].drop_duplicates('Name')

    # renaming col names appropriately
    x.rename(columns={'count': 'No of Medals'}, inplace=True)

    return x

