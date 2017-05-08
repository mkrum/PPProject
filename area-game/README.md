# Programming Paradigms Project

Michael Krumdick (mkrumdi1)

Daniel Kerrigan (dkerriga)

## Gameplay

Our game is inspired by the popular game at the website splix.io.

Your player is a square that you can move up, down, left, and right on a grid. Use 'w' to go up, 's' to go down, 'a' to go left, and 'd' to go right. You start moving out of a solid red block of squares. As you move, a red path is formed behind you. If you return to your solid block of squares, then the area formed by your path is filled in, which makes your solid block of squares bigger. The more squares you have filled in, the higher your score.

Your opponent will be doing the same thing, although their blocks and paths will appear in black on your screen.

If you run into your own path, you lose. If you run into your opponent's path, you win. If you fill in 1000 blocks, you win. If you move out of bounds, you lose. You can tell when you are approaching the boundary when your leading square stops being centered in the screen.

## Set up

The code for the game can be found at https://github.com/mkrum/PPProject/tree/master/area-game.

This game is made for Python 2.7.13 and Twisted 16.6. The server code is set to be run on newt.campus.nd.edu. Copy the code to newt and then run `python server.py`. This sets up the game server on port 40067.

If you want to run the server on a computer other than newt, then edit the line `reactor.connectTCP("newt.campus.nd.edu", 40067, clientConnFactory)` in `client.py`. If you change the port number, then you also must change the port number in the line `reactor.listenTCP(40067, clientFactory)` in `server.py`.

Once the server is running, copy all of the code to whatever computers you want to play the game on. This game is for two players. Once each player has a copy of the code and the correct version of Python, Twisted, and PyGame installed, they can run `python client.py`. This will connect them to the server. The first player that connects will see a waiting screen until the second player connects. Once both players have run `python client.py` and have connected, the game will begin.

The game ends when someone wins or loses. The players will see a message telling them if they won or lost. To stop, click the screen to disconnect. After both players have disconnected, they can play again by running `python client.py` again.

If at any point one player disconnects, the game stops and the other player will see a message informing them that their opponent disconnected. Clicking the screen will disconnect that player.
