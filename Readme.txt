************************************************
MULTI - PLAYER - ASTEROIDS
************************************************

Produced by Rohan Varma - rnvarma@cmu.edu

Program: Play multiplayer Asteroids with another friend online.

***********************************************
REQUIREMENTS
***********************************************

- both players must have different computers with python installed
- one computer must be designated as the server computer; the player
running the server will play as Player1.py and run the player1 File
- the other computer (player2) will run the Player2.py File.
- both players must have their firewalls deactivated such that it allows
python to access the network connection

***********************************************
READ - ME - RUN - INSTRUCTIONS
2-P ASTEROIDS IN 5 EASY STEPS
***********************************************

1. Find Player 1 IP Address:
	Player 1 must google the follow on his computer: "my ip". 
	This will give you the IP address of the wireless connection.
	Give the number (usually 128.237.XXX.XXX) to Player 2.

2. Configure Player2 File:
	Player 2 must go the Player2.py File; go to line 8.
	Set the variable "host" to equal a string of the IP address
	that Player 1 found in step 1. 

3. Run Server on Player 1 Computer:
	Player 1 should open up command prompt (PC) or terminal (macs).
	Change to the directory of the location of the Server.py file.
	Type the following command: "python Server.py"
	HUZZAAHH! That wasn't so hard, right? You guys are now ready to play!

4. Run Player1.py and Player2.py:
	Both players should run their files on their computers.
	Check out the instructions before you play!
	Once you are ready, click on the "2-Player" button to begin.
	Unfortunately Solo-Mode is not available yet :(

5. Kill Server:
	When you and your friend have had enough, you must stop running Server.py
	Do this by going to terminal/command prompt and doing a 
	"ctrl-C" or "ctrl-Break".
	Remember to have a good day after you are done playing :)