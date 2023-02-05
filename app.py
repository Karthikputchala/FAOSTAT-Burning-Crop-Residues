# About: Main app.py for running the project

# import libraries
import pandas as pd
import streamlit as st
from functions import to_do

# read the data
df = pd.read_csv(r"data/faostat.csv", 
                 encoding='ISO-8859-1', low_memory=False)
original_data = pd.read_csv(r"data/Emissions_Agriculture_Burning_crop_residues_E_All_Data_(Normalized).csv", 
                 encoding='ISO-8859-1', low_memory=False)
# get unique list of each category
countries = df.Area.unique().tolist()
items = df.Item.unique().tolist()
elements = df.Element.unique().tolist()
year = df.Year.unique().tolist()

# Set the config
st.set_page_config(layout="wide",initial_sidebar_state = "expanded")
url = 'https://www.fao.org/faostat/en/#data/GB/visualize'
view_raw_data = "https://raw.githubusercontent.com/Karthikputchala/FAOSTAT-Burning-Crop-Residues/main/data/Emissions_Agriculture_Burning_crop_residues_E_All_Data_(Normalized).csv"
with st.sidebar:
  st.header("View Raw Data")
  original_data

st.header(':orange[FAOSTAT: Emission from burning Crop Residues]')
st.caption('Methane (CH4), Nitrous oxide (N2O), and Biomass are the main greenhouse gas (GHG)\
   emissions from burning crop wastes. The FAOSTAT has collected this data from every country\
   through the activity of residue dissemination by burning the selected crops – maize, sugarcane,\
   wheat, and rice. It also includes the emission data reported by countries to the United Nations\
   Framework Convention on Climate Change (UNFCCC).'+ " [(More details about the Data)](%s)" % url+ " [(View raw Data)](%s)"% view_raw_data)

# options selection
col1, col2, col3, col4, col5 = st.columns(5)
area = col1.selectbox('Area',countries)
from_year = col2.selectbox('From Year',year)
to_year = col3.selectbox('To year',year)
item = col4.selectbox('Item',items)
element = col5.selectbox('Element',elements)

def main():
  to_do(area, item, element, from_year, to_year)

if st.button('Generate'):
  main()

