# USAGE
# python multi_object_tracking.py --video videos/soccer_01.mp4 --tracker csrt

# import the necessary packages
import pandas as pd
import argparse
import imutils
import time
import cv2
import os
from shutil import copyfile

# Default Tracking Video Number for first time Product
version = 'v1'

#CSV File of all the Session IDs to fetch Video Link
videoIDs = pd.read_csv('/Users/shubham/Desktop/Niflr/VideoIds.csv')
videoNumber = 175


while (videoNumber != 200):
	print("Opening New Video Stream:", videoNumber)
	time.sleep(1)
	ap = argparse.ArgumentParser()

	ap.add_argument("-t", "--tracker", type=str, default="kcf",
		help="OpenCV object tracker type")

	args = vars(ap.parse_args())
	# initialize a dictionary that maps strings to their corresponding
	# OpenCV object tracker implementations
	OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.TrackerCSRT_create,
		"kcf": cv2.TrackerKCF_create,
	}

	# initialize OpenCV's special multi-object tracker
	trackers = cv2.MultiTracker_create()

	count = 0
	frameTaken = 0

	videoID = videoIDs.iloc[videoNumber].sessionId
	videoLink = 'https://storage.googleapis.com/live-stream-niflr-prod/' + videoID + '/cam1.mp4'
	videoStream = cv2.VideoCapture(videoLink)
	print("Grabbed New Streaming Video")
	print("\n")

	while True:
		# grab the current frame, then handle if we are using a
		# VideoStream or VideoCapture object
		frame = videoStream.read()
		frame = frame[1]
		

		# check to see if we have reached the end of the stream
		if frame is None:
			videoNumber+=1
			print("Closing Current Video and Opening New Video Stream:", videoNumber)
			break

		# resize the frame (so we can process it faster)
		# frame = imutils.resize(frame, width=600)

		# grab the updated bounding box coordinates (if any) for each
		# object that is being tracked
		(success, boxes) = trackers.update(frame)


		# loop over the bounding boxes and draw then on the frame
		for box in boxes:
			(x, y, w, h) = [int(v) for v in box]

			if ((x>0 and y>0 and (x+w)>0 and (y+h)>0)):
				cv2.imwrite(directory+"/frames"+"/frame"+version+classes+str(count)+".jpg",frame)
				copyfile("anno.xml",directory+"/"+ "annot/frame"+version+classes+str(count)+".xml")
				s = open(directory+"/"+"annot/frame"+version+classes+str(count)+".xml").read()
				s = s.replace("jpg","frame"+version+classes+str(count)+".jpg")
				s= s.replace("cream",classes)

				s = s.replace("xmini",str(x))
				s = s.replace("ymini",str(y))
				s = s.replace("xmaxi",str(x+w))
				s = s.replace("ymaxi",str(y+w))
				f = open(directory+"/"+"annot/frame"+version+classes+str(count)+".xml", 'w')
				f.write(s)
				print("frameTaken = ",frameTaken)
				f.close()
				frameTaken = frameTaken + 1
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		count = count+1

		# show the output frame
		
		
		# print(count)
		cv2.imshow("Frame", frame)
		keyStroke = cv2.waitKey(30) & 0xFF

		# if the 's' key is selected, we are going to "select" a bounding
		# box to track
		if keyStroke == ord("s"):
			# select the bounding box of the object we want to track (make
			# sure you press ENTER or SPACE after selecting the ROI)

			box = cv2.selectROI("Frame", frame, fromCenter=False,
				showCrosshair=True)
			
			tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
			trackers.add(tracker, frame, box)
			print("\n")
			trackedProduct = input("Enter Tracked Product Name: ")
			directory = "/Users/shubham/Desktop/Niflr/Annotation-for-object-detectionin-videos-through-object-tracking/items/"+trackedProduct
			classes = trackedProduct
			print("\n")
			flagg = input("Previously Tracked Product? ")
			if flagg == "n" or flagg == "no" or flagg == "N" or flagg == "NO":
				os.mkdir(directory)
				os.mkdir(directory+"/frames")
				os.mkdir(directory+"/annot")
			else:
				videoVersion = input("Video(Version) Number of Being Tracked Product: ")
				version = videoVersion

		# if the `q` key was pressed, break from the loop
		elif (keyStroke == ord("q") or frameTaken == 5):
			print("frameTaken = ", frameTaken)
			videoNumber+=1
			print("\n")
			videoStream.release()
			break

		if (keyStroke == ord("r")):
			videoStream = cv2.VideoCapture(videoLink)
			print("Restarting the Same Video")
			continue

# if we are using a webcam, release the pointer

# otherwise, release the file pointer

videoStream.release()

# close all windows
cv2.destroyAllWindows()