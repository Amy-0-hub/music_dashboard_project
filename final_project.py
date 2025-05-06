#Music and Mental Health Dashboard
#Created by Yaqin She and Vida Chea



#import libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

#load data
df = pd.read_csv("/Users/yaqin/DataVisualization/Music_dashboard_project/music_health.csv").dropna()


#sidebar filters
st.sidebar.title("Filter Options")
genre = st.sidebar.selectbox("Select Genre", df['Fav genre'].unique())
age_range = st.sidebar.slider("Select Age Range", int(df['Age'].min()), int(df['Age'].max()),(20,30))
st.write(f"Your age is: {age_range}")
#filter data
df_filtered = df[(df['Fav genre'] == genre) & (df['Age'].between(*age_range))]

# Main layout
st.title("Music and Mental health Dashboard")
st.markdown("Explore how musical prefereneces relate to mental helath and well-being.")

#This dashboard presents 4 key insights:
## average anxiety by genre
## listening time vs. anxiety
## depression distribution by genre
## happiness by genre

tab1, tab2, tab3, tab4 = st.tabs(["Barplot", "Scatterplot", "Boxplot", "Barplot"])

#visualization 1 
with tab1:
    st.header("Average Mental Health Score by Genre")
    st.markdown("Genres with lower average anxiety may suggest more calming or therapeutic effects.")
    genre_health = df.groupby("Fav genre")["Anxiety"].mean().sort_values()
    fig1 = px.bar(genre_health, 
                  x=genre_health.index, 
                  y=genre_health.values,
                  labels={'x': 'Genre', 'y': 'Average Anxiety'}, 
                  color=genre_health.values)
    st.plotly_chart(fig1, use_container_width=True)

#visualization 2
with tab2:
    st.header("Music Listening Time vs Anxiety")
    fig2, ax = plt.subplots()
    sns.scatterplot(data=df_filtered, 
                    x="Hours per day", 
                    y="Anxiety", 
                    hue="Fav genre", 
                    ax=ax)
    ax.set_xlabel("Hours of Music per Day")
    ax.set_ylabel("Anxiety Level")
    st.pyplot(fig2)
    st.markdown("This scatter plot reveals if spending more time listening to music relates to levels.")

#visulization 3
with tab3:
    st.header("Depression Level Distribution by Genre")
    fig3, ax3 = plt.subplots()
    sns.boxplot(data=df,
                x="Fav genre",
                y="Depression",
                palette="Set3")
    ax3.set_xlabel("Genre")
    ax3.set_ylabel("Depression Score")
    ax3.set_title("Distribution of Depression Scores by Genre")
    st.pyplot(fig3)
    st.markdown("Boxplot shows the spread of depression scores across different musical genres.")

#visualization 4
with tab4:
    st.header("Average Happiness Score by Genre")
    genre_insomnia=df.groupby("Fav genre")["Insomnia"].mean().reset_index().sort_values(by="Insomnia",ascending=False)
    fig4=px.bar(genre_insomnia,
                x="Fav genre",
                y="Insomnia",
                labels={"Fav genre": "Genre", "Insomnia": "Average Insomnia"},
                color="Insomnia",
                title="Insomnia Score by Genre")
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("This chart shows which genres are linked to higher or lower insomnia scores.")



# Expandable raw data
with st.expander("See raw data"):
    st.write("This information is hidden by default but expandable.")
    st.dataframe(df_filtered)
