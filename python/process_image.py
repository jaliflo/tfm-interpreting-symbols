#!C:\Users\jalif\AppData\Local\Programs\Python\Python37\python.exe
import cgi
import json

print('Content-Type: application/json')
print()

import cgitb
cgitb.enable(display=0, logdir="../python/error-log")

import base64
import cv2
import numpy as np
from predict_keras import predict_xception
from scipy.ndimage import imread
from os import listdir
from os.path import isfile, join
from terms_collection import get_term_list_biling

def recortar_imagen(path):
    '''
    Devuelve la imagen dada como entrada recortada a su contenido.

    '''
    img = imread(path, flatten=True).astype(int)

    first_col = len(img)
    first_row = len(img[0])
    last_col = 0
    last_row = 0

    for i in range(len(img)):
        for j in range(len(img[i])):
            if(img[i][j]<255 and j<first_col):
                first_col = j

    for j in range(len(img[0])):
        for i in range(len(img)):
            if img[i][j]<255 and i < first_row:
                first_row = i

    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i][j]<255 and j>last_col:
                last_col = j

    for j in range(len(img[0])):
        for i in range(len(img)):
            if img[i][j]<255 and i > last_row:
                last_row = i

    img = img[first_row:last_row+1]

    num_row = last_row-first_row+1
    num_col = last_col-first_col+1

    recortada = np.ndarray(shape=(num_row, num_col))

    for i in range(len(img)):
        recortada[i] = list(img[i][first_col:last_col+1])

    return recortada

data = cgi.FieldStorage()
img_string_raw = data['imgBase64'].value
img_string = img_string_raw.replace('data:image/jpeg;base64,', '')
img_bytes = img_string.encode()

path_to_image = '..\\python\\img\\input.jpg'

with open(path_to_image, 'wb') as image:
    image.write(base64.decodebytes(img_bytes))

if isfile(path_to_image):
    recortada = recortar_imagen(path_to_image)

    iden = len(listdir('..\\python\\img\\users_images'))+1
    img_name = '..\\python\\img\\users_images\\'+str(iden)+'.jpg'
    cv2.imwrite(img_name, recortada)

    out = predict_xception(img_name)

    term_list = get_term_list_biling('dataset_augmented')
    
    response = {
        'result': "OK",
        'term': out,
        'termList': term_list,
        'path': img_name
    }
else:
    response = {
        'result': "FAIL"
    }

print(json.dumps(response))