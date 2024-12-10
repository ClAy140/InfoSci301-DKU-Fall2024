# Dataset Overview

This folder contains the datasets used for the project **"Analyzing the Impact of Demographic Factors on the U.S. Presidential Election Outcomes: A Case Study of North Carolina"**. The datasets are structured by election year and include both voting data and geospatial data for analysis and visualization.

---


## 1. Geographical Data
### Description
The `Geographical_data` folder contains geospatial datasets of North Carolina's county boundaries. These are used for creating maps and integrating county-level voting data.

### Files
- **`NCDOT_County_Boundaries.csv`**: A CSV file listing county names and associated geographic attributes.  
- **`NCDOT_County_Boundaries.geojson`**: A GeoJSON file defining county boundary polygons.  
- **`NCDOT_County_Boundaries_with_votes.geojson`**: A GeoJSON file combining county boundaries with aggregated voting data.

### Source
Data is sourced from **NC OneMap**:  
- **Website**: [NC OneMap - County Boundaries](https://www.nconemap.gov/datasets/NCDOT::ncdot-county-boundaries/explore?location=34.668240%2C-83.695448%2C8.91)

### Key Attributes
- **County Name**: The name of the county.  
- **Geometry**: Polygon geometry defining county boundaries.  
- **Integrated Votes Data**: In `NCDOT_County_Boundaries_with_votes.geojson`, voting data is linked by county.

---

## 2. Voting Data
### Description
Voting datasets are organized by election year in folders (`vote2008`, `vote2012`, `vote2016`, `vote2020`, `vote2024`). Each folder contains absentee ballot data, preprocessed datasets, and sampled data for analysis.

### Structure by Year
#### Example: `vote2024/`
- **`2024_random_20000_rows.csv`**: A sample of 20,000 randomly selected rows from the full dataset for quick analysis.  
- **`absentee_20241105.csv`**: Raw absentee ballot data from the 2024 election.  
- **`absentee_20241105_preprocessed.csv`**: Preprocessed version of the absentee dataset, ready for analysis.  
- **`absentee_20241105_report.md`**: Report detailing preprocessing steps and key observations.

### Source
The voting data is collected from the **North Carolina State Board of Elections**:
- **Website**: [NC State Board of Elections - Election Results](https://er.ncsbe.gov/?election_dt=11/05/2024&county_id=0&office=FED&contest=0)

### Key Features
All voting datasets include the following columns:
- **Voter ID**: A unique identifier for each voter (anonymized where necessary).  
- **Election Date**: The date of the election.  
- **County**: County name.  
- **Party Affiliation**: Voter's registered party (Democrat, Republican, etc.).  
- **Vote Method**: Absentee, early voting, or election day.  
- **Vote Outcome**: Vote choice or ballot submission status.  

---

## Usage Notes
1. **Geographical Data**:
   - Use GeoJSON files for mapping applications with Python libraries (e.g., Geopandas, Folium) or GIS tools (e.g., QGIS, ArcGIS).  
   - Combine `NCDOT_County_Boundaries_with_votes.geojson` with election year data for enriched geographic analysis.  

2. **Voting Data**:
   - `*_preprocessed.csv` files are cleaned and normalized, suitable for immediate analysis.  
   - Refer to the `*_report.md` files for detailed documentation of data preprocessing and summaries.  

---

## Acknowledgments
We extend our thanks to the following platforms for providing open-access data:  
- **NC OneMap** for geographical data.  
- **North Carolina State Board of Elections** for election data.  

