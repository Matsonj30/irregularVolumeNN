import numpy
from numpy import ravel
import random
import pandas
import math
class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.delta = 0

class Network:

    def __init__(self, learningRate, numberOfInput, numberOfHidden, numberOfOutput):
        self.learningRate = learningRate
        self.numberOfInput = numberOfInput
        self.numberOfHidden = numberOfHidden
        self.numberOfOutput= numberOfOutput


      
        self.inputLayer = {
            "values": [],
            "deltas":[],
            "weights":[],
        }
        self.hiddenLayer = {
            "values": [],
            "deltas":[],
            "weights":[],
        }
        self.outputLayer = {
            "values": [],
            "deltas":[],
        }
    

    def activationFunction(number): #sigmoid for now, will probably swap to reLU if we need to normalize our data
        return 1/(1+ numpy.exp(-abs(number)))

    def sigmoidPrime(number):
        return
    def initializeNetwork(self):
        self.inputLayer["values"].append(1) #bias node
        self.hiddenLayer["values"].append(1) #bias node
        
        data = pandas.ExcelFile("D:/Programming/Repositories/screenerSettings/highVolume.xlsx")

        for inputNode in range(10):
             self.inputLayer["values"].append(inputNode)
        for hiddenNode in range(6):
             self.hiddenLayer["values"].append(hiddenNode)
        for outPutNode in range(2):
             self.outputLayer["values"].append(outPutNode)
        self.initializeWeights()
        

    def initializeWeights(self):
        for i in range(len(self.hiddenLayer["values"])-1):
            self.inputLayer["weights"].append([])
            for j in range(len(self.inputLayer["values"])):
                self.inputLayer["weights"][-1].append(round(random.uniform(-1,1),2))
        print(self.inputLayer)

        for i in range(len(self.outputLayer["values"])):
            self.hiddenLayer["weights"].append([])
            for j in range(len(self.hiddenLayer["values"])):
                self.hiddenLayer["weights"][-1].append(round(random.uniform(-1,1),2))
        print(self.hiddenLayer)
        self.passForward()

    def passForward(self):
        answer = 0
        self.hiddenLayer["values"] = numpy.matmul(self.inputLayer["weights"], self.inputLayer["values"]) #pass to hidden 
        for node in range(len(self.hiddenLayer["values"])):
            self.inputLayer["values"][node] = self.activationFunction(self.inputLayer["values"][node])

            
        self.hiddenLayer["values"] = numpy.insert(self.hiddenLayer["values"], 0, 1) #insert bias (might be a bad idea to do it this way)
        self.outputLayer["values"] = numpy.matmul(self.hiddenLayer["weights"],self.hiddenLayer["values"])
  
        # print(self.hiddenLayer["values"])
        # print(self.hiddenLayer["weights"])

        # print(self.outputLayer["values"])
        # print(self.outputLayer["weights"])

    def trainNetwork(self):
        return


# data = pandas.read_excel("D:/Programming/Repositories/screenerSettings/highVolume.xlsx")

# print(data.iloc[:,4:5])

weight1 = [[1,1,1,1,1,1,1,1,1,1], #6x10
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1],
]
values = [[1], #10x1 INPUT DICT has to look like this for matmult to work
[1], 
[1],
[1],
[1],
[1],
[1],
[1],
[1],
[1],


] #1 x 1


network = Network(0.05, 10, 6, 2)
network.initializeNetwork()
