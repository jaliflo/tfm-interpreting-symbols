# Este es el script con el que se comunica la la aplicación web
# para obtener los términos de los símbolos de entrada.

import numpy as np
import time
import os
from PIL import Image
from keras.applications.xception import Xception
from keras.applications.resnet50 import ResNet50
from keras import models
from terms_collection import get_term_list_english, get_term_list_spanish

def predict_resnet(img_path):
    '''
    Procesa el símbolo de entrada con la red ResNet y devuelve los tres
    términos de mayor porbabilidad.
    '''
    IMG_SIZE = 224
    
    model = ResNet50(include_top=True, weights=None, classes=24)
    model.load_weights("symbol_model_resnet50v2.h5")

    img = Image.open(img_path)
    img = img.convert('RGB')
    img = img.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)

    to_predict = np.array([np.array(img)]).reshape(-1, IMG_SIZE, IMG_SIZE, 3)

    prob = np.array([n*100 for n in model.predict(to_predict)])
    
    array_terms_en = get_term_list_english('dataset_augmented')
    array_terms_es = get_term_list_spanish('dataset_augmented')

    sort_args = np.argsort(prob[0])

    top_3_terms = ""
    top_3_terms = top_3_terms+array_terms_en[sort_args[sort_args.size-1]]+'/'+array_terms_es[sort_args[sort_args.size-1]]+","
    top_3_terms = top_3_terms+array_terms_en[sort_args[sort_args.size-2]]+'/'+array_terms_es[sort_args[sort_args.size-2]]+","
    top_3_terms = top_3_terms+array_terms_en[sort_args[sort_args.size-3]]+'/'+array_terms_es[sort_args[sort_args.size-3]]

    return top_3_terms

def predict_xception(img_path):
    '''
    Procesa el símbolo de entrada con la red Xception y devuelve los tres
    términos de mayor porbabilidad.
    '''
    IMG_SIZE = 299
   
    model = Xception(include_top=True, weights=None, classes=24)
    model.load_weights("symbol_model_xceptionv2_weights.h5")

    img = Image.open(img_path)
    img = img.convert('RGB')
    img = img.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)

    to_predict = np.array([np.array(img)]).reshape(-1, IMG_SIZE, IMG_SIZE, 3)

    prob = np.array([n*100 for n in model.predict(to_predict)])

    array_terms_en = get_term_list_english('dataset_augmented')
    array_terms_es = get_term_list_spanish('dataset_augmented')

    sort_args = np.argsort(prob[0])

    top_3_terms = ""
    top_3_terms = top_3_terms+array_terms_en[sort_args[sort_args.size-1]]+'/'+array_terms_es[sort_args[sort_args.size-1]]+","
    top_3_terms = top_3_terms+array_terms_en[sort_args[sort_args.size-2]]+'/'+array_terms_es[sort_args[sort_args.size-2]]+","
    top_3_terms = top_3_terms+array_terms_en[sort_args[sort_args.size-3]]+'/'+array_terms_es[sort_args[sort_args.size-3]]

    return top_3_terms

if __name__ == '__main__':
    mean_time = 0
    counter = 0

    directory = 'prueba_rendimiento'
    for img in os.listdir(directory):
        path = os.path.join(directory, img)

        predict_xception(path)