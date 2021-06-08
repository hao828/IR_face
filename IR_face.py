import time
import picamera
import numpy as np
import cv2
import dlib
import imutils
from pylepton import Lepton
from pylepton.IR_function import generate_colour_map,raw_to_8bit,ktoc
from multiprocessing  import Queue
BUF_SIZE = 2
q = Queue(BUF_SIZE)

import tkinter as tk
from PIL import Image,ImageTk
from tkinter.ttk import *
window = tk.Tk()
window.title("test")

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()


x=0
while True:
    
    
    while(cap.isOpened()):
        Time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        Data_name = '//home//pi//IR_Body//Data//'+ Time + '.jpg'
        ret,frame = cap.read()
        face_rects,scores,idx = detector.run(frame,0)
    
        for i , d in enumerate(face_rects):
            ### only get people face
            x1 = d.left()
            y1 = d.top()
            x2 = d.right()
            y2 = d.bottom()
            text = "%2.2f(%d)"%(scores[i],idx[i])
            #print(scores[i])
            
            
            #if (scores[i] >=1):
            #cv2.imwrite("IMG.jpg",frame)
        with Lepton() as l:
            a,_ = l.capture()
            IR_x1 = x1/8  ### left -shift  right +shift
            IR_y1 = y1/8 
            IR_x2 = x2/8
            IR_y2 = y2/8
            X = a[:,int(IR_x1):int(IR_x2)]
            Y = X[int(IR_y1):int(IR_y2)]
            q.put(a)
            data = q.get(True,500)
            img = cv2.LUT(raw_to_8bit(data), generate_colour_map())
            minVal, maxVal,minLoc, maxLoc = cv2.minMaxLoc(Y)
            Img = cv2.resize(img,(640,480))
            cv2.putText(Img,str(ktoc(maxVal)+2),(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),5,cv2.LINE_AA)
            print(str(ktoc(maxVal)))
            cv2.waitKey(1)
            #print(x2-x1)
            Time = time.strftime("%Y%m%d %H%M%S", time.localtime())
            Sec = time.strftime("%S", time.localtime())
            #print(Sec)
            print(int(Sec)%6)
            cc = int(Sec)% 6
            print(x2-x1)
            
            if((x2-x1) > 125):
                label_A = tk.Label(window,text='A',fg='#263238',font=('Arial',12))
                label_A.grid(column=1,row=2,sticky = 'e')
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),4,cv2.LINE_AA)
                cv2.rectangle(Img,(x1,y1),(x2,y2),(0,255,0),4,cv2.LINE_AA)
                if(cc == 0):
                    cv2.imwrite(Data_name,frame)
                    print(Data_name +" is written!! to 1")
                    img3 = Image.open(Data_name)
                    img3 = img3.resize((img3.width//4,img3.height//4))
                    imgTk3 = ImageTk.PhotoImage(img3)
                    label3 = tk.Label(window,image=imgTk3)
                    label3.image = imgTk3
                    label3.grid(column=0,row=2,sticky = 'w'  )
                    label_3 = tk.Label(window,text=str(Time),fg='#263238',font=('Arial',12))
                    label_3.grid(column=0,row=3,sticky = 'w')
                if(cc == 2):
                    cv2.imwrite(Data_name,frame)
                    print(Data_name +" is written!! to 2")
                    img4 = Image.open(Data_name)
                    img4 = img4.resize((img4.width//4,img4.height//4))
                    imgTk4 = ImageTk.PhotoImage(img4)
                    label4 = tk.Label(window,image=imgTk4)
                    label4.image = imgTk4
                    label4.grid(column=0,row=2)
                    label_4 = tk.Label(window,text=str(Time),fg='#263238',font=('Arial',12))
                    label_4.grid(column=0,row=3)
                    
                if(cc == 4):
                    cv2.imwrite(Data_name,frame)
                    print(Data_name +" is written!! to 3")
                    img5 = Image.open(Data_name)
                    img5 = img5.resize((img5.width//4,img5.height//4))
                    imgTk5 = ImageTk.PhotoImage(img5)
                    label5 = tk.Label(window,image=imgTk5)
                    label5.image = imgTk5
                    label5.grid(column=0,row=2,sticky = 'e')
                    label_5 = tk.Label(window,text=str(Time),fg='#263238',font=('Arial',12))
                    label_5.grid(column=0,row=3,sticky = 'e')
                        
        window.update()
        #time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        label = tk.Label(window,text=str(Time),bg ='yellow',fg='#263238',font=('Arial',12))
        label.grid(column=0,row=0)
        if((ktoc(maxVal)+2)<=37):
            label_1 = tk.Label(window,text="Normal Body Temperature !",bg ='green',fg='#263238',font=('Arial',20))
            label_1.grid(column=1,row=0)
        if((ktoc(maxVal)+2)>37):
            label_1 = tk.Label(window,text="! Alarm Body Temperature !",bg ='red',fg='#263238',font=('Arial',20))
            label_1.grid(column=1,row=0)
        
        #img1 = Image.open(frame)
        img1 = Image.fromarray(frame)
        imgTk1 = ImageTk.PhotoImage(img1)
        label1 = tk.Label(window,image=imgTk1)
        label1.image = imgTk1
        
        Img = Img[...,::-1]
        img2 = Image.fromarray(Img)
        imgTk2 = ImageTk.PhotoImage(img2)
        label2 = tk.Label(window,image=imgTk2)
        label2.image = imgTk2
        
           
        
        
            
        
        label1.grid(column=0,row=1)
        label2.grid(column=1,row=1)
        
        
        
    window.mainloop()