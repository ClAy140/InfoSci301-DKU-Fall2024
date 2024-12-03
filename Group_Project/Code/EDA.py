import pandas as pd
import matplotlib.pyplot as plt
import os
import math

def feature(data):
    columns_to_keep = ['ncid','county_desc', 'race', 'ethnicity', 'gender', 'age', 'voter_party_code']
    data = data[columns_to_keep]
    # print(data.head())
    return data

def EDA(data, save_path):
    # Ensure the save path exists
    os.makedirs(save_path, exist_ok=True)
    
    # Draw donut charts for race and ethnicity
    def draw_donut_with_legend(data, column, title, filename):
        counts = data[column].value_counts()
        
        # Create a figure with subplots for the donut chart and table
        fig, ax = plt.subplots(2, 1, figsize=(8, 12), gridspec_kw={'height_ratios': [3, 1]})
        
        # Donut chart without proportion labels
        wedges, texts = ax[0].pie(
            counts,
            labels=None,  # Remove labels
            startangle=90,
            wedgeprops=dict(width=0.3)
        )
        ax[0].set_title(title)
        
        # Add a legend
        ax[0].legend(wedges, counts.index, title=column, loc="center left", bbox_to_anchor=(1, 0.5))
        
        # Table below the chart
        table_data = [[category, value, f"{value / counts.sum():.1%}"] for category, value in zip(counts.index, counts.values)]
        table_col_labels = ["Category", "Count", "Percentage"]
        ax[1].axis('tight')
        ax[1].axis('off')
        table = ax[1].table(cellText=table_data, colLabels=table_col_labels, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width(col=list(range(len(table_col_labels))))
        
        # Save the figure to the specified path
        plt.savefig(os.path.join(save_path, filename), bbox_inches='tight')
        plt.close()

    # Generate charts with the updated function
    draw_donut_with_legend(data_first_m, 'race', 'Distribution of Race with Legend', 'race_distribution.png')
    draw_donut_with_legend(data_first_m, 'ethnicity', 'Distribution of Ethnicity with Legend', 'ethnicity_distribution.png')





    


if __name__ == "__main__":
    data_first = pd.read_csv('Dataset/absentee_first_5000.csv')
    data_random = pd.read_csv('Dataset/absentee_random_5000.csv')
    data_first_m =feature(data_first)
    data_random_m = feature(data_random)
    EDA(data_first_m,'Figure')
