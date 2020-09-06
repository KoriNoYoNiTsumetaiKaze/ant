from flask import Flask, render_template
import logging
from threading import Thread, Timer

UP    = 'Up'
DOWN  = 'Down'
LEFT  = 'Left'
RIGHT = 'Right'

FLAG_DEBUG = False

class Ant(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.X = 1000
        self.Y = 1000
        self.contSum = 0
        self.work = False
        self.traces = []
        self.direction = ''
        self.options = []

    def __del__(self):
        self.work = False

    def setX(self,X):
        self.X = X

    def getX(self):
        return self.X

    def setY(self,Y):
        self.Y = Y

    def getY(self):
        return self.Y

    def getArea(self):
        return len(self.traces)

    def getContSum(self):
        return self.contSum

    def setWorking(self):
        self.work = True

    def getWork(self):
        return self.work

    def setTrace(self,xy):
        if not (xy in self.traces):
            self.traces.append(xy)

    def getTraces(self):
        return self.traces

    def setDirection(self,direction):
        self.direction = direction

    def getDirection(self):
        return self.direction

    @staticmethod
    def is_access(cont_sum):
        return not cont_sum>25

    @staticmethod
    def getSumOfDigits(num):
        return sum(map(int, str(num)))

    def setContSum(self,contSum):
        if self.is_access(contSum):
            self.contSum = contSum

    def getOptions(self):
        return self.options

    def checkOption(self,xy):
        loptions = self.getOptions()
        return xy in loptions

    @staticmethod
    def getStrOption(lx,ly):
        return str(lx)+'-'+str(ly)

    def checkDir(self,lx,ly):
        xy = self.getStrOption(lx,ly)
        ltraces = self.getTraces()
        if xy in ltraces:
            return False
        cont_sum = self.getSumOfDigits(lx)+self.getSumOfDigits(ly)
        log("run lx {} ly {} cont_sum {} {}".format(lx,ly,cont_sum, self.is_access(cont_sum)))
        self.setContSum(cont_sum)
        return self.is_access(cont_sum)

    def setOptions(self,lx,ly):
        xy = self.getStrOption(lx,ly)
        loptions = self.getOptions()
        if not (xy in loptions):
            self.options.append(xy)

    def identifyOptions(self,lx,ly):
        if self.checkDir(lx-1,ly):
            self.setOptions(lx-1,ly)
        if self.checkDir(lx+1,ly):
            self.setOptions(lx+1,ly)
        if self.checkDir(lx,ly-1):
            self.setOptions(lx,ly-1)
        if self.checkDir(lx,ly+1):
            self.setOptions(lx,ly+1)

    def delOption(self,xy):
        self.options.remove(xy)

    def checkTrace(self,xy):
        ltraces = self.getTraces()
        return xy in ltraces

    def run(self):
        lx = self.getX()
        ly = self.getY()
        log("run lx {} ly {}".format(lx,ly))
        self.identifyOptions(lx,ly)
        log("run self.getOptions() {}".format(self.getOptions()))
        xyLeft  = self.getStrOption(lx-1,ly)
        log("run xyLeft {}".format(xyLeft))
        xyRight = self.getStrOption(lx+1,ly)
        log("run xyRight {}".format(xyRight))
        xyUp    = self.getStrOption(lx,ly-1)
        log("run xyUp {}".format(xyUp))
        xyDown  = self.getStrOption(lx,ly+1)
        log("run xyDown {}".format(xyDown))
        if self.checkOption(xyRight):
            log("run xyRight!")
            self.setX(lx+1)
            self.delOption(xyRight)
            self.setTrace(xyRight)
            self.setDirection(RIGHT)
        elif self.checkOption(xyDown):
            log("run xyDown!")
            self.setY(ly+1)
            self.delOption(xyDown)
            self.setTrace(xyDown)
            self.setDirection(DOWN)
        elif self.checkOption(xyLeft):
            log("run xyLeft!")
            self.setX(lx-1)
            self.delOption(xyLeft)
            self.setTrace(xyLeft)
            self.setDirection(LEFT)
        elif self.checkOption(xyUp):
            log("run xyUp!")
            self.setY(ly-1)
            self.delOption(xyUp)
            self.setTrace(xyUp)
            self.setDirection(UP)
        else:
            loptions = self.getOptions()
            if len(loptions)==0:
                self.work = False
            else:
                listXY = loptions[0].split('-')
                tx = int(listXY[0])
                ty = int(listXY[1])
                if tx<lx:
                    log("run traces xyLeft!")
                    self.setX(lx-1)
                    self.setDirection(LEFT)
                elif tx>lx:
                    log("run traces xyRight!")
                    self.setX(lx+1)
                    self.setDirection(RIGHT)
                elif ty<ly:
                    log("run traces xyUp!")
                    self.setY(ly-1)
                    self.setDirection(UP)
                elif ty>ly:
                    log("run traces xyDown!")
                    self.setY(ly+1)
                    self.setDirection(DOWN)
        log("run x {} y {}".format(self.getX(),self.getY()))
        log("run self.getOptions() {}".format(self.getOptions()))
        log("run self.getTraces() {}".format(self.getTraces()))
        log("---------------------------------------------------")
        if self.getWork():
            Timer(1, self.run).start()

logging.basicConfig(filename="sample.log", filemode='w', level=logging.DEBUG)
app = Flask(__name__)
ant = Ant()

def log(txt):
    if FLAG_DEBUG:
        logging.debug(txt)

@app.route('/')
def index():
    if not ant.getWork():
        lx = ant.getX()
        ly = ant.getY()
        xy = ant.getStrOption(lx,ly)
        ant.setTrace(xy)
        ant.setWorking()
        ant.start()
    return render_template('index.html')

@app.route('/status')
def status():
    d = {'Direction': ant.getDirection(), 'X': ant.getX(), 'Y': ant.getY(), 'ContSum': ant.getContSum(), 'Area': ant.getArea(), 'Work':ant.getWork()}
    return d

if __name__ == "__main__":
    app.run()
