import math
import cv2
import datetime


class Car:
    tracks = []

    def __init__(self, Id, xi, yi, min_age, up_limit, down_limit):
        self.id = Id
        self.x = xi
        self.y = yi
        self.tracks = [[xi, yi]]
        self.done = False
        self.counted = False
        self.age = 1
        self.min_age = min_age
        self.t1 = datetime.datetime.now()
        self.tracker = cv2.TrackerKCF_create()
        self.speed = 0
        self.down = down_limit
        self.up = up_limit

    def getId(self):
        return self.id

    def getTrack(self):
        return self.tracks

    # def getState(self):
    #     return  self.state

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def get_age(self):
        return self.age

    def setDone(self):
        self.done = True

    def updateCoord(self, xn, yn, w, h):
        self.x = (xn+w)/2
        self.y = (yn+h)/2
        # dist = math.hypot(self.x - self.tracks[-1][2], self.y - self.tracks[-1][1])
        self.tracks.append([(xn+w)/2, (yn+h)/2])
        if self.tracks[-1][1] > self.up:
            t2 = datetime.datetime.now()
            dt = t2 - self.t1
            self.speed = int((20/dt.total_seconds())*3.6)

    def timed_out(self):
        return self.done

    def stop_count(self):
        self.stop += 1
        if self.stop > self.max_stop:
            self.done = True
        return True

    def age_plus(self):
        self.age += 1
        if self.age >= self.min_age:
            if not self.t1:
                self.t1 = time.time()
        return True

    def is_moving(self):
        if len(self.tracks) > 2:
            if abs(self.tracks[-1][1] - self.tracks[-2][1]) > 5:
                return True
            else:
                return False
        else:
            return False
