import pandas as pd
import plotly.graph_objects as go

def load_and_preprocess_data(filepath):
    data = pd.read_csv(filepath)
    
    # Adjust bins and labels as necessary
    bins = [18, 29, 44, 64, 100]
    labels = ['18-29', '30-44', '45-64', '65+']
    data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels, right=False)

    # Filter data to focus on the major parties (DEM and REP)
    data = data[data['voter_party_code'].isin(['REP', 'DEM'])]

    # Count voters by age group and party code
    return data.groupby(['age_group', 'voter_party_code']).size().reset_index(name='counts')

def create_sankey_diagram(data):
    # Labels for nodes (age groups and parties)
    labels = data['age_group'].unique().tolist() + ['Democrat', 'Republican']
    
    # Map party codes to a simpler list index
    label_idx_map = {label: idx for idx, label in enumerate(labels)}
    
    # Sources and targets based on data counts, mapping them to indices in the labels list
    sources = data['age_group'].map(label_idx_map).tolist()
    targets = data['voter_party_code'].map(lambda x: label_idx_map['Democrat'] if x == 'DEM' else label_idx_map['Republican']).tolist()
    values = data['counts'].tolist()

    # Node colors, assigning different light colors to age groups, blue to Democrat, red to Republican
    node_colors = ['lightblue', 'lightgreen', 'lightpink', 'lightyellow', 'blue', 'red']  # Adjust these colors as desired

    # Link colors are set to match the source node color
    link_colors = [node_colors[s] for s in sources]

    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=node_colors  # Apply colors to nodes
        ),
        link=dict(
            source=sources,  # indices of source nodes
            target=targets,  # indices of target nodes
            value=values,    # size of the flows
            color=link_colors  # Apply source matching colors to links
        ))])

    fig.update_layout(title_text="Voter Distribution by Age Group and Party", font_size=10)
    fig.show()

# Path to your dataset
# file_path = 'Dataset/absentee_random_20000.csv'
file_path = 'Dataset/2016_random_20000_rows.csv'
processed_data = load_and_preprocess_data(file_path)
create_sankey_diagram(processed_data)
