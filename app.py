import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# loading the datasets
df = pd.read_csv("athletes_data.csv")
region_df = pd.read_csv("regions_data.csv")

# pre-processing the data
df = preprocessor.preprocess(df, region_df)

# web page title and logo
st.sidebar.title("Olympic Games Analysis")
st.sidebar.image(
    'https://cdn.britannica.com/01/23901-050-33507FA4/flag-Olympic-Games.jpg')

# web page main menu
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis',
     'Country-wise Analysis')
)


# on selecting 'Medal Tally' from the main menu
if user_menu == 'Medal Tally':

    # placing the sidebar title
    st.sidebar.header("Medal Tally")

    # placing the drop-down menus in the sidebar
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    # placing the page title for different cases
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medal Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s performance in " +
                 str(selected_year) + " Olympics")

    # placing the medal tally for different cases
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    st.table(medal_tally)


# on selecting 'Overall Analysis' from the main menu
if user_menu == 'Overall Analysis':

    # placing the page title
    st.title("Top Statistics")

    # placing top statistics in two rows
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    # giving a space before placing the next part
    st.markdown("<br><br>", unsafe_allow_html=True)

    # placing a line chart showing number of participating nations over time
    nations_over_time = helper.data_over_time(df, "region")
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Number of Participating Nations over the years")
    st.plotly_chart(fig)

    # placing a line chart showing number of events  over time
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Number of Events over the years")
    st.plotly_chart(fig)

    # placing a line chart showing number of athletes over time
    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Number of Athletes over the years")
    st.plotly_chart(fig)

    # placing a heatmap showing number of events in each sport over time
    st.title("No. of Events in Each Sport over the years")
    fig, ax = plt.subplots(figsize=(25, 25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                     annot=True)
    st.pyplot(fig)

    # placing a table showing the most successful athletes
    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)


# on selecting 'Country-wise Analysis' from the main menu
if user_menu == 'Country-wise Analysis':

    # placing the sidebar heading
    st.sidebar.title('Country-wise Analysis')

    # placing a drop-down menu in the sidebar to select country
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    # placing a line chart showing year-wise performance of the selected country
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + "'s Medal Tally over the years")
    st.plotly_chart(fig)

    # placing a heatmap showing the sports in which the selected country excels
    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    if pt.size == 0:
        st.subheader(
            "Unable to show as this country hasn't won any medals ever!")
    else:
        ax = sns.heatmap(pt, annot=True)
        plt.show()
        fig, ax = plt.subplots(figsize=(25, 25))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)

    # placing a table showing top 10 athetes of the selected country
    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

# THE END
