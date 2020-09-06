from threading import Thread, Timer
import random
from flask import Flask, render_template
import logging

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
        self.UDLR = [UP,DOWN,LEFT,RIGHT]
        self.work = False
        self.direction = ''
        self.traces = []
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0

    def setMinX(self,X):
        logging.debug("minX {}".format(X))
        self.minX = X

    def getMinX(self):
        return self.minX

    def setMaxX(self,X):
        logging.debug("maxX {}".format(X))
        self.maxX = X

    def getMaxX(self):
        return self.maxX

    def setMinY(self,Y):
        logging.debug("minY {}".format(Y))
        self.minY = Y

    def getMinY(self):
        return self.minY

    def setMaxY(self,Y):
        logging.debug("maxY {}".format(Y))
        self.maxY = Y

    def getMaxY(self):
        return self.maxY

    @staticmethod
    def is_access(cont_sum):
        return not cont_sum>11

    @staticmethod
    def getSumOfDigits(num):
        return sum(map(int, str(num)))

    def checkDir(self,lx,ly):
        # logging.info("--------------------checkDir begin-----------------------------")
        cont_sum = self.getSumOfDigits(lx)+self.getSumOfDigits(ly)
        logging.debug("checkDir lx {} ly {} cont_sum {}".format(lx,ly,cont_sum))
        self.setContSum(cont_sum)
        # logging.info("--------------------checkDir end-----------------------------")
        return self.is_access(cont_sum)

    def setmaxXYmin(self):
        lx = self.getX()
        ly = self.getY()
        minX = lx
        while self.checkDir(minX,ly):
            minX -=1
        self.setMinX(minX)
        maxX = lx
        while self.checkDir(maxX,ly):
            maxX +=1
        self.setMaxX(maxX)
        minY = ly
        while self.checkDir(lx,minY):
            minY -=1
        self.setMinY(minY)
        maxY = ly
        while self.checkDir(lx,maxY):
            maxY +=1
        self.setMaxY(maxY)

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

    def setContSum(self,contSum):
        if self.is_access(contSum):
            self.contSum = contSum

    def getContSum(self):
        return self.contSum

    def setWorking(self):
        random.seed()
        self.work = True

    def getWork(self):
        return self.work

    def getTraces(self):
        return self.traces

    def getDirection(self):
        return self.direction

    def setDirection(self,direction):
        self.direction = direction

    def setTrace(self,lx,ly):
        pix = (lx,ly)
        if not (pix in self.traces):
            self.traces.append(pix)

    def getAccDir(self):
        logging.info("--------------------getAccDir begin-----------------------------")
        listDir = []
        lx = self.getX()
        ly = self.getY()
        logging.info("getAccDir Left")
        if self.checkDir(lx-1,ly):
            listDir.append(LEFT)
        logging.info("getAccDir Right")
        if self.checkDir(lx+1,ly):
            listDir.append(RIGHT)
        logging.info("getAccDir Up")
        if self.checkDir(lx,ly-1):
            listDir.append(UP)
        logging.info("getAccDir Down")
        if self.checkDir(lx,ly+1):
            listDir.append(DOWN)
        logging.info("--------------------getAccDir end-----------------------------")
        return listDir

    def checkMinMaxXY(self,lx,ly):
        minX = self.getMinX()
        if lx<=minX:
            return False
        maxX = self.getMaxX()
        if lx>=maxX:
            return False
        minY = self.getMinY()
        if ly<=minY:
            return False
        maxY = self.getMaxY()
        if ly>=maxY:
            return False
        return True

    def getFullAccDir(self,radius):
        listDir = self.getAccDir()
        logging.info("--------------------getFullAccDir begin-----------------------------")
        logging.debug("getFullAccDir listDir = self.getAccDir() {}".format(listDir))
        if len(listDir)==0:
            self.work = False
            return listDir
        lx = self.getX()
        ly = self.getY()
        logging.debug("getFullAccDir lx {} ly {} radius {}".format(lx,ly,radius))
        ltraces = self.getTraces()
        logging.debug("getFullAccDir ltraces {}".format(ltraces))
        listFDir = []
        for d in listDir:
            if d==UP:
                lyr = ly-radius
                logging.debug("getFullAccDir UP lx {} lyr {}".format(lx,lyr))
                if self.checkMinMaxXY(lx,lyr) and (not ((lx,lyr) in ltraces)):
                    listFDir.append(UP)
            elif d==DOWN:
                lyr = ly+radius
                logging.debug("getFullAccDir DOWN lx {} lyr {}".format(lx,lyr))
                if self.checkMinMaxXY(lx,lyr) and (not ((lx,lyr) in ltraces)):
                    listFDir.append(DOWN)
            elif d==LEFT:
                lxr = lx-radius
                logging.debug("getFullAccDir LEFT lxr {} ly {}".format(lxr,ly))
                if self.checkMinMaxXY(lxr,ly) and (not ((lxr,ly) in ltraces)):
                    listFDir.append(LEFT)
            elif d==RIGHT:
                lxr = lx+radius
                logging.debug("getFullAccDir RIGHT lxr {} ly {}".format(lxr,ly))
                if self.checkMinMaxXY(lxr,ly) and (not ((lxr,ly) in ltraces)):
                    listFDir.append(RIGHT)
        logging.debug("getFullAccDir listFDir {}".format(listFDir))
        if len(listFDir)==0:
            for d in listDir:
                if d==UP:
                    lyr = ly-radius
                    for i in range(radius):
                        off = i+1
                        if self.checkMinMaxXY(lx+off,lyr) and (not ((lx+off,lyr) in ltraces)):
                            listFDir.append(UP)
                        elif self.checkMinMaxXY(lx-off,lyr) and (not ((lx-off,lyr) in ltraces)):
                            listFDir.append(UP)
                elif d==DOWN:
                    lyr = ly+radius
                    for i in range(radius):
                        off = i+1
                        if self.checkMinMaxXY(lx+off,lyr) and (not ((lx+off,lyr) in ltraces)):
                            listFDir.append(DOWN)
                        elif self.checkMinMaxXY(lx-off,lyr) and (not ((lx-off,lyr) in ltraces)):
                            listFDir.append(DOWN)
                elif d==LEFT:
                    lxr = lx-radius
                    for i in range(radius):
                        off = i+1
                        if self.checkMinMaxXY(lxr,ly+off) and (not ((lxr,ly+off) in ltraces)):
                            listFDir.append(LEFT)
                        elif self.checkMinMaxXY(lxr,ly-off) and (not ((lxr,ly-off) in ltraces)):
                            listFDir.append(LEFT)
                elif d==RIGHT:
                    lxr = lx+radius
                    for i in range(radius):
                        off = i+1
                        if self.checkMinMaxXY(lxr,ly+off) and (not ((lxr,ly+off) in ltraces)):
                            listFDir.append(LEFT)
                        elif self.checkMinMaxXY(lxr,ly-off) and (not ((lxr,ly-off) in ltraces)):
                            listFDir.append(LEFT)
            logging.debug("getFullAccDir listFDir+off {}".format(listFDir))
            logging.info("--------------------getFullAccDir end-----------------------------")
            if len(listFDir)==0:
                return self.getFullAccDir(radius+1)
            else:
                logging.info("--------------------getFullAccDir end-----------------------------")
                return listFDir

        else:
            logging.info("--------------------getFullAccDir end-----------------------------")
            return listFDir

    def run(self):
        listDir = self.getFullAccDir(1)
        logging.info("--------------------run begin-----------------------------")
        logging.debug("run listDir = self.getFullAccDir() {}".format(listDir))
        if len(listDir)==0:
            return None
        direction = self.getDirection()
        logging.debug("run direction {}".format(direction))
        if not (direction in listDir):
            if len(listDir)==1:
                direction = listDir[0]
            else:
                direction = random.choice(listDir)
            self.setDirection(direction)
        lx = self.getX()
        ly = self.getY()
        logging.debug("run lx {} ly {}".format(lx,ly))
        logging.debug("run sel direction {}".format(direction))
        if direction==UP:
            ly -= 1
        elif direction==DOWN:
            ly += 1
        elif direction==LEFT:
            lx -= 1
        elif direction==RIGHT:
            lx += 1
        logging.debug("run lx {} ly {}".format(lx,ly))
        if self.checkMinMaxXY(lx,ly):
            self.setX(lx)
            self.setY(ly)
            self.setTrace(lx,ly)
        logging.info("--------------------run end-----------------------------")

        if self.getWork():
            Timer(1, self.run).start()

    def __del__(self):
        self.work = False

logging.basicConfig(filename="sample.log", filemode='w', level=logging.DEBUG)
app = Flask(__name__)
ant = Ant()

@app.route('/')
def index():
    if not ant.getWork():
        lx = ant.getX()
        ly = ant.getY()
        ant.setTrace(lx,ly)
        ant.setmaxXYmin()
        ant.setWorking()
        ant.start()
    return render_template('index.html')

@app.route('/status')
def status():
    d = {'Direction': ant.getDirection(), 'X': ant.getX(), 'Y': ant.getY(), 'ContSum': ant.getContSum(), 'Area': ant.getArea()}
    return d

if __name__ == "__main__":
    app.run()
