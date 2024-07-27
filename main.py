import pandas as pd
import random
from collections import defaultdict

# Read players from csv file
df = pd.read_csv('players.csv')  # replace with your csv file path
pp = pd.read_csv('preferred_positions.csv')

# Extract players' names
players = df['Name'].tolist()  # replace 'Name' with your column name
players_preferred_positions = pd.merge(df[['Name']], pp, on='Name', how='left')

# Separate players by gender
boys = df[df['Gender'] == 'M']['Name'].tolist()
girls = df[df['Gender'] == 'F']['Name'].tolist()

# Separate pitchers
boys_pitchers = df[(df['Gender'] == 'M') & (df['Pitch'] == 'Y')]['Name'].tolist()
girls_pitchers = df[(df['Gender'] == 'F') & (df['Pitch'] == 'Y')]['Name'].tolist()

# Remove pitchers from boys and girls lists
boys_not_pitch = [boy for boy in boys if boy not in boys_pitchers]
girls_not_pitch = [girl for girl in girls if girl not in girls_pitchers]

# Shuffle all lists
random.shuffle(boys)
random.shuffle(girls)
random.shuffle(boys_not_pitch)
random.shuffle(girls_not_pitch)
random.shuffle(boys_pitchers)
random.shuffle(girls_pitchers)

# Create batting order
batting_order = []
boys_pitcher_index = 0
girls_pitcher_index = 0

if len(girls) >= (len(boys) - 1):
    for i in range(max(len(boys), len(girls))):
        # Insert pitcher every 3rd and 5th position, if available
        if (i+1) % 3 == 0 and boys_pitcher_index < len(boys_pitchers):
            batting_order.append(boys_pitchers[boys_pitcher_index])
            boys_pitcher_index += 1
        if (i+1) % 5 == 0 and girls_pitcher_index < len(girls_pitchers):
            batting_order.append(girls_pitchers[girls_pitcher_index])
            girls_pitcher_index += 1
        # populate everyone else
        if i < len(boys_not_pitch):
            batting_order.append(boys_not_pitch[i])
        if i < len(girls_not_pitch):
            batting_order.append(girls_not_pitch[i])
else:
    for i in range(max(len(boys), len(girls))):
        # Insert pitcher every 3rd position, if available
        if (i+1) % 3 == 0 and boys_pitcher_index < len(boys_pitchers):
            batting_order.append(boys_pitchers[boys_pitcher_index])
            boys_pitcher_index += 1
        # populate everyone else
        if i < len(boys_not_pitch):
            batting_order.append(boys_not_pitch[i])
            batting_order.append("G")
    batting_order.append("Girls rotation")
    batting_order.append(girls_not_pitch)


# list of all positions
all_positions = [ '1B', '2B', '3B', 'C', 'SS', 'LF', 'RF', 'CF', 'R']


def generate_lineup_with_preferences(boys, girls, all_positions, players_preferred_positions_df):
    all_players = boys + girls
    num_positions = len(all_positions)
    num_innings = 7
    girl_sub_per_inning = len(girls) - 4
    boy_sub_per_inning = len(boys) - 5
    if boy_sub_per_inning < 0:
        boy_sub_per_inning = 0
        girl_sub_per_inning = len(girls) - 5
    # Initialize a dictionary to keep track of sit-outs
    sit_out_count = {player: 0 for player in all_players}

    # Create a preference matrix from the DataFrame
    preference_matrix = {player: [] for player in all_players}
    for _, row in players_preferred_positions_df.iterrows():
        player = row['Name']
        preferences = [row['P1'], row['P2'], row['P3']]
        preference_matrix[player] = preferences

    lineups = []
    sit_out_lists = []
    previous_sit_outs = []

    for inning in range(num_innings):
        # Prioritize players who sat out in the previous inning
        lineup_players = previous_sit_outs.copy()
        # Add players who have sat out 3 times
        for player in all_players:
            if sit_out_count[player] == 3 and player not in lineup_players:
                lineup_players.append(player)
        
        # Add additional players to reach 9, prioritizing those with lower sit-out counts
        remaining_boys = [p for p in boys if p not in lineup_players]
        remaining_girls = [p for p in girls if p not in lineup_players]
        
        sorted_boys = sorted(remaining_boys, key=lambda x: (sit_out_count[x], random.random()))
        sorted_girls = sorted(remaining_girls, key=lambda x: (sit_out_count[x], random.random()))
        random.shuffle(sorted_girls)
        random.shuffle(sorted_boys)
        
        # Handling of subs: These numbers may need to be changed or commented out if there are not enough players
        if inning == 4:
            b=0
            g=0
            for player in all_players:
                if sit_out_count[player] == 0 and player not in lineup_players:
                    if player in sorted_boys and b < boy_sub_per_inning:
                        sorted_boys.remove(player)
                        b+=1
                    if player in sorted_girls and g < girl_sub_per_inning:
                        sorted_girls.remove(player)
                        g+=1
        if inning == 5:
            b = 0
            g = 0
            for player in all_players:
                # change sit out count if errors happen on lineup_players.append
                if sit_out_count[player] == 1 or sit_out_count[player] == 0 and player not in lineup_players:
                    if player in sorted_boys and b < boy_sub_per_inning:
                        sorted_boys.remove(player)
                        b+=1
                    if player in sorted_girls and g < girl_sub_per_inning:
                        sorted_girls.remove(player)
                        g+=1
        if inning == 6:
            b = 0
            g = 0
            for player in all_players:
                # change sit out count if errors happen on lineup_players.append
                if sit_out_count[player] == 1 or sit_out_count[player] == 0 and player not in lineup_players:
                    if player in sorted_boys and b < boy_sub_per_inning:
                        sorted_boys.remove(player)
                        b+=1
                    if player in sorted_girls and g < girl_sub_per_inning:
                        sorted_girls.remove(player)
                        g+=1

        while len(lineup_players) < 9:
            if len([p for p in lineup_players if p in girls]) < 4 and sorted_girls:
                lineup_players.append(sorted_girls.pop(0))
            elif sorted_boys:
                lineup_players.append(sorted_boys.pop(0))
            else:
                lineup_players.append(sorted_girls.pop(0))
        
        lineup = []
        
        # Assign positions based on preferences
        for position in all_positions:
            candidates = [p for p in lineup_players if position in preference_matrix[p]]
            if candidates:
                player = random.choice(candidates)
                lineup.append((player, position))
                lineup_players.remove(player)
        
        # Fill remaining positions randomly if needed
        while len(lineup) < num_positions and lineup_players:
            player = lineup_players.pop(0)
            position = random.choice([pos for pos in all_positions if pos not in [p[1] for p in lineup]])
            lineup.append((player, position))
        
        # Determine who's sitting out this inning
        sit_out_list = [p for p in all_players if p not in [player for player, _ in lineup]]
        
        # Update sit-out counts
        for player in sit_out_list:
            sit_out_count[player] += 1
        
        lineups.append(lineup)
        sit_out_lists.append(sit_out_list)
        previous_sit_outs = sit_out_list

    return lineups, sit_out_lists, sit_out_count




lineups, sitting, sit_count = generate_lineup_with_preferences(boys, girls, all_positions, players_preferred_positions)

# Print the lineups
for i, (lineup, sit_out_list) in enumerate(zip(lineups, sitting), 1):
    print(f"Inning {i}:")
    for player, position in lineup:
        print(f"  {player}: {position}")
    print(f"Sitting out: {', '.join(sit_out_list)}\n")


print("Times sitting", sit_count)
print("Batting order", batting_order)

