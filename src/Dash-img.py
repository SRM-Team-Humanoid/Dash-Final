#!/usr/bin/env python

import cv2
import numpy as np
import rospy
import time
from std_msgs.msg import String
y,u,v = 0,0,0

cap = cv2.VideoCapture(0)
x =360

flag1 = True
def getArea() :
	move="nothing"
	global x,y,flag1
	[y1,u,v] = [0,90,70]
	rec=True
	area1=0
	while rec:
		boln,f = cap.read()
		img_yuv = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)
		#cv2.imshow("yuv",img_yuv)
		
		mask = cv2.inRange(img_yuv, (np.array([0,u-45,v-45])), (np.array([255,u+45,v+45])))
		#cv2.imshow("Masking",mask)
		erode = cv2.erode(mask,None,iterations = 1)
		dilate = cv2.dilate(erode,None,iterations = 1)
		image,contour,hierarchy = cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		#cv2.drawContours(img_yuv, contour, -1, (0,255,0), 2)
		if contour:
			cnt = contour[0]
			(x,y),radius = cv2.minEnclosingCircle(cnt)
		#center = (int(x),int(y))

		
		if x>340+90 :
			move = "right"

		elif x<300-90 :
			move = "left"
		elif y>240+90:
			move = "tilt_d"

		else:

			if len(contour)>0:
				cnt = contour[0]
				move = "forward"
		print move
		if cv2.waitKey(1) == 27:
			break

                return move



def talker() :
	#msg=raw_input()
	pub=rospy.Publisher('get_area',String,queue_size=1)
	rospy.init_node('talker',anonymous=True) 
	rate=rospy.Rate(10)

	while not rospy.is_shutdown() :
		msg = getArea()
		pub.publish(msg)
              

if __name__=="__main__" :
	try :
		talker()
	except rospy.ROSInterruptException :
		pass
