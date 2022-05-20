#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
from PIL import Image
import numpy as np
import cv2
import time

import dataclasses
import sys
from typing import List, Any

pixel_ascii_map = "         .`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$Ñ"

#pixel_ascii_map = "    XYUJCLQ0OZ#MW%BÑ"
"""
Note that the sequence object returned by this method is an internal PIL data type, 
which only supports certain sequence operations. To convert it to an ordinary sequence
(e.g. for printing), use list(im.getdata()).
"""


class OpenCV2():
    def __init__(self,type_input,pathfile,n_cam,totalscale):
        # ----------------------------------------
        self.start_time=time.time()
        self.display_time=2
        self.fps=0

        # Create a black image
        self.img = np.zeros((900,1200,3), np.uint8)
        self.img_clean=self.img.copy()
        # we create the video capture object cap
        if  type_input== "image":
            #self.cap = cv2.VideoCapture("./img/file.mp4")
            self.cap = cv2.VideoCapture(pathfile)
        # or select webcam
        elif  type_input== "webcam":
            self.cap = cv2.VideoCapture(n_cam)

        if not self.cap.isOpened():
            raise IOError("We cannot open webcam/file")
        
        W  = self.cap.get(3)   # float `width`
        H = self.cap.get(4)  # float `height`
        #scale_to fit in window and keeping original image relation
        if W>H:
            width_chr=120
            heigth_chr=(H/W)*width_chr
        else:
            heigth_chr=90
            width_chr=(W/H)*heigth_chr
        
        scaled_x = (width_chr*totalscale)
        scaled_y=(heigth_chr*totalscale)
        print(scaled_x,scaled_y)
        #return
        self.WIDTH = int( scaled_x)
        self.HEIGHT = int(scaled_y)
        self.dim = (self.WIDTH, self.HEIGHT)
        print(self.WIDTH,self.HEIGHT)
        self.show_frame()
        
    #Function to show every frame from a movie, webcam or only a pic.
    def show_frame(self):

        while True:
            #return tuple (boolean, one frame video)
            ret, frame = self.cap.read()
            if ret==True:
                # Our operations on the frame come here
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

                # resize our captured frame if we need
                frame = cv2.resize(gray, self.dim, interpolation=cv2.INTER_AREA)


                #window.after(1000,print("hola"))

                #Cleaning image
                self.img=self.img_clean.copy()

                text = "This is \n some text"
                y0, dy = 0, 10
                for i, line in enumerate(load_pixel(frame,self.WIDTH).split('\n')):
                    y = y0 + i*dy
                    #cv2.putText(img, line, (50, y ), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                    #print(line)
                    x0, dx = 0, 10
                    for j, char in enumerate(list(line)):
                        x = x0 + j*dx
                        #(104, 220, 70)
                        cv2.putText(self.img,char, (x,y),1, 1, (255, 255, 255), cv2.FONT_HERSHEY_PLAIN, cv2.LINE_AA,False)

                # show frame with text
                cv2.imshow("Web cam input", self.img)
                #Waiting for key press
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    print("g")
                    break
                self.fps+=1
                TIME=time.time()-self.start_time
                if TIME>self.display_time:
                    print("FPS:", self.fps/TIME)
                    self.fps=0
                    self.start_time=time.time()
            else:
                self.cap.release()
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    cv2.destroyAllWindows() 
                    break
            
def get_average():
    
    im=np.array(im)
    w,h=im.shape
    print(w,h)
    return np.average(im.reshape(w*h))
    
    
def load_pixel(frame,WIDTH):
    x=list(Image.fromarray(frame).getdata())
    count=0
    string_pic=""
    for pixel in iter(x):
        if count<=WIDTH-2:

            pixel = (pixel * len(pixel_ascii_map))//256 # rescaling
            ascii_val = pixel_ascii_map[pixel]
            

            string_pic=string_pic+ascii_val

            count+=1
        else:
            count=0

            pixel = (pixel * len(pixel_ascii_map)) // 256 # rescaling
            ascii_val = pixel_ascii_map[pixel]

            string_pic=string_pic+"\n"+ascii_val

    # show us frame with detection
    return string_pic

USAGE = f"[OPTION]...\nOPTION \n-w, --webcamera   Select Webcamera '0' (internal) '1' USB camera \n-i, --image   Select image/vido path './img/myvideo.mp4'" 

HELP = f"Usage: python {sys.argv[0]} [-h] [--help] | wecam or file  scale] \n " 

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        print(USAGE)
        return False

def main() -> None: #'->' PEP 3107 – Function Annotations
    #get argument from console
    args = sys.argv[1:]
    type_input="webcam"
    pathfile=""
    n_cam=0
    totalscale=1
    #print(args)
    if not args:
        #print(USAGE)
        raise SystemExit(HELP)
    for i,a in enumerate(args):
        if a == "--help" or  a == "-h"  :
            print(USAGE)
            return
        elif a == "--webcam" or  a == "-w":
            type_input="webcam"
        elif i==1  and a.isdigit():
            n_cam = int(a)

        elif a == "--image" or  a == "-i":
            type_input="image"
        elif i==1  and not a.isdigit():
            pathfile =a

        elif i==2  and isfloat(a):
            totalscale = float(a)   
        else:
            raise SystemExit(HELP)
    
    #print(type_input,pathfile,n_cam,totalscale)
    app = OpenCV2(type_input,pathfile,n_cam,totalscale)

if __name__ == '__main__':
    main()

            


