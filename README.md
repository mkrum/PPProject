# Programming Paradigms Project

Michael Krumdick (mkrumdi1)

Daniel Kerrigan (dkerriga)

GitHub Repo: https://github.com/mkrum/PPProject

## Games

For this project, we have worked on two games that are similar.

The game we originally set out to make is in the area-game folder. This game is more complex than the other, but unfortunately it has some major bugs. Concerned that this game would not work by submission time, we simplified and modified the game into light-cycle as a backup plan. We did not want to end up submitting something that did not work. We are including both games in our submission because although area-game is not fully working, we spent most of our time trying to get it to work and we thought it was worth including to show our effort.

View the two game folders for code and more detailed READMEs.


## Networking Code

Both games use the same networking code, which is found in `server.py` and `client.py`. Both players use `client.py` to connect to `server.py`. In our testing, we run `server.py` on newt and `client.py` from our local machines. The two clients communicate to eachother through the server. The clients communicate their moves to eachother and the location that their move happened at. We originally tried only sending the move, but due to the networking latency, they would become out of sync because the opponent's move would be taking place at a different spot than where they actually did it in their own client. We also communicate the starting of the game and the game results over the server.
