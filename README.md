# average-point-differential
Given the url to a Pro-Football-Reference boxscore webpage or a gamelog file, calculates the in-game average point differential. That is, the average point differential throughout the course of the game.

Usage:
user$ python apd.py [mode] [url or path] [playoffs]

Mode:
0 if providing a relative path to a correctly formatted logfile
1 if providing a url for a Pro-Football-Reference

URL or Path:
Relative path if mode 0
URL if mode 1

Playoffs:
0 if regular season game
1 if playoff game

(This is necessary because overtime periods are 10 minutes in the regular season and 15 minutes in the playoffs)
