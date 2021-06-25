import cv2
# import cvlib as cv
import vehicle
import numpy as np
import math
cars_cascade = cv2.CascadeClassifier('haarcascade_car.xml')
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40, detectShadows=True)


def get_center(x, y, x1, y1):
    cx = int((x+x1)/2)
    cy = int((y+y1)/2)
    return cx, cy


def detect_cars(frame):
    # frame_cropped = frame[100:int(frame.shape[1]/1.5), :, :]
    cars = cars_cascade.detectMultiScale(frame, 1.05, 6)
    return cars


def yolo_detector(frame):
    bbox, label, conf = cv.detect_common_objects(frame)
    detection = []
    for i in range(len(bbox)):
        if label[i] == 'car' and conf[i] >= 0.92:
            detection.append(bbox[i])
    return detection


def detector_subtract(frame):
    kernelop = np.ones((5, 5), np.uint8)
    kernelcl = np.ones((11, 11), np.uint8)
    mask = cv2.GaussianBlur(frame, (11, 11), 0)
    mask = cv2.GaussianBlur(mask, (11, 11), 0)
    mask = cv2.GaussianBlur(mask, (21, 21), 0)
    mask = object_detector.apply(mask, 1)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelop)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelcl)
    mask = cv2.dilate(mask, (9, 9), 2)
    mask = cv2.dilate(mask, (9, 9), 2)
    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detection = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 600:
            x, y, w, h = cv2.boundingRect(cnt)

            detection.append([x, y, w, h])
    return detection, mask


def real_time():
    # getting video frame
    cap = cv2.VideoCapture('cars.mp4')
    pid = 1
    cars = []
    min_age = 5
    count = 0
    min_speed = 80
    FONT = cv2.FONT_HERSHEY_COMPLEX_SMALL
    # looping through video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (640, 480))
        h, w, _ = frame.shape
        up_limit = int(h/1.5)
        down_limit = 100
        roi = frame[100:int(h/1.5), :, :]
        frame = cv2.line(frame, (0, 100), (frame.shape[1], 100), (0, 255, 0), thickness=2)
        frame = cv2.line(frame, (0, up_limit), (frame.shape[1], up_limit), (0, 255, 0)
                         , thickness=2)
        # Detection
        detected, mask = detector_subtract(frame)
        # detected = detect_cars(frame)
        # detected = yolo_detector(frame)
        for item in detected:
            x, y, w, h = item
            bb = [x, y, w, h]
            cx, cy = get_center(x, y, w, h)
            new = True
            if y in range(down_limit, up_limit + 20):
                for car in cars:
                    # Tracking
                    ok, bbox = car.tracker.update(frame)
                    print(car.id)
                    bbox = list(map(int, bbox))
                    # dist = math.hypot(cx - car.tracks[-1][0], cy - car.tracks[-1][1])
                    if ok:
                        new = False
                        car.updateCoord(x, y, w+x, h+y)
                        if car.is_moving():
                            if car.speed > min_speed:
                                cv2.rectangle(frame, (x, y), (x+w, y+h),
                                              color=(0, 0, 255), thickness=2)
                                cv2.putText(frame, str(car.speed), (x, y + 5), FONT, 1, (0, 0, 255))
                                if not car.counted:
                                    count += 1
                            else:
                                cv2.rectangle(frame, (x, y), (x+w, y+h), color=(0, 255, 0), thickness=2)
                                cv2.putText(frame, str(car.speed), (x, y + 5), FONT, 1, (0, 0, 255))

                    if not car.done:
                        if len(car.tracks) >= 2 and car.tracks[-1][1] >= up_limit >= car.tracks[-2][1]:
                            car.setDone()
                            # frame = cv2.line(frame, (0, up_limit), (frame.shape[1], up_limit), (0, 0, 255)
                            #                  , thickness=2)
                            # count += 1
                            # print("done", car.id)
                    if car.done:
                        if y > up_limit:
                            i = cars.index(car)
                            cars.pop(i)
                            del car
                if new:
                    newCar = vehicle.Car(pid, x, y, min_age, up_limit, down_limit)
                    newCar.tracker.init(frame, tuple(bb))
                    cars.append(newCar)
                    pid += 1
        # Display
        cv2.putText(frame, f"OUT:{count}", (50, 40), FONT, 1, (0, 255, 0), 1)
        cv2.imshow('mask', mask)
        cv2.imshow('frame', frame)
        if cv2.waitKey(40) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    real_time()
    print("finish")
