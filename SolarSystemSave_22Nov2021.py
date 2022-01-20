from math import cos, sin
import random
#import time
from tkinter import Variable, Widget
from tkinter.constants import NONE, S, SEL_FIRST, X, Y
from typing import Coroutine
from graphics import *

scaleInTimes = 5000000000
scale = pow(scaleInTimes,-1)
sizeGenerosity = 250000
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


class Coord(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def getX(self):
        # Getter method for a Coordinate object's x coordinate.
        # Getter methods are better practice than just accessing an attribute directly
        return self.x

    def getY(self):
        # Getter method for a Coordinate object's y coordinate
        return self.y

    def __str__(self):
        return '<' + str(self.getX()) + ',' + str(self.getY()) + '>'
    
    def __eq__(self, other):
        return self.y == other.y and self.x == other.x
    
    def __repr__(self):
        return "Coordinate(%d, %d)" % (self.x, self.y)




class SolarSystem(object):

    def __init__(self, name, centrePoint):
        self.name = name
        self.centrePoint = centrePoint

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
            self.celestialBodies.append(star)

        def add_asteroid(self, asteroid):
            self.asteroids.append(asteroid)
            self.celestialBodies.append(asteroid)
        
        def setPlanetPoints(self):
            for s in self.planets:
                x = s.distancefromsun + Sun.size + Sun.point.getX()
                print(s.name)
                print(x)
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
                    s.position = Saturn.point



#        def setPlanetColor(self):
#            for s in self.planets:
#                s.setFill("green")

        def setCelestialBodiesPoints(self):
            self.setStarPoints()
            self.setPlanetPoints()
            self.setMoonPoints()
            self.setAsteroidPoints()


        def DisplayName(self):
            for planet in self.planets:
                print(planet.name)

        class Planet:

            def __init__(self, name, size, distancefromsun, color):
                self.name = name
                self.size = size
                self.distancefromsun = distancefromsun
                self.point = SolarSystem.centrePoint
                self.showname = False
                self.color = color
                self.path = Circle

        class Moon:

            def __init__(self, name, size, parentPlanet, distanceFromParentPlanet, color):
                self.name = name
                self.size = size
                self.parentPlanet = parentPlanet
                self.color = color
                self.point = Point(0,0)
                self.distanceFromParentPlanet = distanceFromParentPlanet
                self.path = Circle
        
        class Star:

            def __init__(self, name, size, color):
                self.name = name
                self.size = size
                self.color = color
                self.point = SolarSystem.centrePoint
        
        class Asteroids:

            def __init__(self, name, size, width, position, functionCall):
                self.name = name
                self.size = size
                self.width = width
                self.position = position
                self.functionCall = functionCall
            
            def saturnsRings(self, window):
                win = window
                s = self


                p1 = Point(s.position.getX()-s.size, s.position.getY()-s.size*0.75)
                p2 = Point(s.position.getX()+s.size, s.position.getY()+s.size*0.75)   
                c = Oval(p1,p2)
                c.draw(win)
                p1 = Point(s.position.getX()-(s.size*1.1), s.position.getY()-(s.size*0.75*1.08))
                p2 = Point(s.position.getX()+(s.size*1.1), s.position.getY()+(s.size*0.75*1.08))   
                c = Oval(p1,p2)
                c.draw(win)
                p1 = Point(s.position.getX()-(s.size*1.2), s.position.getY()-(s.size*0.75*1.16))
                p2 = Point(s.position.getX()+(s.size*1.2), s.position.getY()+(s.size*0.75*1.16))   
                c = Oval(p1,p2)
                c.draw(win)
            
            def asteroidBelt(self, window):
                u = 0
                win = window
                s = self
        
                innerRing = s.size
                #outerRing = s.size + s.width
                #c1 = graphics.Circle(s.position, innerRing)
                #c1.draw(win)
                #c2 = graphics.Circle(s.position, outerRing)
                #c2.draw(win)
                density = (s.width/MainAsteroidBelt.width)*(innerRing/MainAsteroidBelt.size)
                amountOfAsteroids = 4000*density
                while u < amountOfAsteroids:
                    theta = random.randint(0,36000)/100
                    r = (weightedRandom(1,2) * s.width)+innerRing
                    x = r*cos(theta) + Sun.point.getX()
                    y = r*sin(theta)+Sun.point.getY()
                    p = Point(x,y)
                    p.draw(win)
                    u += 1





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
#Sun.size + 320*scale = size

KuiperBelt = SolarSystem.CelestialBodies.Asteroids("KuiperBelt", Sun.size + 30*AU*scale, 2*AU*scale, SolarSystem.centrePoint, CelestialBodies.Asteroids.asteroidBelt)
#Sun.size + 3000*scale = size

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








def main():
    win = GraphWin("SolarSystem", 1920, 1080)
    GraphWin.setCoords(win, -960, -540, 960, 540)
    CelestialBodies.setCelestialBodiesPoints()

    for s in CelestialBodies.celestialBodies:
        if s.__class__ == CelestialBodies.Planet:
            c = Circle(SolarSystem.centrePoint, s.point.getX())
            c.draw(win)

    for s in CelestialBodies.planets:
        c = Circle(s.point, s.size)
        c.setFill(s.color)
        c.draw(win)

    for s in CelestialBodies.moons:
        c = Circle(s.point, s.size)
        c.setFill(s.color)
        c.draw(win)
        #c = Circle(s.parentPlanet.point, 2.5*s.parentPlanet.size)
        #c.draw(win)

    for s in CelestialBodies.stars:
        c = Circle(s.point, s.size)
        c.setFill(s.color)
        c.draw(win)

    for s in CelestialBodies.asteroids: 
        s.functionCall(s, win)


    win.getMouse()
    win.close()



if __name__ == "__main__":
    main()

