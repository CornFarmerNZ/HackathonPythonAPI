from flask import Flask
import keras
import numpy as np


from keras.layers import Dense
from keras.models import Sequential

import pickle


app = Flask(__name__)


@app.route('/')
def home():
    print("Running...")
    modelTest()

    return "Home."


def modelTest():
    model = pickle.load(open('DalmatianNewModel.pkl', 'rb'))
    # sex, age, weight, height
    inputPet = [5, 12, 55, 22], [5, 12, 5, 60], [5, 12, 28, 58]
    #examples - 1 is overweight; 2 is underweight; 3 is healthy2
    #1: over, 2: under, 0: healthy
    array = np.asarray(inputPet)
    print(array)
    #result = model.predict(array)
    #print(result)

    y_pred = model.predict(inputPet)
    print(y_pred)
    pred = list()

    for i in range(len(y_pred)):
        pred.append(np.argmax(y_pred[i]))
    print(pred)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
