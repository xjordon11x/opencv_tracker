# Import the required modules
import urllib
import numpy as np
import dlib
import cv2
import argparse as ap
import get_points

def run(source=0, dispLoc=True):
    # Create the VideoCapture object
    url='http://10.9.0.8:8080/video/video.jpg'
    cva=cv2.VideoCapture(url)
    # Use urllib to get the image and convert into a cv2 usable format
    imgResp=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    #cam = cv2.VideoCapture(source)

    # If Camera Device is not opened, exit the program
    #if not cam.isOpened():
    #    print "Video device or file couldn't be opened"
    #    exit() 
    print "Press key `p` to pause the video to start tracking"
    while True:
        # Retrieve an image and Display it.
#	imga=cv2.imread(imgNp,-1)
        #retval, img = cam.read()
        #if not retval:
        #    print "Cannot capture frame device"
        #    exit()
        imgResp=urllib.urlopen(url)
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
        img=cv2.imdecode(imgNp,-1)

        if(cv2.waitKey(10)==ord('p')):
            break
#        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
#    cv2.destroyWindow("Image")
    print("TEST")
    # Co-ordinates of objects to be tracked 
    # will be stored in a list named `points`
    points = get_points.run(img) 

    if not points:
        print "ERROR: No object to be tracked."
        exit()
    
#    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    imgResp=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)

    cv2.imshow("Image", img)

    # Initial co-ordinates of the object to be tracked 
    # Create the tracker object
    tracker = dlib.correlation_tracker()
    # Provide the tracker the initial position of the object
    tracker.start_track(img, dlib.rectangle(*points[0]))

    while True:
        # Read frame from device or file
        # Update the tracker  
        imgResp=urllib.urlopen(url)
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
        img=cv2.imdecode(imgNp,-1)

        tracker.update(img)
        # Get the position of the object, draw a 
        # bounding box around it and display it.
        rect = tracker.get_position()
        pt1 = (int(rect.left()), int(rect.top()))
        pt2 = (int(rect.right()), int(rect.bottom()))
        cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
        print "Object tracked at [{}, {}] \r".format(pt1, pt2),
        if dispLoc:
            loc = (int(rect.left()), int(rect.top()-20))
            txt = "Object tracked at [{}, {}]".format(pt1, pt2)
            cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
 #       cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
        # Continue until the user presses ESC key
        if cv2.waitKey(1) == 27:
            break

    # Relase the VideoCapture object

if __name__ == "__main__":
    # Parse command line arguments

    # Get the source of videoW
    run(0, True)
