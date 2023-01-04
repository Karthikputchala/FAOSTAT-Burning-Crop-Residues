# About: Contains all the functions to search the required data

# import all the libraries
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import streamlit as st
import altair as alt

from plot import line_chart, line_and_bar

# read the data
df = pd.read_csv(r"data/faostat.csv", 
                 encoding='ISO-8859-1', low_memory=False)

countries_df = pd.read_csv(r"data/countries.csv", 
                 encoding='ISO-8859-1', low_memory=False)

organizations_df = pd.read_csv(r"data/organizations.csv", 
                 encoding='ISO-8859-1', low_memory=False)

# get a list of countries in the data
unique_area_countries = countries_df.Area.unique().tolist()

# Check the year range
def Year_Checking(from_year, to_year):
  if (from_year <  to_year):
    return True

# check if the data is present for the required selected preferences
def check_for_data(area, item, element, from_year, to_year):
    check_df = df.query('Area == @area and Element == @element and Item == @item and Year >= @from_year and Year <= @to_year')
    if(check_df.empty ==  True):
        present = False
    else:
        present  = True
    return present

# common algorithm to extract the required data from the dataset as per the user preferences
def algorithm(df, area, item, element, from_year, to_year, category):
    #  create a Dataframe as emission "per crops" or "per elements" or per overall user prefernces
    if category == "per crops":
        avoid = 'All Crops'
        # quering the data as per the preferences
        lines_df = df.query('Area == @area and Element == @element and Item != @avoid and Year >= @from_year and Year <= @to_year')
        # list of unique Items (Item Category in dataset)
        unique_list = lines_df.Item.unique().tolist()
        position = ''
        # remove unwanted data from the data frame 
        drop = ['Area', 'Element']
    elif category == 'per elements':
        avoid = "Biomass burned (dry matter)"
        # quering the data as per the preferences
        lines_df = df.query('Area == @area and Item == @item and Element != @avoid and Year >= @from_year and Year <= @to_year')
        # list of unique Elements (Element Category in dataset)
        unique_list = lines_df.Element.unique().tolist()
        position = ''
        # remove unwanted data from the data frame 
        drop = ['Area', 'Item']
    else:
        # quering the data as per the preferences
        lines_df = df.query('Element == @element and Item == @item and Year >= @from_year and Year <= @to_year')
        # list of unique Areas (Area Category in dataset)
        unique_list = lines_df.Area.unique().tolist()
        # remove unwanted data from the data frame
        drop = ['Element', 'Item']

    # empty lists
    output_value_list = [] # QUATITY OF EMISSIONS
    output_unit_list = [] # tonnes or killotonnes
    per_category_values = [] # list of values for each category in an Item, Element, or an Area. 

    # 
    for res in unique_list:
        # extract a seperate dataframe for each unique option (item, element or area) in the list
        if category == "per crops":
            temp_df = lines_df.query("Item == @res")
        elif category == "per elements":
            temp_df = lines_df.query("Element == @res")
        else:
            temp_df = lines_df.query('Area == @res')
        # get the total added value
        total = sum(temp_df['Value'])
        output_value_list.append(total)# append total value
        per_category_values.append(temp_df['Value']) # append list of values
        output_unit_list.append(temp_df['Unit'].unique().tolist()[0]) # unit
    
    # generate percentage and modified output_value_list as per the unit
    percent, output_value_list = percentage(output_unit_list,output_value_list)
    # generate modified per_category_values and its releated unit list with mentioning chnged =  True...
    # if the values are modified. 
    per_category_values, output_unit_list, changed = value_conversion(per_category_values, output_unit_list)
    # per_category_values are modified
    if changed == True:
        lines_df['Value'] = per_category_values
    # remove unwanted data from the data frame 
    lines_df = lines_df.drop(drop, axis=1) # plotted in the form of line chart
    bars_df = pd.DataFrame(list(zip(percent,unique_list)),columns = ['Percentage','Categories']) # plotted in the form of bar chart.

    if category != 'per crops' and category != 'per elements':
        # create a data frame
        top_five_df = pd.DataFrame(list(zip(unique_list,output_value_list)), columns=['Area','Values'])
        # sort according to values
        top_five_df = top_five_df.sort_values(by="Values", ascending=False)
        # get top 5 listed areas
        top_five_df = top_five_df.head()
        five_areas = top_five_df['Area']
        # get the dataframe for the top 5 areas
        lines_df = lines_df.query('Area  in @five_areas')
        # sort the dataframe by percentage
        bars_df = bars_df.sort_values(by="Percentage", ascending=False, ignore_index=True)
        # get the area's position in the world as per the selected preferences
        position = next(iter(bars_df[bars_df['Categories']==area].index), 'no match')
        bars_df = bars_df.head()
    return bars_df, lines_df, position

