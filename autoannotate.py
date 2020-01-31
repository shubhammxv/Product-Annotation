# USAGE

"""
Load the CSV File of the Video IDs and run the script by following Command in the Terminal

python (filename).py --tracker csrt

Press "x" to skip the current Video
Press "r" to restart the same video
Press "c" to cancel the process
Press "Enter" after making box to enter the tracked product details

"""

# Import the necessary packages
import pandas as pd
import argparse
import imutils
import time
import cv2
import os
from shutil import copyfile

# Default Tracking Video Number for first time Product
version = 'v1'

# CSV File of all the Session IDs to fetch Video Link
csvPath = '/Users/shubham/Desktop/Niflr/Annotation-for-object-detectionin-videos-through-object-tracking/CSV Files/Doritos.csv'
print(csvPath)
videoIDs = pd.read_csv(csvPath)
videoNumber = 20			   											# Initial Video Number in the file to Start From


while (videoNumber != 30):      					   					# Please Choose No. of Videos to Play in one loop as per convenience
	print("Opening New Video Stream:", videoNumber)    					# Track of the Current Video Number
	time.sleep(1)
	ap = argparse.ArgumentParser()

	ap.add_argument("-t", "--tracker", type=str, default="kcf",
		help="OpenCV object tracker type")

	args = vars(ap.parse_args())
	# Initialize a dictionary that maps strings to their corresponding
	# OpenCV object tracker implementations
	OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.TrackerCSRT_create,
		"kcf": cv2.TrackerKCF_create,
	}

	#Initialize OpenCV's special multi-object tracker
	trackers = cv2.MultiTracker_create()
	count = 0
	frameTaken = 0

	videoID = videoIDs.iloc[videoNumber].sessionId
	videoLink = 'https://storage.googleapis.com/live-stream-niflr-prod/' + videoID + '/cam1.mp4'
	videoStream = cv2.VideoCapture(videoLink)
	print("Grabbed New Streaming Video")
	print("\n")

	while True:
		frame = videoStream.read()
		frame = frame[1]

		# Check to see if we have reached the end of the stream
		if frame is None:
			videoNumber+=1
			print("Closing Current Video and Opening New Video Stream:", videoNumber)
			break

		# Resize the frame (so we can process it faster)
		# Frame = imutils.resize(frame, width=600)

		# Grab the updated bounding box coordinates (if any) for each object that is being tracked
		(success, boxes) = trackers.update(frame)

		# Loop over the bounding boxes and draw them on the frame
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

		cv2.imshow("Frame", frame)
		keyStroke = cv2.waitKey(60) & 0xFF

		# If the 's' key is selected, we are going to "select" a bounding box to track
		if keyStroke == ord("s"):
			# Select the bounding box of the object we want to track (make
			# Sure you press ENTER or SPACE after selecting the ROI)

			box = cv2.selectROI("Frame", frame, fromCenter=False,
				showCrosshair=True)

			tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
			trackers.add(tracker, frame, box)
			print("\n")
			trackedProduct = input("Enter Tracked Product Name: ")

			#Enter the directory Path where tracked objects are to be saved in the system

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

		# If the `q` key was pressed, break from the loop
		elif (keyStroke == ord("q") or frameTaken == 10):
			print("frameTaken = ", frameTaken)
			videoNumber+=1
			print("\n")
			videoStream.release()
			break

		if (keyStroke == ord("r")):
			videoStream = cv2.VideoCapture(videoLink)
			print("Restarting the Same Video")
			continue

		if (keyStroke == ord("x")):
			videoNumber+=1
			videoID = videoIDs.iloc[videoNumber].sessionId
			videoLink = 'https://storage.googleapis.com/live-stream-niflr-prod/' + videoID + '/cam1.mp4'
			videoStream = cv2.VideoCapture(videoLink)
			print("Skipping Current Video and Opening New Video Stream:", videoNumber)
			continue


# Release the file pointer
videoStream.release()

# Close all windows
cv2.destroyAllWindows()
