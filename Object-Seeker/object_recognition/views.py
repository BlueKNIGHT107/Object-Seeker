from django.shortcuts import render
from django.http import HttpResponse 
from django.urls import path

import cv2
import numpy as np
import json
# Create your views here.


    
def home(request):
    message=obj_recog(request)
    file=open("obj.txt",'w')
    print(type(message),message)
    json.dump(message, file)
    file.close()
    return render(request, 'index.html', {'items':'Nothing Entered'})

def search(request):
    file=open("obj.txt")
    message=json.load(file)
    message=recog(request, message)
    file.close()
    return render(request, 'index.html', {'items':message})


def obj_recog(request):
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    cap.set(10,70)

    Objects_in_frame=[]
    classNames= []
    classFile = 'objects.names'
    with open(classFile,'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')




    configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'frozen_inference_graph.pb'




    net = cv2.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)



    while True:
        current_objects=[]
        success,img = cap.read()
        
        classIds, confs, bbox = net.detect(img,confThreshold=0.5)
        





        if len(classIds) != 0:
            for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):

                #cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),color=(0,255,0),thickness=2)
                cv2.rectangle(img, box, color=(255, 255, 0), thickness=2)

                cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                            cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                            cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                b=[]
                for i in range(len(box)):
                    b.append(int(box[i]))
                current_objects.append({str(classId-1):b})
                
        Objects_in_frame.append(current_objects)

        cv2.imshow("Output",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return(Objects_in_frame)

def recog(request,Objects_in_frame):
    classNames= []
    classFile = 'objects.names'
    with open(classFile,'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')
    lost_object= request.GET['itemseeker']
    lost_object=lost_object.lower()

    if lost_object in classNames:
        lost_object_ID=classNames.index(lost_object)
    else:
        lost_object_ID="null"

    hx1, hy1, hx2, hy2 = 0,0,0,0
    search_index=-1
    TotalFrames=len(Objects_in_frame)
    for frames in range(TotalFrames-1,-1,-1):
        for objects in Objects_in_frame[frames]:
            if str(lost_object_ID) in objects:
                search_index=frames
                hx1, hy1, hx2, hy2 = objects[str(lost_object_ID)][0] , objects[str(lost_object_ID)][1] , objects[str(lost_object_ID)][2] , objects[str(lost_object_ID)][3]
                break

    found_in=0
    found=[]
    for frames in range(search_index,TotalFrames):
        for objects in Objects_in_frame[frames]:
            object_id=list(objects.keys())[0]
            if object_id!=lost_object_ID:
                found_in=object_id
                px1, py1, px2, py2 = objects[found_in][0],objects[found_in][1],objects[found_in][2],objects[found_in][3]
                if hx1 >= px1 and hy1 >= py1 and hx2 <= px2 and hy2 <= py2:
                    found.append(classNames[int(found_in)])

    found=set(found) 
    print(found)
    found_in=''
    if found==[]:
        found_in ="Sorry "+lost_object+" not found :-("
    
    else:
        if len(found)!=1:
            found.remove(lost_object)
        for i in found:
            found_in+=i+', '
        found_in=found_in.rstrip(', ')

    return( found_in)

