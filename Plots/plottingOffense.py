import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox
import pandas as pd
import os
from PIL import Image

# Load the data
data = pd.read_csv('Plots/plotData/rbsdm.comstats.csv')

# Load the team logos
logos = {}
for file in os.listdir('Plots/logos'):
    team_abbr = file.split('.')[0]
    logo_path = f'Plots/logos/{file}'
    logo = Image.open(logo_path)
    logo = logo.resize((500, 500))  # Resize the logo to a specific size (e.g. (300, 300) pixels)
    logo = logo.convert('RGBA')
    logos[team_abbr] = logo

# Create a plot
fig, ax = plt.subplots()

ax.set_facecolor('#AAAAAA')
ax.grid(True, linestyle='--', alpha=0.5)


# Add team logos to the plot
for index, row in data.iterrows():
    team_abbr = row['Abbr']
    logo = logos[team_abbr]
    imagebox = offsetbox.OffsetImage(logo, zoom=0.07)  # Zoom out the logos
    ab = offsetbox.AnnotationBbox(imagebox, (row['Dropback EPA'], row['Rush EPA']), frameon=False)
    ax.add_artist(ab)

# Add title and labels
ax.set_title('Relationship between Dropback EPA and Rush EPA')
ax.set_xlabel('Dropback EPA/Play')
ax.set_ylabel('Rush EPA/Play')

# Set the limits of the axes to show all 4 quadrants
ax.set_xlim(-0.5, 0.5)  # Set the x-axis range
ax.set_ylim(-0.5, 0.5)  # Set the y-axis range


# ...

# Add annotations to the 4 quadrants
ax.annotate("Run & Pass Efficient", xy=(0.3, 0.2), xytext=(0.3, 0.2), ha='center', va='center', fontsize=10, color='red')
ax.annotate("Only Pass Efficient", xy=(-0.4, 0.2), xytext=(-0.4, 0.2), ha='center', va='center', fontsize=10, color='blue')
ax.annotate("Neither Run Nor Pass Efficient", xy=(-0.4, -0.2), xytext=(-0.4, -0.2), ha='center', va='center', fontsize=10, color='green')
ax.annotate("Only Run Efficient", xy=(0.3, -0.2), xytext=(0.3, -0.2), ha='center', va='center', fontsize=10, color='orange')

# ...
# Set the axis to cross at (0,0)
ax.axhline(0, color='black')
ax.axvline(0, color='black')

ax.text(0.95, -0.1, '@baridesignz', ha='right', va='bottom', fontsize=15, transform=ax.transAxes)



# Show the plot
plt.show()