from math import cos, sin, sqrt
import math
from pyexpat.errors import XML_ERROR_UNKNOWN_ENCODING
import random
import time
from tkinter.constants import X, Y
from tkinter.messagebox import NO
from graphics import *
import graphics

scaleInTimes = 2000000000
scale = pow(scaleInTimes,-1)
sizeGenerosity = 500000
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


class Camera(graphics._BBox):
    def __init__(self, win):
        self.win = win
        self.point = Point(0,0)
        self.updateCamera()
    
    def updateCamera(self):
        x = self.point.getX()
        y = self.point.getY()
        self.x1 = x - 960
        self.y1 = y - 540
        self.x2 = x + 960
        self.y2 = y + 540

    
    def moveCameraLeft(self):
        x = self.point.getX() - 20
        y = self.point.getY()
        self.point = (x, y)
        self.win.update()

    
    def moveCameraRight(self):
        x = self.point.getX() + 20
        y = self.point.getY()
        self.point = (x, y)
        self.win.update()


class SolarSystem(object):

    def __init__(self, name, centrePoint):
        self.name = name
        self.centrePoint = centrePoint
        self.spacialPartitioningCubes = {}
        self.partitioninglist = []
        self.partitioningDict = {}
        self.partitioningDict["other"] = []

    
    def generateSpacialPartitioning(self, win):
        gridx = range(-5,6)
        gridy = range(-5,6)
        rektXSize = win.getWidth()/2
        rektYSize = win.getHeight()/2

        for x in gridx:
            for y in gridy:
                p1 = Point(x*rektXSize,y*rektYSize)
                p2 = Point((x+1)*rektXSize,(y+1)*rektYSize)
                r = Rectangle(p1,p2)
                r.draw(win)
                self.spacialPartitioningCubes[Point(x,y)] = r
                self.partitioningDict[Point(x,y).__repr__()] = []

    class CelestialBodies:

        def __init__(self):
            self.planets = []
            self.moons = []
            self.stars = []
            self.asteroids = []
            self.celestialBodies = []

        def add_planet(self, planet):
            self.planets.append(planet)
            self.celestialBodies.append(planet)
        
        def add_moon(self, moon):
            self.moons.append(moon)
            self.celestialBodies.append(moon)

        def add_star(self,star):
            self.stars.append(star)

        def add_asteroid(self, asteroid):
            self.asteroids.append(asteroid)
            self.celestialBodies.append(asteroid)
            if __class__ == Point:
                self.celestialBodies.remove(asteroid)
        
        def setPlanetPoints(self):
            for s in self.planets:
                x = s.distancefromsun + Sun.size + Sun.point.getX()
                y = s.point.getY() + Sun.point.getY() - SolarSystem.centrePoint.getY()
                s.point = Point(x,y)

        def setMoonPoints(self):
            for s in self.moons:
                x = s.parentPlanet.point.getX()
                y = s.parentPlanet.point.getY() - s.parentPlanet.size - s.distanceFromParentPlanet
                s.point = Point(x,y)

        def setStarPoints(self):
            for s in self.stars:
                if s == Sun:
                    s.point = SolarSystem.centrePoint
        
        def setAsteroidPoints(self):
            for s in self.asteroids:
                if s == SaturnsRings:
                    s.point = Saturn.point
                    s.path = Saturn.path

        def setCelestialBodiesPoints(self):
            self.setStarPoints()
            self.setPlanetPoints()
            self.setMoonPoints()
            self.setAsteroidPoints()


        def displayName(self):
            print(self.name)

        class Planet:

            def __init__(self, name, size, distancefromsun, color):
                self.name = name
                self.obj = None
                self.size = size
                self.distancefromsun = distancefromsun
                self.point = SolarSystem.centrePoint
                self.showname = False
                self.color = color
                self.point = Point(0,0)
                self.theta = 0
                self.path = []

        class Moon:

            def __init__(self, name, size, parentPlanet, distanceFromParentPlanet, color):
                self.name = name
                self.obj = None
                self.size = size
                self.parentPlanet = parentPlanet
                self.color = color
                self.point = Point(0,0)
                self.theta = 0
                self.distanceFromParentPlanet = distanceFromParentPlanet
                self.path = []
        
        class Star:

            def __init__(self, name, size, color):
                self.name = name
                self.obj = None
                self.size = size
                self.color = color
                self.point = SolarSystem.centrePoint
        
        class Asteroids:

            def __init__(self, name, size, width, point, functionCall):
                self.name = name
                self.obj = []
                self.size = size
                self.width = width
                self.point = point
                self.theta = 0
                self.functionCall = functionCall
                self.path = []
            

            def saturnsRings(self, window):
                win = window
                s = self

                p1 = Point(s.point.getX()-s.size, s.point.getY()-s.size*0.75)
                p2 = Point(s.point.getX()+s.size, s.point.getY()+s.size*0.75)   
                c = Oval(p1,p2)
                self.obj.append(c)
                c.draw(win)
                p1 = Point(s.point.getX()-(s.size*1.1), s.point.getY()-(s.size*0.75*1.08))
                p2 = Point(s.point.getX()+(s.size*1.1), s.point.getY()+(s.size*0.75*1.08))   
                c = Oval(p1,p2)
                self.obj.append(c)
                c.draw(win)
                p1 = Point(s.point.getX()-(s.size*1.2), s.point.getY()-(s.size*0.75*1.16))
                p2 = Point(s.point.getX()+(s.size*1.2), s.point.getY()+(s.size*0.75*1.16))   
                c = Oval(p1,p2)
                self.obj.append(c)
                c.draw(win)
                
            
            def asteroidBelt(self, window):
                i = 0
                win = window
                s = self
            
                innerRing = s.size
                density = (s.width/MainAsteroidBelt.width)*(innerRing/MainAsteroidBelt.size)
                amountOfAsteroids = 2000*density
                while i < amountOfAsteroids:
                    theta = random.randint(0,36000)/100
                    r = (weightedRandom(1,2) * s.width)+innerRing
                    x = r*cos(theta) + Sun.point.getX()
                    y = r*sin(theta) + Sun.point.getY()
                    p = Point(x,y)
                    gx = x // (win.width/2)
                    gy =  y // (win.height/2)
                    SolarSystem.partitioningDict[Point(gx,gy).__repr__()].append(p)
                    i += 1




