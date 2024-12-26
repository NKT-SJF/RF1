import cv2 as cv
import os
import serial
import requests
import time

#Configuración de la ip del arduino
ard_ip = "http://10.50.4.205"

dataPath = r'C:\Users\garri\OneDrive\Escritorio\Reconocimiento Facial\Data'
imagePaths = os.listdir(dataPath)
print('imagePaths=',imagePaths)

#face_recognizer = cv.face.EigenFaceRecognizer_create()
face_recognizer = cv.face.FisherFaceRecognizer_create()
#face_recognizer = cv.face.LBPHFaceRecognizer_create()

#Leyendo modelo
#face_recognizer.read('modeloEigenFace.xml')
face_recognizer.read('modeloFisherFace.xml')
#face_recognizer.read('modeloLBPHFace.xml')

#cap = cv.VideoCapture("rtsp://admin:admin@10.50.4.191/cam/realmonitor?channel=1&subtype=0",cv.CAP_FFMPEG)
cap = cv.VideoCapture(0,cv.CAP_DSHOW)

cap.set(cv.CAP_PROP_FRAME_HEIGHT,640)
cap.set(cv.CAP_PROP_FRAME_WIDTH,480)

faceClassif = cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_default.xml')

tiempo_contador = 5
ultimo_envio = time.time()
frame_cant = 0
skip_frames = 1

registro_path = r'C:\Users\garri\OneDrive\Escritorio\Reconocimiento Facial\Registro'
if not os.path.exists(registro_path):
    os.makedirs(registro_path)
while True:
    ret, frame = cap.read()
    if ret == False:
        break

    frame_cant+=1
    if frame_cant%skip_frames!=0:
        continue

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    auxframe = gray.copy()

    faces = faceClassif.detectMultiScale(gray,1.3,5)

    for(x,y,w,h) in faces:
        rostro = auxframe[y:y+h,x:x+w]
        rostro = cv.resize(rostro,(150,150), interpolation=cv.INTER_CUBIC)
        result = face_recognizer.predict(rostro)

        cv.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv.LINE_AA)
        
        #EigenFaces
        #if result[1]<5700:
        #    cv.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(255,255,0),1,cv.LINE_AA)
        #    cv.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
        #else:
        #    cv.putText(frame, 'Desconocido', (x,y-20),2,0.8,(0,0,255),1,cv.LINE_AA)
        #    cv.rectangle(frame, (x,y), (x+w, y+h), (0,0,255),2)
        

        #FisherFaces
        if result[1]<500:
            cv.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(255,255,0),1,cv.LINE_AA)
            cv.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)

            if time.time() - ultimo_envio >= tiempo_contador:
                try:
                    tiempo = 0
                    #envia señal al arduino por una solicitud HTTP
                    response = requests.get(f"{ard_ip}/ON")
                    print("Se envió la señal al arduino: ", response.text)
                    
                    ultimo_envio = time.time()

                    rostro_imagen = frame[y:y + h, x:x + w]
                    rostro_filename = f'{imagePaths[result[0]]}_{int(time.time())}.jpg'
                    rostro_path = os.path.join(registro_path, rostro_filename)
                    cv.imwrite(rostro_path, rostro_imagen)
                    print(f"Imagen guardada como {rostro_filename}")

                except Exception as e:
                    print("Error al enviar la señal: ", e)

        else:
            cv.putText(frame, 'Desconocido', (x,y-20),2,0.8,(0,0,255),1,cv.LINE_AA)
            cv.rectangle(frame, (x,y), (x+w, y+h), (0,0,255),2)

        #LBPH
        #if result[1]<65:
        #    cv.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(255,255,0),1,cv.LINE_AA)
        #    cv.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
        #else:
        #    cv.putText(frame, 'Desconocido', (x,y-20),2,0.8,(0,0,255),1,cv.LINE_AA)
        #    cv.rectangle(frame, (x,y), (x+w, y+h), (0,0,255),2)

    cv.imshow('frame', frame)
    k = cv.waitKey(5)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()