'''
Voter Distribution by Factor(s) and Party
**Data Description:** The county-level voting results and voter informotion from 2004 to 2024 in North Carolina for U.S. presidential election.

**Data Source:** Ncsbe.gov. “NC SBE Contest Results,” November 20, 2024. https://er.ncsbe.gov/?election_dt=11/05/2024&county_id=0&office=FED&contest=0.

**Interactivity**: 
(1) Freely choosing the Year to view; 
(2) Freely choosing Color Palette to view; 
(3) Freely choose one or two factors to view it/thier connection(s) with the party preference; 
(4) Hovering to view voter group of interest in highlight and detialed information.

'''
!pip install dash

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

def load_and_preprocess_data(filepath, factors):
    data = pd.read_csv(filepath)

    # Replace 'age' with 'age_group' and bin ages if applicable
    if 'age_group' in factors:
        if 'age' not in data.columns or not pd.api.types.is_numeric_dtype(data['age']):
            raise ValueError("The dataset does not contain a valid 'age' column for creating 'age_group'.")
        bins = [18, 29, 44, 64, 100]
        labels = ['18-29', '30-44', '45-64', '65+']
        data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels, right=False)

    # Filter to focus on major parties
    data = data[data['voter_party_code'].isin(['REP', 'DEM'])]

    # Group data by selected factors and party preference
    group_columns = factors + ['voter_party_code']
    grouped_data = data.groupby(group_columns).size().reset_index(name='counts')

    return grouped_data

def create_sankey_data(data, factors, palette_colors):
    # Create labels for nodes
    labels = list(data[factors[0]].unique())
    if len(factors) == 2:
        labels += list(data[factors[1]].unique())
    labels += ['Democrat', 'Republican']

    # Map labels to indices
    label_idx_map = {label: idx for idx, label in enumerate(labels)}

    # Define sources, targets, and values
    sources = data[factors[0]].map(label_idx_map).tolist()
    if len(factors) == 2:
        targets = data[factors[1]].map(label_idx_map).tolist()
    else:
        targets = data['voter_party_code'].map(
            lambda x: label_idx_map['Democrat'] if x == 'DEM' else label_idx_map['Republican']
        ).tolist()

    # Adjust targets for two factors
    if len(factors) == 2:
        party_targets = data['voter_party_code'].map(
            lambda x: label_idx_map['Democrat'] if x == 'DEM' else label_idx_map['Republican']
        ).tolist()
        sources += targets
        targets += party_targets

    values = data['counts'].tolist() * (2 if len(factors) == 2 else 1)

    # Dynamically assign link colors
    num_links = len(values)
    link_colors = palette_colors * (num_links // len(palette_colors) + 1)
    link_colors = link_colors[:num_links]  # Ensure the list matches the number of links

    return go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors  # Apply link colors
        )
    )

# Dash App
app = Dash(__name__)

# Define file paths for datasets
file_paths = {
    "2016": "Dataset/Vote2016/2016_random_20000_rows.csv",
    "2020": "Dataset/Vote2020/2020_random_20000_rows.csv",
    "2024": "Dataset/Vote2024/2024_random_20000_rows.csv"
}

# Define color palettes
color_palettes = {
    "Pastel": ['#AEC6CF', '#FFB347', '#77DD77', '#836953', '#F49AC2', '#B39EB5', '#FF6961', '#CB99C9', '#FDFD96', '#779ECB'],
    "Morandi": ['#a36055', '#8595a4', '#e7daa6', '#95b995', '#D4B8B4', '#976666', '#DFBFB2', '#CA774B', '#F4BAAF', '#82ABA3', '#66828E', '#C1CCC7'],
    "Viridis": ['#fde725', '#5ec962', '#21918c', '#3b528b', '#440154', '#d0e11c', '#4ac16d', '#3f4788', '#481b6d', '#440154']
}

# App Layout
app.layout = html.Div([
    html.H1("Sankey Diagram: Voter Distribution by Factor(s) and Party"),
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in file_paths.keys()],
            value='2016',
            clearable=False
        )
    ], style={'width': '30%', 'display': 'inline-block'}),
    html.Div([
        html.Label("Select Factors:"),
        dcc.Checklist(
            id='factor-checklist',
            options=[
                {'label': 'Age Group', 'value': 'age_group'},
                {'label': 'Gender', 'value': 'gender'},
                {'label': 'Race', 'value': 'race'}
            ],
            value=['age_group'],  # Default to one factor
            inline=True
        )
    ], style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        html.Label("Select Color Palette:"),
        dcc.Dropdown(
            id='color-dropdown',
            options=[{'label': name, 'value': name} for name in color_palettes.keys()],
            value='Pastel',
            clearable=False
        )
    ], style={'width': '30%', 'display': 'inline-block'}),
    dcc.Graph(id='sankey-diagram')
])

@app.callback(
    Output('sankey-diagram', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('factor-checklist', 'value'),
     Input('color-dropdown', 'value')]
)
def update_sankey(selected_year, selected_factors, selected_palette):
    if len(selected_factors) == 0:
        return go.Figure()  # Return an empty figure if no factors are selected

    try:
        # Load and preprocess data
        filepath = file_paths[selected_year]
        data = load_and_preprocess_data(filepath, selected_factors)

        # Get link colors from the selected palette
        link_colors = color_palettes[selected_palette]

        # Create Sankey diagram
        sankey = create_sankey_data(data, selected_factors, link_colors)

        # Build and return figure
        fig = go.Figure(data=[sankey])
        fig.update_layout(
            title=f"{' & '.join(selected_factors).title()} vs Party Preference ({selected_year})",
            font=dict(size=14),
            margin=dict(t=50, l=50, r=50, b=50)
        )
        return fig

    except ValueError as e:
        # Return an empty figure with an error message
        fig = go.Figure()
        fig.update_layout(title=str(e), font=dict(size=14), margin=dict(t=50, l=50, r=50, b=50))
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
