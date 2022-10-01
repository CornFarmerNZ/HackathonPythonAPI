import pickle
import random

import numpy as np
from flask import Flask, request

app = Flask(__name__)

petHealthyWeights = {"Other": [2, 3], "Beagles": [1.34, 2.33], "Boxers": [2.62, 3.51], "Bullmastiff": [3.88, 5.24],
                     "Bloodhounds": [3.36, 4.44],
                     "Dalmatian": [1.89, 3.71], "German Shepherd": [2.1, 3.78], "Great Danes": [3.7, 5.88],
                     "Labrador Retriever": [2.36, 3.58],
                     "Pug": [1.09, 1.81],
                     "Rottweilers": [3.23, 5.67], "St. Bernards": [4.32, 6.48]}


@app.route('/')
def home():
    print("Running...")
    # modelTest()

    return modelDalmatian()


@app.route('/predictHealthyWeight', methods=['GET'])
def predictHealthyWeight():
    breed = str(request.args.get('breed'))
    sex = str(request.args.get('sex'))
    sexString = sex
    age = float(request.args.get('age'))
    weight = float(request.args.get('weight'))
    height = float(request.args.get('height'))

    bmiUserInput = (weight * 2.54) / (height / 2.205)
    bmiRange = (petHealthyWeights.get(breed))

    match sex:
        case "Male":
            sex = 1
        case "Female":
            bmiRange[0] *= 0.95
            bmiRange[1] *= 0.95
            sex = 0
        case "Neutered":
            bmiRange[0] *= 0.98
            bmiRange[1] *= 0.98
            sex = 2
        case "Spayed":
            bmiRange[0] *= 0.94
            bmiRange[1] *= 0.94
            sex = 3
    print("INPUT - Breed " + breed + " Age: " + str(age) + " Sex: " + sexString + " Weight: " + str(
        weight) + " " + "Height: " + str(height))
    print("Normal BMI range: " + "{:.2f}".format((bmiRange[0])) + " to " + "{:.2f}".format(
        bmiRange[1]) + " Input's BMI: " + "{:.2f}".format(
        bmiUserInput))
    if breed == "Dalmatian":
        return modelDalmatian(sex, age, weight, height)
    if bmiRange[0] < bmiUserInput < bmiRange[1]:
        return "Healthy"
    elif bmiRange[0] > bmiUserInput:
        return "Underweight"
    else:
        return "Overweight"


def modelDalmatian(sex, age, weight, height):
    model = pickle.load(open('DalmatianNewModel.pkl', 'rb'))
    # sex, age, weight, height

    inputArray = [sex, age, weight, height], [sex, age, weight, height]
    array = np.asarray(inputArray)
    print(array)

    y_pred = model.predict(array)
    print(y_pred)
    pred = list()

    for i in range(len(y_pred)):
        pred.append(np.argmax(y_pred[i]))
    print(pred)
    # result is a classification from either 0,1,2, since I used OneHotEncoder to convert them into binary
    # 1: over, 2: under, 0: healthy
    match pred[0]:
        case 1:
            return "Overweight"
        case 2:
            return "Underweight"
        case 0:
            return "Healthy"
    return "Error 404. Please try again."


@app.route('/predictIllness', methods=['GET'])
def predictIllness():
    breed = str(request.args.get('breed'))
    sex = str(request.args.get('sex'))
    age = float(request.args.get('age'))
    weight = float(request.args.get('weight'))
    height = float(request.args.get('height'))

    return "{:.2f}".format(random.uniform(10, 98))


@app.route('/predictBehaviour', methods=['GET'])
def predictBehaviour():
    breed = str(request.args.get('breed'))
    sex = str(request.args.get('sex'))
    age = float(request.args.get('age'))
    weight = float(request.args.get('weight'))
    height = float(request.args.get('height'))
    behaviours = ['Energetic', 'Loving', 'Protective', 'Loud', 'Quiet', 'Enthusiastic', 'Active', 'Calm', 'Relaxed',
                  'Content', 'Happy', 'Cheerful', 'Affectionate', 'Playful', 'Loyal', 'Friendly', 'Intelligent']  # 16

    result = "Error 404: Result not found"
    match breed:
        case "Other":
            result = behaviours[random.randrange(0, 10)]
        case "Beagles":
            result = behaviours[12] + " and " + behaviours[11]
        case "Boxers":
            result = behaviours[0] + ", " + behaviours[5] + " and " + behaviours[2]
        case "Bullmastiff":
            result = behaviours[1] + ", " + behaviours[11] + " and " + behaviours[9]
        case "Dalmatian":
            result = behaviours[0] + ", " + behaviours[13] + " and " + behaviours[14]
        case "German Shepherd":
            result = behaviours[2] + " and " + behaviours[14]
        case "Great Danes":
            result = behaviours[1] + ", " + behaviours[5] + " and " + behaviours[15]
        case "Labrador Retriever":
            result = behaviours[16] + ", " + behaviours[15] + " and " + behaviours[1]
        case "Pug":
            result = behaviours[7] + ", " + behaviours[12] + " and " + behaviours[9]
        case "Rottweilers":
            result = behaviours[13] + " and " + behaviours[7]
        case "St. Bernards":
            result = behaviours[12] + " and " + behaviours[8]

    return result


@app.route('/test')
def test():
    results = ""
    #   "Male", "Female", "Neutered", "Spayed"
    breed = "Dalmatian"
    sexes = [1, 0, 2, 3]
    age = 12
    weight = 29
    height = 58
    results += "Breed: " + breed + " Sex: " + "Male" + " Age: " + str(age) + " Weight: " + str(
        weight) + " Height: " + str(height) + "<br>"
    results += "Resulting classification: " + (predictHealthyWeightTest(breed, sexes[0], age, weight, height) + "<br>")
    results += "Breed: " + breed + " Sex: " + "Neutered" + " Age: " + str(age) + " Weight: " + str(
        weight) + " Height: " + str(height) + "<br>"
    results += "Resulting classification: " + (predictHealthyWeightTest(breed, sexes[2], age, weight, height) + "<br>")

    return results


def predictHealthyWeightTest(breed, sex, age, weight, height):
    bmiUserInput = (weight * 2.54) / (height / 2.205)
    bmiRange = (petHealthyWeights.get(breed))
    sexString = ""
    match sex:
        case 0:
            sexString = "Female"
        case 1:
            sexString = "Male"
        case 2:
            sexString = "Neutered"
        case 3:
            sexString = "Spayed"

    match sex:
        case "Male":
            sex = 1
        case "Female":
            bmiRange[0] *= 0.95
            bmiRange[1] *= 0.95
            sex = 0
        case "Neutered":
            bmiRange[0] *= 0.98
            bmiRange[1] *= 0.98
            sex = 2
        case "Spayed":
            bmiRange[0] *= 0.94
            bmiRange[1] *= 0.94
            sex = 3
    print("INPUT - Breed " + breed + " Age: " + str(age) + " Sex: " + sexString + " Weight: " + str(
        weight) + " " + "Height: " + str(height))
    print("Normal BMI range: " + "{:.2f}".format((bmiRange[0])) + " to " + "{:.2f}".format(
        bmiRange[1]) + " Input's BMI: " + "{:.2f}".format(
        bmiUserInput))
    if breed == "Dalmatian":
        return modelDalmatian(sex, age, weight, height)
    if bmiRange[0] < bmiUserInput < bmiRange[1]:
        return "Healthy"
    elif bmiRange[0] > bmiUserInput:
        return "Underweight"
    else:
        return "Overweight"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
