import pandas as pd
import csv
from tqdm import tqdm
import os
import argparse


def preprocess_csv(input_file, output_file):
    """
    Preprocess the input CSV file by reading and writing its content with specified encoding.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to save the preprocessed file.
    """
    print(f"Starting preprocessing for file: {input_file}")
    try:
        with open(input_file, 'r', encoding='latin1') as infile:
            reader = csv.reader(infile)
            rows = list(reader)  # Read and collect all rows

        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(rows)

        print(f"Preprocessing complete. File saved as: {output_file}")
    except Exception as e:
        print(f"An error occurred during preprocessing: {e}")
        raise

# def preprocess_csv(input_file, output_file):
#     """
#     Preprocess the input CSV file using pandas, handling null bytes and encoding issues.
#     """
#     print(f"Starting preprocessing for file: {input_file}")
#     try:
#         # Replace null bytes in the file
#         with open(input_file, 'rb') as infile:
#             content = infile.read().replace(b'\0', b'')  # Replace null bytes
#         with open(input_file, 'wb') as outfile:
#             outfile.write(content)  # Save the cleaned content back to the file

#         # Load the cleaned file with pandas, skipping problematic lines
#         df = pd.read_csv(input_file, encoding='latin1', on_bad_lines='skip', engine='python')

#         # Log the number of rows and columns
#         print(f"File loaded: {df.shape[0]} rows, {df.shape[1]} columns")

#         if df.empty:
#             print(f"Error: The loaded DataFrame is empty. Please check the input file for issues.")
#             return  # Stop processing if the DataFrame is empty

#         # Save the cleaned DataFrame to the output CSV
#         df.to_csv(output_file, index=False, encoding='utf-8')
#         print(f"Preprocessing complete. File saved as: {output_file}")
#     except Exception as e:
#         print(f"An error occurred during preprocessing: {e}")
#         raise


def feature(data):
    """
    Select specific columns from the dataset.

    Args:
        data (pd.DataFrame): The dataframe to process.

    Returns:
        pd.DataFrame: A dataframe with only the selected columns.
    """
    print("Selecting relevant columns...")
    columns_to_keep = ['ncid', 'county_desc', 'race', 'ethnicity', 'gender', 'age', 'voter_party_code']
    return data[columns_to_keep]

def generate_report(data):
    """
    Generate a detailed report for the specified features in the dataset.

    Args:
        data (pd.DataFrame): The dataset to analyze.

    Returns:
        dict: A dictionary containing the report for each feature.
    """
    print("Generating report for dataset...")
    report = {}

    # Continuous variable analysis (age)
    if 'age' in data.columns:
        print("Analyzing 'age' column...")

        # Ensure 'age' is numeric, coercing errors (non-numeric values become NaN)
        data['age'] = pd.to_numeric(data['age'], errors='coerce')

        # Drop rows where 'age' is NaN (invalid ages)
        valid_age_data = data['age'].dropna()

        if valid_age_data.empty:
            print("The 'age' column is empty or contains no valid numeric values.")
            report['age'] = {
                "message": "No valid numeric data found in 'age' column."
            }
        else:
            # Calculate statistics
            age_stats = valid_age_data.describe(percentiles=[0.25, 0.5, 0.75])
            report['age'] = {
                "mean": age_stats['mean'],
                "median": age_stats['50%'],
                "25%": age_stats['25%'],
                "75%": age_stats['75%'],
                "std_dev": age_stats['std'],
                "min": age_stats['min'],
                "max": age_stats['max'],
                "missing_values": data['age'].isnull().sum()
            }

    # Discrete variable analysis
    discrete_features = ['county_desc', 'race', 'ethnicity', 'gender', 'voter_party_code']
    for feature in tqdm(discrete_features, desc="Processing categorical features"):
        if feature in data.columns:
            print(f"Analyzing '{feature}' column...")
            value_counts = data[feature].value_counts()
            proportions = data[feature].value_counts(normalize=True) * 100
            missing_values = data[feature].isnull().sum()

            report[feature] = {
                "value_counts": value_counts.to_dict(),
                "proportions": proportions.round(2).to_dict(),
                "missing_values": missing_values,
                "unique_values": data[feature].nunique()
            }

    print("Report generation complete.")
    return report



def save_report_to_markdown(report, output_file):
    """
    Save the report to a Markdown file.

    Args:
        report (dict): The report dictionary to save.
        output_file (str): The file path to save the Markdown report.
    """
    print(f"Saving report to Markdown file: {output_file}")
    try:
        with open(output_file, 'w') as md_file:
            md_file.write("# Data Report\n\n")
            for feature, stats in report.items():
                md_file.write(f"## Feature: {feature}\n\n")
                md_file.write("-" * 40 + "\n\n")
                
                if feature == 'age':
                    md_file.write(f"- **Mean**: {stats['mean']:.2f}\n")
                    md_file.write(f"- **Median**: {stats['median']:.2f}\n")
                    md_file.write(f"- **25%**: {stats['25%']:.2f}\n")
                    md_file.write(f"- **75%**: {stats['75%']:.2f}\n")
                    md_file.write(f"- **Standard Deviation**: {stats['std_dev']:.2f}\n")
                    md_file.write(f"- **Min**: {stats['min']}\n")
                    md_file.write(f"- **Max**: {stats['max']}\n")
                    md_file.write(f"- **Missing Values**: {stats['missing_values']}\n\n")
                else:
                    md_file.write("- **Value Counts**:\n")
                    for category, count in stats['value_counts'].items():
                        proportion = stats['proportions'][category]
                        md_file.write(f"  - {category}: {count} ({proportion}%)\n")
                    md_file.write(f"- **Missing Values**: {stats['missing_values']}\n")
                    md_file.write(f"- **Unique Categories**: {stats['unique_values']}\n\n")

        print(f"Report successfully saved as: {output_file}")
    except Exception as e:
        print(f"An error occurred while saving the report: {e}")
        raise


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process and analyze a CSV dataset.")
    parser.add_argument('input', help="Path to the input CSV file.")
    parser.add_argument('-p', '--save_preprocessed', action='store_true', help="Save the preprocessed dataset.")
    parser.add_argument('-r', '--save_report', action='store_true', help="Save the analysis report as Markdown.")
    args = parser.parse_args()

    # File paths
    input_file = args.input
    preprocessed_file = input_file.replace(".csv", "_preprocessed.csv")
    report_md_file = input_file.replace(".csv", "_report.md")

    # Step 1: Preprocess the input file if required
    if args.save_preprocessed:
        preprocess_csv(input_file, preprocessed_file)
        input_file = preprocessed_file  # Use the preprocessed file for analysis

    # Step 2: Load data for analysis
    print(f"Loading dataset: {input_file}")
    try:
        with tqdm(total=100, desc="Loading file", unit="chunk") as pbar:
            data = pd.read_csv(input_file, chunksize=100000)
            full_data = pd.concat(data)
            pbar.update(100)
    except Exception as e:
        print(f"An error occurred while loading the dataset: {e}")
        raise

    # Step 3: Generate report
    try:
        report = generate_report(full_data)
    except Exception as e:
        print(f"An error occurred while generating the report: {e}")
        raise

    # Step 4: Save the report if required
    if args.save_report:
        try:
            save_report_to_markdown(report, report_md_file)
        except Exception as e:
            print(f"An error occurred while saving the report: {e}")
