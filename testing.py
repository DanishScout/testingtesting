import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.font_manager as fm
from PIL import Image
import os 
import os
from PIL import Image
import streamlit as st

# Font paths
font_path = "Rajdhani-Bold.ttf"
font_pathh = "Alexandria-Regular.ttf"
font_pathhh = "Alexandria-SemiBold.ttf"

# Load the font using FontProperties
custom_font = fm.FontProperties(fname=font_path)
custom_fontt = fm.FontProperties(fname=font_pathh)
custom_fonttt = fm.FontProperties(fname=font_pathhh)

import pandas as pd

# Load the new CSV files into DataFrames
df1 = pd.read_csv('den1.csv')
df2 = pd.read_csv('swe1.csv')
df3 = pd.read_csv('nor1.csv')
df4 = pd.read_csv('eng1.csv')
df5 = pd.read_csv('ger1.csv')
df6 = pd.read_csv('fra1.csv')
df7 = pd.read_csv('ita1.csv')
df8 = pd.read_csv('spa1.csv')
df9 = pd.read_csv('por1.csv')
df10 = pd.read_csv('ned1.csv')
df11 = pd.read_csv('bel1.csv')
df12 = pd.read_csv('sco1.csv')

# Combine all DataFrames into one
data = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12], ignore_index=True)

# Filter players with at least 150 minutes played
data = data[data['Minutes Played'] >= 150]

# Filter players based on the specified leagues
valid_leagues = ['Superligaen', 'Allsvenskan', 'Eliteserien', 'Premier League', 'LaLiga',
                 'Bundesliga', 'Serie A', 'Ligue 1', 'Eredivisie', 'Liga Portugal', 'First Division A',
                 'Premiership']
data = data[data['League'].isin(valid_leagues)]


# Available metrics categories
available_metrics = {
    # Shooting
    "Goals": ("Shooting", "Goals"),
    "xG": ("Shooting", "xG"),
    "xG excl. penalty": ("Shooting", "xG excl. penalty"),
    "xGOT": ("Shooting", "xGOT"),
    "Shots": ("Shooting", "Shots"),
    "Shots on target": ("Shooting", "Shots on target"),

    # Passing
    "Assists": ("Passing", "Assists"),
    "xA": ("Passing", "xA"),
    "Chances created": ("Passing", "Chances created"),
    "Accurate passes": ("Passing", "Accurate passes"),
    "Pass accuracy": ("Passing", "Pass accuracy"),  # Removed the percentage sign
    "Accurate long balls": ("Passing", "Accurate long balls"),
    "Long ball accuracy": ("Passing", "Long ball accuracy"),  # Removed the percentage sign
    "Successful crosses": ("Passing", "Successful crosses"),
    "Cross accuracy": ("Passing", "Cross accuracy"),  # Removed the percentage sign

    # Possession
    "Dribbles": ("Possession", "Dribbles"),
    "Dribbles success rate": ("Possession", "Dribbles success rate"),
    "Touches": ("Possession", "Touches"),
    "Touches in opposition box": ("Possession", "Touches in opposition box"),
    "Fouls won": ("Possession", "Fouls won"),
    "Dispossessed": ("Possession", "Dispossessed"),

    # Defending
    "Tackles won": ("Defending", "Tackles won"),
    "Tackles won %": ("Defending", "Tackles won %"),
    "Duels won": ("Defending", "Duels won"),
    "Duels won %": ("Defending", "Duels won %"),
    "Aerials won": ("Defending", "Aerials won"),
    "Aerials won %": ("Defending", "Aerials won %"),
    "Interceptions": ("Defending", "Interceptions"),
    "Blocked scoring attempt": ("Defending", "Blocked scoring attempt"),
    "Fouls committed": ("Defending", "Fouls committed"),
    "Recoveries": ("Defending", "Recoveries"),
    "Possession won final 3rd": ("Defending", "Possession won final 3rd"),
    "Dribbled past": ("Defending", "Dribbled past"),

    # Goalkeeping Metrics
    "Saves": ("Goalkeeping", "Saves"),
    "Save percentage": ("Goalkeeping", "Save percentage"),
    "Goals conceded": ("Goalkeeping", "Goals conceded"),
    "Goals prevented": ("Goalkeeping", "Goals prevented"),
    "Clean sheets": ("Goalkeeping", "Clean sheets"),
    "Penalties faced": ("Goalkeeping", "Penalties faced"),
    "Penalty goals conceded": ("Goalkeeping", "Penalty goals conceded"),
    "Penalty saves": ("Goalkeeping", "Penalty saves"),
    "Error led to goal": ("Goalkeeping", "Error led to goal"),
    "Acted as sweeper": ("Goalkeeping", "Acted as sweeper"),
    "High claim": ("Goalkeeping", "High claim"),
}

