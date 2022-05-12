from ctypes.wintypes import tagRECT
from math import cos, dist, sin, sqrt
import random
from re import X
from tkinter import Variable
from turtle import distance
import graphics

scaleInTimes = 1000000000
scale = pow(scaleInTimes,-1)
sizeGenerosity = 1000000
rate=60 #update rate
#values for all scale comes from: https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_ratio.html

#Astronomical Unit in km (distance from sun to earth)
AU = 149597870700
#Unit for earths radius in km
EAU = 6371 * sizeGenerosity

def weightedRandom(max, numDice): 
    num = 0
    i = 0
    while ( i < numDice): 
        num += random.random() * (max/numDice)
        i +=1
        
    return num


class SolarSystem(object):

    def __init__(self, name, centrePoint):
        self.name = name
        self.centrePoint = centrePoint
        self.planets = []
        self.moons = []
        self.stars = []
        self.rings = []
        self.asteroidBelts = []
        self.celestialBodyList = []
        self.orbits = {}
        self.tethers = {}
        self.Time = 0
        self.unitTime = 0.05/rate

    
    def generateSpacialPartitioning(self):
        gridx = range(-5,6)
        gridy = range(-5,6)
        rektXSize = win.getWidth()/2
        rektYSize = win.getHeight()/2

        for x in gridx:
            for y in gridy:
                p1 = graphics.Point(x*rektXSize,y*rektYSize)
                p2 = graphics.Point((x+1)*rektXSize,(y+1)*rektYSize)
                r = graphics.Rectangle(p1,p2)
                r.draw(win)
                self.spacialPartitioningCubes[graphics.Point(x,y)] = r
                self.partitioningDict[graphics.Point(x,y).__repr__()] = []
    
    def add_planet(self, planet):
        self.planets.append(planet)
        
    def add_moon(self, moon):
        self.moons.append(moon)

    def add_star(self, star):
        self.stars.append(star)

    def add_ring(self, ring):
        self.rings.append(ring)

    def add_asteroidBelt(self, asteroidBelt):
        self.asteroidBelts.append(asteroidBelt)

    def setStarPoints(self):
        for star in self.stars:
            star.point = self.centrePoint

    def setPlanetPoints(self):
        for planet in self.planets:
            x = planet.distancefromsun + Sun.size + Sun.point.getX()
            y = planet.point.getY() + Sun.point.getY() - self.centrePoint.getY()
            planet.point = graphics.Point(x,y)

    def setMoonPoints(self):
        for moon in self.moons:
            x = moon.parentPlanet.point.getX()
            y = moon.parentPlanet.point.getY() + moon.parentPlanet.size + moon.distanceFromParentPlanet + moon.size
            moon.point = graphics.Point(x,y)

    def setRingPoints(self):
        for ring in self.rings:
            ring.point = ring.parentPlanet.point

    def setBeltPoints(self):
        for belt in self.asteroidBelts:
            x = Sun.size + belt.distancefromsun
            y = 0
            belt.point = graphics.Point(x,y)
        
    def generateCelestialBodyLists(self):
        for body in self.celestialBodyList:
            if type(body) == Star:
                self.add_star(body)

            elif type(body) == Planet:
                self.add_planet(body)
                body.defineOrbit(Sun)

            elif type(body) == Moon:
                self.add_moon(body)
                body.defineOrbit(body.parentPlanet)

            elif type(body) == Ring:
                self.add_ring(body)

            elif type(body) == AsteroidBelt:
                self.add_asteroidBelt(body)
                
    def generateCelestialBodyPoints(self):
        self.setStarPoints()
        self.setPlanetPoints()
        self.setMoonPoints()
        self.setRingPoints()
        self.setBeltPoints()
    
    def updateInternalTimeState(self):
        self.Time = self.Time + self.unitTime


    def orbit(self):
        for planet, target in self.orbits.items():
            distance = target[1]
            orbitialSpeed = target[2]
            theta = orbitialSpeed*solarSystem.Time
            
            x = distance*cos(theta) + target[0].point.getX()
            y = distance*sin(theta) + target[0].point.getY()
            
            dx = x - planet.point.getX()
            dy = y - planet.point.getY()

            planet.obj.move(dx,dy)
            planet.point = graphics.Point(x,y)

            
    
    def tether(self):
        for tethered, target in self.tethers.items():

            x = target.point.getX()
            y = target.point.getY()

            dx = x - tethered.point.getX()
            dy = y - tethered.point.getY()

            tethered.objs(graphics.GraphicsObject.move, [dx,dy])
            tethered.point = graphics.Point(x,y)

    def update(self):
        self.updateInternalTimeState()
        self.orbit()
        self.tether()
        graphics.update(rate)


