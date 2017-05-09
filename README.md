# Programming Paradigms Project

Michael Krumdick (mkrumdi1)

Daniel Kerrigan (dkerriga)

GitHub Repo: https://github.com/mkrum/PPProject

## Games

For this project, we have worked on two games that are similar.

The game we originally set out to make is in the area-game folder. This game is more complex than the other. We have been able to fix most of the bugs in area-game, but some remain. We were concerned that this game would not work by submission time, so we simplified and modified the game into light-cycle as a backup plan. We did not want to end up submitting something that did not work. We are including both games in our submission because we thought it was worth while to show our effort.

For grading purposes, our main submission is light-cycle.

View the two game folders for code and more detailed READMEs.


## Code

A lot of the code is the same between the two games. The main difference is that area-game has code to handle filling areas formed by paths. In both games, the clients use the server to communicate their moves to each other and the location that their move happened at. Information is not sent every tick. Whenever one player presses a WASD key, the move direction and location is sent to the other player. In area-game, clients also communicate to each other paths that need to be filled. We also communicate the starting of the game and the game results over the server.

In our testing, we ran `server.py` on newt and `client.py` from our local machines. The two clients communicate to each other through the server.
