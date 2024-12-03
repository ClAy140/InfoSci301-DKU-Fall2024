import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px

# Load data
DATA_PATHS = {
    '2016': 'Dataset/vote2016/2016_random_20000_rows.csv',
    '2020': 'Dataset/vote2020/2020_random_20000_rows.csv',
    '2024': 'Dataset/vote2024/2024_random_20000_rows.csv'
}
GEOJSON_PATH = "Dataset/Geographical_data/NCDOT_County_Boundaries.geojson"

def process_data(year):
    """
    Process the data for a given year to include vote proportions for each party.
    """
    # Load vote data for the selected year
    data_path = DATA_PATHS[year]
    data_random = pd.read_csv(data_path)

    # Calculate total votes and votes by party for each county
    party_counts = data_random.groupby(['county_desc', 'voter_party_code']).size().unstack(fill_value=0)
    party_counts['Total Votes'] = party_counts.sum(axis=1)
    party_counts['REP %'] = (party_counts.get('REP', 0) / party_counts['Total Votes']) * 100
    party_counts['DEM %'] = (party_counts.get('DEM', 0) / party_counts['Total Votes']) * 100
    party_counts['UNA %'] = (party_counts.get('UNA', 0) / party_counts['Total Votes']) * 100

    # Determine the dominant party in each county
    party_counts['Dominant Party'] = party_counts[['REP', 'DEM', 'UNA']].idxmax(axis=1)
    party_counts = party_counts.reset_index()
    party_counts['county_desc'] = party_counts['county_desc'].str.strip().str.upper()

    # Load geographical data
    counties = gpd.read_file(GEOJSON_PATH)
    counties["CountyName"] = counties["CountyName"].str.strip().str.upper()

    # Merge vote data with geographical data
    counties = counties.merge(
        party_counts[['county_desc', 'Dominant Party', 'REP %', 'DEM %', 'UNA %']],
        left_on='CountyName',
        right_on='county_desc',
        how='left'
    )
    counties['Dominant Party'] = counties['Dominant Party'].fillna('No Data')
    counties['REP %'] = counties['REP %'].fillna(0)
    counties['DEM %'] = counties['DEM %'].fillna(0)
    counties['UNA %'] = counties['UNA %'].fillna(0)

    return counties


def create_figure(year):
    counties = process_data(year)
    counties_json = counties.geometry.__geo_interface__
    fig = px.choropleth_mapbox(
        counties,
        geojson=counties_json,
        locations=counties.index,
        color="Dominant Party",
        hover_name="CountyName",  # Display county name in the hover tooltip
        hover_data={
        "Dominant Party": True,   # Include the dominant party
        "REP %": ':.2f',          # Display Republican vote proportion with 2 decimal places
        "DEM %": ':.2f',          # Display Democrat vote proportion with 2 decimal places
        "UNA %": ':.2f',          # Display Unaffiliated vote proportion with 2 decimal places
    },
        color_discrete_map={
            'REP': 'red', 
            'DEM': 'blue', 
            'UNA': 'gray', 
            'No Data': 'lightgray'
        },
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 35.5, "lon": -80},
        opacity=1
    )
    fig.update_layout(
        margin={"r":0,"t":30,"l":30,"b":0},
        title=f"Party Preference by County in North Carolina ({year})"
    )
    return fig

# Streamlit interface
st.title("Party Preference by County in North Carolina")
year = st.selectbox("Select Year", ['2016', '2020', '2024'])
st.plotly_chart(create_figure(year))