# Mapping of original metrics to themselves (no shortening)
metric_short_names = {
    "Goals": "Goals",
    "xG": "xG",
    "xG excl. penalty": "npxG",
    "xGOT": "xGOT",
    "Shots": "Shots",
    "Shots on target": "Shots\nOn target",

    "Assists": "Assists",
    "xA": "xA",
    "Chances created": "Key Passes",
    "Accurate passes": "Accurate\nPasses",
    "Pass accuracy": "Pass\nAccuracy %",
    "Accurate long balls": "Accurate\nLong Balls",
    "Long ball accuracy": "Long Ball\nAccuracy %",
    "Successful crosses": "Successful\nCrosses",
    "Cross accuracy": "Cross\nAccuracy%",

    "Dribbles": "Successful\nTake-ons",
    "Dribbles success rate": "Take-On\nSuccess %",
    "Touches": "Touches",
    "Touches in opposition box": "Touches In\nOpp. Box",
    "Fouls won": "Fouls Won",
    "Dispossessed": "Dispossessed",

    "Tackles won": "Tackles\nWon",
    "Tackles won %": "Tackles\nWon %",
    "Duels won": "Duels\nWon",
    "Duels won %": "Duels\nWon %",
    "Aerials won": "Aerials\nWon",
    "Aerials won %": "Aerials\nWon %",
    "Interceptions": "Interceptions",
    "Blocked scoring attempt": "Blocks",
    "Fouls committed": "Fouls\nCommitted",
    "Recoveries": "Recoveries",
    "Possession won final 3rd": "Poss. Won\nIn Final 3rd",
    "Dribbled past": "Dribbled\nPast",

    "Saves": "Saves",
    "Save percentage": "Save %",
    "Goals conceded": "Goals\nConceded",
    "Goals prevented": "Goals\nPrevented",
    "Clean sheets": "Clean\nSheets",
    "Penalties faced": "Penalties\nFaced",
    "Penalty goals conceded": "Penalty Goals\nConceded",
    "Penalty saves": "Penalty\nSaves",
    "Error led to goal": "Errors\nLed to goal",
    "Acted as sweeper": "Sweeper\nActions",
    "High claim": "High\nClaims",
}


# Set up the Streamlit app
st.markdown("<h1 style='font-size: 34px;'>Make Your Own Data Visualizations</h1>", unsafe_allow_html=True)

# Add the h2 markdown with adjusted margin for closer positioning
st.markdown("<h2 style='font-size: 20px; font-weight: normal; margin-top: -25px;'>Data Updated Weekly | By <a href='https://x.com/DanishScout_' target='_blank'>@DanishScout_</a> | <a href='https://buymeacoffee.com/danishscout' target='_blank'>Support My Work</a></h2>", unsafe_allow_html=True)

# Add a horizontal line
st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

# Add your existing title and content
st.markdown("<h1 style='font-size: 24px;'>Pizza Chart</h1>", unsafe_allow_html=True)




# Player search
player_name = st.text_input("Enter Player Name:")

