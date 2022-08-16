from email.policy import default
from optparse import Values
import numpy
import random
import pandas
import math
from operator import neg
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
        for i in range(len(self.hiddenLayer["values"])-1): #-1 because we dont want to pass to the bias node
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
       

    def trainNetwork(self):
        data = pandas.read_excel("D:/Programming/Repositories/irregularVolumeNN/normalizedData.xlsx") #We are going to use 500 data points
        correctClassifications = 0
        numberOfClassifications = 0
        for ticker in range(5): #one epoch, 500 data points
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
                    print("No mktcap found")
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

    def backpropagation(self,correctValue):
        self.hiddenLayer["deltas"] = []
        self.outputLayer["deltas"] = []
        if correctValue == 1:
            correctValue = [1,0]
        else:
            correctValue = [0,1]
        print(correctValue)
        for i in range(self.numberOfOutput): #calculate delta at each point, expected - actual for error
            error = correctValue[i] - (self.outputLayer["values"][i]) #if expected output is 1, "values"[0]=1, otherwise [1]=1 
            self.outputLayer["deltas"].append(self.sigmoidPrime(self.outputLayer["values"][i]) * error) #****pretty sure we use original values here, not the reLU values...
         
        for i in range(self.numberOfHidden + 1): 
            delta = 0
            for j in range(self.numberOfOutput): 
                # print("sigmoid " + str(self.sigmoidPrime(self.hiddenLayer["values"][i])))
                # print("weight " + str(self.hiddenLayer["weights"][j][i]))
                # print("delta " + str(self.outputLayer["deltas"][j]))
                delta += ((self.sigmoidPrime(self.hiddenLayer["values"][i])) * self.hiddenLayer["weights"][j][i] * self.outputLayer["deltas"][j]) #how can we change the weight of a bias if it's delta will always be zero?
            self.hiddenLayer["deltas"].append(delta)
            print(self.hiddenLayer["deltas"])
        self.changeWeights()



def changeWeights(self):
    # for i in range(self.numberOfInput):
    return
network = Network(0.1, 9, 6, 2) #maybe should be 9,5,2
network.initializeNetwork()


#values 1x10
#weights 6x10

#values 1x7
#weights 2x7

#This means that weights of the first hidden node to both nodes will be the first index in each array
#the weights of the second node will be the second index of each array etc etc. 