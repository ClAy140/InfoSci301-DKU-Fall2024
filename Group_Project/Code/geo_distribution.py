import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import pandas as pd
from EDA import feature, EDA
import math
'''
The GEO data is download from [website](https://www.nconemap.gov/datasets/NCDOT::ncdot-county-boundaries/explore?location=34.679395%2C-83.695448%2C8.91)


'''


# def create_interactive_map(counties_geojson, output_html="nc_county_map.html"):
#     """Create an interactive map using Folium."""
#     # Initialize the map centered on North Carolina
#     m = folium.Map(location=[35.5, -79.0], zoom_start=7)
    
#     # Add GeoJSON data to the map
#     folium.GeoJson(
#         counties_geojson,
#         name="North Carolina Counties"
#     ).add_to(m)
    
#     # Save the map to an HTML file
#     m.save(output_html)
#     print(f"Interactive map saved as {output_html}")

# def main():
#     # Path to the GeoJSON file (replace with your file path)
#     geojson_path = "Dataset/NCDOT_County_Boundaries.geojson"  # Replace with your file's path
#     counties = gpd.read_file(geojson_path)
#     # Load the GeoJSON file
#     # print(counties.columns)
#     # print(counties[['CountyName', 'NAME']].head())

#     # Create an interactive map
#     create_interactive_map(geojson_path)


def vote():
    # Load the vote data
    file_path = 'Dataset/vote2024/2024_random_20000_rows.csv'
    data_random = pd.read_csv(file_path)
    data_random_m = feature(data_random)  # Assuming feature processes the data
    
    # Count votes by county
    county_counts = data_random_m['county_desc'].value_counts().reset_index()
    county_counts.columns = ['county_desc', 'Votes']  # Rename for clarity
    # print(county_counts.head())  # Preview the vote counts
    
    # Load the GeoJSON file
    geojson_path = "Dataset/Geographical_data/NCDOT_County_Boundaries.geojson"
    counties = gpd.read_file(geojson_path)

    
    # Convert CountyName in counties to uppercase for matching
    counties["CountyName"] = counties["CountyName"].str.upper()
    # print("CountyName (GeoJSON):", counties["CountyName"].unique())  # Debugging unique CountyName values
    
    # convert the Votes to is log scale
    # county_counts['Votes'] = county_counts['Votes'].apply(lambda x: math.log(x+1))
    # Convert county_desc in county_counts to uppercase for matching
    county_counts["county_desc"] = county_counts["county_desc"].str.upper()
    # print("county_desc (Vote Data):", county_counts["county_desc"].unique())  # Debugging unique county_desc values
    
    # Merge votes into counties based on matching CountyName and county_desc
    counties = counties.merge(
        county_counts,  # The DataFrame with vote counts
        left_on='CountyName',  # Column in counties GeoJSON
        right_on='county_desc',  # Column in vote data
        how='left'  # Keep all counties even if no votes
    )
    
    # Fill missing Votes with 0 for counties with no votes
    counties['Votes'] = counties['Votes'].fillna(0)
    
    # Debugging: Check the merged dataset
    # print(counties[["CountyName", "Votes"]].head())
    
    # Optional: Save the updated GeoDataFrame to a new GeoJSON file
    counties.to_file("Dataset/NCDOT_County_Boundaries_with_votes.geojson", driver="GeoJSON")
    
    # You can now visualize this data in the next steps
    plot_vote_map(counties, column='Votes', cmap='OrRd')
    plot_vote_map_with_labels(
        counties,
        column='Votes',          # Use Votes to color the map
        label_column='CountyName',  # Use CountyName for the labels
        cmap='OrRd',
        output_image="Figure/votes_by_county_with_names.png"
    )

def plot_vote_map(geo_data, column, cmap='OrRd', output_image="Figure/votes_map.png"):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot the GeoDataFrame with the vote data
    geo_data.plot(
        column=column,
        cmap=cmap,       # Colormap for visualization
        legend=True,     # Add a legend
        edgecolor='black',  # Add borders for counties
        ax=ax
    )
    
    plt.title("Votes by County", fontsize=16)
    plt.savefig(output_image, dpi=300)
    print(f"Visualization saved as {output_image}")
    plt.show()
def plot_vote_map_with_labels(geo_data, column, label_column='CountyName', cmap='OrRd', output_image="Figure/votes_map_with_labels.png"):
    """
    Plot the vote counts using a color map with county name labels.

    Parameters:
    - geo_data: GeoDataFrame containing vote counts and geometries.
    - column: Column name with vote data to visualize.
    - label_column: Column to use for labeling the counties (e.g., CountyName).
    - cmap: Colormap for visualization.
    - output_image: Filepath to save the output map.
    """
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Plot the GeoDataFrame with the vote data
    geo_data.plot(
        column=column,
        cmap=cmap,
        legend=True,
        edgecolor='black',
        ax=ax
    )
    
    # Add county name labels
    for idx, row in geo_data.iterrows():
        if row['geometry'].centroid.is_valid:  # Avoid invalid geometries
            centroid = row['geometry'].centroid.coords[0]
            ax.annotate(
                text=row[label_column],   # Use county name as label
                xy=centroid,             # Position at the centroid
                fontsize=6,
                ha='center',
                color='black'
            )
    
    plt.title("Votes by County with County Name Labels", fontsize=16)
    plt.savefig(output_image, dpi=600)
    print(f"Visualization with labels saved as {output_image}")
    plt.show()


    
if __name__ == "__main__":
    vote()
    # main()
