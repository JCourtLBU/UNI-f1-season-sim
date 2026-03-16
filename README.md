# 🏎️ | F1 Season Simulator
### By Jack Court

-----

Please find the description and instructions to run my project below. 


## 📝 | Project Description

This program simulates a racing season using data provided in a JSON file. It reads in lists of drivers, teams, and tracks, plus settings for randomness and DNF rate.  

For each race/track, it calculates a performance score for each driver by combining their attributes (experience, racecraft, awareness, pace), their team’s performance, and the track’s pace factor — with a bit of randomness added. There’s also a chance a driver fails to finish (DNF), based partly on their awareness.  

After computing scores, the program sorts drivers by score to get finishing order. It then applies a predefined points table to award points to top finishers (excluding DNFs). Both driver and team points are tracked across races.  

Once all races are done, the program prints two standings tables: one showing total driver points, the other showing team (constructor) points. The code stays organized with separate functions for loading data, simulating races, calculating scores, assigning points, and printing results.  

## ❓ | How do I run it?

Simply navigate to the project folder in the command line, and run this line of code:

```cmd
python simulate_season.py season_data.json
```

And the expected output should be two tables, one showing the driver's standings, one showing the constructors standings. 
