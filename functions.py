# Contains all the functions used the app.py

import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import streamlit as st
import altair as alt

from plot import plot_line, line_per

df = pd.read_csv(r"C:\Users\personal\Projects\FAOSTAT\faostat.csv", 
                 encoding='ISO-8859-1', low_memory=False)

countries_df = pd.read_csv(r"C:\Users\personal\Projects\FAOSTAT\countries.csv", 
                 encoding='ISO-8859-1', low_memory=False)

organizations_df = pd.read_csv(r"C:\Users\personal\Projects\FAOSTAT\organizations.csv", 
                 encoding='ISO-8859-1', low_memory=False)

unique_area_countries = countries_df.Area.unique().tolist()

# year checking
def Year_Checking(from_year, to_year):
  if (from_year <  to_year):
    return True

def common(df, area, item, element, from_year, to_year, category):
    # Dataframes
    if category == "per crops":
        avoid = 'All Crops'
        lines_df = df.query('Area == @area and Element == @element and Item != @avoid and Year >= @from_year and Year <= @to_year')
        unique_list = lines_df.Item.unique().tolist()
        position = ''
        drop = ['Area', 'Element']
    elif category == 'per elements':
        avoid = "Biomass burned (dry matter)"
        lines_df = df.query('Area == @area and Item == @item and Element != @avoid and Year >= @from_year and Year <= @to_year')
        unique_list = lines_df.Element.unique().tolist()
        position = ''
        drop = ['Area', 'Item']
    else:
        lines_df = df.query('Element == @element and Item == @item and Year >= @from_year and Year <= @to_year')
        unique_list = lines_df.Area.unique().tolist()
        drop = ['Element', 'Item']

    # empty lists
    output_value_list = []
    output_unit_list = []
    per_category_values = []

    for res in unique_list:
        if category == "per crops":
            temp_df = lines_df.query("Item == @res")
        elif category == "per elements":
            temp_df = lines_df.query("Element == @res")
        else:
            temp_df = lines_df.query('Area == @res')
        total = sum(temp_df['Value'])
        output_value_list.append(total)# value
        per_category_values.append(temp_df['Value']) # list
        output_unit_list.append(temp_df['Unit'].unique().tolist()[0]) # unit
    
    percent, output_value_list = percentage(output_unit_list,output_value_list)
    per_category_values, output_unit_list, changed = value_conversion(per_category_values, output_unit_list)
    
    if changed == True:
        lines_df['Value'] = per_category_values
    lines_df = lines_df.drop(drop, axis=1)

    bars_df = pd.DataFrame(list(zip(percent,unique_list)),columns = ['Percentage','Categories'])

    if category != 'per crops' and category != 'per elements':
        top_five_df = pd.DataFrame(list(zip(unique_list,output_value_list)), columns=['Area','Values'])
        top_five_df = top_five_df.sort_values(by="Values", ascending=False)
        top_five_df = top_five_df.head()
        five_areas = top_five_df['Area']
        lines_df = lines_df.query('Area  in @five_areas')
        bars_df = bars_df.sort_values(by="Percentage", ascending=False)
        position = next(iter(bars_df[bars_df['Categories']==area].index), 'no match')
        st.write(position)
        #bars_df = bars_df.sort_values(by="Percentage", ascending=False)
        bars_df = bars_df.head()

    return bars_df, lines_df, position

def value_conversion(per_crop_values, output_unit_list):
    changed = False
    # checks if all units are same
    if ([output_unit_list[0]]*len(output_unit_list) == output_unit_list):
        changed = False
        return per_crop_values, output_unit_list, changed
    else:
        values = []
        for i in range(len(output_unit_list)):
            if output_unit_list[i] == "tonnes":
                for j in range(len(per_crop_values[i])):
                    values.append(int(per_crop_values[i][j]*0.001))
                output_unit_list[i] = "kilotonnes"
        changed = True
        return values, output_unit_list, changed

def percentage(output_unit_list,output_value_list):
    if("tonnes" in output_unit_list and "kilotonnes" in output_unit_list):
            for i in range(len(output_value_list)):
                if (output_unit_list[i] == "tonnes"):
                    output_value_list[i] = round(output_value_list[i]*0.001, 2)
                    output_unit_list[i] = "kilotonnes"
    sum_total_value = sum(output_value_list)
    percent = [round((value/sum_total_value)*100, 2) for value in output_value_list]
    return percent, output_value_list

def check_for_data(area, item, element, from_year, to_year):
    check_df = df.query('Area == @area and Element == @element and Item == @item and Year >= @from_year and Year <= @to_year')
    if(check_df.empty ==  True):
        present = False
    else:
        present  = True
    return present

def area_stands(area, item, element, from_year, to_year):
    if area in unique_area_countries:
        bars_df, lines_df, position = common(countries_df, area, item, element, from_year, to_year, 'other')
        line_per(bars_df, lines_df, item_bool = False, area_bool = True)
        st.subheader(area +" stands in the "+str(position+1)+"th position comapred to the other Countries.")
    else:
        bars_df, lines_df, position = common(organizations_df, area, item, element, from_year, to_year, 'other')
        line_per(bars_df, lines_df, item_bool = False, area_bool = True)
        st.subheader(area +" stands in the "+str(position+1)+"th position comapred to the other Continents & ANNEX Groups") 

def functionone(area, item, element, from_year, to_year):
    categories = ["per crops","per elements"]
    item_bool = [True, False]
    area_bool = [False, False]
    for i in range(len(categories)):
        bars_df, lines_df, position = common(df, area, item, element, from_year, to_year, categories[i])
        line_per(bars_df, lines_df, item_bool = item_bool[i],area_bool = area_bool[i])
    area_stands(area, item, element, from_year, to_year)

def algorithm(area, item, element, from_year, to_year):
    if (Year_Checking(from_year,to_year)== True):
        if check_for_data(area, item, element, from_year, to_year) == True:
            line_df = df.query('Area == @area and Element == @element and Item == @item and Year >= @from_year and Year <= @to_year')
            plot_line (line_df,element)
            if element != 'Biomass burned (dry matter)':
                functionone(area, item, element, from_year, to_year)
            else:
                area_stands(area, item, element, from_year, to_year)
        else:
            st.subheader(':orange[Data is not Present for the current selection, Please try new a selection.]')
    else:
        st.subheader(":orange[Select correct Range for the Year]")