

# import the necessary packages

from imutils.video import WebcamVideoStream
import numpy as np
import face_recognition 
import argparse
import imutils
import pickle
import time
import cv2
import pymysql
from datetime import datetime, timedelta
from tkinter import *
import sys
import pyautogui 



# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
    help="path to serialized db of facial encodings")
ap.add_argument("-o", "--output", type=str,
    help="path to output video")
ap.add_argument("-y", "--display", type=int, default=1,
    help="whether or not to display output frame to screen")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
    help="face detection model to use: either `hog` or `cnn`")

args = vars(ap.parse_args())

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

# initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = WebcamVideoStream(src=0).start()
writer = None
orig_stdout = sys.stdout
f = open('D:/hadi/SEAS/Log.txt', 'w')
sys.stdout = f

# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream
    # convert the input frame from BGR to RGB then resize it to have
    # a width of 750px (to speedup processing)
    frame = vs.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb = imutils.resize(frame, width=750)
    r = frame.shape[1] / float(rgb.shape[1])

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input frame, then compute
    # the facial embeddings for each face
    boxes = face_recognition.face_locations(rgb,
        model=args["detection_method"])
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
            encoding)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)
        
        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # rescale the face coordinates
        top = int(top * r)
        right = int(right * r)
        bottom = int(bottom * r)
        left = int(left * r)

        # draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom),
            (230, 230, 250), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_TRIPLEX,
            0.75, (221, 160, 221), 2)

    # if the video writer is None *AND* we are supposed to write
    # the output video to disk initialize the writer
    if writer is None and args["output"] is not None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(args["output"], fourcc, 20,
            (frame.shape[1], frame.shape[0]), True)

      # check to see if we are supposed to display the output frame to
    # the screen
    if args["display"] > 0:
        cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Frame",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    
    # if the writer is not None, write the frame with recognized
    # faces t odisk
    if writer is not None:
        writer.write(frame)
        for name in names:
            if name != "Unknown":
                root = Tk()
                root.update_idletasks()
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
                x = screen_width/2 - size[0]/2
                y = screen_height/2 - size[1]/2
                root.geometry("+%d+%d" % (x, y)) 
                root.title("STATUS") 
                l = Label(root, text = "Please wait...")   
                l.pack()
                root.after(5000, root.destroy)
                root.mainloop()

                # Recheck Face..
                frame = vs.read()
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb = imutils.resize(frame, width=750)
                r = frame.shape[1] / float(rgb.shape[1])
                boxes = face_recognition.face_locations(rgb,
                    model=args["detection_method"])
                encodings = face_recognition.face_encodings(rgb, boxes)
                names = []
                for encoding in encodings:
                    matches = face_recognition.compare_faces(data["encodings"],
                        encoding)
                    name = "Unknown"
                    if True in matches:
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}
                        for i in matchedIdxs:
                            name = data["names"][i]
                            counts[name] = counts.get(name, 0) + 1
                        name = max(counts, key=counts.get)
                    names.append(name)
                for ((top, right, bottom, left), name) in zip(boxes, names):
                    top = int(top * r)
                    right = int(right * r)
                    bottom = int(bottom * r)
                    left = int(left * r) 
                    cv2.rectangle(frame, (left, top), (right, bottom),
                        (230, 230, 250), 2)
                    y = top - 15 if top - 15 > 15 else top + 15
                    cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_TRIPLEX,
                        0.75, (221, 160, 221), 2)
                if writer is not None:
                    writer.write(frame)
                    for name in names:

                        # Checking and Quering for Punching IN and OUT
                        if name != "Unknown": 

                            now = datetime.today()
                            now1= now.strftime('%Y%m%d%H%M%S')
                            nowdate= now.strftime("%Y-%m-%d")
                            nowtime= now.strftime("%H:%M:%S")
                            yesterday =now - timedelta(days = 1)
                            yesdate= yesterday.strftime("%Y-%m-%d")
                            

                            conn = pymysql.connect(host="localhost",port=3308,db="employee",user="Hadi",password="Douda.@12345")
                            cursor = conn.cursor()
                            conn.begin()
                            sql = "SELECT COUNT(*) FROM time_in WHERE staffid= (%s) and date = (%s)  "
                            cursor.execute(sql , (name, nowdate))
                            conn.commit()
                            (number_of_rows,)= cursor.fetchone()

                            conn2 = pymysql.connect(host="localhost",port=3308,db="employee",user="Hadi",password="Douda.@12345")
                            cursor2 = conn2.cursor()
                            conn2.begin()
                            sql2 = "SELECT COUNT(*) FROM time_out WHERE staffid= (%s) and date = (%s)  "
                            cursor2.execute(sql2 , (name, nowdate))
                            conn2.commit()
                            (number_of_rows2,)= cursor2.fetchone()

                            conn3 = pymysql.connect(host="localhost",port=3308,db="employee",user="Hadi",password="Douda.@12345")
                            cursor3 = conn3.cursor()
                            conn3.begin()
                            sql3 = "SELECT COUNT(*) FROM time_in WHERE staffid= (%s) and date = (%s)  "
                            cursor3.execute(sql3 , (name, yesdate))
                            conn3.commit()
                            (number_of_rows3,)= cursor3.fetchone() 

                            conn4 = pymysql.connect(host="localhost",port=3308,db="employee",user="Hadi",password="Douda.@12345")
                            cursor4 = conn4.cursor()
                            conn4.begin()
                            sql4 = "SELECT COUNT(*) FROM time_out WHERE staffid= (%s) and date = (%s)  "
                            cursor4.execute(sql4 , (name, yesdate))
                            conn4.commit()
                            (number_of_rows4,)= cursor4.fetchone() 
                
                            print(" FIRST Connection established sucessfully")

                            if  number_of_rows == number_of_rows2 and number_of_rows3 == number_of_rows4   : 
                                root = Tk()
                                root.update_idletasks()
                                screen_width = root.winfo_screenwidth()
                                screen_height = root.winfo_screenheight()
                                size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
                                x = screen_width/2 - size[0]/2
                                y = screen_height/2 - size[1]/2
                                root.geometry("+%d+%d" % (x, y)) 
                                root.title("STATUS") 
                                l = Label(root, text = "Checking IN...")   
                                l.pack()
                                root.after(5000, root.destroy)
                                root.mainloop()
                                now = datetime.today()
                                conn1 = pymysql.connect(host="localhost",port=3308,db="employee",user="Hadi",password="Douda.@12345")
                                print(" SECOND Connection established sucessfully")
                                cursor1 = conn1.cursor()
                                conn1.begin()
                                sql1 = """INSERT INTO time_in VALUES (%s, %s, %s)""", (name , nowtime, nowdate)
                                cursor1.execute(*sql1)
                                conn1.commit()
                                cursor1.close()
                                conn1.close() 
                                image = pyautogui.screenshot()  
                                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) 
                                cv2.imwrite("D:/hadi/SEAS/output/" + now1 + ".png", image) 
                                print(" checked IN Sucessfully for ",name, " at ",nowdate, " ",nowtime)
                                root = Tk() 
                                root.update_idletasks()
                                screen_width = root.winfo_screenwidth()
                                screen_height = root.winfo_screenheight()
                                size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
                                x = screen_width/2 - size[0]/2
                                y = screen_height/2 - size[1]/2
                                root.geometry("+%d+%d" % (x, y)) 
                                root.title("STATUS") 
                                l = Label(root, text = "Checked IN SUCCESSFULLY")       
                                l.pack()
                                root.after(5000, root.destroy)
                                root.mainloop()

                            if  number_of_rows != number_of_rows2 and number_of_rows3 != number_of_rows4  : 
                                root = Tk()
                                root.update_idletasks()
                                screen_width = root.winfo_screenwidth()
                                screen_height = root.winfo_screenheight()
                                size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
                                x = screen_width/2 - size[0]/2
                                y = screen_height/2 - size[1]/2
                                root.geometry("+%d+%d" % (x, y)) 
                                root.title("STATUS") 
                                l = Label(root, text = "Checking IN...")   
                                l.pack()
                                root.after(5000, root.destroy)
                                root.mainloop()
                                now = datetime.today()
                                conn1 = pymysql.connect(host="localhost",port=3308,db="employee",user="Hadi",password="Douda.@12345")
                                print(" SECOND Connection established sucessfully")
                                cursor1 = conn1.cursor()
                                conn1.begin()
                                sql1 = """INSERT INTO time_in VALUES (%s, %s, %s)""", (name , nowtime, nowdate)
                                cursor1.execute(*sql1)
                                conn1.commit()
                                cursor1.close()
                                conn1.close()
                                image = pyautogui.screenshot()  
                                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) 
                                cv2.imwrite("D:/hadi/SEAS/output/" + now1 + ".png", image)   
                                print(" checked IN Sucessfully for ",name, " at ",nowdate, " ",nowtime)
                                root = Tk() 
                                root.update_idletasks()
                                screen_width = root.winfo_screenwidth()
                                screen_height = root.winfo_screenheight()
                                size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
                                x = screen_width/2 - size[0]/2
                                y = screen_height/2 - size[1]/2
                                root.geometry("+%d+%d" % (x, y)) 
                                root.title("STATUS") 
                                l = Label(root, text = "Checked IN SUCCESSFULLY")       
                                l.pack()
                                root.after(5000, root.destroy)
                                root.mainloop()

                            if  number_of_rows != number_of_rows2 and number_of_rows3 == number_of_rows4  :  
                                root = Tk()
                                root.update_idletasks()
                                screen_width = root.winfo_screenwidth()
                                screen_height = root.winfo_screenheight()
                                size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
                                x = screen_width/2 - size[0]/2
                                y = screen_height/2 - size[1]/2
                                root.geometry("+%d+%d" % (x, y)) 
                                root.title("STATUS") 
                                l = Label(root, text = "Checking OUT...")   
                                l.pack()
                                root.after(5000, root.destroy)
                                root.mainloop()  
                                now = datetime.today()
                                conn1 = pymysql.connect(host="localhost",port=3308,db="employee",user="Hadi",password="Douda.@12345")
                                print(" SECOND Connection established sucessfully")
                                cursor1 = conn1.cursor()
                                conn1.begin()
                                sql1 = """INSERT INTO time_out VALUES (%s, %s, %s)""", (name , nowtime, nowdate)
                                cursor1.execute(*sql1)
                                conn1.commit()
                                cursor1.close()
                                conn1.close()
                                image = pyautogui.screenshot()  
                                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) 
                                cv2.imwrite("D:/hadi/SEAS/output/" + now1 + ".png", image) 
                                print(" checked OUT Sucessfully for ",name, " at ",nowdate, " ",nowtime)
                                root = Tk()
                                root.update_idletasks()
                                screen_width = root.winfo_screenwidth()
                                screen_height = root.winfo_screenheight()
                                size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
                                x = screen_width/2 - size[0]/2
                                y = screen_height/2 - size[1]/2
                                root.geometry("+%d+%d" % (x, y))
                                root.title("STATUS") 
                                l = Label(root, text = "Checked OUT SUCCESSFULLY")   
                                l.pack()
                                root.after(5000, root.destroy)
                                root.mainloop()

                            if  number_of_rows == number_of_rows2 and number_of_rows3 != number_of_rows4  :  
                                root = Tk()
                                root.update_idletasks()
                                screen_width = root.winfo_screenwidth()
                                screen_height = root.winfo_screenheight()
                                size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
                                x = screen_width/2 - size[0]/2
                                y = screen_height/2 - size[1]/2
                                root.geometry("+%d+%d" % (x, y)) 
                                root.title("STATUS") 
                                l = Label(root, text = "Checking OUT...")   
                                l.pack()
                                root.after(5000, root.destroy)
                                root.mainloop()  
                                now = datetime.today()
                                conn1 = pymysql.connect(host="localhost",port=3308,db="employee",user="Hadi",password="Douda.@12345")
                                print(" SECOND Connection established sucessfully")
                                cursor1 = conn1.cursor()
                                conn1.begin()
                                sql1 = """INSERT INTO time_out VALUES (%s, %s, %s)""", (name , nowtime, nowdate)
                                cursor1.execute(*sql1)
                                conn1.commit()
                                cursor1.close()
                                conn1.close()
                                image = pyautogui.screenshot()  
                                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) 
                                cv2.imwrite("D:/hadi/SEAS/output/" + now1 + ".png", image) 
                                print(" checked OUT Sucessfully for ",name, " at ",nowdate, " ",nowtime)
                                root = Tk()
                                root.update_idletasks()
                                screen_width = root.winfo_screenwidth()
                                screen_height = root.winfo_screenheight()
                                size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
                                x = screen_width/2 - size[0]/2
                                y = screen_height/2 - size[1]/2
                                root.geometry("+%d+%d" % (x, y))
                                root.title("STATUS") 
                                l = Label(root, text = "Checked OUT SUCCESSFULLY")   
                                l.pack()
                                root.after(5000, root.destroy)
                                root.mainloop() 

                            

                        else:   
                            root = Tk()
                            root.update_idletasks()
                            screen_width = root.winfo_screenwidth()
                            screen_height = root.winfo_screenheight()
                            size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
                            x = screen_width/2 - size[0]/2
                            y = screen_height/2 - size[1]/2
                            root.geometry("+%d+%d" % (x, y)) 
                            root.title("STATUS") 
                            l = Label(root, text = "Try Again")   
                            l.pack()
                            root.after(5000, root.destroy)
                            root.mainloop() 
                            cursor.close()
                            conn.close()
                            cursor2.close()
                            conn2.close()
                            cursor3.close()
                            conn3.close()
                            cursor4.close()
                            conn4.close()
                            

                if writer is None and args["output"] is not None:
                    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                    writer = cv2.VideoWriter(args["output"], fourcc, 20,
                        (frame.shape[1], frame.shape[0]), True)
                
                  
                if args["display"] > 0:
                    cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
                    cv2.setWindowProperty("Frame",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
                    cv2.imshow("Frame", frame)
                    key = cv2.waitKey(1) & 0xFF

                    
                    if key == ord("q"):
                        break
                   
                
  

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
sys.stdout = orig_stdout
f.close()
# check to see if the video writer point needs to be released
if writer is not None:
    writer.release()
