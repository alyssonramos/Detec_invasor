import numpy as np
import cv2 as cv
import time
from datetime import datetime
from playsound import playsound

x=0
data = datetime.now()
cap = cv.VideoCapture(0)
#ip = "http://192.168.15.2:8080/video"
#cap.open(ip)
# Captura quadro a quadro

ret, frame = cap.read()

#Retângulo vermelho que vai delimitar a área pega pelo sensor

#Webcan do Pc:
a = cv.rectangle(frame,(100,400),(400,128),(0,0,255),1)

#Webcan do celular
#a = cv.rectangle(frame, (1007, 148), (327, 507), (0, 0, 255), 1)

#Webcan do Pc:
#Variáveis para o corte delimitado pelo retângulo vermelho
y1 = 129
h1 = 270

x1 = 101
w1 = 298

#Webcan do celular
#Variáveis para o corte delimitado pelo retângulo vermelho
#y1 = 148
#h1 = 359

#x1 = 327
#w1 = 680

#Pegando a imagem de referência
reference1 = frame[y1:y1+h1, x1:x1+w1]
gray1 = cv.cvtColor(reference1, cv.COLOR_BGR2GRAY)
median1 = cv.medianBlur(gray1,5)
#cv.imshow('image1', a)
cv.imshow('Imagem de referencia', median1)
while True:
    #time.sleep(0.25)
    check, img = cap.read()
    #cv.imshow('cell', img)

    # Webcan do Pc:
    b = cv.rectangle(img, (100, 400), (400, 128), (0, 0, 255), 1)

    # Webcan do celular
    #b = cv.rectangle(img, (1007, 148), (327, 507), (0, 0, 255), 1)

    # Variáveis para o corte delimitado pelo retângulo vermelho

    # Webcan do Pc:
    y2 = 129
    h2 = 270

    x2 = 101
    w2 = 298
    # Pegando a imagem de referência

    # Webcan do celular
    #y2 = 148
    #h2 = 359

    #x2 = 327
    #w2 = 680


    reference2 = img[y2:y2 + h2, x2:x2 + w2]
    gray2 = cv.cvtColor(reference2, cv.COLOR_BGR2GRAY)
    median2 = cv.medianBlur(gray2,5)
    imgdif = abs(median2 - median1)
    ret, thresh1 = cv.threshold(imgdif, 80, 255, cv.THRESH_BINARY)
    laplacian = cv.Laplacian(imgdif, cv.CV_64F)
    ret, thresh2 = (cv.threshold(laplacian, 50, 255, cv.THRESH_BINARY))
    cv.imshow('image2', b)
    cv.imshow('imagem capturada', median2)
    cv.imshow('img diferenca', imgdif)
    cv.imshow('Area', thresh1)
    cv.imshow('Perimetro', thresh2)
    area = np.sum(thresh1 == 255)
    peri = abs(np.sum(thresh2 == 255))


    k = cv.waitKey(250)

    if(x != data):
        print('Area:', area)
        print('Perimetro:', peri)
        if((area > 100) & (peri > 100)):
            check, frame = cap.read()
            #webcan do PC
            y2 = 129
            h2 = 270

            x2 = 101
            w2 = 298

            #Webcan do celular
            #y2 = 148
            #h2 = 359

            #x2 = 327
            #w2 = 680

            reference3 = img[y2:y2 + h2, x2:x2 + w2]

            invasor = cv.putText(reference3, "Invasao!", (30, 100), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
            cv.imshow('invasor', invasor)
            print(data)
            playsound("Alarme2.wav")
            x = data
    if k == ord('q'):
        break

# Libera os recursos ao final.
cap.release()
cv.destroyAllWindows()