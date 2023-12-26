import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Sample data
data = {
    'Player Name': ['jmb', '?', 'julian', 'Lia', 'maren'],
    'Time Taken': [[6.31], [11.82], [7.96, 3.05], [9.73, 13.71], [25.22, 26.36]],
    'Hints Used': [[3], [0], [0, 0], [0, 0], [0, 0]],
    'Puzzle Name': ['Logic Puzzle', 'Logic Puzzle', 'Logic Puzzle', 'Logic Puzzle', 'Logic Puzzle']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Flatten the lists in 'Time Taken' and 'Hints Used'
df['Time Taken'] = df['Time Taken'].apply(lambda x: x[0] if len(x) > 0 else None)
df['Hints Used'] = df['Hints Used'].apply(lambda x: x[0] if len(x) > 0 else None)

# Set color palette
palette = sns.color_palette("mako_r", df.shape[0])

# Use seaborn for plotting
sns.set(style="darkgrid")

# Create a 2D scatter plot with color representing Puzzle Name
fig, ax = plt.subplots(figsize=(10, 8))
sc = sns.scatterplot(x='Hints Used', y='Time Taken', hue='Puzzle Name', data=df, palette=palette, s=100)

# Adding labels and title
plt.xlabel('Number of Hints')
plt.ylabel('Time Taken (seconds)')
plt.title('2D Scatter Plot: Time vs. Number of Hints for Different Puzzles')

# Add legend
legend_labels = df['Player Name'].unique()
legend = ax.legend(legend_labels, loc='upper right', title='Player Name')
ax.add_artist(legend)

# Show the plot
plt.show()
