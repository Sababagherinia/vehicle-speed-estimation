# vehicle-speed-estimation
a program to detect and track moving vehicle on a highway video example and estimating their speed
this process consists of four major steps:
1. capturing video
2. detecting objects
3. tracking detected objects
4. estimating speed of tracked objects
## capturing video
using **open-cv** **videocapture** method we take every frame of the input video on by one and start processing that and while there is frame to process we prepare our **ROI**
and start detecting
## detection
we tried three different approches to achieve this goal
### Haarcascade Classifier
a method which uses **viola-jones** algorithm to detect objects and is provided by **cv2.CascadeClassifier()** method and it needs some computed weights in form of .xml file which is
provided by name the function written to apply that is called **detect_cars**  **haarcascade_car.xml** here to detect vehicles ****although due to being a very old and inaccurate method to detect objects it didn't give very good result and thus
we moved on to next method***
### Background Subtraction
the second method which is provided by **cv2.createBackgroundSubtractorMOG2()** is method that takes a series of consecutive frames and subtract the background from moving objects.
**detector_subtract** function after getting the subtracted mask and applying some preprocessing and post processing on that returns the desired moving objects from the extracted contours
in form of a list of **bounding boxes**
### Yolo object detector
the last method to try was using a model created by neural networks **Yolo object detector** learned on **coco** dataset which has the weights of some commen objects pre-traind and ready
to use including vehicles to used this we imported and installed **cvlib** and **tensorflow** packages **yolo_detector** function applyes object detector of Yolo and returns the bounding boxes
with desired confidence in form of a list. this method has the best accuracy result and is recommended if convenient hard-ware is provided.
## Tracking
this part is applied on every detected object by creating **KCF** tracker provided by **open-cv** in the car class from vehicle module which we wrote our selves
it creates a tracker whenever an object is created and set the initial states and update the tracker every time on next frame to keep the track of moving objects
it is to ensure when to create new object and also used to estimate the speed
## estimating speed
for this mean we take the first time an object is created and if it reaches some point in the frame we take the time again then we divide the difference if distance by difference of two times
and multiply by **3.6** to convert it to **KMh** it's all done in **car** calss of vehicle module in function **updateCoord**

* notice : this part is highly depended on the position of road and camera and shoud be calibrated by the sitution the numbers used here are completely hypothetical
