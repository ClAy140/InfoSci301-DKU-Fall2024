import pandas as pd
import plotly.graph_objects as go

def load_and_preprocess_data(filepath):
    data = pd.read_csv(filepath)

    # Segments and sorts data into bins
    bins = [18, 29, 44, 64, 100]
    labels = ['18-29', '30-44', '45-64', '65+']
    data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels, right=False) # create new col 'aga_group' to categorize each individual's age into bins

    # Filter data to focus on the major parties (DEM and REP)
    data = data[data['voter_party_code'].isin(['REP', 'DEM'])] # filter the dataset to include only the rows where 'voter_party_code' is 'REP' or 'DEM'

    # Count voters by age group and party code
    return data.groupby(['age_group', 'voter_party_code']).size().reset_index(name='counts')

def create_sankey_data(data, node_colors):
    # Labels for nodes (age groups and parties)
    labels = data['age_group'].unique().tolist() + ['Democrat', 'Republican'] # Result: ['18-29', '30-44', '45-64', '65+', 'Democrat', 'Republican']

    # Map party codes to a simpler list index： indices for nodes
    label_idx_map = {label: idx for idx, label in enumerate(labels)} # Result: {'18-29': 0, '30-44': 1, '45-64': 2, '65+': 3, 'Democrat': 4, 'Republican': 5}

    # Sources and targets based on data counts, mapping them to indices in the labels list
    sources = data['age_group'].map(label_idx_map).tolist() # Start ndoe index for each link
    targets = data['voter_party_code'].map(lambda x: label_idx_map['Democrat'] if x == 'DEM' else label_idx_map['Republican']).tolist() # End node index for each link
    values = data['counts'].tolist() # Size of each link, i.e., weight

    # Generate link colors dynamically
    link_colors = generate_link_colors(sources, node_colors)

    # Return the data in Sankey format
    return go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=node_colors,  # Apply colors to nodes
            hoverinfo="all",
            hovertemplate='%{label}'
        ),
        link=dict(
            source=sources,  # indices of source nodes
            target=targets,  # indices of target nodes
            value=values,    # size of the flows
            color=link_colors,  # Apply source matching colors to links
            hoverinfo="all",
            hovertemplate='Age: %{source.label}<br>Party: %{target.label}<br>Weight: %{value}'
        ))

def generate_link_colors(sources, node_colors):
    # Dynamically generate link colors based on source nodes
    if not sources:
        return []
    return [node_colors[source] for source in sources]  # Match source index to node colors

def create_interactive_sankey_diagram(file_paths_by_year, color_palettes):
    fig = go.Figure()

    # Default colors (first palette)
    default_colors = color_palettes[0]

    # Load and preprocess data for all years
    sankey_data_by_year = {}
    sources_and_targets_by_year = {}  # Store sources and targets for each year
    for year, file_path in file_paths_by_year.items(): # Iterate over each year and the corresponding file path in the file_paths_by_year dictionary.
        data = load_and_preprocess_data(file_path)

        # Generate sources and targets dynamically for each year
        labels = data['age_group'].unique().tolist() + ['Democrat', 'Republican']
        label_idx_map = {label: idx for idx, label in enumerate(labels)}
        sources = data['age_group'].map(label_idx_map).tolist()
        targets = data['voter_party_code'].map(
            lambda x: label_idx_map['Democrat'] if x == 'DEM' else label_idx_map['Republican']
        ).tolist()

        # Save sources and targets for later use
        sources_and_targets_by_year[year] = (sources, targets)

        # Create initial Sankey diagram with default colors
        sankey_data_by_year[year] = create_sankey_data(data, default_colors['node'])

    # Add traces for each year but make them invisible initially
    for year, sankey_data in sankey_data_by_year.items():
        fig.add_trace(sankey_data)
        fig.data[-1].visible = False

    # Make the first year's data visible
    fig.data[0].visible = True
    current_year = list(file_paths_by_year.keys())[0]  # Store the first year as default in current_year

    # Create dropdown menu for Years
    year_button = [
        dict(
            label=str(year),
            method="update",
            args=[
                {"visible": [i == idx for i in range(len(file_paths_by_year))]},  # Update visibility: boolean value
                {"title": f"Voter Distribution by Age Group and Party ({year})"}
            ],
            execute=True  # Ensure this triggers palette logic when switching years
        )
        for idx, year in enumerate(file_paths_by_year.keys()) # enumerate(file_paths_by_year.keys()) = [(0, 2016), (1, 2020), (2, 2024)]
    ]

    # Create dropdown menu for Color Palettes
    color_button = [
        dict(
            label=palette['label'],
            method="update",
            args=[
                {  # Dynamically update node and link colors
                    "node.color": palette['node'],
                    "link.color": generate_link_colors(
                        sources=sources_and_targets_by_year[year][0],  # Use current year's sources
                        node_colors=palette['node']
                    )
                }
            ]
        )
        for palette in color_palettes # Iterate each palette in the color_palettes dict and create a button for then respectively
    ]

    # Update layout with dropdown
    fig.update_layout(
        annotations=[
            dict(  # Annotation for year_button
                text="Year:", x=0.31, y=1.09, showarrow=False
            ),
            dict(  # Annotation for color_button
                text="Color Palette:", x=0.58, y=1.09, showarrow=False
            )
        ],
        title=dict(
            text="Voter Distribution by Age Group and Party",
            x=0.5,
            xanchor="center",
            y=0.95  # Adjust title closer to the dropdown
        ),
        font=dict(size=20, family="Arial, sans-serif", color="black"),
        updatemenus=[
            dict(
                buttons=year_button,
                direction="down",
                showactive=True,
                x=0.4,
                xanchor="center",
                y=1.1
            ),
            dict(
                buttons=color_button,
                direction="down",
                showactive=True,
                x=0.7,
                xanchor="center",
                y=1.1
            )
        ]
    )

    fig.show()

# Define file paths for each year's dataset
file_paths = {
    # 2004: '2004_random_20000_rows..csv',
    # 2008: '2008_random_20000_rows..csv',
    # 2012: '2012_random_20000_rows..csv',
    2016: 'Dataset/2016_random_20000_rows.csv',
    2020: 'Dateset/2020_random_20000_rows.csv',
    2024: 'Dataset/2024_random_20000_rows.csv'
}

# Define color palettes for users to choose
color_palettes = [
    {"label": 'Pastel',
     "node": ['lightblue', 'lightgreen', 'lightpink', 'lightyellow', 'blue', 'red'],
     "link": None}, # link color will be assigned
    {"label": 'Morandi',
     "node": ['#a36055', '#8595a4', '#e7daa6', '#95b995', 'blue', 'red'],
     "link": None},
    {"label": 'Viridis',
     "node": ['#440154', '#482878', '#3E4A89', '#31688E', 'blue', 'red'],
     "link": None},
    {"label": 'Grayscale',
     "node": ['#D9D9D9', '#B3B3B3', '4D4D4D', '#000000', 'blue', 'red'],
     "link": None}
]

create_interactive_sankey_diagram(file_paths, color_palettes)