class CelestialBody:

    def __init__(self, name, size, color, speed):
        solarSystem.celestialBodyList.append(self)
        self.name = name
        self.size = size/2
        self.color = color
        self.speed = speed

    def initiateCelestialBody(self):
        self.generateGraphicsObjFromBody()
        self.draw()

    def generateGraphicsObjFromBody(self):
        objTypeDict = {
            Moon : graphics.Circle,
            Planet : graphics.Circle,
            Star : graphics.Circle,
            Ring : Ring.Make3Rings,
            AsteroidBelt : AsteroidBelt.asteroidBelt
        }
        objType = objTypeDict[type(self)]

        ringToPlanetScale = 1.2
        objVariableDict = {
            graphics.Circle : (self.point, self.size),
            Ring.Make3Rings : (self, graphics.Point(self.point.x-self.size*ringToPlanetScale, self.point.y-self.size),graphics.Point(self.point.x+self.size*ringToPlanetScale, self.point.y+self.size)),
            AsteroidBelt.asteroidBelt : [self]
        }
        objVariables = objVariableDict[objType]

        obj = objType(*objVariables)

        if objType == graphics.Circle:
            obj.setFill(self.color)
        self.obj = obj
    
    def defineOrbit(self, target):
        solarSystem.orbits[self] = [target, dist((self.point.getX(),self.point.getY()),(target.point.getX(), target.point.getY())), self.speed]

    def defineTether(self, target):
        solarSystem.tethers[self] = target




class Planet(CelestialBody):

    def __init__(self, name, size, color, speed, distancefromsun):
        CelestialBody.__init__(self, name, size, color, speed)
        self.point = graphics.Point(0,0)
        self.distancefromsun = distancefromsun
    
    def draw(self):
        ezpz = graphics.GraphicsObject.draw
        ezpz(self.obj, win)
                
class Moon(CelestialBody):

    def __init__(self, name, size, color, speed, parentPlanet, distanceFromParentPlanet):
        CelestialBody.__init__(self, name, size, color, speed)
        self.point = graphics.Point(0,0)
        self.parentPlanet = parentPlanet
        self.distanceFromParentPlanet = distanceFromParentPlanet
    
    def draw(self):
        graphics.GraphicsObject.draw(self.obj, win)

class Star(CelestialBody):

    def __init__(self, name, size, color, speed):
        CelestialBody.__init__(self, name, size, color, speed)
        self.point = graphics.Point(0,0)

    def draw(self):
        graphics.GraphicsObject.draw(self.obj, win)
        
class Ring(CelestialBody):

    def __init__(self, name, size, color, speed, parentPlanet):
        CelestialBody.__init__(self, name, size, color, speed)
        self.point = graphics.Point(0,0)
        self.parentPlanet = parentPlanet

    def objs(self, function, variables):
        for obj in self.obj:
            function(obj, *variables)

    def draw(self):
        self.objs(graphics.GraphicsObject.draw, [win])

    def Make3Rings(self, p1, p2):
            obj = []
            ringScales = [0.9,1,1.1]
            for ringScale in ringScales:
                centerX = (p1.x+p2.x)/2.0
                centerY = (p1.y+p2.y)/2.0

                x = centerX-((centerX-p1.x)*ringScale)
                y = centerY-((centerY-p1.y)*ringScale)
                newp1 = graphics.Point(x,y)

                x = centerX-((centerX-p2.x)*ringScale)
                y = centerY-((centerY-p2.y)*ringScale)
                newp2 = graphics.Point(x,y)

                ring = graphics.Oval(newp1, newp2)
                obj.append(ring)
            return obj