# generate modified per_category_values and its releated unit list with mentioning chnged =  True...
# if the values are modified.
def value_conversion(per_crop_values, output_unit_list):
    changed = False
    # checks if all units are same
    if ([output_unit_list[0]]*len(output_unit_list) == output_unit_list):
        # no modification happens
        changed = False
        return per_crop_values, output_unit_list, changed
    else:
        values = []
        # convert each value to unit killotonnes if it is in unit tonnes
        for i in range(len(output_unit_list)):
            if output_unit_list[i] == "tonnes":
                for j in range(len(per_crop_values[i])):
                    values.append(int(per_crop_values[i][j]*0.001))
                output_unit_list[i] = "kilotonnes"
        changed = True
        return values, output_unit_list, changed

# generate percentage and modified output_value_list as per the unit
def percentage(output_unit_list,output_value_list):
    # convert each value to unit killotonnes if it is in unit tonnes
    if("tonnes" in output_unit_list and "kilotonnes" in output_unit_list):
            for i in range(len(output_value_list)):
                if (output_unit_list[i] == "tonnes"):
                    output_value_list[i] = round(output_value_list[i]*0.001, 2)
                    output_unit_list[i] = "kilotonnes"
    # calculate the percentage
    sum_total_value = sum(output_value_list)
    percent = [round((value/sum_total_value)*100, 2) for value in output_value_list]
    return percent, output_value_list

# used for generating plots for top 5 areas and obataining the position of emmision  in the world for the selected area.
def area_stands(area, item, element, from_year, to_year):
    # check if area is in list of countries
    if area in unique_area_countries:
        bars_df, lines_df, position = algorithm(countries_df, area, item, element, from_year, to_year, 'other')
        # generate the plots
        line_and_bar(bars_df, lines_df, item_bool = False, area_bool = True)
        # obtain the position
        st.subheader(':orange[Position of the Area in the world]')
        st.write(area +" stands in the position- ["+str(position+1)+"] with the emission of " + element+ " compared to the other Countries.")
    else: # check if area is in list of continents or organizations
        bars_df, lines_df, position = algorithm(organizations_df, area, item, element, from_year, to_year, 'other')
        # generate the plots
        line_and_bar(bars_df, lines_df, item_bool = False, area_bool = True)
        # obtain the position
        if area != "World":
            st.subheader(':orange[Position of the Area in the world]')
            st.write(area +" stands in the position- ["+str(position+1)+"] with the emission of " + element+ " compared to the other Continents & ANNEX countries.") 

# function to 
def functionone(area, item, element, from_year, to_year):
    categories = ["per crops","per elements"]
    item_bool = [True, False]
    area_bool = [False, False]
    # generate dataframes and plots per each category
    for i in range(len(categories)):
        bars_df, lines_df, position = algorithm(df, area, item, element, from_year, to_year, categories[i])
        line_and_bar(bars_df, lines_df, item_bool = item_bool[i],area_bool = area_bool[i])
    area_stands(area, item, element, from_year, to_year)

# to-do by using all the above defined functions as per the user preferences. 
def to_do(area, item, element, from_year, to_year):
    # check year range
    if (Year_Checking(from_year,to_year)== True):
        # check if the data is present
        if check_for_data(area, item, element, from_year, to_year) == True:
            # plot the line chart for the selected preferences
            line_df = df.query('Area == @area and Element == @element and Item == @item and Year >= @from_year and Year <= @to_year')
            line_chart(line_df,element)
            # as Bimass includes CH2 AND N2O we represent to generate plots by emission per CH2 & N2O here.
            if element != 'Biomass burned (dry matter)':
                functionone(area, item, element, from_year, to_year)
            else:
                area_stands(area, item, element, from_year, to_year)
        else:
            st.subheader(':purple[Data is not Present for the current selection, Please try new a selection.]')
    else:
        st.subheader(":purple[Select correct Range for the Year.]")
