import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

@st.cache_data
def load_data():
    return pd.read_csv('dataset/anime_dataset.csv')

df = load_data()

st.title('Animation Production Dashboard')

# Top 5 Studios
st.header('Top 5 Studios based  on the title was worked on')
studio_count = df['Main_Studio'].value_counts().reset_index()
studio_count.columns = ['studio', 'title_count']
top_5_studio = studio_count.nlargest(5, 'title_count')

tab1, tab2 = st.tabs(["Pie Chart", "Bar Chart"])

with tab1:
    studio_fig = px.pie(top_5_studio, values='title_count', names='studio', title='Top 5 Studios')
    studio_fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(studio_fig)

with tab2:
    studio_bar_fig = px.bar(top_5_studio, x='studio', y='title_count', title='Top 5 Studios')
    st.plotly_chart(studio_bar_fig)

# Rating Distribution Overview
st.header('Rating Distribution Overview')
selected_genre = st.selectbox('Select Genre', ['All'] + list(df['Genre'].unique()))
selected_setting = st.selectbox('Select Setting', ['All'] + list(df['Setting'].unique()))

filtered_df = df
if selected_genre != 'All':
    filtered_df = filtered_df[filtered_df['Genre'] == selected_genre]
if selected_setting != 'All':
    filtered_df = filtered_df[filtered_df['Setting'] == selected_setting]

fig = px.scatter(filtered_df, x="Genre", y="Rating", color="Setting", symbol="Subgenres", 
                 title="Rating Distribution by Genre, Setting, and Subgenres",
                 hover_data=['Title'])
st.plotly_chart(fig)

# Mean Rating by Genre
st.header('Mean Rating by Genre')
genre_mean_ratings = df.groupby('Genre')['Rating'].agg(['mean', 'std']).reset_index()
genre_mean_ratings = genre_mean_ratings.sort_values('mean', ascending=False)

fig = go.Figure()
fig.add_trace(go.Bar(x=genre_mean_ratings['Genre'], y=genre_mean_ratings['mean'],
                     error_y=dict(type='data', array=genre_mean_ratings['std']),
                     name='Mean Rating'))
fig.update_layout(title='Mean Rating by Genre (with standard deviation)',
                  xaxis_title='Genre', yaxis_title='Mean Rating')
st.plotly_chart(fig)

# # Mean Rating by Number of Episodes
# st.header('Mean Rating by Number of Episodes')
# eps_mean_ratings = df.groupby('Number_of_Episodes')['Rating'].mean().reset_index()

# def episode_group(eps):
#     if eps == 1:
#         return '1 (One-shot)'
#     elif eps <= 12:
#         return '2-12'
#     elif eps <= 24:
#         return '13-24'
#     else:
#         return '25+'

# eps_mean_ratings['Episode_Group'] = eps_mean_ratings['Number_of_Episodes'].apply(episode_group)
# eps_group_mean = eps_mean_ratings.groupby('Episode_Group')['Rating'].mean().reset_index()

# fig = px.bar(eps_group_mean, x="Episode_Group", y="Rating", title="Mean Rating by Episode Count")
# fig.update_layout(xaxis_title="Episode count group", yaxis_title="Mean Rating")

# # Add trend line
# fig.add_trace(go.Scatter(x=eps_group_mean['Episode_Group'], y=eps_group_mean['Rating'],
#                          mode='lines', name='Trend'))

# st.plotly_chart(fig)

# Add some interactivity
st.sidebar.header('Filter Data')
selected_genres = st.sidebar.multiselect('Select Genres', df['Genre'].unique())
selected_settings = st.sidebar.multiselect('Select Settings', df['Setting'].unique())

if selected_genres or selected_settings:
    filtered_df = df[df['Genre'].isin(selected_genres) | df['Setting'].isin(selected_settings)]
    st.subheader('Filtered Data')
    st.write(filtered_df)

