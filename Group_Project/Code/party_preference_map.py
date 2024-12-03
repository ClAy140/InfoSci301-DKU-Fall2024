import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
import argparse


def vote_with_party_preference(save_figures, display_figures):
    """
    Processes vote data and generates a map showing the dominant party by county.

    Parameters:
    - save_figures (bool): Whether to save the figures to disk.
    - display_figures (bool): Whether to display the figures in a pop-up window.
    """
    # Load the vote data
    # data_path = 'Dataset/absentee_random_20000.csv'
    data_path = 'Dataset/vote2016/2016_random_20000_rows.csv'    
    data_random = pd.read_csv(data_path)
    
    # Aggregate votes by county and party
    party_counts = data_random.groupby(['county_desc', 'voter_party_code']).size().unstack(fill_value=0)
    party_counts['Dominant Party'] = party_counts.idxmax(axis=1)
    party_counts = party_counts.reset_index()
    party_counts['county_desc'] = party_counts['county_desc'].str.strip().str.upper()

    # Map party abbreviations to full names
    party_mapping = {'REP': 'Republican', 'DEM': 'Democrat', 'UNA': 'Unaffiliated'}
    party_counts['Dominant Party'] = party_counts['Dominant Party'].map(party_mapping)
    party_counts['Dominant Party'] = party_counts['Dominant Party'].fillna('No Data')

    # Load GeoJSON file with county boundaries
    geojson_path = "Dataset/Geographical_data/NCDOT_County_Boundaries.geojson"
    counties = gpd.read_file(geojson_path)
    counties["CountyName"] = counties["CountyName"].str.strip().str.upper()

    # Merge party data into the GeoDataFrame
    counties = counties.merge(
        party_counts[['county_desc', 'Dominant Party']],
        left_on='CountyName',
        right_on='county_desc',
        how='left'
    )
    counties['Dominant Party'] = counties['Dominant Party'].fillna('No Data')

    # Generate visualizations
    cmap = {'Republican': 'red', 'Democrat': 'blue', 'Unaffiliated': 'gray', 'No Data': 'lightgray'}
    plot_party_preference_map(
        geo_data=counties,
        column='Dominant Party',
        cmap=cmap,
        output_image="Figure/party_preference_map.png",
        save=save_figures,
        display=display_figures
    )

def plot_party_preference_map(geo_data, column, cmap, output_image="Figure/party_preference_map.png", save=False, display=True):
    """
    Generate a map visualizing party preference by county.

    Parameters:
    - geo_data: GeoDataFrame containing county geometries and party data.
    - column: Column to use for color-coding (e.g., 'Dominant Party').
    - cmap: Dictionary mapping party names to colors (e.g., {'Republican': 'red', ...}).
    - output_image: Filepath to save the output map image.
    - save (bool): Whether to save the figure.
    - display (bool): Whether to display the figure.
    """
    # Set colors directly from cmap to ensure correct color per category
    colors = geo_data[column].map(cmap).fillna('lightgray')

    # Plot the map
    fig, ax = plt.subplots(figsize=(12, 8))
    geo_data.plot(
        color=colors,
        legend=False,  # Disable automatic legend to customize
        edgecolor='black',
        ax=ax
    )

    # Create a legend manually
    legend_labels = [Patch(facecolor=cmap[label], edgecolor='k', label=label) for label in cmap]
    ax.legend(handles=legend_labels, title="Party")

    plt.title("Party Preference by County", fontsize=16)
    if save:
        plt.savefig(output_image, dpi=300)
        print(f"Map saved as {output_image}")
    if display:
        plt.show()
    else:
        plt.close()

if __name__ == "__main__":
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate a party preference map by county.")
    parser.add_argument(
        "-s", "--save", 
        action="store_true", 
        help="If set, saves the figure to disk."
    )
    parser.add_argument(
        "-d", "--display", 
        action="store_true", 
        help="If set, displays the figure in a pop-up window."
    )
    args = parser.parse_args()

    # Run the party preference visualization
    vote_with_party_preference(save_figures=args.save, display_figures=args.display)