SolarSystem = SolarSystem("OurSolarSystem", Point(0,0))

CelestialBodies = SolarSystem.CelestialBodies()

Sun = SolarSystem.CelestialBodies.Star("TheSun", 109.298*EAU*scale, "orange")

Mercury = SolarSystem.CelestialBodies.Planet("Mercury", 0.383*EAU*scale, 0.387*AU*scale, "grey")

Venus = SolarSystem.CelestialBodies.Planet("Venus", 0.949*EAU*scale, 0.723*AU*scale, "grey")

Earth = SolarSystem.CelestialBodies.Planet("Earth", 1*EAU*scale, 1*AU*scale, "green")

Moon = SolarSystem.CelestialBodies.Moon("TheMoon", 0.2724*EAU*scale, Earth, 2.56955*pow(10,-7)*AU*scale, "grey")

Mars = SolarSystem.CelestialBodies.Planet("Mars", 0.532*EAU*scale, 1.52*AU*scale, "orange")

Jupiter = SolarSystem.CelestialBodies.Planet("Jupiter", 11.21*EAU*scale, 5.20*AU*scale, "beige")

Saturn = SolarSystem.CelestialBodies.Planet("Saturn", 9.45*EAU*scale, 9.58*AU*scale, "yellow")

SaturnsRings = SolarSystem.CelestialBodies.Asteroids("SaturnsRings", Saturn.size*1.5, 0, Saturn.point, CelestialBodies.Asteroids.saturnsRings)

Uranus = SolarSystem.CelestialBodies.Planet("Uranus", 4.01*EAU*scale, 19.20*AU*scale, "light blue")