# Filter the player data based on the search
if player_name:
    # Get all players matching the name
    matching_players = data[data['Player Name'].str.contains(player_name, case=False)]

    # Check if any players were found
    if matching_players.empty:
        st.error("Player not found. Please try a different name.")
    else:
        # Create a dropdown to select a specific player from the matches
        player_options = matching_players['Player Name'].unique()  # Get unique player names
        selected_player_name = st.selectbox("Select Player:", player_options)

        # Get data for the selected player
        player_data = matching_players[matching_players['Player Name'] == selected_player_name].iloc[0]  # Get the first match

        # Function to get valid metrics for a specific category with short names
        def get_valid_metrics_with_short_names(category):
            return [
                metric_short_names[metric] for metric, (cat, metric_name) in available_metrics.items()
                if cat == category and pd.notna(player_data.get(metric_name, None))
            ]

        # Rest of your code continues here...


        
        # Dropdowns for each metric category allowing multiple selection with short names
        shooting_metrics = st.multiselect(
            "Select Shooting Metrics:", 
            options=get_valid_metrics_with_short_names("Shooting"),
            default=[]
        )
        
        passing_metrics = st.multiselect(
            "Select Passing Metrics:", 
            options=get_valid_metrics_with_short_names("Passing"),
            default=[]
        )
        
        possession_metrics = st.multiselect(
            "Select Possession Metrics:", 
            options=get_valid_metrics_with_short_names("Possession"),
            default=[]
        )
        
        defending_metrics = st.multiselect(
            "Select Defending Metrics:", 
            options=get_valid_metrics_with_short_names("Defending"),
            default=[]
        )
        
        goalkeeping_metrics = st.multiselect(
            "Select Goalkeeping Metrics:", 
            options=get_valid_metrics_with_short_names("Goalkeeping"),
            default=[]
        )



        # Combine selected metrics (using the original names)
        selected_metrics = []
        for selected_metric in shooting_metrics + passing_metrics + possession_metrics + defending_metrics + goalkeeping_metrics:
            # Reverse lookup to get the original name from short name
            original_metric = next((metric for metric, short in metric_short_names.items() if short == selected_metric), None)
            if original_metric:
                selected_metrics.append(original_metric)
        
        # Create a set to track selected categories
        selected_categories = set(available_metrics[metric][0] for metric in selected_metrics)
        
        # Prepare values for plotting using original names
        selected_values = {metric: player_data[available_metrics[metric][1]] for metric in selected_metrics if metric in available_metrics}
        
        # Check if at least 3 metrics are selected
        if len(selected_metrics) < 3:
            st.error("Choose at least 3 metrics.")
        else:
            # Proceed with the visualization
            # Normalize values to [0, 100]
            max_value = 100  # Set maximum value to 100 for all metrics
            normalized_values = [value / max_value for value in selected_values.values()]
        
            # Number of slices (equal to number of metrics)
            num_slices = len(selected_metrics)
        
            # Calculate angles for each slice
            angles = np.linspace(0, 2 * np.pi, num_slices + 1)
        
            # Create the figure and axis
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})
        
            # Set the figure face color
            fig.set_facecolor('#f5f5f5')
                    
            # Define colors based on categories
            category_colors = {
                "Shooting": '#1A78CF',
                "Passing": '#FF9300',
                "Possession": '#aa42af',
                "Defending": '#58AC4E',
                "Goalkeeping": '#e35858'
            }
        
            # Create bars for each slice
            for i, metric in enumerate(selected_metrics):
                if metric in selected_values:  # Check if the metric is in selected_values
                    category = available_metrics[metric][0]  # Get the category
                    
                    # Plot the actual value for the metric
                    value = normalized_values[i]  # Get the normalized value
                    ax.bar(angles[i], value, width=angles[1] - angles[0], color=category_colors[category], alpha=0.4, edgecolor='black')
                    
                    # Extend the edge of the bar to the maximum (1.0)
                    ax.bar(angles[i], 1.0, width=angles[1] - angles[0], color='none', edgecolor='black', linewidth=0.9, alpha=0.4)
            
            # Fill the area outside the radar chart with a circular shape
            theta = np.linspace(0, 2 * np.pi, 100)  # 100 points around the circle
            r = np.ones_like(theta)  # Radius is 1 for a full circle
            ax.fill(theta, r, color='#f5f5f5', alpha=1, zorder=-1)  # Fill with black
            
            # Set the radius limits (0 to 1)
            ax.set_ylim(0, 1)  # This keeps the values normalized to [0, 1]

        
            # Prepare legend handles with black edge color
            legend_handles = [
                plt.Line2D([0], [0], marker='o', color='w', label=cat,
                             markerfacecolor=category_colors[cat], 
                             markersize=10, 
                             markeredgecolor='black',  # Add black edge color
                             markeredgewidth=1)  # Set edge width
                for cat in selected_categories
            ]
            
            # Add legend to the plot with customized position and no frame
            ax.legend(handles=legend_handles, loc='lower right', fontsize=10, 
                      frameon=False, bbox_to_anchor=(1.125, -0.05), handletextpad=0.5)  # Adjust handletextpad


        
            # The rest of your plotting code (e.g., title, text, etc.)...

            
            # Define the y-ticks at specified positions
            y_tick_positions = np.arange(0, 1.1, 0.2)  # Positions for y-ticks (0, 0.2, 0.4, ..., 1)
            ax.set_yticks(y_tick_positions)  # Set the y-ticks without displaying them
            
            # Remove default y-tick labels
            ax.set_yticklabels([])  # This hides the default y-tick labels
            
            # Add custom y-tick labels at specified positions
            y_tick_labels = ['20', '40', '60', '80']
            for i, label in enumerate(y_tick_labels):
                ax.text(0, (i + 1) * 0.2, label, ha='center', va='center', fontproperties=custom_fontt, alpha=0.5)


            
            # Remove default x-ticks and labels
            ax.set_xticks([])  # This hides the default angle labels
            
            # Place each label at the edge of each slice with rotation
            for i, metric in enumerate(selected_metrics):
                # Position the label at the edge of the slice
                label_angle = angles[i]  # Use the angle for the current slice
                radial_distance = 1.05  # Place the label slightly outside the bar
            
                # Get the short name from the mapping
                short_name = metric_short_names.get(metric, metric)  # Default to the original if not found
            
                # Calculate rotation for enhanced readability
                rotation = label_angle * 180 / np.pi - 90  # Convert radians to degrees and adjust
                if label_angle > np.pi:  # Flip the rotation for angles on the left side
                    rotation += 180
            
                # Place the label text at the edge angle with rotation
                ax.text(label_angle, radial_distance, short_name, ha='center', va='center',
                        rotation=rotation, rotation_mode='anchor', color='black', alpha=0.85, fontproperties=custom_fontt, fontsize=12)


            
            # Add grid lines for radial background
            ax.grid(color='grey', alpha=0.25)

            # Add a horizontal line at the top with the team's primary color
            fig.add_artist(plt.Line2D((0, 1), (0.93, 0.93), color='black', linewidth=1.5, alpha=0.8, transform=fig.transFigure))
            
            # Load the league table CSV file
            league_data = pd.read_csv('league_tables.csv')
            
            # Get the Team ID from the player data
            team_id = player_data['Team ID']
            
            # Match Team ID to get the corresponding Team Name
            team_name = league_data.loc[league_data['Team ID'] == team_id, 'Team Name'].values[0]
            
            # Retrieve Minutes Played and Age from the player data
            minutes_played = player_data['Minutes Played']  # Assuming 'Minutes Played' exists
            age = player_data['Age']  # Assuming 'Age' exists
            
            # Update the plot title to include both Player Name and Team Name
            plt.title(f'{player_data["Player Name"]}, {team_name}', y=1.15, fontproperties=custom_fontt, fontsize=26, color='black', x=-0.1, ha='left')
            
            # Add text below the title for Minutes Played and Age
            fig.text(0.05225, 0.95, f'Percentile Rank vs. Positional Peers | Stats per 90\nMinutes Played: {minutes_played} | Age: {age} | Opta Data\nData as of 29/09 | Code by @DanishScout_', fontproperties=custom_fontt, fontsize=10, color='black', alpha=0.4, ha='left')

    
    # Directory where the team logos are stored
    logo_directory = 'team_logos'  # Path to your folder with the logos
    
    # Example player data (in your actual app, this will be dynamic)
    # player_data = {'Team ID': '4678', ...}
    selected_team_id = player_data['Team ID']  # Get Team ID of the selected player
    
    # Construct the path to the team logo
    team_logo_path = os.path.join(logo_directory, f'{selected_team_id}.png')  # Assuming the logo files are in PNG format
    
    # Check if the logo file exists
    if os.path.isfile(team_logo_path):
        # Load the logo image
        team_logo = Image.open(team_logo_path)
        
        # Display the logo in the Streamlit app
        st.image(team_logo, caption=f'Team Logo for Team ID {selected_team_id}', use_column_width=True)




            # Button to display the plot
        if st.button("Show Pizza Chart"):
            st.pyplot(fig)
