# About: contains all the functions to generate plots.

# import libraries
import streamlit as st
import altair as alt
#import pandas as pd
#import random
#import matplotlib.pyplot as plt

# plot a line chart as per the all the selected preferences.
def line_chart(line_df,element):
    c = alt.Chart(line_df).mark_line().encode(
        alt.X("Year", title="Years", scale=alt.Scale(domain=[1961,2050])),
        alt.Y("Value",title = str(line_df.Unit.unique().tolist()[0]) + "  of  " + element +"  released"))
    st.subheader(':orange[Emission over time]')
    st.altair_chart(c,use_container_width=True,)

# plot the line and Bar charts for...
# 1) emission per Items & Elements
# 2) Area stands
def line_and_bar(bars_df,lines_df,item_bool,area_bool):
    # Measure of different Items over time
    if item_bool == True:
        lines = alt.Chart(lines_df).mark_line().encode(
            x='Year',
            y='Value',
            color='Item',
            strokeDash='Item'
        )  
        # Percentage of emmision per Item
        bars = alt.Chart(bars_df).mark_bar().encode(
            alt.X("Percentage", title="Percentage", scale=alt.Scale(domain=[0,100])),
            alt.Y("Categories",title = "List of Items per Area"),
            alt.Color("Categories")
        )
    elif area_bool == True:
        # Measure of different Areas over time
        lines = alt.Chart(lines_df).mark_line().encode(
            x='Year',
            y='Value',
            color='Area',
            strokeDash='Area'
        )  
        # Percentage of emmision per Area
        bars = alt.Chart(bars_df).mark_bar().encode(
            alt.X("Percentage", title="Percentage", scale=alt.Scale(domain=[0,100])),
            alt.Y("Categories",title = "Areas"),
            alt.Color("Categories")
        )
    else:
        # Measure of different Elements over time
        lines = alt.Chart(lines_df).mark_line().encode(
            x='Year',
            y='Value',
            color='Element',
            strokeDash='Element'
        )
        # Percentage of emmision per Element
        bars = alt.Chart(bars_df).mark_bar().encode(
            alt.X("Percentage", title="Percentage", scale=alt.Scale(domain=[0,100])),
            alt.Y("Categories",title = "List of Elements per Area"),
            alt.Color("Categories")
        )
    col1, col2 = st.columns(2)
    with col1:
        if item_bool == True:
            st.subheader(':orange[Measure of different Items over time]')
        elif area_bool == True:
            st.subheader(':orange[Measure of different Areas over time]')
        else:
            st.subheader(':orange[Measure of different Elements over time]')
        # plot the chart
        st.altair_chart(lines, use_container_width=True,)

    with col2:
        if item_bool == True:
            st.subheader(':orange[Percentage of emmision per Item]')
        elif area_bool == True:
            st.subheader(':orange[Percentage of emmision per Area]')
        else:
            st.subheader(':orange[Percentage of emmision per Element]')
        # plot the chart
        st.altair_chart(bars,use_container_width=True)




