from threading import Thread, Timer
import random
from flask import Flask, render_template

class Ant(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.X = 1000
        self.Y = 1000
        self.contSum = 0
        self.UDLR = ['Up','Down','Left','Right']
        self.work = False
        self.direction = random.choice(self.UDLR)
        self.minX = self.X
        self.maxX = self.X
        self.minY = self.Y
        self.maxY = self.Y
       
    def setX(self,X):
        self.X = X
        if X>self.maxX:
            self.maxX = X
        elif X<self.minX:
            self.minX = X

    def getX(self):
        return self.X

    def setY(self,Y):
        self.Y = Y
        if Y>self.maxY:
            self.maxY = Y
        elif Y<self.minY:
            self.minY = Y

    def getY(self):
        return self.Y

    def getArea(self):
        areaX = self.maxX-self.minX
        areaY = self.maxY-self.minY
        if areaX==0:
            return areaY
        elif areaY==0:
            return areaX
        elif areaX==0 and areaY==0:
            return 0
        return areaX*areaY

    def setContSum(self,contSum):
        self.contSum = contSum

    def getContSum(self):
        return self.contSum

    def setWorking(self):
        random.seed()
        self.work = True

    def getWork(self):
        return self.work

    def setDirection(self):
        self.direction = random.choice(self.UDLR)

    def getDirection(self):
        return self.direction

    @staticmethod
    def getSumOfDigits(num):
        return sum(map(int, str(num)))
    
    def run(self):
        nx = self.getX()
        ny = self.getY()
        if self.direction=='Up':
            ny -= 1
        elif self.direction=='Down':
            ny += 1
        elif self.direction=='Left':
            nx -= 1
        elif self.direction=='Right':
            nx += 1
        cont_sum = self.getSumOfDigits(nx)+self.getSumOfDigits(ny)
        if not cont_sum>25:
            self.setContSum(cont_sum)
            self.setX(nx)
            self.setY(ny)
        else:
            self.setDirection()
        if self.getWork():
            Timer(1, self.run).start()

    def __del__(self):
        self.work = False

app = Flask(__name__)
ant = Ant()

@app.route('/')
def index():
    if not ant.getWork():
        ant.setWorking()
        ant.start()
    return render_template('index.html')

@app.route('/status')
def status():
    d = {'Direction': ant.getDirection(), 'X': ant.getX(), 'Y': ant.getY(), 'ContSum': ant.getContSum(), 'Area': ant.getArea()}
    return d

if __name__ == "__main__":
    app.run()
