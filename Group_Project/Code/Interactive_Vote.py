import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
import math

# Load data paths for different years
DATA_PATHS = {
    '2016': 'Dataset/vote2016/2016_random_20000_rows.csv',
    '2020': 'Dataset/vote2020/2020_random_20000_rows.csv',
    '2024': 'Dataset/vote2024/2024_random_20000_rows.csv'
}
GEOJSON_PATH = "Dataset/Geographical_data/NCDOT_County_Boundaries.geojson"

def process_data(year, scale_type):
    """
    Process the data for a given year to include vote proportions for each party and apply scale transformation.
    """
    # Load vote data for the selected year
    data_path = DATA_PATHS[year]
    data_random = pd.read_csv(data_path)
    
    # Aggregate votes by county
    county_counts = data_random['county_desc'].value_counts().reset_index()
    county_counts.columns = ['county_desc', 'Votes']  # Rename for clarity
    county_counts['county_desc'] = county_counts['county_desc'].str.upper()  # Standardize names
    
    # Apply selected scale type (Log scale, Sqrt scale, Inverse scale, or Normal scale)
    if scale_type == "Log Scale":
        county_counts['Votes'] = county_counts['Votes'].apply(lambda x: math.log(x + 1))  # Apply log scale
    elif scale_type == "Sqrt Scale":
        county_counts['Votes'] = county_counts['Votes'].apply(lambda x: math.sqrt(x))  # Apply square root scale
    elif scale_type == "Inverse Scale":
        county_counts['Votes'] = county_counts['Votes'].apply(lambda x: 1 / (x + 1) if x != 0 else 0)  # Apply inverse scale
    else:
        county_counts['Votes'] = county_counts['Votes']  # Normal scale (no transformation)
    
    # Load GeoJSON file with county boundaries
    counties = gpd.read_file(GEOJSON_PATH)
    counties["CountyName"] = counties["CountyName"].str.upper()  # Standardize names
    
    # Merge votes into the GeoDataFrame
    counties = counties.merge(
        county_counts,
        left_on='CountyName',
        right_on='county_desc',
        how='left'
    )
    counties['Votes'] = counties['Votes'].fillna(0)  # Fill missing counties with 0 votes

    return counties


def create_figure(year, color_scale, scale_type):
    counties = process_data(year, scale_type)
    counties_json = counties.geometry.__geo_interface__
    
    fig = px.choropleth_mapbox(
        counties,
        geojson=counties_json,
        locations=counties.index,
        hover_name="CountyName",  # Display county name in the hover tooltip
        color="Votes",  # Color based on Votes
        color_continuous_scale=color_scale,  # Use selected color scale
        range_color=[counties['Votes'].min(), counties['Votes'].max()],  # Set color range
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 35.5, "lon": -80},
        opacity=1
    )
    
    # Update layout with title and color bar
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 30, "b": 0},
        title=f"Vote Amount by County in North Carolina ({year})",
        coloraxis_colorbar_title="Vote Count (Log Scale)" if scale_type == "Log Scale" else 
        ("Vote Count (Sqrt Scale)" if scale_type == "Sqrt Scale" else
         ("Vote Count (Inverse Scale)" if scale_type == "Inverse Scale" else "Vote Count"))
    )
    
    return fig

# Streamlit interface
st.title("Party Preference by County in North Carolina")

# Dropdown to select Year
year = st.selectbox("Select Year", ['2016', '2020', '2024'])

# Radio button to choose between Log scale, Sqrt scale, Inverse scale, or Normal scale for Votes
scale_type = st.radio("Select Scale Type", ["Log Scale", "Sqrt Scale", "Inverse Scale", "Normal Scale"])

# Dropdown to select Color Scale
color_scale = st.selectbox(
    "Select Color Scale", 
    ["Viridis", "Cividis", "Blues", "Inferno", "RdBu", "YlGnBu"]
)

# Plot the interactive map with the selected year, scale, and color scale
st.plotly_chart(create_figure(year, color_scale, scale_type))
