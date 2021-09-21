# En este script se procesan las imágenes utilizando el modelo generado
# con el perceptrón multicapa. Este script se ha utilizado para las pruebas
# mostradas en la memoria.

from sklearn.neural_network import MLPClassifier
from joblib import load
from os import listdir
from os.path import isfile, join
from PIL import Image
import numpy as np
import sys, getopt
import time

def preprocess_image(img_path):
    '''
    Transforma la imagen de entrada en un vector de números.
    '''
    img = Image.open(img_path)
    img = img.convert('L')
    img = img.resize((299, 299), Image.ANTIALIAS)
    img = np.array(img)

    nx, ny = img.shape
    img = img.reshape(nx*ny)

    return img

def predict(img_path):
    '''
    Carga el modelo del MLPerceptron y devuelve el resultado procesado
    por el mismo.
    '''
    clf = load('symbol_model.joblib')
    
    img = preprocess_image(img_path)
    return clf.predict([img])[0]

if __name__ == '__main__':
    mean_time = 0
    counter = 0

    directory = 'prueba_rendimiento'
    for img in listdir(directory):
        path = join(directory, img)

        pre = time.time()
        print(predict(path))
        post = time.time()

        pred_time = post-pre
        mean_time = mean_time + pred_time
        counter = counter+1
        print('Pred time: '+str(pred_time))

    mean_time = mean_time/counter
    print('Mean time: '+str(mean_time))
