import numpy
import random
import pandas
import math

class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.weight = []
        self.delta = 0

def activationFunction(number): #sigmoid for now, will probably swap to reLU if we need to normalize our data
    return 1/(1+ numpy.exp(-abs(number)))

def initializeNetwork():
    inputLayer = []
    hiddenLayer = []
    outputLayer = []
    inputLayer.append(Node(1)) #bias node
    hiddenLayer.append(Node(1)) #bias node

    data = pandas.ExcelFile("D:/Programming/Repositories/screenerSettings/highVolume.xlsx")

 
    for hiddenNode in range(10):
        hiddenLayer.append(Node(None))
    for outPutNode in range(2):
        outputLayer.append(Node(None))
    initializeWeights(inputLayer, hiddenLayer, outputLayer)

def initializeWeights(inputLayer, hiddenLayer, outputLayer):
    for node in inputLayer:
        for randomWeight in range(10):
            node.append(round(random.uniform(0,1),2)) #10 weight values for each hidden node a input node passes to

    for node in hiddenLayer:
        for randomWeight in range(3):
            node.append((round(random.uniform(0,1),2)))


data = pandas.read_excel("D:/Programming/Repositories/screenerSettings/highVolume.xlsx")

print(data.iloc[:,4:5])