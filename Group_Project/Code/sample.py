import pandas as pd

def select_rows(file_path, num_rows_to_select, output_file_random, random_seed=42):
    """
    Randomly selects a specified number of rows from a CSV file.

    Args:
        file_path (str): Path to the input CSV file.
        num_rows_to_select (int): Number of rows to randomly select.
        output_file_random (str): Path to save the sampled CSV file.
        random_seed (int): Seed for the random number generator (default: 42).
    """
    # Load the large dataset
    print(f"Loading dataset: {file_path}")
    df = pd.read_csv(file_path)

    # Randomly select rows with a fixed random seed
    print(f"Selecting {num_rows_to_select} random rows...")
    df_random = df.sample(n=num_rows_to_select, random_state=random_seed)

    # Save the sampled rows to a new CSV file
    df_random.to_csv(output_file_random, index=False)
    print(f"Random {num_rows_to_select} rows saved to: {output_file_random}")

if __name__ == "__main__":
    # Example usage
    # input_file = 'Dataset/vote2024/absentee_20241105_preprocessed.csv'
    # output_file = 'Dataset/vote2024/2024_random_20000_rows.csv'
    # input_file = 'Dataset/vote2020/absentee_20201103_preprocessed.csv'
    # output_file = 'Dataset/vote2020/2020_random_20000_rows.csv'
    input_file = 'Dataset/vote2016/absentee_20161108_preprocessed.csv'
    output_file = 'Dataset/vote2016/2016_random_20000_rows.csv'

    num_rows = 20000
    random_seed = 42  # Set the random seed

    select_rows(input_file, num_rows, output_file, random_seed)
