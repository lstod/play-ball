# play-ball

A tool to assist making lineups for slow pitch

## Usage
This has been set up to work with 4-pitch (teammate pitches to batter) softball with 7 innings

## Requirements 
You need to provide a list of players in `players.csv`
the list must follow the format of Name, Gender and Pitch.
- Gender accepts M or F
- Pitches are denoted with a Y

Follow formatting in `example_players.csv`

Setting positions completely random is not ideal. Set the top 3 preferred positions of each player in `preferred_positions.csv`.
- `P1`, `P2` and `P3` must match `all_positions` in main.py
- `Name` must match `Name` in `players.csv`
- Setting multiple players with identical preferences will make the preference matrix less effective and could result in players assigned outside of favoured positions

Look to `example_preferred_positions.csv` and follow formatting

## Output
Currently the lineup and batting order are printed to the console, this will be improved in a later update