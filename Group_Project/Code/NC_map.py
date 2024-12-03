import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import math
import argparse
from EDA import feature

"""
This script processes vote data and visualizes the results on a map of North Carolina counties.
The geographic data is downloaded from:
https://www.nconemap.gov/datasets/NCDOT::ncdot-county-boundaries/explore
"""

def vote(save_figures, display_figures):
    """
    Processes vote data and generates two visualizations:
    1. A choropleth map showing vote counts by county.
    2. A choropleth map with county names labeled.

    Parameters:
    - save_figures (bool): Whether to save the figures to disk.
    - display_figures (bool): Whether to display the figures in a pop-up window.
    """
    # Load the vote data
    # 2024
    # data_path = 'Dataset/absentee_random_20000.csv'
    # 2016
    data_path = 'Dataset/vote2016/2016_random_20000_rows.csv'
    data_random = pd.read_csv(data_path)
    data_random_processed = feature(data_random)  # Custom preprocessing function
    
    # Aggregate votes by county
    county_counts = data_random_processed['county_desc'].value_counts().reset_index()
    county_counts.columns = ['county_desc', 'Votes']  # Rename for clarity
    county_counts['county_desc'] = county_counts['county_desc'].str.upper()  # Standardize names
    county_counts['Votes'] = county_counts['Votes'].apply(lambda x: math.log(x + 1))  # Apply log scale
    
    # Load GeoJSON file with county boundaries
    geojson_path = "Dataset/Geographical_data/NCDOT_County_Boundaries.geojson"
    counties = gpd.read_file(geojson_path)
    counties["CountyName"] = counties["CountyName"].str.upper()  # Standardize names
    
    # Merge votes into the GeoDataFrame
    counties = counties.merge(
        county_counts,
        left_on='CountyName',
        right_on='county_desc',
        how='left'
    )
    counties['Votes'] = counties['Votes'].fillna(0)  # Fill missing counties with 0 votes
    
    # Save updated GeoJSON for future use (optional)
    output_geojson_path = "Dataset/Geographical_data/NCDOT_County_Boundaries_with_votes.geojson"
    counties.to_file(output_geojson_path, driver="GeoJSON")
    print(f"Updated GeoJSON saved to {output_geojson_path}")
    
    # Generate visualizations
    # plot_vote_map(
    #     geo_data=counties,
    #     column='Votes',
    #     cmap='OrRd',
    #     output_image="Figure/votes_map.png",
    #     save=save_figures,
    #     display=display_figures
    # )
    plot_vote_map_with_labels(
        geo_data=counties,
        column='Votes',
        label_column='CountyName',
        cmap='OrRd',
        output_image="Figure/votes_by_county_with_names.png",
        save=save_figures,
        display=display_figures
    )

def plot_vote_map(geo_data, column, cmap='OrRd', output_image="Figure/votes_map.png", save=False, display=True):
    """
    Generate a choropleth map visualizing votes by county.

    Parameters:
    - geo_data: GeoDataFrame containing county geometries and vote data.
    - column: Column to use for color-coding (e.g., 'Votes').
    - cmap: Colormap to use for the visualization.
    - output_image: Filepath to save the output map image.
    - save (bool): Whether to save the figure.
    - display (bool): Whether to display the figure.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    geo_data.plot(
        column=column,
        cmap=cmap,
        legend=True,
        edgecolor='black',
        ax=ax
    )
    plt.title("Votes by County", fontsize=16)
    if save:
        plt.savefig(output_image, dpi=300)
        print(f"Map saved as {output_image}")
    if display:
        plt.show()
    else:
        plt.close()

def plot_vote_map_with_labels(geo_data, column, label_column='CountyName', cmap='OrRd', output_image="Figure/votes_map_with_labels.png", save=False, display=True):
    """
    Generate a choropleth map visualizing votes by county with labels.

    Parameters:
    - geo_data: GeoDataFrame containing county geometries and vote data.
    - column: Column to use for color-coding (e.g., 'Votes').
    - label_column: Column to use for labeling counties (e.g., 'CountyName').
    - cmap: Colormap to use for the visualization.
    - output_image: Filepath to save the output map image.
    - save (bool): Whether to save the figure.
    - display (bool): Whether to display the figure.
    """
    fig, ax = plt.subplots(figsize=(15, 8))
    geo_data.plot(
        column=column,
        cmap=cmap,
        legend=True,
        edgecolor='black',
        ax=ax
    )
    
    # Annotate map with county names
    for _, row in geo_data.iterrows():
        if row['geometry'].centroid.is_valid:  # Check for valid geometries
            centroid = row['geometry'].centroid.coords[0]
            ax.annotate(
                text=row[label_column],
                xy=centroid,
                fontsize=6,
                ha='center',
                color='black'
            )
    
    plt.title("Votes by County with County Name Labels", fontsize=16)
    if save:
        plt.savefig(output_image, dpi=600)
        print(f"Map with labels saved as {output_image}")
    if display:
        plt.show()
    else:
        plt.close()

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate maps of votes by county.")
    parser.add_argument(
        "-s", "--save", 
        action="store_true", 
        help="If set, saves the figures to disk."
    )
    parser.add_argument(
        "-d", "--display", 
        action="store_true", 
        help="If set, displays the figures in a pop-up window."
    )
    args = parser.parse_args()

    # Run the vote visualization
    vote(save_figures=args.save, display_figures=args.display)
