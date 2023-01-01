import pandas as pd
import streamlit as st
import tkinter

from functions import algorithm

df = pd.read_csv(r"C:\Users\personal\Projects\FAOSTAT\faostat.csv", 
                 encoding='ISO-8859-1', low_memory=False)

# paramenters
countries = df.Area.unique().tolist()
items = df.Item.unique().tolist()
elements = df.Element.unique().tolist()
elements.append('All Emissions')
year = df.Year.unique().tolist()

st.set_page_config(layout="wide")
url = 'https://www.fao.org/faostat/en/#data/GB/visualize'
st.header(':orange[FAOSTAT: Emission from burning Crop Residues]')
#st.markdown("[link](%s)" % url)
st.caption('Methane (CH4), Nitrous oxide (N2O), and Biomass are the main greenhouse gas (GHG)\
   emissions from burning crop wastes. The FAOSTAT has collected this data from every country\
   through the activity of residue dissemination by burning the selected crops – maize, sugarcane,\
   wheat, and rice. It also includes the emission data reported by countries to the United Nations\
   Framework Convention on Climate Change (UNFCCC).'+ " [(More details about the Data)](%s)" % url)

# options selection
col1, col2, col3, col4, col5 = st.columns(5)
area = col1.selectbox('Area',countries)
from_year = col2.selectbox('From Year',year)
to_year = col3.selectbox('To year',year)
item = col4.selectbox('Item',items)
element = col5.selectbox('Element',elements)

def main():
  algorithm(area, item, element, from_year, to_year)

if st.button('Generate'):
  main()

