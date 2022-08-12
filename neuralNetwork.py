from email.policy import default
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
    

    def activationFunction(self,number): #sigmoid for now, will probably swap to reLU cause apparently it is king
        return(max(0, number)) #RELU
        #return 1/(1+ numpy.exp(-abs(number))) #sigmoid

    def sigmoidPrime(number):
        return
    def initializeNetwork(self):
        self.inputLayer["values"].append(1) #bias node
        self.hiddenLayer["values"].append(1) #bias node
        
       
        for inputNode in range(self.numberOfInput):
             self.inputLayer["values"].append(0)
        for hiddenNode in range(self.numberOfHidden):
             self.hiddenLayer["values"].append(0)
        for outputNode in range(self.numberOfOutput):
             self.outputLayer["values"].append(0)
        self.initializeWeights()
        self.trainNetwork()

    def initializeWeights(self):
        for i in range(len(self.hiddenLayer["values"])-1):
            self.inputLayer["weights"].append([])
            for j in range(len(self.inputLayer["values"])):
                self.inputLayer["weights"][-1].append(round(random.uniform(-1,1),2))
        

        for i in range(len(self.outputLayer["values"])):
            self.hiddenLayer["weights"].append([])
            for j in range(len(self.hiddenLayer["values"])):
                self.hiddenLayer["weights"][-1].append(round(random.uniform(-1,1),2))
      
       

    def passForward(self):
        answer = 0
        self.hiddenLayer["values"] = numpy.matmul(self.inputLayer["weights"], self.inputLayer["values"]) #pass to hidden 
        for node in range(len(self.hiddenLayer["values"])):
            self.hiddenLayer["values"][node] = self.activationFunction(self.hiddenLayer["values"][node])
        self.hiddenLayer["values"] = numpy.insert(self.hiddenLayer["values"], 0, 1) #insert bias (might be a bad idea to do it this way)

        self.outputLayer["values"] = numpy.matmul(self.hiddenLayer["weights"],self.hiddenLayer["values"])
        for node in range(len(self.outputLayer["values"])):
            self.outputLayer["values"][node] = self.activationFunction(self.outputLayer["values"][node])

        print(self.hiddenLayer["values"])
        print(self.outputLayer["values"])
       

    def trainNetwork(self):
        data = pandas.read_excel("D:/Programming/Repositories/irregularVolumeNN/normalizedData.xlsx") #We are going to use 500 data points
        correctClassifications = 0
        numberOfClassifications = 0
        for ticker in range(207): #one epoch, 500 data points
            for i in range(5): #reset one hot values
                self.inputLayer["values"][i+1] = 0
            match data.iloc[ticker, 4:5].values[0]: #mkt cap column in excel file
                case "Nano":
                    self.inputLayer["values"][1] = 1
                case "Micro":
                      self.inputLayer["values"][2] = 1
                case "Small":
                    self.inputLayer["values"][3] = 1
                case "Mid":
                    self.inputLayer["values"][4] = 1
                case "Large":
                    self.inputLayer["values"][5] = 1
                case "Mega":
                    self.inputLayer["values"][6] = 1
                case _:
                    print("No mktcap found")
            self.inputLayer["values"][7] = data.iloc[ticker, 3:4].values[0] #volume node
            self.inputLayer["values"][8] = data.iloc[ticker, 5:6].values[0] #price
            self.inputLayer["values"][9] = data.iloc[ticker, 6:7].values[0] #change when found
            ticker += 1

            self.passForward() #passforwardeachrow

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

network = Network(0.05, 9, 6, 2)
network.initializeNetwork()
