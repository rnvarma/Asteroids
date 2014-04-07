#!/usr/bin/env python 

import socket,math, time, random
from Tkinter import *

def parseData(data):
	action = ""
	i = 0
	while data[i] != ".":
		action += data[i]
		i += 1
	message = data[i+1:]
	return action,message

class Asteroids(object):
    def airResistance(self):
        if self.velocity >1:
            if self.timeSpent % 200 == 0:
                self.velocity /= 1.2
                self.timeSpent = 0
                if self.velocity <1:
                    self.velocity = 1

    def airResistance2(self):
        if self.velocity2 >1:
            if self.timeSpent2 % 200 == 0:
                self.velocity2 /= 1.2
                self.timeSpent2 = 0
                if self.velocity2 <1:
                    self.velocity2 = 1

    def moveBullets(self):
        for i in xrange(len(self.bullets)):
            self.bullets[i][0] += self.bulletV*math.cos(self.bullets[i][2])
            self.bullets[i][1] += self.bulletV*math.sin(self.bullets[i][2])
            self.bullets[i][0] = round(self.bullets[i][0],3)
            self.bullets[i][1] = round(self.bullets[i][1],3)
        for i in xrange(len(self.bullets2)):
            self.bullets2[i][0] += self.bulletV*math.cos(self.bullets2[i][2])
            self.bullets2[i][1] += self.bulletV*math.sin(self.bullets2[i][2])
            self.bullets2[i][0] = round(self.bullets2[i][0],3)
            self.bullets2[i][1] = round(self.bullets2[i][1],3)

    def removeBullets(self):
        exitedBullets = []
        if len(self.bullets)>5:
            for i in xrange(len(self.bullets)):
                (bx,by,dir) = self.bullets[i]
                if bx<0 or by<0 or by>self.height or bx>self.width:
                    exitedBullets.append(i)
            for i in exitedBullets[::-1]:
                self.bullets.pop(i)
        exitedBullets = []
        if len(self.bullets2)>5:
            for i in xrange(len(self.bullets2)):
                (bx,by,dir) = self.bullets2[i]
                if bx<0 or by<0 or by>self.height or bx>self.width:
                    exitedBullets.append(i)
            for i in exitedBullets[::-1]:
                self.bullets2.pop(i)
        exitedBullets = []
        if len(self.badGuyBullets)>4:
            for i in xrange(len(self.badGuyBullets)):
                (bx,by,dir, bV) = self.badGuyBullets[i]
                if bx<0 or by<0 or by>self.height or bx>self.width:
                    exitedBullets.append(i)
            for i in exitedBullets[::-1]:
                self.badGuyBullets.pop(i)

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

    def moveAsteroids(self):
        for i in xrange(len(self.asteroids)):
            dir = 2*math.pi*(self.asteroids[i][-1]/360.0)
            asteroidV = self.asteroids[i][-2]*1.5
            asize = self.asteroids[i][2] * 20
            self.asteroids[i][0] = round((self.asteroids[i][0] + asteroidV*math.cos(dir)) % (self.width + asize),3)
            self.asteroids[i][1] = round((self.asteroids[i][1] + asteroidV*math.sin(dir)) % (self.height + asize),3)

    def hitAsteroids(self):
        br = self.br
        popBullets = []
        popAsteroids = []
        for i in xrange(len(self.bullets)):
            (bx,by,bdir) = self.bullets[i]
            for j in xrange(len(self.asteroids)):
                (ax,ay,asize,aspeed,adir) = self.asteroids[j]
                ar = asize*20
                if ((ax+ar)>(bx-br) and (ax-ar)<(bx-br) and ((by-ar)<ay<(by+ar))) or(
                    (ax-ar)<(bx+br) and (ax+ar)>(bx+br) and ((by-ar)<ay<(by+ar))) or(
                    (ay+ar)>(by-br) and (ay-ar)<(by-br) and ((bx-ar)<ax<(bx+ar))) or(
                    (ay-ar)<(by+br) and (ay+ar)>(by+br) and ((bx-ar)<ax<(bx+ar))):
                    popBullets.append(i)
                    popAsteroids.append((ax,ay,asize,j))
                    self.score += self.scores[asize]
        for i in popBullets[::-1]:
            if len(self.bullets)>i:
                self.bullets.pop(i)
        for (ax,ay,asize,j) in popAsteroids:
            if len(self.asteroids)>j:
                self.asteroids.pop(j)
                self.asteroidExplosions.append([ax,ay,10])
            if asize >1:
                dir1 = random.randint(self.dirs[0],self.dirs[1])
                dir2 = random.randint(self.dirs[0],self.dirs[1])
                size = asize - 1
                speed1 = random.choice(self.speeds)
                speed2 = random.choice(self.speeds)
                self.asteroids.append([ax,ay,size,speed1,dir1])
                self.asteroids.append([ax,ay,size,speed2,dir2])

    def hitAsteroids2(self):
        br = self.br
        popBullets = []
        popAsteroids = []
        for i in xrange(len(self.bullets2)):
            (bx,by,bdir) = self.bullets2[i]
            for j in xrange(len(self.asteroids)):
                (ax,ay,asize,aspeed,adir) = self.asteroids[j]
                ar = asize*20
                if ((ax+ar)>(bx-br) and (ax-ar)<(bx-br) and ((by-ar)<ay<(by+ar))) or(
                    (ax-ar)<(bx+br) and (ax+ar)>(bx+br) and ((by-ar)<ay<(by+ar))) or(
                    (ay+ar)>(by-br) and (ay-ar)<(by-br) and ((bx-ar)<ax<(bx+ar))) or(
                    (ay-ar)<(by+br) and (ay+ar)>(by+br) and ((bx-ar)<ax<(bx+ar))):
                    popBullets.append(i)
                    popAsteroids.append((ax,ay,asize,j))
                    self.score2 += self.scores[asize]
        for i in popBullets[::-1]:
            if len(self.bullets2)>i:
                self.bullets2.pop(i)
        for (ax,ay,asize,j) in popAsteroids:
            if len(self.asteroids)>j:
                self.asteroids.pop(j)
                self.asteroidExplosions.append([ax,ay,10])
            if asize >1:
                dir1 = random.randint(self.dirs[0],self.dirs[1])
                dir2 = random.randint(self.dirs[0],self.dirs[1])
                size = asize - 1
                speed1 = random.choice(self.speeds)
                speed2 = random.choice(self.speeds)
                self.asteroids.append([ax,ay,size,speed1,dir1])
                self.asteroids.append([ax,ay,size,speed2,dir2])

    def killAsteroidExplosions(self):
        completeExplosions = []
        if len(self.asteroidExplosions)>0:
            for i in xrange(len(self.asteroidExplosions)):
                self.asteroidExplosions[i][-1] -= 1
                if self.asteroidExplosions[i][-1] < 1:
                    completeExplosions.append(i)
            for k in completeExplosions[::-1]:
                self.asteroidExplosions.pop(k)

    def addAsteroids(self):
        randlowlim = random.randint(1,self.asteroidLowLim)
        if len(self.asteroids) <= randlowlim:
            randnewnum = randlowlim * random.choice([1,2])
            for i in xrange(randnewnum):
                newRoid = self.createAsteroid()
                self.asteroids.append(newRoid)

    def moveStars(self):
        self.starV = self.velocity
        for i in xrange(len(self.starLocations)):
            self.starLocations[i][0] += self.starV*math.cos(self.shipDirection)*(-1)
            self.starLocations[i][1] += self.starV*math.sin(self.shipDirection)*(-1)
            self.starLocations[i][0] = round(self.starLocations[i][0],3)
            self.starLocations[i][1] = round(self.starLocations[i][1],3)

    def removeAndAddStars(self):
        starRemoves = []
        for i in xrange(len(self.starLocations)):
            if (self.starLocations[i][0] - self.sl) > self.width:
                cx = 0
                cy = random.randrange(self.height)
                starRemoves.append((i,cx,cy))
            elif (self.starLocations[i][0] + self.sl) < 0:
                cx = self.width
                cy = random.randrange(self.height)
                starRemoves.append((i,cx,cy))
            elif (self.starLocations[i][1] - self.sl) > self.height:
                cx = random.randrange(self.width)
                cy = 0
                starRemoves.append((i,cx,cy))
            elif (self.starLocations[i][1] + self.sl) < 0:
                cx = random.randrange(self.width)
                cy = self.height
                starRemoves.append((i,cx,cy))
        for (i,cx,cy) in starRemoves[::-1]:
            self.starLocations.pop(i)
            self.starLocations.append([cx,cy])

    def createInvincibility(self):
        spawnTime = random.randint(10,15) * 1000
        if len(self.invincibility) == 0 and (self.invincibleBitches or self.invincibleBitches2):
            self.invTotalTime = 0
        if (self.invTotalTime > spawnTime) and (len(self.invincibility) == 0) and self.invTotalTime !=0:
            self.invTotalTime = 0
            cx = random.randrange(self.width)
            cy = random.randrange(self.height)
            dir = random.randrange(360)
            self.invincibility.append([cx,cy,dir])

    def moveInvincibility(self):
        if len(self.invincibility) > 0:
            (ix,iy,idir) = self.invincibility[0]
            self.invincibility[0][0] = (self.invincibility[0][0] + self.inV*math.cos((idir/360.0)*math.pi*2)) % self.width
            self.invincibility[0][1] = (self.invincibility[0][1] + self.inV*math.sin((idir/360.0)*math.pi*2)) % self.height

    def hitInvincibility(self):
        if len(self.invincibility) > 0:
            (ix,iy,idir) = self.invincibility[0]
            sx,sy = self.shipX,self.shipY
            ar = 18
            br = 5
            if ((ix+ar)>(sx-br) and (ix-ar)<(sx-br) and ((sy-ar)<iy<(sy+ar))) or(
                (ix-ar)<(sx+br) and (ix+ar)>(sx+br) and ((sy-ar)<iy<(sy+ar))) or(
                (iy+ar)>(sy-br) and (iy-ar)<(sy-br) and ((sx-ar)<ix<(sx+ar))) or(
                (iy-ar)<(sy+br) and (iy+ar)>(sy+br) and ((sx-ar)<ix<(sx+ar))):
                self.invincibleBitches = True
                self.invincibility.pop()
            
    def hitInvincibility2(self):
        if len(self.invincibility) > 0:
            (ix,iy,idir) = self.invincibility[0]
            sx,sy = self.ship2X,self.ship2Y
            ar = 18
            br = 5
            if ((ix+ar)>(sx-br) and (ix-ar)<(sx-br) and ((sy-ar)<iy<(sy+ar))) or(
                (ix-ar)<(sx+br) and (ix+ar)>(sx+br) and ((sy-ar)<iy<(sy+ar))) or(
                (iy+ar)>(sy-br) and (iy-ar)<(sy-br) and ((sx-ar)<ix<(sx+ar))) or(
                (iy-ar)<(sy+br) and (iy+ar)>(sy+br) and ((sx-ar)<ix<(sx+ar))):
                self.invincibleBitches2 = True
                self.invincibility.pop()

    def shipHitAsteroid(self):
        for (ax,ay,asize,aspeed,adir) in self.asteroids:
            sx,sy = self.shipX,self.shipY
            ar = asize*20
            br = 5
            if ((ax+ar)>(sx-br) and (ax-ar)<(sx-br) and ((sy-ar)<ay<(sy+ar))) or(
                (ax-ar)<(sx+br) and (ax+ar)>(sx+br) and ((sy-ar)<ay<(sy+ar))) or(
                (ay+ar)>(sy-br) and (ay-ar)<(sy-br) and ((sx-ar)<ax<(sx+ar))) or(
                (ay-ar)<(sy+br) and (ay+ar)>(sy+br) and ((sx-ar)<ax<(sx+ar))):
                    return True
        return False

    def shipHitAsteroid2(self):
        for (ax,ay,asize,aspeed,adir) in self.asteroids:
            sx,sy = self.ship2X,self.ship2Y
            ar = asize*20
            br = 5
            if ((ax+ar)>(sx-br) and (ax-ar)<(sx-br) and ((sy-ar)<ay<(sy+ar))) or(
                (ax-ar)<(sx+br) and (ax+ar)>(sx+br) and ((sy-ar)<ay<(sy+ar))) or(
                (ay+ar)>(sy-br) and (ay-ar)<(sy-br) and ((sx-ar)<ax<(sx+ar))) or(
                (ay-ar)<(sy+br) and (ay+ar)>(sy+br) and ((sx-ar)<ax<(sx+ar))):
                    return True
        return False

    def stopInvincibility(self):
        if self.invincibleBitches or self.invincibleBitches2:
            if self.invStopCounter == 0:
                self.invStartTime = time.time()
                self.invStopCounter +=1
            elapsedTime = int(time.time() - self.invStartTime)
            if elapsedTime > self.invTime:
                self.invincibleBitches = False
                self.invincibleBitches2 = False
                self.invStopCounter = 0
                self.itemDrawCounter = 0
                self.invFlashCounter = 0

    def spawnBadGuy(self):
        if len(self.badGuySpawnScores) > 0:
            if (self.score+self.score2) > self.badGuySpawnScores[0]:
                self.badGuySpawnScores.pop(0)
                (bx,by,bsize,bspeed,bdir) = self.createAsteroid()
                self.badGuy.extend([bx,by,bdir])
                self.startBadGuyShooting = True

    def moveBadGuy(self):
        if len(self.badGuy) > 0:
            (bx,by,bdir) = self.badGuy
            self.badGuy[0] = (self.badGuy[0] + self.badGuyV*math.cos((bdir/360.0)*math.pi*2)) % self.width
            self.badGuy[1] = (self.badGuy[1] + self.badGuyV*math.sin((bdir/360.0)*math.pi*2)) % self.height

    def badGuyShoot(self):
        if len(self.badGuy)>0:
            if self.startBadGuyShooting == True:
                self.badGuyShootStart = time.time()
                self.startBadGuyShooting = False
            elapsedTime = int(time.time() - self.badGuyShootStart)
            if elapsedTime>self.badGuyBulletCount:
                self.badGuyBulletCount += 1
                (bx,by,bdir) = self.badGuy
                (sx,sy,sdir,sV) = (self.shipX,self.shipY,self.shipDirection,self.velocity)
                bulletV = 7
                bulletDir = math.atan((sy - by)/(sx - bx))
                if (sx - bx) < 0: 
                    bulletDir += (math.pi)
                self.badGuyBullets.append([bx,by,bulletDir,bulletV])

    def moveBadGuyBullets(self):
        for i in xrange(len(self.badGuyBullets)):
            bdir = self.badGuyBullets[i][2]
            bV = self.badGuyBullets[i][-1]
            self.badGuyBullets[i][0] += bV*math.cos(bdir)
            self.badGuyBullets[i][1] += bV*math.sin(bdir)
            self.badGuyBullets[i][0] = round(self.badGuyBullets[i][0],3)
            self.badGuyBullets[i][1] = round(self.badGuyBullets[i][1],3)

    def shipHitBadGuyBullet(self):
        if len(self.badGuyBullets)>0:
            for (bx,by,bdir,bV) in self.badGuyBullets:
                br = self.br
                sr = 5
                sx,sy = self.shipX, self.shipY
                if ((bx+br)>(sx-sr) and (bx-br)<(sx-sr) and ((sy-br)<by<(sy+br))) or(
                    (bx-br)<(sx+sr) and (bx+br)>(sx+sr) and ((sy-br)<by<(sy+br))) or(
                    (by+br)>(sy-sr) and (by-br)<(sy-sr) and ((sx-br)<bx<(sx+br))) or(
                    (by-br)<(sy+sr) and (by+br)>(sy+sr) and ((sx-br)<bx<(sx+br))):
                    return True
                return False

    def shipHitBadGuyShip(self):
        if len(self.badGuy)>0:
            (bx,by,bdir) = self.badGuy
            sx,sy = self.shipX,self.shipY
            br = self.badGuyRadius
            sr = 5
            if ((bx+br)>(sx-sr) and (bx-br)<(sx-sr) and ((sy-br)<by<(sy+br))) or(
                (bx-br)<(sx+sr) and (bx+br)>(sx+sr) and ((sy-br)<by<(sy+br))) or(
                (by+br)>(sy-sr) and (by-br)<(sy-sr) and ((sx-br)<bx<(sx+br))) or(
                (by-br)<(sy+sr) and (by+br)>(sy+sr) and ((sx-br)<bx<(sx+br))):
                return True
            return False

    def shipHitBadGuyBullet2(self):
        if len(self.badGuyBullets)>0:
            for (bx,by,bdir,bV) in self.badGuyBullets:
                br = self.br
                sr = 5
                sx,sy = self.ship2X, self.ship2Y
                if ((bx+br)>(sx-sr) and (bx-br)<(sx-sr) and ((sy-br)<by<(sy+br))) or(
                    (bx-br)<(sx+sr) and (bx+br)>(sx+sr) and ((sy-br)<by<(sy+br))) or(
                    (by+br)>(sy-sr) and (by-br)<(sy-sr) and ((sx-br)<bx<(sx+br))) or(
                    (by-br)<(sy+sr) and (by+br)>(sy+sr) and ((sx-br)<bx<(sx+br))):
                    return True
                return False

    def shipHitBadGuyShip2(self):
        if len(self.badGuy)>0:
            (bx,by,bdir) = self.badGuy
            sx,sy = self.ship2X,self.ship2Y
            br = self.badGuyRadius
            sr = 5
            if ((bx+br)>(sx-sr) and (bx-br)<(sx-sr) and ((sy-br)<by<(sy+br))) or(
                (bx-br)<(sx+sr) and (bx+br)>(sx+sr) and ((sy-br)<by<(sy+br))) or(
                (by+br)>(sy-sr) and (by-br)<(sy-sr) and ((sx-br)<bx<(sx+br))) or(
                (by-br)<(sy+sr) and (by+br)>(sy+sr) and ((sx-br)<bx<(sx+br))):
                return True
            return False
   
    def shipHitBadGuy(self):
        if self.shipHitBadGuyShip() or self.shipHitBadGuyBullet():
            return True
        return False

    def shipHitBadGuy2(self):
        if self.shipHitBadGuyShip2() or self.shipHitBadGuyBullet2():
            return True
        return False

    def hitBadGuy(self):
        br = self.br
        for i in xrange(len(self.bullets)):
            (bx,by,bdir) = self.bullets[i]
            if len(self.badGuy)>0:
                (ax,ay,adir) = self.badGuy
                ar = self.badGuyRadius
                if ((ax+ar)>(bx-br) and (ax-ar)<(bx-br) and ((by-ar)<ay<(by+ar))) or(
                    (ax-ar)<(bx+br) and (ax+ar)>(bx+br) and ((by-ar)<ay<(by+ar))) or(
                    (ay+ar)>(by-br) and (ay-ar)<(by-br) and ((bx-ar)<ax<(bx+ar))) or(
                    (ay-ar)<(by+br) and (ay+ar)>(by+br) and ((bx-ar)<ax<(bx+ar))):
                    self.bullets.pop(i)
                    self.badGuy = []
                    self.score += 1000
                    self.badGuyExplosion.append([ax,ay,40])
                    self.asteroidExplosions.append([ax,ay,30])
                    break

    def hitBadGuy2(self):
        br = self.br
        for i in xrange(len(self.bullets2)):
            (bx,by,bdir) = self.bullets2[i]
            if len(self.badGuy)>0:
                (ax,ay,adir) = self.badGuy
                ar = self.badGuyRadius
                if ((ax+ar)>(bx-br) and (ax-ar)<(bx-br) and ((by-ar)<ay<(by+ar))) or(
                    (ax-ar)<(bx+br) and (ax+ar)>(bx+br) and ((by-ar)<ay<(by+ar))) or(
                    (ay+ar)>(by-br) and (ay-ar)<(by-br) and ((bx-ar)<ax<(bx+ar))) or(
                    (ay-ar)<(by+br) and (ay+ar)>(by+br) and ((bx-ar)<ax<(bx+ar))):
                    self.bullets2.pop(i)
                    self.badGuy = []
                    self.score2 += 1000
                    self.badGuyExplosion.append([ax,ay,40])
                    self.asteroidExplosions.append([ax,ay,30])
                    break

    def killBadGuyExplosion(self):
        completeExplosions = []
        if len(self.badGuyExplosion)>0:
            for i in xrange(len(self.badGuyExplosion)):
                self.badGuyExplosion[i][-1] -= 1
                if self.badGuyExplosion[i][-1] < 1:
                    completeExplosions.append(i)
            for k in completeExplosions[::-1]:
                self.badGuyExplosion.pop(i)

    def operateSS(self):
        if self.SSTurnedOn == False:
            self.SSPointCounter = self.score - self.SSPointStartCount
            if self.SSPointCounter >= self.SSPointsNeeded:
                self.SSPointCounter = self.SSPointsNeeded
                self.SSTurnedOn = True
        elif self.SSTurnedOn:
            if self.SSJustTurnedOn:
                self.SStimer = time.time()
                self.SSJustTurnedOn = False
            elapsedTime = int(time.time() - self.SStimer)
            self.SSelapsedTime = elapsedTime
            if self.SSelapsedTime >= self.SSTimeRetained:
                self.SSJustTurnedOn = True
                self.SSTurnedOn = False
                self.SSPointCounter = 0
                self.SSPointStartCount = self.score
                self.SSPointsNeeded *= 2

    def operateSS2(self):
        if self.SSTurnedOn2 == False:
            self.SSPointCounter2 = self.score2 - self.SSPointStartCount2
            if self.SSPointCounter2 >= self.SSPointsNeeded2:
                self.SSPointCounter2 = self.SSPointsNeeded2
                self.SSTurnedOn2 = True
        elif self.SSTurnedOn2:
            if self.SSJustTurnedOn2:
                self.SStimer2 = time.time()
                self.SSJustTurnedOn2 = False
            elapsedTime2 = int(time.time() - self.SStimer2)
            self.SSelapsedTime2 = elapsedTime2
            if self.SSelapsedTime2 >= self.SSTimeRetained:
                self.SSJustTurnedOn2 = True
                self.SSTurnedOn2 = False
                self.SSPointCounter2 = 0
                self.SSPointStartCount2 = self.score2
                self.SSPointsNeeded2 *= 2

    def checkAcceleration(self):
        if self.velocity > self.previousVelocity:
            self.accelerating = True
        else:
            self.accelerating = False
        self.previousVelocity = self.velocity
        if self.velocity2 > self.previousVelocity2:
            self.accelerating2 = True
        else:
            self.accelerating2 = False
        self.previousVelocity2 = self.velocity2

    def operateLevels(self):
        totalscore = self.score + self.score2
        if totalscore>(self.levels[0]):
            self.asteroidLowLim += 1
            self.levels.pop(0)

    def timerFired(self):
        while 1:
            self.timerFiredDelay = 10
            if self.roundOver == False:
                self.totalTime += self.timerFiredDelay
                self.invTotalTime += self.timerFiredDelay
                self.timeSpent += self.timerFiredDelay
                self.timeSpent2 += self.timerFiredDelay
                self.shipX = (self.shipX + self.velocity*math.cos(self.shipDirection))%(
                        self.width - self.shipLength)
                self.shipY = (self.shipY + self.velocity*math.sin(self.shipDirection))%(
                        self.height - self.shipLength)
                self.ship2X = (self.ship2X + self.velocity2*math.cos(self.ship2Direction))%(
                        self.width - self.shipLength)
                self.ship2Y = (self.ship2Y + self.velocity2*math.sin(self.ship2Direction))%(
                        self.height - self.shipLength)
                if self.movesLeft:
                    self.shipDirection -= 2*math.pi*(8/360.0)
                if self.movesRight:
                    self.shipDirection += 2*math.pi*(8/360.0)
                if self.invincibleBitches == False:
                    self.airResistance()
                if self.invincibleBitches2 == False:
                    self.airResistance2()
                if self.movesLeft2:
                    self.ship2Direction -= 2*math.pi*(8/360.0)
                if self.movesRight2:
                    self.ship2Direction += 2*math.pi*(8/360.0)
                if self.totalTime%120 == 0:
                    self.checkAcceleration()
                if self.totalTime - self.p1ShootTime > 100:
                    self.p1CanShoot = True
                if self.totalTime - self.p2ShootTime > 100:
                    self.p2CanShoot = True
                self.moveBullets()
                self.moveAsteroids()
                self.moveStars()
                if self.bothPlayersReady:
                    self.moveInvincibility()
                    self.moveBadGuy()
                    self.moveBadGuyBullets()
                    self.addAsteroids()
                    self.createInvincibility()
                    self.spawnBadGuy()
                    self.badGuyShoot()
                    self.killAsteroidExplosions()
                    self.killBadGuyExplosion()
                    self.hitAsteroids()
                    self.hitAsteroids2()
                    self.hitBadGuy()
                    self.hitBadGuy2()
                    self.hitInvincibility()
                    self.hitInvincibility2()
                    self.stopInvincibility()
                    self.removeAndAddStars()
                    self.removeBullets()
                    self.operateSS()
                    self.operateSS2()
                    self.operateLevels()
                    if (self.invincibleBitches == False):
                        if self.shipHitAsteroid() or self.shipHitBadGuy():
                            self.accelerating = False
                            self.lives -= 1
                            self.killedPlayer = self.username1
                            if self.lives == 0:
                                self.gameOver = True
                            else:
                                self.roundOver = True
                                if len(self.badGuy)>0:
                                    self.badGuy = []
                    if self.invincibleBitches2 == False:
                        if self.shipHitAsteroid2() or self.shipHitBadGuy2():
                            self.accelerating2 = False
                            self.lives2 -=1
                            self.killedPlayer = self.username2
                            if self.lives2 == 0:
                                self.gameOver = True
                            else:
                                self.roundOver = True
                                if len(self.badGuy)>0:
                                    self.badGuy = []
            client, address = s.accept() 
            data = client.recv(size) 
            if data: 
                action,actionData = parseData(data)
                if action == "updateGame":
                    gameState = self.getGameState()
                    client.send(gameState)
                elif action == "enterUsername1":
                    self.username1 = actionData
                    self.startScreen1 = False
                    self.lobbyScreen1 = True
                elif action == "enterUsername2":
                    self.username2 = actionData
                    self.startScreen2 = False
                    self.lobbyScreen2 = True
                elif actionData == "player1":
                    self.handlePlayer1(action)
                elif actionData == "player2":
                    self.handlePlayer2(action)
            client.close()
            self.getGameState()
            time.sleep(.01)

    def handlePlayer1(self, action):
        if action == "readyToPlay":
            self.p1Ready = True
            if self.p2Ready:
                self.bothPlayersReady = True
                self.lobbyScreen1= False
                self.lobbyScreen2= False
                self.initAsteroids()
        elif action == "upKey":
            self.accelerating = True
            if self.velocity <=10:
                self.velocity += 2
            self.shipX += self.velocity*math.cos(self.shipDirection)
            self.shipY += self.velocity*math.sin(self.shipDirection)
        elif action == "leftKeyPress":
            self.movesLeft = True
        elif action == "rightKeyPress":
            self.movesRight = True
        elif action == "leftKeyRelease":
            self.movesLeft = False
        elif action == "rightKeyRelease":
            self.movesRight = False
        elif action == "spaceKey":
            if self.p1CanShoot:
                self.p1CanShoot = False
                self.p1ShootTime = self.totalTime
                self.bullets.append([self.shipX,self.shipY,self.shipDirection])
                if self.SSTurnedOn == True:
                    self.bullets.append([self.shipX,self.shipY,self.shipDirection + (math.pi/4.0)])
                    self.bullets.append([self.shipX,self.shipY,self.shipDirection - (math.pi/4.0)])
        elif action == "letterR":
            self.init()
            if self.gameOver == True:
                self.initScores()
                self.initLives()
                self.initBadGuy()
                self.init()
                self.lobbyScreen1 = True
                self.lobbyScreen2 = True
                self.p1Ready,self.p2Ready = False,False
        elif action == "exitLobby":
            self.startScreen1 = True
            self.lobbyScreen1 = False
            self.username1 = ""

    def handlePlayer2(self, action):
        if action == "readyToPlay":
            self.p2Ready = True
            if self.p1Ready:
                self.bothPlayersReady = True
                self.lobbyScreen1= False
                self.lobbyScreen2= False
                self.initAsteroids()
        elif action == "upKey":
            self.accelerating2 = True
            if self.velocity2 <=10:
                self.velocity2 += 2
            self.ship2X += self.velocity2*math.cos(self.ship2Direction)
            self.ship2Y += self.velocity2*math.sin(self.ship2Direction)
        elif action == "leftKeyPress":
            self.movesLeft2 = True
        elif action == "rightKeyPress":
            self.movesRight2 = True
        elif action == "leftKeyRelease":
            self.movesLeft2 = False
        elif action == "rightKeyRelease":
            self.movesRight2 = False
        elif action == "spaceKey":
            if self.p2CanShoot:
                self.p2CanShoot = False
                self.p2ShootTime = self.totalTime
                self.bullets2.append([self.ship2X,self.ship2Y,self.ship2Direction])
                if self.SSTurnedOn2 == True:
                    self.bullets2.append([self.ship2X,self.ship2Y,self.ship2Direction + (math.pi/4.0)])
                    self.bullets2.append([self.ship2X,self.ship2Y,self.ship2Direction - (math.pi/4.0)])
        elif action == "letterR":
            self.init()
            if self.gameOver == True:
                self.initScores()
                self.initLives()
                self.initBadGuy()
                self.init()
                self.lobbyScreen1 = True
                self.lobbyScreen2 = True
                self.p1Ready,self.p2Ready = False,False
        elif action == "exitLobby":
            self.startScreen2 = True
            self.lobbyScreen2 = False
            self.username2 = ""

    def initAsteroids(self):
        self.xcoords = [0,self.width]
        self.ycoords = [0,self.height]
        self.astSizes = [1,2,3]
        self.dirs = [0,360]
        self.speeds = [1,1,1]
        self.asteroids = []
        self.asteroidExplosions = []
        for i in xrange(random.randint(1,2)):
            newRoid = self.createAsteroid()
            self.asteroids.append(newRoid)

    def initLives(self):
        self.lives = 3
        self.lives2 = 3
        self.livesR = 15
        self.gameOver = False

    def initScores(self):
        self.score = 0
        self.score2 = 0
        self.scores = [None, 100, 50, 25]
        self.asteroidLowLim = 2
        self.SSPointsNeeded = 2000
        self.SSPointsNeeded2 = 2000
        self.levels = [2500]
        for i in xrange(20):
            self.levels.append(self.levels[i]*1.5)
            

    def initInvincibility(self):
        self.invincibleBitches = False
        self.invincibleBitches2 = False
        self.invincibility = []
        self.invTotalTime = 0
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
        self.velocity = 0
        self.previousVelocity = 0
        self.accelerating = False
        self.movesLeft,self.movesRight = 0,0
        self.acceleratingColors = ["red","orange","yellow"]

    def initShip2(self):
        self.ship2X = self.width/2.0
        self.ship2Y = self.height/2.0
        self.shipLength = 20
        self.ship2Direction = 0
        self.velocity2 = 0
        self.previousVelocity2 = 0
        self.accelerating2 = False
        self.movesLeft2,self.movesRight2 = 0,0
        self.acceleratingColors = ["red","orange","yellow"]

    def initStartScreenStuff(self):
        w,h = self.width,self.height
        self.startButtonX = w/2.0
        self.startButtonY = h/2.0 + 20

    def initBadGuy(self):
        self.badGuy = []
        self.badGuyRadius = 10
        self.badGuyV = 5
        self.badGuySpawnScores = [2500]
        for i in xrange(20):
            self.badGuySpawnScores.append(self.badGuySpawnScores[i]+2500)
        self.badGuyBullets = []
        self.startBadGuyShooting = False
        self.badGuyBulletCount = 1
        self.badGuyExplosion = []

    def initSuperShooter(self):
        self.SSPointStartCount = self.score
        self.SSPointCounter = 0
        self.SSTimeRetained = 10 #milliseconds
        self.SSBarYLength = 300
        self.SSbarXLength = 20
        self.SSTurnedOn = False
        self.SStimer = 0
        self.SSelapsedTime = 0
        self.SSJustTurnedOn = True
        self.SSFlashTimer = 0
        self.SSPointStartCount2 = self.score2
        self.SSPointCounter2 = 0
        self.SSTurnedOn2 = False
        self.SSelapsedTime2 = 0
        self.SSJustTurnedOn2 = True
        self.SStimer2 = 0

    def getStarLocations(self):
        self.starLocations = []
        self.starV = self.velocity
        for i in xrange(10):
            cx = random.randrange(self.width)
            cy = random.randrange(self.height)
            self.starLocations.append([cx,cy])

    def init(self):
        self.initShip()
        self.initShip2()
        self.p1CanShoot = True
        self.p2CanShoot = True
        self.p1ShootTime = 0
        self.p2ShootTime = 0
        self.killedPlayer = None
        self.timerFiredDelay = 10
        self.timeSpent = 0
        self.timeSpent2 = 0
        self.totalTime = 0
        self.bullets = []
        self.bullets2 = []
        self.br = 4
        self.bulletV = 13
        self.roundOver = False
        self.itemr = 25
        self.itemDrawCounter = 0
        self.sl = 5
        self.startTime = time.time()
        self.getStarLocations()
        self.initAsteroids()
        self.initInvincibility()
        self.initStartScreenStuff()
        self.initSuperShooter()

    def initLobbyScreen(self):
        self.lobbyScreen1 = False
        self.lobbyScreen2 = False
        self.username1 = ""
        self.username2 = ""
        self.p1Ready = False
        self.p2Ready = False
        self.bothPlayersReady = False

    def getGameState(self):
        gameState = dict()
        gameState["sS1"] = self.startScreen1
        gameState["sS2"] = self.startScreen2
        gameState["lS1"] = self.lobbyScreen1
        gameState["lS2"] = self.lobbyScreen2
        gameState["u1"] = self.username1
        gameState["u2"] = self.username2
        gameState["p1r"] = self.p1Ready
        gameState["p2r"] = self.p2Ready
        gameState["rO"] = self.roundOver
        gameState["kP"] = self.killedPlayer
        gameState["SSTO"] = self.SSTurnedOn
        gameState["SSET"] = self.SSelapsedTime
        gameState["SSPC"] = self.SSPointCounter
        gameState["SSPN"] = self.SSPointsNeeded
        gameState["aR"] = self.asteroids
        gameState["aE"] = self.asteroidExplosions
        gameState["b"] = self.bullets
        gameState["b2"] = self.bullets2
        gameState["sX"] = self.shipX
        gameState["sY"] = self.shipY
        gameState["s2X"] = self.ship2X
        gameState["s2Y"] = self.ship2Y
        gameState["sD"] = self.shipDirection
        gameState["s2D"] = self.ship2Direction
        gameState["a"] = self.accelerating
        gameState["a2"] = self.accelerating2
        gameState["bG"] = self.badGuy
        gameState["sBGS"] = self.startBadGuyShooting
        gameState["bGB"] = self.badGuyBullets
        gameState["bGE"] = self.badGuyExplosion
        gameState["i"] = self.invincibility
        gameState["iB"] = self.invincibleBitches
        gameState["iB2"] = self.invincibleBitches2
        gameState["gO"] = self.gameOver
        gameState["sL"] = self.starLocations
        gameState["s"] = self.score
        gameState["s2"] = self.score2
        gameState["l"] = self.lives
        gameState["l2"] = self.lives2
        gameState["SSPC2"] = self.SSPointCounter2
        gameState["SSTO2"] = self.SSTurnedOn2
        gameState["SSET2"] = self.SSelapsedTime2
        gameState["SSPN2"] = self.SSPointsNeeded
        return repr(gameState)

    def __init__(self):
        root = Tk()
        self.width = 800
        self.height = 600
        self.initLives()
        self.initScores()
        self.initBadGuy()
        self.init()
        self.initLobbyScreen()
        self.startScreen1 = True
        self.startScreen2 = True
        self.timerFired()

host = '' 
port = 50014	
backlog = 5
size = 10000 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog)
client,address = s.accept()
data = client.recv(size)
if data:
    client.close()
    game = Asteroids()
