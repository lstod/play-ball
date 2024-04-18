import pandas as pd
import random

# Read players from csv file
df = pd.read_csv('players.csv')  # replace with your csv file path

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

