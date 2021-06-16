import math
import cv2

class Car:
    tracks = []

    def __init__(self, Id, xi, yi, min_age):
        self.id = Id
        self.x = xi
        self.y = yi
        self.tracks = [[xi, yi]]
        self.done = False
        self.age = 1
        self.min_age = min_age
        # self.tracker = cv2.legacy
        # self.state = '0'

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
        self.x = (xn+w+xn)/2
        self.y = (yn+h+yn)/2
        # dist = math.hypot(self.x - self.tracks[-1][2], self.y - self.tracks[-1][1])
        self.tracks.append([(xn+w+xn)/2, (yn+h+yn)/2])

    def timed_out(self):
        return self.done

    def stop_count(self):
        self.stop += 1
        if self.stop > self.max_stop:
            self.done = True
        return True

    def age_plus(self):
        self.age += 1
        return True

    def is_moving(self):
        if len(self.tracks) > 2:
            if abs(self.tracks[-1][1] - self.tracks[-2][1]) > 5:
                return True
            else:
                return False
        else:
            return False
