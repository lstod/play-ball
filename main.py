import pandas as pd
import random

# Read players from csv file
df = pd.read_csv('players.csv')  # replace with your csv file path
pp = pd.read_csv('preferred_positions.csv')
# # Extract players' names
# players = df['Name'].tolist()  # replace 'Name' with your column name

# # Separate players by gender
# boys = df[df['Gender'] == 'M']['Name'].tolist()
# girls = df[df['Gender'] == 'F']['Name'].tolist()

# # Shuffle players within each gender
# random.shuffle(boys)
# random.shuffle(girls)

# # Create batting order
# batting_order = []
# for i in range(max(len(boys), len(girls))):
#     if i < len(boys):
#         batting_order.append(boys[i])
#     if i < len(girls):
#         batting_order.append(girls[i])

# Extract players' names
players = df['Name'].tolist()  # replace 'Name' with your column name
players_preferred_positions = pd.merge(df[['Name']], pp, on='Name', how='left')
print (players_preferred_positions)
breakpoint()
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
for i in range(max(len(boys), len(girls))):
    if i < len(boys):
        batting_order.append(boys[i])
    if i < len(girls):
        batting_order.append(girls[i])
    # Insert pitcher every 5th position, if available
    if (i+1) % 5 == 0 and boys_pitcher_index < len(boys_pitchers):
        batting_order.append(boys_pitchers[boys_pitcher_index])
        boys_pitcher_index += 1
    if (i+1) % 5 == 0 and girls_pitcher_index < len(girls_pitchers):
        batting_order.append(girls_pitchers[girls_pitcher_index])
        girls_pitcher_index += 1

# list of all positions
all_positions = [ '1B', '2B', '3B', 'C', 'SS', 'LF', 'RF', 'CF', 'R']

import random
from collections import defaultdict

def generate_lineup_with_preferences(boys, girls, all_positions, players_preferred_positions_df):
    all_players = boys + girls
    num_positions = len(all_positions)
    num_iterations = 7

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

    for iteration in range(num_iterations):
        # Prioritize players who sat out in the previous iteration
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
        
        if iteration == 4:
            for player in all_players:
                if sit_out_count[player] == 0 and player not in lineup_players:
                    if player in sorted_boys:
                        sorted_boys.remove(player)
                    if player in sorted_girls:
                        sorted_girls.remove(player)
                    print(player, "sat 0")
        if iteration == 5:
            b = 0
            g = 0
            for player in all_players:
                if sit_out_count[player] == 1 or sit_out_count[player] == 0 and player not in lineup_players:
                    if player in sorted_boys and b<2:
                        sorted_boys.remove(player)
                        b+=1
                    if player in sorted_girls and g<2:
                        sorted_girls.remove(player)
                        g+=1
                    print(player, "max 2")
        if iteration == 6:
            for player in all_players:
                if sit_out_count[player] == 1 and player not in lineup_players:
                    if player in sorted_boys:
                        sorted_boys.remove(player)
                    if player in sorted_girls:
                        sorted_girls.remove(player)
                    print(player)

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
        
        # Determine who's sitting out this iteration
        sit_out_list = [p for p in all_players if p not in [player for player, _ in lineup]]
        
        # Update sit-out counts
        for player in sit_out_list:
            sit_out_count[player] += 1
        
        print(sit_out_count)
        lineups.append(lineup)
        sit_out_lists.append(sit_out_list)
        previous_sit_outs = sit_out_list

    return lineups, sit_out_lists




lineups, sitting = generate_lineup_with_preferences(boys, girls, all_positions, players_preferred_positions)

# Print the lineups
for i, (lineup, sit_out_list) in enumerate(zip(lineups, sitting), 1):
    print(f"Lineup {i}:")
    for player, position in lineup:
        print(f"  {player}: {position}")
    print(f"Sitting out: {', '.join(sit_out_list)}\n")


breakpoint()
# List of fielding positions
positions = [ '1B', '2B', '3B', 'SS', 'LF', 'CF', 'Rover'] 
# removed C and RF

# List of girl's preferred positions
girls_positions = ['C', '2B', '3B', 'RF', 'Rover']

# Function to generate batting order and fielding positions
def generate_lineup(boys, girls, positions, girls_positions):
    fielding_positions = {i: {} for i in range(1, 7)}
    sitting_out = {0: []}
    all_players = boys + girls

    for inning in range(1, 7):
        players_this_inning = all_players[:]
        positions_copy = positions[:]
        girls_positions_copy = girls_positions[:]
        players_sitting_out = []

        # Prioritize players who sat out last inning
        for player in sitting_out[inning - 1]:
            if player in players_this_inning:
                players_this_inning.remove(player)
                if positions_copy and player in boys:
                    position = random.choice(positions_copy)
                    positions_copy.remove(position)
                    if position in girls_positions_copy:
                        girls_positions_copy.remove(position)
                    fielding_positions[inning][player] = position
                elif girls_positions_copy and player in girls:
                    position = random.choice(girls_positions_copy)
                    girls_positions_copy.remove(position)
                    if position in positions_copy:
                        positions_copy.remove(position)
                    fielding_positions[inning][player] = position
                else:
                    players_sitting_out.append(player)

        for player in players_this_inning:
                if player in girls and girls_positions_copy:
                    position = random.choice(girls_positions_copy)
                    girls_positions_copy.remove(position)
                    if position in positions_copy:
                        positions_copy.remove(position)
                    fielding_positions[inning][player] = position
                elif player in boys and positions_copy:
                    position = random.choice(positions_copy)
                    positions_copy.remove(position)
                    if position in girls_positions_copy:
                        girls_positions_copy.remove(position)
                    fielding_positions[inning][player] = position
                else:
                    players_sitting_out.append(player)

        # Determine who is sitting out this inning
        sitting_out[inning] = players_sitting_out

        # Shuffle players for the next inning
        random.shuffle(all_players)

    return fielding_positions, sitting_out

# Generate and print batting order and fielding positions
fielding_positions, sitting = generate_lineup(boys, girls, positions, girls_positions)

print(batting_order)
for inning in range(1, 7):
    print(f"\nInning {inning}")
    print("Fielding Positions:", fielding_positions[inning])
    print("Sitting:", sitting[inning])




lineups = generate_lineup_with_preferences(boys, girls, all_positions, players_preferred_positions)

# Print the lineups
for i, lineup in enumerate(lineups, 1):
    print(f"Lineup {i}:")
    for player, position in lineup:
        print(f"  {player}: {position}")
    print()

