import torch

import numpy
import random
import pandas
import math
from operator import indexOf, neg
import sys
class Network:
    def __init__(self, learningRate, numberOfInput, numberOfHidden, numberOfOutput):
        self.learningRate = learningRate
        self.numberOfInput = numberOfInput
        self.numberOfHidden = numberOfHidden
        self.numberOfOutput= numberOfOutput
       

        self.inputLayer = {
            "values": [],
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
        # if(number > 0):
        #     return number
        # else:
        #     return int(0)
        return 1/(1+ numpy.exp(neg(number))) #sigmoid

    def reLUPrime(self, number):
        if(number < 0):
            return 0
        else:
            return 1
    def sigmoidPrime(self, number):
        return(number*(1-number))
    def initializeNetwork(self):
        sys.setrecursionlimit(2500)
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
        #self.trainDrugNetwork(0)

    def initializeWeights(self):
        for i in range(len(self.hiddenLayer["values"])-1): #-1 because we dont want to pass to the bias node
            self.inputLayer["weights"].append([])
            for j in range(len(self.inputLayer["values"])):
                self.inputLayer["weights"][-1].append(round(random.uniform(-1,1),2) * math.sqrt(1/10)) #variance is 10 because we have 10 weights with a variance of 1 being added to each hidden node
                                                                                                      #standard deviation is then sqrt(10) which is ~3 which is way higher than the STD of 1 we want
                                                                                                      #therefore we will multiply our std of 1 by sqrt(1/n) to achieve a std and variance of 1
        

        for i in range(len(self.outputLayer["values"])):
            self.hiddenLayer["weights"].append([])
            for j in range(len(self.hiddenLayer["values"])):
                self.hiddenLayer["weights"][-1].append(round(random.uniform(-1,1),2) * math.sqrt(1/7))
        print(self.inputLayer["weights"])

    def passForward(self):
        answer = 0
        self.hiddenLayer["values"] = numpy.matmul(self.inputLayer["weights"], self.inputLayer["values"]) #pass to hidden 
        for node in range(len(self.hiddenLayer["values"])):
            self.hiddenLayer["values"][node] = self.activationFunction(self.hiddenLayer["values"][node])
        self.hiddenLayer["values"] = numpy.insert(self.hiddenLayer["values"], 0, 1) #insert bias (might be a bad idea to do it this way)
        self.outputLayer["values"] = numpy.matmul(self.hiddenLayer["weights"],self.hiddenLayer["values"])
        for node in range(len(self.outputLayer["values"])):
            self.outputLayer["values"][node] = self.activationFunction(self.outputLayer["values"][node])
       

    def trainNetwork(self):
        data = pandas.read_excel("D:/Programming/Repositories/irregularVolumeNN/normalization/normalizedData.xlsx") #We are going to use 500 data points
        correctClassifications = 0
        numberOfClassifications = 0
        
        for ticker in range(500): #one epoch, 500 data points
            numberOfClassifications += 1
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
                    pass
            self.inputLayer["values"][7] = data.iloc[ticker, 3:4].values[0] #volume node
            self.inputLayer["values"][8] = data.iloc[ticker, 5:6].values[0] #price
            self.inputLayer["values"][9] = data.iloc[ticker, 6:7].values[0] #change when found
            ticker += 1

            self.passForward() #passforwardeachrow
           
            correctValue = data.iloc[ticker, 7:8].values[0] #expectedOutPut in table
            if(self.outputLayer["values"][0] > self.outputLayer["values"][1]): #1 = Green, 0 = Red
                estimatedValue = 1
            else:
                estimatedValue = 0

            if(correctValue==estimatedValue):
                correctClassifications += 1
                continue
            else:
                self.backpropagation(correctValue)
        print(correctClassifications/numberOfClassifications)
        while(correctClassifications/numberOfClassifications <= 0.85): #looking for 85% accuracy

            self.trainNetwork()
           
    def trainDrugNetwork(self, success):
        data = pandas.read_excel("D:/Programming/Repositories/irregularVolumeNN/normalization/normalizedDrugData.xlsx")
        correctClassifications = 0
        numberOfClassifications = 0

        for sample in range(200):
            numberOfClassifications += 1
            for i in range(8):
                self.inputLayer["values"][i+1] = 0 #reset one hot values 
            match data.iloc[sample, 1:2].values[0]: #gender
                case 'M':
                    self.inputLayer["values"][1] = 1
                case 'F':
                    self.inputLayer["values"][2] = 1
                case _:
                    pass
            match data.iloc[sample, 2:3].values[0]: #BP
                case "HIGH":
                    self.inputLayer["values"][3] = 1
                case "NORMAL":
                    self.inputLayer["values"][4] = 1
                case "LOW":
                    self.inputLayer["values"][5] = 1
                case _:
                    pass
            match data.iloc[sample, 3:4].values[0]: #chlorestrol
                case "HIGH":
                    self.inputLayer["values"][6] = 1
                case "NORMAL":
                    self.inputLayer["values"][7] = 1
                case _:
                    pass
            self.inputLayer["values"][8] = data.iloc[sample, 4:5].values[0]
            self.inputLayer["values"][9] = data.iloc[sample, 0:1].values[0]
            self.passForward()
         
            correctValue = data.iloc[sample, 5:6].values[0]
            match correctValue:
                case "DrugY":
                    correctAnswer = [1,0,0,0,0]
                case "drugX":
                    correctAnswer = [0,1,0,0,0]
                case "drugA":
                    correctAnswer = [0,0,1,0,0]
                case "drugB":
                    correctAnswer = [0,0,0,1,0]
                case "drugC":
                    correctAnswer = [0,0,0,0,1]
            if(indexOf(correctAnswer,max(correctAnswer))) == indexOf(self.outputLayer["values"],max(self.outputLayer["values"])):
                correctClassifications += 1
            else:
                self.backpropagation(correctAnswer) 
        successRate = (correctClassifications / numberOfClassifications)
        print(successRate)
        if((successRate) < 0.92):
            self.trainDrugNetwork(successRate)
        else:
            print(self.inputLayer)
            print(self.outputLayer)

    #to determine delta in output nodes, we will calculate the error in the output nodes (expected - actual) and then multiply that by our Fprime value
    #to determine delta in hidden nodes, we will get its fprime value, multiply it by the weight and once again multiply by the delta in the output layer
    #the total delta for the hidden nodes will be a summation of these calculations, one for each time a hidden node points to an output node 
    # (f’(w11x1+w21x2+w01x0) x w14xΔ4+ f’(w11x1+w21x2+w01x0) x w15xΔ5) for example if there was two output nodes

    def backpropagation(self,correctValue):
        self.hiddenLayer["deltas"] = []
        self.outputLayer["deltas"] = []
        if correctValue == 1:  #band aid fix, we shouldnt have the correct value be specific to one data set 
            correctValue = [1,0]
        if correctValue == 0: 
            correctValue = [0,1]

        for i in range(self.numberOfOutput): #calculate delta at each point, expected - actual for error
            error = correctValue[i] - (self.outputLayer["values"][i]) #if expected output is 1, "values"[0]=1, otherwise [1]=1 
            self.outputLayer["deltas"].append(self.sigmoidPrime(self.outputLayer["values"][i]) * error)
         
        for i in range(self.numberOfHidden + 1): 
            delta = 0
            for j in range(self.numberOfOutput): 
                delta += ((self.sigmoidPrime(self.hiddenLayer["values"][i])) * self.hiddenLayer["weights"][j][i] * self.outputLayer["deltas"][j]) #how can we change the weight of a bias if it's delta will always be zero?
            self.hiddenLayer["deltas"].append(delta)
        self.changeWeights()


    #Each weight will be updated to -> current weight += (learning rate * delta of the node it points to * input value node where weights are being changed)
    def changeWeights(self):
        #change hidden layer weights, access weight [0][0] first then [1][0] then iterate upwards to access each weight as the matrix is a 2x7
        for i in range(self.numberOfHidden + 1):
            for j in range(self.numberOfOutput):
                self.hiddenLayer["weights"][j][i] += self.learningRate * self.outputLayer["deltas"][j] * self.hiddenLayer["values"][i]
      
        #change input layer weights
        for i in range(self.numberOfInput + 1):
            for j in range(self.numberOfHidden):
                self.inputLayer["weights"][j][i] += self.learningRate * self.hiddenLayer["deltas"][j] * self.inputLayer["values"][i]


#drugNetwork = Network(0.09,9,15,5)
#15 hidden neurons works really well
#0.07 got to ~85 *** so did 0.075 idk
#0.1 -> ~73
#same with 0.05^
#0.08 -> ~63
#drugNetwork.initializeNetwork()

network = Network(0.075, 9, 18, 2) #maybe should be 9,5,2
network.initializeNetwork()


#values 1x10
#weights 6x10

#values 1x7
#weights 2x7

#This means that weights of the first hidden node to both nodes will be the first index in each array
#the weights of the second node will be the second index of each array etc etc. 