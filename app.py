import streamlit as st
import pandas as pd
import medal_tally, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

events_df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")


events_df = medal_tally.preprocess(events_df, region_df)

st.sidebar.title("Olympic Analysis")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete-Wise Analysis')
)



# st.dataframe(events_df)

if user_menu =='Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(events_df)

    select_years = st.sidebar.selectbox("Select Years", years)
    select_country = st.sidebar.selectbox("Select Country", country)
    
    medal_tally = helper.fetch_medal_tally(events_df, select_years, select_country)
    if select_years == 'Overall' and select_country== 'Overall':
        st.title("Overall Tally")
    if select_years == 'Overall' and select_country != 'Overall':
        st.title(f"Overall performance of {select_country} country")
    if select_years != 'Overall' and select_country == 'Overall':
        st.title(f"Medal Tally in {select_years} Olympics")
    if select_years != 'Overall' and select_country != 'Overall':
        st.title(f"{select_country} performance in {select_years} Olympics")
    # st.dataframe(medal_tally)
    st.table(medal_tally)




if user_menu == 'Overall Analysis':
    editions =events_df['Year'].unique().shape[0]-1
    cities= events_df['City'].unique().shape[0]
    sports = events_df['Sport'].unique().shape[0]
    events= events_df['Event'].unique().shape[0]
    athletes= events_df['Name'].unique().shape[0]
    nations= events_df['region'].unique().shape[0]

    st.title("Overall Statistics")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1,col2,col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_participants = helper.data_over_time(events_df, 'region')
    fig = px.line(nations_participants, x= 'region', y='country_counts')
    st.title("Participating nations over the years ")
    st.plotly_chart(fig)

    events_held = helper.data_over_time(events_df, 'Event')
    fig = px.line(events_held, x= 'Event', y='country_counts')
    st.title("Events held over the years ")
    st.plotly_chart(fig)

    events_held = helper.data_over_time(events_df, 'Name')
    fig = px.line(events_held, x= 'Name', y='country_counts')
    st.title("Athelete over the years ")
    st.plotly_chart(fig)

    st.title("Number of events over time(Every Sport)")
    fig,ax = plt.subplots(figsize= (20, 20))
    x = events_df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax= sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)

    st.pyplot(fig)

    st.title("Most Successful Athlete")
    sports_list = events_df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')
    selected_sport= st.selectbox('Select a sport', sports_list)
    x = helper.most_successful(events_df, selected_sport)
    st.table(x)

if user_menu == 'Country-Wise Analysis':

    st.sidebar.title("Country-Wise Ananlysis")

    country_list = events_df['region'].dropna().unique().tolist()
    country_list.sort()

    select_country= st.sidebar.selectbox("Select a country", country_list)

    country_df = helper.yearwise_medal(events_df, select_country)
    fig = px.line(country_df, x= 'Year', y= 'Medal')
    st.title(select_country + " Medal tally over the years")
    st.plotly_chart(fig)

    st.title(select_country + " in the following sports")

    pt = helper.yearwise_heatmap(events_df, select_country)
    fig, ax = plt.subplots(figsize= (20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title(f"Top 10 Athlete of {select_country}")
    top10_df = helper.most_successful_countrywise(events_df, select_country)
    st.table(top10_df)
    

if user_menu == 'Athlete-Wise Analysis':
    athlete_df= events_df.drop_duplicates(subset =['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4], ['Overall Age','Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height= 600)
    
    st.title("Distribution of age")

    st.plotly_chart(fig)









    