Neptune = SolarSystem.CelestialBodies.Planet("Neptune", 3.88*EAU*scale, 30.05*AU*scale, "blue")

MainAsteroidBelt = SolarSystem.CelestialBodies.Asteroids("MainAsteroidBelt", Sun.size + 2.2*AU*scale, 1*AU*scale, SolarSystem.centrePoint, CelestialBodies.Asteroids.asteroidBelt)

KuiperBelt = SolarSystem.CelestialBodies.Asteroids("KuiperBelt", Sun.size + 30*AU*scale, 2*AU*scale, SolarSystem.centrePoint, CelestialBodies.Asteroids.asteroidBelt)



CelestialBodies.add_star(Sun)
CelestialBodies.add_planet(Mercury)
CelestialBodies.add_planet(Venus)
CelestialBodies.add_planet(Earth)
CelestialBodies.add_moon(Moon)
CelestialBodies.add_planet(Jupiter)
CelestialBodies.add_planet(Mars)
CelestialBodies.add_planet(Saturn)
CelestialBodies.add_asteroid(SaturnsRings)
CelestialBodies.add_asteroid(MainAsteroidBelt)
CelestialBodies.add_planet(Uranus)
CelestialBodies.add_planet(Neptune)
CelestialBodies.add_asteroid(KuiperBelt)



def initialize():
    win = GraphWin("SolarSystem", 1920, 1080)
    camera = Camera(win)
    CelestialBodies.setCelestialBodiesPoints()
    camera.updateCamera()
    win.setCoords(camera.x1, camera.y1, camera.x2, camera.y2)
    SolarSystem.generateSpacialPartitioning(win, 10, 10)



def main():
    win = GraphWin("SolarSystem", 1920, 1080)
    camera = Camera(win)
    CelestialBodies.setCelestialBodiesPoints()
    camera.updateCamera()
    win.setCoords(camera.x1, camera.y1, camera.x2, camera.y2)
    SolarSystem.generateSpacialPartitioning(win)

    
    for s in CelestialBodies.planets:

        #planets path
        c = Circle(SolarSystem.centrePoint, s.point.x)
        SolarSystem.partitioningDict["other"].append(c)
        s.path.append(c)
        
        c.draw(win)
        #planet itself
        c = Circle(s.point, s.size)
        c.setFill(s.color)
        SolarSystem.partitioningDict["other"].append(c)
        s.obj = c
        c.draw(win)

    for s in CelestialBodies.moons:
        c = Circle(s.point, s.size)
        s.path.append(c)
        c.setFill(s.color)
        SolarSystem.partitioningDict["other"].append(c)
        s.obj = c
        c.draw(win)

    for s in CelestialBodies.stars:
        c = Circle(s.point, s.size)
        c.setFill(s.color)
        SolarSystem.partitioningDict["other"].append(c)
        c.draw(win)

    for s in CelestialBodies.asteroids: 
        s.functionCall(s, win)

    win.secondCustomSetCoords(camera.x1,camera.y1,camera.x2,camera.y2,SolarSystem.partitioningDict)
    
    close = False
    while close == False:
        time.sleep(1)
        print("looping")
        for s in CelestialBodies.celestialBodies:
            if s == MainAsteroidBelt or s == KuiperBelt:
                pass
            else:
                for circle in s.path:
                    x = s.point.x
                    y = s.point.y
                    r = Circle.getRadius(circle)
                    s.theta += 0.1
                    xnew = r*sin(s.theta)
                    ynew = r*cos(s.theta)
                    dx = xnew-x
                    dy = ynew-y
                    s.point.x += dx
                    s.point.y += dy
                    if s.obj.__class__ == list:
                        for each in s.obj:
                            each.move(dx,dy)
                    else:
                        s.obj.move(dx,dy)

        camera.point = win.checkMouse()
        if camera.point:
            camera.updateCamera()
            win.secondCustomSetCoords(camera.x1,camera.y1,camera.x2,camera.y2,SolarSystem.partitioningDict)


if __name__ == "__main__":
    main()

#make SaturnsRings one obj with clones instead