import random,math,time,socket, tkMessageBox
from Tkinter import *

###########################################
# Set up server
###########################################

host = 'localhost' 
port = 50014
size = 10000 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

###########################################
# Animation class
###########################################
 
class Animation(object):
    # Override these methods when creating your own animation
    def mousePressed(self, event): pass
    def keyPressed(self, event): pass
    def keyReleased(self,event): pass
    def timerFired(self): pass
    def init(self): pass
    def redrawAll(self): pass
    def resizeWindow(self,event):
        self.width=event.width
        self.height=event.height
    
    # Call app.run(width,height) to get your app started
    def run(self, width=800, height=600):
        # create the root and the canvas
        root = Tk()
        self.width = width
        self.height = height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack(fill=BOTH,expand=YES)
        # set up events
        def redrawAllWrapper():
            self.canvas.delete(ALL)
            self.redrawAll()
        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()
        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()
        def keyReleasedWrapper(event):
            self.keyReleased(event)
            redrawAllWrapper()
        root.bind("<Button-1>", mousePressedWrapper)
        root.bind("<KeyPress>", keyPressedWrapper)
        root.bind("<KeyRelease>",keyReleasedWrapper)
        root.bind("<Configure>", self.resizeWindow)
        # set up timerFired events
        self.timerFiredDelay = 250 # milliseconds
        def timerFiredWrapper():
            self.timerFired()
            redrawAllWrapper()
            # pause, then call timerFired again
            self.canvas.after(10, timerFiredWrapper)
        # init and get timerFired running
        self.init()
        timerFiredWrapper()
        # and launch the app
        root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

###########################################
# Asteroids class
###########################################

