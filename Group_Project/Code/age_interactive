import streamlit as st
import pandas as pd
import plotly.express as px

# Define file paths for each year's dataset
file_paths = {
    2016: '/Users/xiaoyikuang/Downloads/2016_random_20000_rows.csv',
    2020: '/Users/xiaoyikuang/Downloads/2020_random_20000_rows.csv',
    2024: '/Users/xiaoyikuang/Downloads/2024_random_20000_rows.csv'
}

# Function to load and preprocess data
def load_data(year):
    data = pd.read_csv(file_paths[year])
    data['age_group'] = pd.cut(data['age'], bins=[18, 29, 44, 64, 100], labels=['18-29', '30-44', '45-64', '65+'], right=False)
    return data

# Function to create the plot
def plot_age_distribution(year):
    data = load_data(year)

    # Create a plotly express plot
    fig = px.histogram(data, x="age", color="voter_party_code", 
                        labels={'voter_party_code': 'Party Affiliation', 'age': 'Age (Years)'},
                        title=f"Age Distribution by Party Affiliation in {year}",
                        nbins=30, opacity=0.6, marginal="box")

    fig.update_layout(
        barmode='overlay',
        template='plotly_dark'
    )

    # Display the figure
    st.plotly_chart(fig)

# Title of the app
st.title("Voter Age Distribution by Party Affiliation")

# Dropdown to select year
year = st.selectbox("Select Year", [2016, 2020, 2024])

# Display the plot based on selected year
plot_age_distribution(year)
