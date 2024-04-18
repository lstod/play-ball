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
positions = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'Rover']

# List of girl's preferred positions
girls_positions = ['C', '2B', '3B', 'RF', 'Rover']

# Function to generate batting order and fielding positions
def generate_lineup(boys, girls, positions, girls_positions):
    fielding_positions = {}
    sitting_out = {}

    for inning in range(1, 7):
        all_players = boys + girls
        fielding_positions[inning] = {}
        players_this_inning = all_players.copy()

        girls_in_positions = random.sample([girl for girl in girls if girl in players_this_inning], min(3, len(girls)))
        for girl in girls_in_positions:
            players_this_inning.remove(girl)

        boys_in_positions = random.sample([boy for boy in boys if boy in players_this_inning], min(len(positions) - len(girls_in_positions), len(boys)))
        for boy in boys_in_positions:
            players_this_inning.remove(boy)

        players_in_positions = girls_in_positions + boys_in_positions
        random.shuffle(players_in_positions)

        positions_copy = positions.copy()
        girls_positions_copy = girls_positions.copy()

        for girl in girls_in_positions:
            girl_position = random.choice(girls_positions_copy)
            girls_positions_copy.remove(girl_position)
            positions_copy.remove(girl_position)
            fielding_positions[inning][girl] = girl_position

        for boy in boys_in_positions:
            boy_position = random.choice(positions_copy)
            positions_copy.remove(boy_position)
            fielding_positions[inning][boy] = boy_position

        sitting_out[inning] = players_this_inning

    return fielding_positions, sitting_out

# Generate and print batting order and fielding positions
fielding_positions, sitting = generate_lineup(boys, girls, positions, girls_positions)

print(batting_order)
for inning in range(1, 7):
    print(f"\nInning {inning}")
    print("Fielding Positions:", fielding_positions[inning])
    print("Sitting:", sitting[inning])

