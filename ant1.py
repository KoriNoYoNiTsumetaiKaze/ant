from flask import Flask, render_template
import logging
from threading import Thread, Timer

UP    = 'Up'
DOWN  = 'Down'
LEFT  = 'Left'
RIGHT = 'Right'

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

    def getX(self):
        return self.X

    def setX(self,X):
        self.X = X

    def getY(self):
        return self.Y

    def setY(self,Y):
        self.Y = Y

    def getArea(self):
        return len(self.traces)

    def getContSum(self):
        return self.contSum

    @staticmethod
    def is_access(cont_sum):
        return not cont_sum>10

    def setContSum(self,contSum):
        if self.is_access(contSum):
            self.contSum = contSum

    def getWork(self):
        return self.work

    def setWorking(self):
        self.work = True

    def getTraces(self):
        return self.traces

    def setTrace(self,xy):
        if not (xy in self.traces):
            self.traces.append(xy)

    def getDirection(self):
        return self.direction

    def setDirection(self,direction):
        self.direction = direction

    def getOptions(self):
        return self.options

    @staticmethod
    def getStrOption(lx,ly):
        return str(lx)+'-'+str(ly)

    def setOptions(self,lx,ly):
        xy = self.getStrOption(lx,ly)
        loptions = self.getOptions()
        if not (xy in loptions):
            self.options.append(xy)        

    @staticmethod
    def getSumOfDigits(num):
        return sum(map(int, str(num)))

    def checkDir(self,lx,ly):
        xy = self.getStrOption(lx,ly)
        ltraces = self.getTraces()
        if xy in ltraces:
            return False
        cont_sum = self.getSumOfDigits(lx)+self.getSumOfDigits(ly)
        logging.debug("run lx {} ly {} cont_sum {}".format(lx,ly,cont_sum))
        self.setContSum(cont_sum)
        return self.is_access(cont_sum)

    def identifyOptions(self,lx,ly):
        if self.checkDir(lx-1,ly):
            self.setOptions(lx-1,ly)
        if self.checkDir(lx+1,ly):
            self.setOptions(lx+1,ly)
        if self.checkDir(lx,ly-1):
            self.setOptions(lx,ly-1)
        if self.checkDir(lx,ly+1):
            self.setOptions(lx,ly+1)

    def checkOption(self,xy):
        loptions = self.getOptions()
        return xy in loptions

    def delOption(self,xy):
        if self.checkOption(xy):
            self.options.remove(xy)

    def run(self):
        lx = self.getX()
        ly = self.getY()
        logging.debug("run lx {} ly {}".format(lx,ly))
        self.identifyOptions(lx,ly)
        loptions = self.getOptions()
        logging.debug("run self.getOptions() {}".format(self.getOptions()))
        if len(loptions)==0:
            self.work = False
        else:
            listXY = loptions[0].split('-')
            tx = int(listXY[0])
            ty = int(listXY[1])
            logging.debug("run tx {} ty {}".format(tx,ty))
            if tx<lx:
                xy = self.getStrOption(lx-1,ly)
                logging.debug("run LEFT xy {}".format(xy))
                self.setX(lx-1)
                self.delOption(xy)
                self.setTrace(xy)
                self.setDirection(LEFT)
            elif tx>lx:
                xy = self.getStrOption(lx+1,ly)
                logging.debug("run RIGHT xy {}".format(xy))
                self.setX(lx+1)
                self.delOption(xy)
                self.setTrace(xy)
                self.setDirection(RIGHT)
            elif ty<ly:
                xy = self.getStrOption(lx,ly-1)
                logging.debug("run UP xy {}".format(xy))
                self.setY(ly-1)
                self.delOption(xy)
                self.setTrace(xy)
                self.setDirection(UP)
            elif ty>ly:
                xy = self.getStrOption(lx,ly+1)
                logging.debug("run DOWN xy {}".format(xy))
                self.setY(ly+1)
                self.delOption(xy)
                self.setTrace(xy)
                self.setDirection(DOWN)        
        logging.debug("run self.getOptions() {}".format(self.getOptions()))
        logging.debug("run x {} y {}".format(self.getX(),self.getY()))
        logging.debug("run self.getOptions() {}".format(self.getOptions()))
        logging.debug("run self.getTraces() {}".format(self.getTraces()))
        logging.info("---------------------------------------------------")
        if self.getWork():
            Timer(1, self.run).start()

logging.basicConfig(filename="sample.log", filemode='w', level=logging.DEBUG)
app = Flask(__name__)
ant = Ant()

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
    d = {'Direction': ant.getDirection(), 'X': ant.getX(), 'Y': ant.getY(), 'ContSum': ant.getContSum(), 'Area': ant.getArea()}
    return d

if __name__ == "__main__":
    app.run()