class Asteroids(Animation):
    def contactServer(self,message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.connect((host,port))
        s.send(message) 
        data = s.recv(size)
        s.close()
        return data

    def keyPressed(self,event):
        if self.roundOver:
            if event.char == "r":
                self.contactServer("letterR.player2")
        if self.lobbyScreen == False:
            if event.keysym == "Up":
                self.contactServer("upKey.player2")
            elif event.keysym == "Left":
                self.contactServer("leftKeyPress.player2")
            elif event.keysym == "Right":
                self.contactServer("rightKeyPress.player2")
            elif event.keysym == "space":
                if self.instructionScreen and self.instructionPage == 2:
                    self.ibullets.append([self.shipX,self.shipY,self.shipDirection])
                else:     
                    self.contactServer("spaceKey.player2")

    def keyReleased(self,event):
        if self.roundOver == False:
            if event.keysym == "Left":
                self.contactServer("leftKeyRelease.player2")
            if event.keysym == "Right":
                self.contactServer("rightKeyRelease.player2")

    def typeUserName(self,event):
        if event.char in "abcdefghijklmnopqrstuvwxyz":
            if len(self.username) < 10:
                self.username += event.char
                self.redrawUserPage()

    def backspaceUserName(self,event):
        if len(self.username)>0:
            self.username = self.username[:len(self.username)-1]
            self.redrawUserPage()

    def drawValidUserName(self):
        cy = self.userheight/2.0
        cx = self.userwidth/2.0 + 120
        r = 9
        if len(self.username)>3:
            color = "green"
        else:
            color = "red"
        self.userCanvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill = color)

    def redrawUserPage(self):
        if len(self.username)>3:
            textcolor = "green"
        else:
            textcolor = "red"
        self.userCanvas.create_rectangle(0,0,self.userwidth,self.userheight,fill='black')
        self.userCanvas.create_text(self.userwidth/2.0,30,text="Type a Username",
                                    font = "d 30", fill = "green")
        self.userCanvas.create_text(self.userwidth/2.0,self.userheight/2.0,
                                    text = self.username, fill = textcolor,
                                    font = "d 20")
        self.userCanvas.create_line((self.userwidth/2.0 -110,self.userheight/2.0 + 12),
                                    (self.userwidth/2.0 +110,self.userheight/2.0 + 12),
                                    fill = "white", width = 2)
        self.userCanvas.create_rectangle(self.userwidth/2.0 -80,self.userheight-80,
                                         self.userwidth/2.0 +80,self.userheight-20,
                                         outline = "white", width = 2)
        self.userCanvas.create_text(self.userwidth/2.0,self.userheight-50,
                                    text = "Submit", font = "d 20",
                                    fill = "green")
        self.drawValidUserName()

    def handleUserClose(self):
        if tkMessageBox.askyesno("Don't close it yet :(",
                               "Are you sure you want to close before" +
                               " choosing a username?"):
            self.creatingUserName = False
            self.toplevel.destroy()
        else:
            self.toplevel.focus_force()

    def getUserName(self,event):
        x,y = event.x,event.y
        bx,by = self.userwidth/2.0,self.userheight-50
        bxr,byr = 80,30
        if (((bx-bxr)<x<(bx+bxr)) and (
            (by-byr)<y<(by+byr))):
            if len(self.username) < 4:
                tkMessageBox.showwarning("Username Error",
                                         "Youre username must be atleast" +
                                         " 4 letters long")
                self.toplevel.focus_force()
            else:
                self.contactServer("enterUsername2." + self.username)
                self.toplevel.destroy()

    def handleEnterPress(self,event):
        if len(self.username) < 4:
            tkMessageBox.showwarning("Username Error",
                                     "Youre username must be atleast" +
                                     " 4 letters long")
            self.toplevel.focus_force()
        else:
            self.contactServer("enterUsername2." + self.username)
            self.toplevel.destroy()
        
    def usernamePage(self):
        self.toplevel = Toplevel()
        self.toplevel.focus_force()
        self.username = ""
        self.userwidth = 500
        self.userheight = 300
        self.userCanvas = Canvas(self.toplevel, width=self.userwidth,height=self.userheight)
        self.userCanvas.pack()
        self.redrawUserPage()
        self.toplevel.bind("<Key>",self.typeUserName)
        self.toplevel.bind("<BackSpace>",self.backspaceUserName)
        self.toplevel.protocol('WM_DELETE_WINDOW', self.handleUserClose)
        self.toplevel.bind("<Button-1>",self.getUserName)
        self.toplevel.bind("<Return>",self.handleEnterPress)

    def clickedOnInstructions(self,x,y):
        sx, sxr = self.startButtonX, 70
        sy, syr = self.startButtonY+70, 30
        if (((sx-sxr)<x<(sx+sxr)) and (
            (sy-syr)<y<(sy+syr))):
            if self.startScreen and self.creatingUserName == False:
                return True
        return False

    def clickedBox(self,x,y,bx,by,xr,yr):
        if (((bx-xr)<x<(bx+xr)) and (
            (by-yr)<y<(by+yr))):
            return True
        return False

    def handleInstructionPageClicks(self,x,y):
        for i in xrange(5):
            xr,yr = 70,20
            bx,by=self.width/2.0-280+(i*140),self.height/2.0+230
            if self.clickedBox(x,y,bx,by,xr,yr):
                self.instructionPage = i+1
        px,py = self.width/2.0 - 280,self.height/2.0-220
        pxr,pxy = 70,10
        if self.clickedBox(x,y,px,py,pxr,pxy):
            if self.instructionPage>1:
                self.instructionPage-=1
        nx,ny = self.width/2.0 + 280,self.height/2.0-220
        nxr,nxy = 70,10
        if self.clickedBox(x,y,nx,ny,nxr,nxy):
            if self.instructionPage<5:
                self.instructionPage+= 1
        mx,my = self.width/2.0,self.height-30
        mxr,myr = 50,10
        if self.clickedBox(x,y,mx,my,mxr,myr):
            self.instructionScreen = False

    def mousePressed(self, event):
        sx, sxr = self.startButtonX, 70
        sy, syr = self.startButtonY, 30
        if self.instructionScreen:
            self.handleInstructionPageClicks(event.x,event.y)
        if self.lobbyScreen:
            mx,my = self.width/2.0,self.height-30
            mxr,myr = 50,10
            if self.clickedBox(event.x,event.y,mx,my,mxr,myr):
                self.creatingUserName = False
                self.contactServer("exitLobby.player2")
        if (((sx-sxr)<event.x<(sx+sxr)) and (
            (sy-syr)<event.y<(sy+syr))):
            if self.startScreen and self.creatingUserName == False:
                self.creatingUserName = True
                self.usernamePage()
        rx,ry = self.width/2.0, self.height/2.0 + 125
        rxr,ryr = 100,25
        if (((rx-rxr)<event.x<(rx+rxr)) and (
            (ry-ryr)<event.y<(ry+ryr))):
            if self.lobbyScreen and len(self.username1)>0:
                self.contactServer("readyToPlay.player2")
        if self.clickedOnInstructions(event.x,event.y):
            self.instructionScreen = True

    def instructionMoveBadGuy(self):
        self.ibgX +=  self.ibgV
        if self.ibgX >self.width/2.0 +250:
            self.ibgV *= (-1)
        elif self.ibgX <self.width/2.0+50:
            self.ibgV *= (-1)

    def instructionMoveBullets(self):
        if len(self.ibullets)>0:
            for i in xrange(len(self.ibullets)):
                self.ibullets[i][0] += self.bulletV*math.cos(self.ibullets[i][2])
                self.ibullets[i][1] += self.bulletV*math.sin(self.ibullets[i][2])
                self.ibullets[i][0] = round(self.ibullets[i][0],3)
                self.ibullets[i][1] = round(self.ibullets[i][1],3)

    def timerFired(self):
        self.instructionMoveBadGuy()
        self.instructionMoveBullets()
        gameState = self.contactServer("updateGame.noData")
        try:
            gameState = eval(gameState)
            self.startScreen = gameState["sS2"]
            self.lobbyScreen = gameState["lS2"]
            self.username1 = gameState["u1"]
            self.username2 = gameState["u2"]
            self.roundOver = gameState["rO"]
            self.p1Ready = gameState["p1r"]
            self.p2Ready = gameState["p2r"]
            self.SSTurnedOn = gameState["SSTO"]
            self.SSelapsedTime = gameState["SSET"]
            self.SSPointCounter = gameState["SSPC"]
            self.SSPointsNeeded = gameState["SSPN"]
            self.killedPlayer = gameState["kP"]
            self.asteroids = gameState["aR"]
            self.asteroidExplosions = gameState["aE"]
            self.bullets = gameState["b"]
            self.bullets2 = gameState["b2"]
            self.shipX = gameState["sX"]
            self.shipY = gameState["sY"]
            self.ship2X = gameState["s2X"]
            self.ship2Y = gameState["s2Y"]
            self.shipDirection = gameState["sD"]
            self.ship2Direction = gameState["s2D"]
            self.accelerating = gameState["a"]
            self.accelerating2 = gameState["a2"]
            self.badGuy = gameState["bG"]
            self.startBadGuyShooting = gameState["sBGS"]
            self.badGuyBullets = gameState["bGB"]
            self.badGuyExplosion = gameState["bGE"]
            self.invincibility = gameState["i"]
            self.invincibleBitches = gameState["iB"]
            self.invincibleBitches2 = gameState["iB2"]
            self.gameOver = gameState["gO"]
            self.starLocations = gameState["sL"]
            self.score = gameState["s"]
            self.score2 = gameState["s2"]
            self.lives = gameState["l"]
            self.lives2 = gameState["l2"]
            self.SSPointCounter2 = gameState["SSPC2"]
            self.SSTurnedOn2 = gameState["SSTO2"]
            self.SSelapsedTime2 = gameState["SSET2"]
            self.SSPointsNeeded2 = gameState["SSPN2"]
        except:
            print gameState
            print len(gameState)

    def drawBackground(self):
        self.canvas.create_rectangle(0,0,self.width,self.height, fill = "grey1")
        sl = self.sl 
        for (cx,cy) in self.starLocations:    
            self.canvas.create_line((cx,cy-sl),(cx,cy+sl), fill = "yellow", width = 2)
            self.canvas.create_line((cx-sl,cy),(cx+sl,cy), fill = "yellow", width = 2)

    def drawShip(self):
        if self.invincibleBitches == True:
            color = random.choice(self.invColors)
        else:
            color = "white"
        tail1D = self.shipDirection + (135/360.0)*(2*math.pi)
        tail2D = self.shipDirection + (225/360.0)*(2*math.pi)
        tail1X = self.shipX + self.shipLength*math.cos(tail1D)
        tail1Y = self.shipY + self.shipLength*math.sin(tail1D)
        tail2X = self.shipX + self.shipLength*math.cos(tail2D)
        tail2Y = self.shipY + self.shipLength*math.sin(tail2D)
        self.canvas.create_line((self.shipX,self.shipY),(tail1X,tail1Y), width = 2, fill = color)
        self.canvas.create_line((self.shipX,self.shipY),(tail2X,tail2Y), width = 2, fill = color)

    def drawShip2(self):
        if self.invincibleBitches2 == True:
            color = random.choice(self.invColors)
        else:
            color = "red"
        tail1D = self.ship2Direction + (135/360.0)*(2*math.pi)
        tail2D = self.ship2Direction + (225/360.0)*(2*math.pi)
        tail1X = self.ship2X + self.shipLength*math.cos(tail1D)
        tail1Y = self.ship2Y + self.shipLength*math.sin(tail1D)
        tail2X = self.ship2X + self.shipLength*math.cos(tail2D)
        tail2Y = self.ship2Y + self.shipLength*math.sin(tail2D)
        self.canvas.create_line((self.ship2X,self.ship2Y),(tail1X,tail1Y), width = 2, fill = color)
        self.canvas.create_line((self.ship2X,self.ship2Y),(tail2X,tail2Y), width = 2, fill = color)

    def drawBullets(self):
        r = self.br
        for (bx,by,dir) in self.bullets:
            self.canvas.create_oval(bx-r,by-r,bx+r,by+r, fill = "red", width = 0)
        for (bx,by,dir) in self.bullets2:
            self.canvas.create_oval(bx-r,by-r,bx+r,by+r, fill = "blue", width = 0)
        for (bx,by,dir) in self.ibullets:
            self.canvas.create_oval(bx-r,by-r,bx+r,by+r, fill = "blue", width = 0)

    
    def drawAsteroids(self):
        for (ax,ay,size,speed,dir) in self.asteroids:
            ar = 20*size
            adir = 2*math.pi*(dir/360.0)
            self.canvas.create_oval(ax-ar,ay-ar,ax+ar,ay+ar, outline = "white",
                fill = "black", width = 3)

    def drawRoundOver(self):
        w,h = self.width,self.height
        self.canvas.create_rectangle(w/2.0-300,h/2.0-200,w/2.0+300,h/2.0+200, fill = "black",
                                     outline = "white",width = 3)
        self.canvas.create_text(w/2.0,h/2.0 - 100, text= self.killedPlayer + " lost a life", font = "d 40", fill = "red")
        self.canvas.create_text(w/2.0, h/2.0+50, text = "Press 'r' to respawn", font = "d 30", fill = "white")

    def drawScore(self):
        w = self.width/2.0 - 75
        h = self.height - 20
        scoreText = "SCORE 1: %5d" % self.score
        self.canvas.create_text(w,h,text = scoreText, fill = "blue", font = "d 15")

    def drawScore2(self):
        w = self.width/2.0 + 75
        h = self.height - 20
        scoreText = "SCORE 2: %5d" % self.score2
        self.canvas.create_text(w,h,text = scoreText, fill = "blue", font = "d 15")

    def drawInvincibilityPiece(self,cx,cy,dir):
        p1 = (cx,cy-18)
        p2 = (cx-6,cy-6)
        p3 = (cx-18,cy)
        p4 = (cx-6,cy+6)
        p5 = (cx,cy+18)
        p6 = (cx+6,cy+6)
        p7 = (cx+18,cy)
        p8 = (cx+6,cy-6)
        self.canvas.create_polygon(p1,p2,p3,p4,p5,p6,p7,p8, p1, fill = "purple")

    def drawInvFlash(self):
        w,h = self.width,self.height
        secondCounter = self.invTime
        self.canvas.create_rectangle(0,0,w,h, fill = "yellow")
        self.canvas.create_text(w/2.0, h/3.0, text = str(secondCounter), font = "d 50 bold",
            fill = "black")
        self.canvas.create_text(w/2.0,h/2.0, text = "INVINCIBILITY", font = "d 50 bold",
            fill = "black")

    def drawLives(self):
        textX = 70
        textY = self.height - 50
        r = self.livesR
        self.canvas.create_text(textX,textY, text ="LIVES 1: ", fill = "blue",
            font = "d 20")
        for i in xrange(self.lives):
            cx = 150 + 40 * i
            cy = self.height - 50
            self.canvas.create_rectangle(cx-r,cy-r,cx+r,cy+r, fill = "white")
            self.canvas.create_rectangle(cx-4,cy-r,cx+4,cy+r, fill = "red", width = 0)
            self.canvas.create_rectangle(cx-r,cy-4,cx+r,cy+4, fill = "red", width = 0)

    def drawLives2(self):
        textX = self.width - 200
        textY = self.height - 50
        r = self.livesR
        self.canvas.create_text(textX,textY, text ="LIVES 2: ", fill = "blue",
            font = "d 20")
        for i in xrange(self.lives2):
            cx = self.width - 120 + 40 * i
            cy = self.height - 50
            self.canvas.create_rectangle(cx-r,cy-r,cx+r,cy+r, fill = "white")
            self.canvas.create_rectangle(cx-4,cy-r,cx+4,cy+r, fill = "red", width = 0)
            self.canvas.create_rectangle(cx-r,cy-4,cx+r,cy+4, fill = "red", width = 0)

    def drawGameOver(self):
        w,h = self.width,self.height
        self.canvas.create_rectangle(w/2.0-300,h/2.0-200,w/2.0+300,h/2.0+200, fill = "black",
                                     outline = "white",width = 3)
        self.canvas.create_text(w/2.0,h/2.0-150, text= "GAME OVER", font = "d 50", fill = "red")
        self.canvas.create_text(w/2.0, h/2.0+150, text = "Press 'r' to play again", font = "d 15", fill = "white")
        self.canvas.create_text(self.width/2.0-200,self.height/2.0 - 80,
                                fill = "white", font = "d 30",
                                text = "Scores:")
        self.canvas.create_line(self.width/2.0-280,self.height/2.0-60,
                                self.width/2.0-120,self.height/2.0-60,
                                fill = "white", width = 3)
        self.canvas.create_text(self.width/2.0-200,self.height/2.0 - 40,
                                fill = "white", font = "d 20",
                                text = self.username1 + ":")
        self.canvas.create_text(self.width/2.0-175,self.height/2.0 - 10,
                                fill = "red", font = "d 16",
                                text = str(self.score))
        self.canvas.create_text(self.width/2.0-200,self.height/2.0 + 15,
                                fill = "white", font = "d 20",
                                text = self.username2 + ":")
        self.canvas.create_text(self.width/2.0-175,self.height/2.0+45,
                                fill = "red", font = "d 16",
                                text = str(self.score2))
        self.canvas.create_text(self.width/2.0-200,self.height/2.0 + 70,
                                fill = "white", font = "d 20",
                                text = "total:")
        self.canvas.create_text(self.width/2.0-175,self.height/2.0+100,
                                fill = "red", font = "d 16",
                                text = str(self.score2+self.score))

    def drawInvincibilityItem(self,boxX,boxY):
        if self.itemDrawCounter == 0:
            self.startedItemCounter = time.time()
            self.itemDrawCounter += 1
        self.drawInvincibilityPiece(boxX,boxY, None)
        elapsedTime = int(time.time() - self.startedItemCounter)
        secondsLeft = self.invTime - elapsedTime % self.invTime
        self.canvas.create_text(boxX,boxY, text = str(secondsLeft), font = "d 15",
            fill = "white")

    def drawItem(self):
        w,h = self.width,self.height
        textX = 50
        textY = 50
        self.canvas.create_text(textX,textY, text = "ITEM:", fill = "blue", font = "d 20")
        boxX = 130
        boxY = 50
        ir = self.itemr
        self.canvas.create_rectangle(boxX-ir,boxY-ir,boxX+ir,boxY+ir, outline = "blue",
            width = "3")
        if self.invincibleBitches == True:
            self.drawInvincibilityItem(boxX,boxY)
        elif self.invincibleBitches2 == False:
            self.itermDrawCounter = 0

    def drawItem2(self):
        w,h = self.width,self.height
        textX = w - 150
        textY = 50
        self.canvas.create_text(textX,textY, text = "ITEM:", fill = "blue", font = "d 20")
        boxX = w - 70
        boxY = 50
        ir = self.itemr
        self.canvas.create_rectangle(boxX-ir,boxY-ir,boxX+ir,boxY+ir, outline = "blue",
            width = "3")
        if self.invincibleBitches2 == True:
            self.drawInvincibilityItem(boxX,boxY)
        elif self.invincibleBitches == False:
            self.itemDrawCounter = 0

    def drawStartScreen(self):
        w,h = self.width,self.height
        self.startButtonX = w/2.0
        self.startButtonY = h/2.0 + 20
        self.canvas.create_rectangle(w/2.0-200,h/2.0-200,w/2.0+200,h/2.0+200, outline = "white",
            width = 3, fill = "black")
        self.canvas.create_text(w/2.0, h/2.0 - 150, text = "ASTEROIDS", fill = "white",
            font = "d 30")
        boxX,boxY = self.startButtonX,self.startButtonY-70
        self.canvas.create_rectangle(boxX-70,boxY-30,boxX+70,boxY+30, outline = "white",
            width = 3)
        self.canvas.create_text(boxX,boxY, text = "Solo-Mode", fill = "white",
            font = "d 17")
        boxX,boxY = self.startButtonX,self.startButtonY
        self.canvas.create_rectangle(boxX-70,boxY-30,boxX+70,boxY+30, outline = "white",
            width = 3)
        self.canvas.create_text(boxX,boxY, text = "2-Player", fill = "white",
            font = "d 17")
        boxX,boxY = self.startButtonX,self.startButtonY+70
        self.canvas.create_rectangle(boxX-70,boxY-30,boxX+70,boxY+30, outline = "white",
            width = 3)
        self.canvas.create_text(boxX,boxY, text = "Instructions", fill = "white",
            font = "d 17")

    def drawBadGuy(self,bx,by,bdir):
        br = self.badGuyRadius
        self.canvas.create_oval(bx-br,by-br,bx+br,by+br, fill = "black",
            width = 2, outline = "white")
        self.canvas.create_oval(bx-25,by-5,bx+25,by+5, fill = "black",
            width = 2, outline = "white")

    def drawBadGuyBullets(self):
        br = self.br
        if len(self.badGuyBullets) > 0:
            for (bx,by,bdir,bV) in self.badGuyBullets:
                self.canvas.create_oval(bx-br,by-br,bx+br,by+br, fill = "green", width = 0)

    def drawSSBar(self):
        w,h = self.width,self.height
        x = self.SSbarXLength + 20
        y = self.height - self.SSBarYLength - 100
        self.canvas.create_rectangle(x,y,x + self.SSbarXLength,y+self.SSBarYLength, fill = "blue",
            width = 10, outline = "blue")
        self.canvas.create_rectangle(x,y,x + self.SSbarXLength,y+self.SSBarYLength, fill = "grey")
        powerY = y + self.SSBarYLength -  self.SSBarYLength*(float(self.SSPointCounter)/self.SSPointsNeeded)
        self.canvas.create_rectangle(x,powerY,x+self.SSbarXLength,y+self.SSBarYLength, fill = "red")
        if self.SSTurnedOn:
            timeLeft = self.SSTimeRetained - self.SSelapsedTime
            self.canvas.create_text(w/2.0,h/2.0, text = str(timeLeft), fill = "red", 
                font = "d 100 bold")
            if self.totalTime % 150 == 0:
                self.canvas.create_rectangle(x,powerY,x+self.SSbarXLength,y+self.SSBarYLength, fill = "yellow")

    def drawSSBar2(self):
        w,h = self.width,self.height
        x = self.width - self.SSbarXLength - 20
        y = self.height - self.SSBarYLength - 100
        self.canvas.create_rectangle(x,y,x + self.SSbarXLength,y+self.SSBarYLength, fill = "blue",
            width = 10, outline = "blue")
        self.canvas.create_rectangle(x,y,x + self.SSbarXLength,y+self.SSBarYLength, fill = "grey")
        powerY = y + self.SSBarYLength -  self.SSBarYLength*(float(self.SSPointCounter2)/self.SSPointsNeeded2)
        self.canvas.create_rectangle(x,powerY,x+self.SSbarXLength,y+self.SSBarYLength, fill = "red")
        if self.SSTurnedOn2:
            timeLeft = self.SSTimeRetained - self.SSelapsedTime2
            self.canvas.create_text(w/2.0,h/2.0, text = str(timeLeft), fill = "red", 
                font = "d 100 bold")
            if self.totalTime % 150 == 0:
                self.canvas.create_rectangle(x,powerY,x+self.SSbarXLength,y+self.SSBarYLength, fill = "yellow")

    def drawAcceleration(self):
        if self.accelerating:
            accelL = random.choice([1.8,2,2.2,3])
            color1 = random.choice(self.acceleratingColors)
            color2 = random.choice(self.acceleratingColors)
            color3 = random.choice(self.acceleratingColors)
            if self.invincibleBitches:
                color1 = random.choice(self.invColors)
                color2 = random.choice(self.invColors)
                color3 = random.choice(self.invColors)
            p4X = self.shipX % (self.width - self.shipLength)
            p4Y = self.shipY % (self.height - self.shipLength)
            p1D = self.shipDirection + (135/360.0)*(2*math.pi)
            p2D = self.shipDirection + (225/360.0)*(2*math.pi)
            p3D = self.shipDirection + (.5)*(2*math.pi)
            p1X = self.shipX + (self.shipLength/1.5)*math.cos(p1D)
            p1Y = self.shipY + (self.shipLength/1.5)*math.sin(p1D)
            p2X = self.shipX + (self.shipLength/1.5)*math.cos(p2D)
            p2Y = self.shipY + (self.shipLength/1.5)*math.sin(p2D)
            p3X = self.shipX + self.shipLength*accelL*math.cos(p3D)
            p3Y = self.shipY + self.shipLength*accelL*math.sin(p3D)
            p5X = self.shipX + self.shipLength*1.5*math.cos(p3D)
            p5Y = self.shipY + self.shipLength*1.5*math.sin(p3D)
            p6X = self.shipX + self.shipLength*1.2*math.cos(p3D)
            p6Y = self.shipY + self.shipLength*1.2*math.sin(p3D)
            self.canvas.create_polygon((p4X,p4Y),(p2X,p2Y),(p3X,p3Y),(p1X,p1Y),
                fill = color1)
            self.canvas.create_polygon((p4X,p4Y),(p2X,p2Y),(p5X,p5Y),(p1X,p1Y),
                fill = color2)
            self.canvas.create_polygon((p4X,p4Y),(p2X,p2Y),(p6X,p6Y),(p1X,p1Y),
                fill = color3)

    def drawAcceleration2(self):
        if self.accelerating2:
            accelL = random.choice([1.8,2,2.2,3])
            color1 = random.choice(self.acceleratingColors)
            color2 = random.choice(self.acceleratingColors)
            color3 = random.choice(self.acceleratingColors)
            if self.invincibleBitches2:
                color1 = random.choice(self.invColors)
                color2 = random.choice(self.invColors)
                color3 = random.choice(self.invColors)
            p4X = self.ship2X % (self.width - self.shipLength)
            p4Y = self.ship2Y % (self.height - self.shipLength)
            p1D = self.ship2Direction + (135/360.0)*(2*math.pi)
            p2D = self.ship2Direction + (225/360.0)*(2*math.pi)
            p3D = self.ship2Direction + (.5)*(2*math.pi)
            p1X = self.ship2X + (self.shipLength/1.5)*math.cos(p1D)
            p1Y = self.ship2Y + (self.shipLength/1.5)*math.sin(p1D)
            p2X = self.ship2X + (self.shipLength/1.5)*math.cos(p2D)
            p2Y = self.ship2Y + (self.shipLength/1.5)*math.sin(p2D)
            p3X = self.ship2X + self.shipLength*accelL*math.cos(p3D)
            p3Y = self.ship2Y + self.shipLength*accelL*math.sin(p3D)
            p5X = self.ship2X + self.shipLength*1.5*math.cos(p3D)
            p5Y = self.ship2Y + self.shipLength*1.5*math.sin(p3D)
            p6X = self.ship2X + self.shipLength*1.2*math.cos(p3D)
            p6Y = self.ship2Y + self.shipLength*1.2*math.sin(p3D)
            self.canvas.create_polygon((p4X,p4Y),(p2X,p2Y),(p3X,p3Y),(p1X,p1Y),
                fill = color1)
            self.canvas.create_polygon((p4X,p4Y),(p2X,p2Y),(p5X,p5Y),(p1X,p1Y),
                fill = color2)
            self.canvas.create_polygon((p4X,p4Y),(p2X,p2Y),(p6X,p6Y),(p1X,p1Y),
                fill = color3)

    def drawAsteroidExplosions(self):
        if len(self.asteroidExplosions) > 0:
            for i in xrange(len(self.asteroidExplosions)):
                (ax,ay,NotUsingThis) = self.asteroidExplosions[i]
                for j in xrange(random.randint(1,5)):
                    r = random.randint(5,20)
                    color = random.choice(self.acceleratingColors)
                    dx = random.randint(-10,10)
                    dy = random.randint(-10,10)
                    newX = ax + dx
                    newY = ay + dy
                    self.canvas.create_oval(newX-r,newY-r,newX+r,newY+r,fill = color,
                        width = 0)

    def drawBadGuyExplosion(self):
        completeExplosions = []
        if len(self.badGuyExplosion)>0:
            for i in xrange(len(self.badGuyExplosion)):
                (cx,cy,sizeCounter) = self.badGuyExplosion[i]
                longr = 70 - sizeCounter
                smallr = 12 - (sizeCounter/3.0)
                self.canvas.create_oval(cx-smallr,cy-longr,cx+smallr,cy+longr, outline = "red", width = 2)
                self.canvas.create_oval(cx-longr,cy-smallr,cx+longr,cy+smallr, outline = "red", width = 2)

    def drawLobbyScreen(self):
        if len(self.username1)>0:
            toptext = "Both players ready to play!"
            buttontext = "Play"
            buttoncolor = "green"
        else:
            toptext = "Waiting for player 1 to join..."
            buttontext = "Waiting..."
            buttoncolor = "grey"
        p1Color = "green" if self.p1Ready else "red"
        p2Color = "green" if self.p2Ready else "red"
        self.canvas.create_rectangle(self.width/2.0 - 300,self.height/2.0-200,
                                     self.width/2.0 + 300,self.height/2.0+200,
                                     fill = "black", outline = "white", width = 3)
        self.canvas.create_text(self.width/2.0,self.height/2.0 - 150,
                                fill = "white", font = "d 30", text=toptext)
        self.canvas.create_text(self.width/2.0-150,self.height/2.0 - 50,
                                fill = "white", font = "d 15",
                                text = "Player 1:")
        self.canvas.create_text(self.width/2.0+150,self.height/2.0 - 50,
                                fill = "white", font = "d 15",
                                text = "Player 2:")
        self.canvas.create_text(self.width/2.0-150,self.height/2.0,
                                fill = p1Color, font = "d 20",
                                text = self.username1)
        self.canvas.create_text(self.width/2.0+150,self.height/2.0,
                                fill = p2Color, font = "d 20",
                                text = self.username2)
        self.canvas.create_rectangle(self.width/2.0-100,self.height/2.0 + 100,
                                     self.width/2.0+100,self.height/2.0 + 150,
                                     width = 3, fill = buttoncolor, outline = "white")
        self.canvas.create_text(self.width/2.0, self.height/2.0 + 125,
                         fill = "black", font = "d 20", text = buttontext)
        self.canvas.create_text(self.width/2.0,self.height-30,text = "Return to Main Menu", fill = "white",
                                activefill = "yellow", font = "d 15 bold")

    def drawInstructionScreenTemplate(self):
        w,h = self.width,self.height
        prevAFill = "green" if (self.instructionPage>1) else "grey"
        nextAFill = "green" if (self.instructionPage<5) else "grey"
        self.canvas.create_rectangle(w/2.0-350,h/2.0-250,w/2.0+350,h/2.0+250, fill = "black",
                                     outline = "white",width = 3)
        self.canvas.create_text(w/2.0-280,h/2.0-220, text = "< < Previous Page", fill = "white",
                                activefill = prevAFill,font = "d 10 bold")
        self.canvas.create_text(w/2.0+280,h/2.0-220, text = "Next Page > >", fill = "white",
                                activefill = nextAFill,font = "d 10 bold")
        self.canvas.create_text(w/2.0,h/2.0-225, text = self.instructionTabs[self.instructionPage-1], fill = "white",
                                font = "d 20 bold")
        self.canvas.create_line((w/2.0-350,h/2.0+210),(w/2.0+350,h/2.0+210), fill = "white",
                                width = 3)
        self.canvas.create_line((w/2.0-210,h/2.0+210),(w/2.0-210,h/2.0+250), fill = "white",
                                width = 3)
        self.canvas.create_line((w/2.0-70,h/2.0+210),(w/2.0-70,h/2.0+250), fill = "white",
                                width = 3)
        self.canvas.create_line((w/2.0+70,h/2.0+210),(w/2.0+70,h/2.0+250), fill = "white",
                                width = 3)
        self.canvas.create_line((w/2.0+210,h/2.0+210),(w/2.0+210,h/2.0+250), fill = "white",
                                width = 3)
        self.canvas.create_text(w/2.0,h-30,text = "Return to Main Menu", fill = "white",
                                activefill = "yellow", font = "d 15 bold")
        for i in xrange(5):
            if self.instructionPage == (i+1):
                aFill = "green"
                fill = "green"
            else:
                aFill = "red"
                fill = "white"
            self.canvas.create_text(w/2.0 - 280 +(i*140),h/2.0+230, text = self.instructionTabs[i], fill = fill,
                                    activefill = aFill,font = "d 15 bold")

    def drawInstructionPage1(self):
        self.drawInstructionScreenTemplate()
        self.canvas.create_text(self.width/2.0-330,self.height/2.0-200, text = """
  Asteroids is a space-based shooting game where you control a spaceship and defend your
           ship from destruction as asteroids come pummeling towards you in outerspace.


    Shoot Asteroids to                                                            And try to avoid Alien
    avoid getting hit                                                                         SpaceShips








    Grab Invincibility Boosters                                             Get enough points and
                                                                                            you can use a super shooter
""", fill = "white",anchor = NW, font = "d 12")

    def drawInstructionPage2(self):
        self.drawInstructionScreenTemplate()
        self.canvas.create_text(self.width/2.0-330,self.height/2.0-200, text ="""
Press the SpaceBar to shoot bullets""", fill = "white", anchor = NW, font = "d 30")
        self.canvas.create_text(self.width/2.0,self.height/2.0+150, text ="Try it out!", fill = "white", font = "d 25")

    def drawInstructionPage3(self):
        self.drawInstructionScreenTemplate()
        self.canvas.create_text(self.width/2.0,self.height/2.0, text ="""
Use the arrow keys to move around the map.
              Up makes you accelerate.
           Left and Right are used to turn""", fill = "white", font = "d 25")

    def drawInstructionPage4(self):
        self.drawInstructionScreenTemplate()
        self.canvas.create_text(self.width/2.0,self.height/2.0-50, text ="""
Survive for as long as you can and rack up as many points as possible.
You will have 3 lives and the game is over when you use all 3 of them.""", fill = "white", font = "d 15")

    def drawInstructionPage5(self):
        self.drawInstructionScreenTemplate()
        self.canvas.create_text(self.width/2.0,self.height/2.0-75, text ="""
Create a username and play with another friend in a cooperative game.
You will each start out with 3 lives. After someone loses 3 lives, the
round is over. Try to reach the highest possible combined score or just
                     try and get more points than your friend!""", fill = "white", font = "d 15")

    def drawInstructionScreen(self):
        w,h = self.width,self.height
        if self.instructionPage == 1:
            self.drawInstructionPage1()
            self.asteroids = [[w/2.0-300,h/2.0,1,0,0],
                              [w/2.0-250,h/2.0,2,0,0],
                              [w/2.0-200,h/2.0,3,0,0]]
            self.badGuy = [[self.ibgX,self.ibgY,0]]
            self.drawInvincibilityItem(w/2.0-275,h/2.0+150)
            self.accelerating = True
            self.invincibleBitches = True
            self.shipX,self.shipY = self.width/2.0-175,self.height/2.0+150
            self.drawAsteroids()
            self.drawBadGuy(*self.badGuy[0])
            self.drawShip()
            self.drawAcceleration()
        else:
            self.asteroids = []
            self.badGuy = []
            self.invincibility = []
            self.accelerating = False
            self.invincibleBitches = False
            self.shipX,self.shipY = self.width/2.0,self.height/2.0
            self.shipDirection = 0
        if self.instructionPage == 2:
            self.drawInstructionPage2()
            self.shipX,self.shipY = self.width/2.0-200,self.height/2.0
            self.drawShip()
            self.drawBullets()
        else:
            self.shipX,self.shipY = self.width/2.0,self.height/2.0
            self.ibullets = []
        if self.instructionPage == 3:
            self.drawInstructionPage3()
        elif self.instructionPage == 4:
            self.drawInstructionPage4()
        elif self.instructionPage == 5:
            self.drawInstructionPage5()

    def redrawAll(self):
        self.drawBackground()
        self.drawAsteroids()
        if self.instructionScreen:
            self.drawInstructionScreen()
        elif self.startScreen == True:
            self.drawStartScreen()
        elif self.lobbyScreen:
            self.drawLobbyScreen()
        elif self.gameOver == True:
            self.drawGameOver()
        else:
            self.drawScore()
            self.drawScore2()
            self.drawLives()
            self.drawLives2()
            self.drawItem()
            self.drawItem2()
            self.drawSSBar()
            self.drawSSBar2()
            self.drawShip()
            self.drawShip2()
            self.drawAcceleration()
            self.drawAcceleration2()
            self.drawBullets()
            self.drawBadGuyBullets()
            self.drawBadGuyExplosion()
            self.drawAsteroidExplosions()
            if len(self.invincibility) > 0:
                self.drawInvincibilityPiece(*self.invincibility[0])
            if len(self.badGuy) > 0:
                self.drawBadGuy(*self.badGuy)
            if self.invincibleBitches2:
                if (self.invFlashCounter < 50) and (self.invFlashCounter%3 == 0):
                    self.drawInvFlash()
                self.invFlashCounter += 1
            if self.roundOver == True:
                self.drawRoundOver()

    def createAsteroid(self):
        if random.randint(0,3) == 1:
            x = random.choice(self.xcoords)
            y = random.randint(self.ycoords[0],self.ycoords[1])
        else:
            x = random.randint(self.xcoords[0],self.xcoords[1])
            y = random.choice(self.ycoords)
        size = random.choice(self.astSizes)
        dir = random.randint(self.dirs[0],self.dirs[1])
        speed = random.choice(self.speeds)
        return [x,y,size,speed,dir]

    def initAsteroids(self):
        self.xcoords = [0,self.width]
        self.ycoords = [0,self.height]
        self.astSizes = [1,2,3]
        self.dirs = [0,360]
        self.speeds = [1,2,3]
        self.asteroids = []
        self.asteroidExplosions = []
        for i in xrange(random.randint(1,4)):
            newRoid = self.createAsteroid()
            self.asteroids.append(newRoid)

    def initLives(self):
        self.lives = 3
        self.lives2 = 3
        self.livesR = 15

    def initScores(self):
        self.score = 0
        self.score2 = 0
        self.scores = [None, 100, 50, 25]

    def initInvincibility(self):
        self.inV = 3
        self.invFlashCounter = 0
        self.invStopCounter = 0
        self.invTime = 10
        self.invColors = ["red","blue","yellow","orange","green","purple"]

    def initShip(self):
        self.shipX = self.width/2.0
        self.shipY = self.height/2.0
        self.shipLength = 20
        self.shipDirection = 0
        self.movesLeft,self.movesRight = 0,0
        self.acceleratingColors = ["red","orange","yellow"]

    def initShip2(self):
        self.ship2X = self.width/2.0
        self.ship2Y = self.height/2.0
        self.shipLength = 20
        self.ship2Direction = 0
        self.movesLeft2,self.movesRight2 = 0,0
        self.acceleratingColors = ["red","orange","yellow"]

    def initStartScreenStuff(self):
        w,h = self.width,self.height
        self.startButtonX = w/2.0
        self.startButtonY = h/2.0 + 20

    def initBadGuy(self):
        self.badGuyRadius = 10
        self.badGuyV = 5

    def initSuperShooter(self):
        self.SSPointsNeeded = 2000
        self.SSTimeRetained = 10 #milliseconds
        self.SSBarYLength = 300
        self.SSbarXLength = 20

    def initUselessVals(self):
        self.startScreen = None
        self.roundOver = None
        self.SSTurnedOn = None
        self.SSelapsedTime = None
        self.SSPointCounter = None
        self.asteroids = None
        self.asteroidExplosions = None
        self.bullets = None
        self.bullets2 = None
        self.shipX = None
        self.shipY = None
        self.ship2X = None
        self.ship2Y = None
        self.accelerating = None
        self.accelerating2 = None
        self.badGuy = None
        self.startBadGuyShooting = None
        self.badGuyBullets = None
        self.badGuyExplosion = None
        self.invincibility = None
        self.invincibility2 = None
        self.invincibleBitches = None
        self.gameOver = None
        self.starLocations = []

    def initInstructions(self):
        self.instructionScreen = False
        self.instructionPage = 1
        self.instructionTabs = ["Asteroids","Shooting","Movement","Solo-Mode","2-Player"]
        self.ibgX,self.ibgY = self.width/2.0+250,self.height/2.0
        self.ibgV = -3
        self.ibullets = []

    def init(self):
        self.initShip()
        self.initInstructions()
        self.killedPlayer = ""
        self.creatingUserName = False
        self.timeSpent = 0
        self.totalTime = 0
        self.br = 4
        self.bulletV = 13
        self.itemr = 25
        self.itemDrawCounter = 0
        self.startTime = time.time()
        self.sl = 5
        self.initAsteroids()
        self.initInvincibility()
        self.initStartScreenStuff()
        self.initSuperShooter()
        self.initUselessVals()

    def initLobbyScreen(self):
        self.lobbyScreen = True
        self.username1 = ""
        self.username2 = ""
        self.p1Ready = False
        self.p2Ready = False

    def __init__(self):
        self.initLives()
        self.initScores()
        self.initBadGuy()
        self.initLobbyScreen()
        self.contactServer("startGame.noData")

    def updateGameState(self, gameState):
        pass

Asteroids().run()
