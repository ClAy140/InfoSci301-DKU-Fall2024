import pandas as pd
import plotly.graph_objects as go

def load_and_preprocess_data(filepath):
    # Load the data
    data = pd.read_csv(filepath)
    
    # Filter data to focus on the major parties (DEM and REP)
    data = data[data['voter_party_code'].isin(['REP', 'DEM'])]
    
    # Group by race and party, and count the number of voters in each group
    grouped_data = data.groupby(['race', 'voter_party_code']).size().reset_index(name='counts')
    
    # Calculate total counts for each race (to determine sorting order)
    total_counts = grouped_data.groupby('race')['counts'].sum().reset_index(name='total_counts')
    
    # Merge total counts back into the grouped data
    grouped_data = grouped_data.merge(total_counts, on='race')
    
    # Normalize proportions **within each race group**
    grouped_data['proportion'] = grouped_data.groupby('race')['counts'].transform(lambda x: x / x.sum())
    
    # Sort races by total counts in descending order
    total_counts = total_counts.sort_values(by='total_counts', ascending=False)
    
    return grouped_data, total_counts

def create_sankey_diagram(data, total_counts):
    # Get ordered race labels based on total counts
    race_labels = total_counts['race'].tolist()
    party_labels = ['Democrat', 'Republican']
    labels = race_labels + party_labels  # Combine race and party labels in the correct order
    
    # Map race and party labels to indices in the `labels` list
    label_idx_map = {label: idx for idx, label in enumerate(labels)}
    
    # Sources and targets based on data proportions, mapping them to indices in the labels list
    sources = data['race'].map(label_idx_map).tolist()
    targets = data['voter_party_code'].map(lambda x: label_idx_map['Democrat'] if x == 'DEM' else label_idx_map['Republican']).tolist()
    values = data['proportion'].tolist()  # Use normalized proportions
    
    # Node colors, assigning distinct colors to races and parties
    node_colors = [
        'lightblue', 'lightgreen', 'lightpink', 'lightyellow', 
        'mediumpurple', 'orange', 'lightgray', 'blue', 'red' ,'yellow' # Valid colors
    ]
    
    # Link colors match the source node colors
    link_colors = [node_colors[s] for s in sources]

    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=node_colors[:len(labels)]  # Ensure colors match the number of labels
        ),
        link=dict(
            source=sources,  # indices of source nodes
            target=targets,  # indices of target nodes
            value=values,    # scaled as proportions
            color=link_colors  # Apply source matching colors to links
        ))])

    fig.update_layout(title_text="Voter Distribution by Race and Party (Sorted by Scale)", font_size=10)
    fig.show()

# Path to your dataset
# file_path = 'Dataset/2016_random_20000_rows.csv'
file_path = 'Dataset/absentee_random_20000.csv'
processed_data, race_totals = load_and_preprocess_data(file_path)
create_sankey_diagram(processed_data, race_totals)