class AsteroidBelt(CelestialBody):

    def __init__(self, name, size, color, speed, distancefromsun):
        CelestialBody.__init__(self, name, size, color, speed)
        self.point = graphics.Point(0,0)
        self.distancefromsun = distancefromsun

    def asteroidBelt(self):
        i = 0
        obj = []
        refrence = MainAsteroidBelt
        density = (self.size/refrence.size)*(self.distancefromsun/refrence.distancefromsun)
        amountOfAsteroids = 2000*density
        while i < amountOfAsteroids:
            theta = random.randint(0,36000)/100
            r = (weightedRandom(1,2) * self.size)+self.distancefromsun+Sun.size
            x = r*cos(theta) + Sun.point.getX()
            y = r*sin(theta) + Sun.point.getY()
            p = graphics.Point(x,y)
            #gx = x // (win.size/2)
            #gy =  y // (win.height/2)
            obj.append(p)
            #SolarSystem.partitioningDict[Point(gx,gy).__repr__()].append(p)
            i += 1
        return obj

    def objs(self, function):
        for obj in self.obj:
            function(obj, win)

    def draw(self):
        self.obj = self.asteroidBelt()
        self.objs(graphics.GraphicsObject.draw)

def initialize():
    global win
    win = graphics.GraphWin("SolarSystem", 1920, 1080, autoflush=False)
    win.setCoords(-960, -540, 960, 540)
    win.setBackground("light grey")
    solarSystem.generateCelestialBodyLists()
    solarSystem.generateCelestialBodyPoints()
    

    for Body in solarSystem.celestialBodyList:
        Body.initiateCelestialBody()
        if type(Body) == Planet:
            Body.defineOrbit(Sun)
        elif type(Body) == Moon:
            Body.defineOrbit(Body.parentPlanet)
        elif type(Body) == Ring:
            Body.defineTether(Body.parentPlanet)


def run():
    close = False
    while close == False:
        point = win.checkMouse()
        if point:
            x1 = point.x-(win.getWidth()/2)
            y1 = point.y-(win.getHeight()/2)
            x2 = point.x+(win.getWidth()/2)
            y2 = point.y+(win.getHeight()/2)
            win.setCoords(x1,y1,x2,y2)
        solarSystem.update()
        

def main():
    initialize()
    run()
    win.getMouse()
    win.close()


solarSystem = SolarSystem("OurSolarSystem", graphics.Point(0,0))

Sun = Star("TheSun", 109.298*EAU*scale, "orange", 0)

Mercury = Planet("Mercury", 0.383*EAU*scale, "grey", 1.59, 0.387*AU*scale)

Venus = Planet("Venus", 0.949*EAU*scale, "grey", 1.18, 0.723*AU*scale)

Earth = Planet("Earth", 1*EAU*scale, "green", 1, 1*AU*scale)

Luna = Moon("Luna", 0.2724*EAU*scale, "grey", 365, Earth, 2.56955*pow(10,-7)*AU*scale)

Mars = Planet("Mars", 0.532*EAU*scale, "orange", 0.808, 1.52*AU*scale)

Jupiter = Planet("Jupiter", 11.21*EAU*scale, "beige", 0.439, 5.20*AU*scale)

Saturn = Planet("Saturn", 9.45*EAU*scale, "yellow", 0.325, 9.58*AU*scale)

SaturnsRings = Ring("SaturnsRings", Saturn.size*1.5, "beige", 0.325, Saturn)

Uranus = Planet("Uranus", 4.01*EAU*scale, "light blue", 0.288, 19.20*AU*scale)

Neptune = Planet("Neptune", 3.88*EAU*scale, "blue", 0.182, 30.05*AU*scale)

MainAsteroidBelt = AsteroidBelt("MainAsteroidBelt", 1*AU*scale, "grey", 0, 2.2*AU*scale)

KuiperBelt = AsteroidBelt("KuiperBelt", 2*AU*scale, "grey", 0, 30*AU*scale)





if __name__ == "__main__":
    main()

#make SaturnsRings one obj with clones instead








