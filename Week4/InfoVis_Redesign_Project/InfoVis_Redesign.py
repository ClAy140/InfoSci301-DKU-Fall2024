import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Simulating Data (Sequence divergence rates vs % contribution)
divergence_rates = np.arange(0, 41, 1)  # 0% to 40%
# Simulating percentages for different repetitive element types
DNA = np.exp(-0.1 * divergence_rates) * 2  # Decay pattern for DNA elements
LINE = np.exp(-0.08 * (divergence_rates - 10)**2) * 1.5  # Gaussian peak for LINE
LTR = np.exp(-0.1 * (divergence_rates - 15)**2)          # Gaussian peak for LTR
SINE = np.exp(-0.2 * divergence_rates) * 0.5            # Rapid decay for SINE

# Ensure no values exceed 4% (cap percentages as in original chart)
DNA = np.clip(DNA, 0, 4)
LINE = np.clip(LINE, 0, 4)
LTR = np.clip(LTR, 0, 4)
SINE = np.clip(SINE, 0, 4)

# --- Prepare the data for Seaborn ---
data = pd.DataFrame({
    "Divergence Rate (%)": divergence_rates,
    "DNA": DNA,
    "LINE": LINE,
    "LTR": LTR,
    "SINE": SINE
})

# Add a column for the "stacked" effect
data["Total"] = data["DNA"] + data["LINE"] + data["LTR"] + data["SINE"]

# Convert to a long format (required for Seaborn's `sns.lineplot` or `sns.barplot`)
data_melted = data.melt(
    id_vars="Divergence Rate (%)",
    value_vars=["DNA", "LINE", "LTR", "SINE"],
    var_name="Category",
    value_name="Percentage"
)

# --- Seaborn Plotting ---
sns.set_theme(style="whitegrid")

# Create the Stacked Area Plot using sns.lineplot
fig, ax = plt.subplots(figsize=(12, 8))

# Line plot with a filled area for stacking
sns.lineplot(
    data=data_melted,
    x="Divergence Rate (%)",
    y="Percentage",
    hue="Category",
    ax=ax,
    palette={"DNA": "#d73027", "LINE": "#4575b4", "LTR": "#91bfdb", "SINE": "#fee090"},
    linewidth=2
)

# Fill the area under each curve for stacking effect
categories = ["DNA", "LINE", "LTR", "SINE"]
bottom = np.zeros(len(divergence_rates))  # Start with zeros for stacking

for category in categories:
    ax.fill_between(
        data["Divergence Rate (%)"],
        bottom,
        bottom + data[category],
        color={"DNA": "#d73027", "LINE": "#4575b4", "LTR": "#91bfdb", "SINE": "#fee090"}[category],
        alpha=0.7,
        label=category
    )
    bottom += data[category]

# Annotate Key Insights
ax.annotate("LINE peak at 10–15%", xy=(12, 2.5), xytext=(25, 3.5),
            arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=12)
ax.annotate("DNA elements dominate", xy=(5, 3), xytext=(20, 3.8),
            arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=12)

# Titles and Labels
ax.set_title("Redesigned Visualization of Repetitive Elements in Genome", fontsize=16)
ax.set_xlabel("Sequence Divergence Rate (%)", fontsize=14)
ax.set_ylabel("Percentage of Genome (%)", fontsize=14)

# Legend
ax.legend(title="Repetitive Element Categories", fontsize=12, title_fontsize=14)

# --- Summary Table Below the Chart ---
# Create a summary table using Pandas
summary_table = pd.DataFrame({
    "Category": ["DNA", "LINE", "LTR", "SINE"],
    "Total Contribution (%)": [
        round(data["DNA"].sum(), 2),
        round(data["LINE"].sum(), 2),
        round(data["LTR"].sum(), 2),
        round(data["SINE"].sum(), 2)
    ]
})

# Style the summary table for display
fig.subplots_adjust(bottom=0.3)  # Add space below for the table
table_ax = fig.add_axes([0.1, -0.35, 0.8, 0.25])  # Create space for the table below the plot
table_ax.axis("off")  # Hide axes for the table

# Render the styled table
styled_table = summary_table.style.set_table_styles(
    [{'selector': 'thead th', 'props': [('font-size', '12pt'), ('text-align', 'center'), ('font-weight', 'bold')]},
     {'selector': 'tbody td', 'props': [('font-size', '10pt'), ('text-align', 'center')]}]
).hide(axis='index')  # Hide row index

table_ax.table(cellText=summary_table.values, colLabels=summary_table.columns, loc='center')

plt.show()
