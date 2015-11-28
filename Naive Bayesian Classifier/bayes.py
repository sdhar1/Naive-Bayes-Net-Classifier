'''
Created on Nov 19, 2015

@author: satyamdhar
'''
import sys
import arff
import math
import random

trainingData = arff.load(open(sys.argv[1], 'rb'))
testData = arff.load(open(sys.argv[2],'rb'))

class trainInst:
    def __init__(self, instance):
        self.attrValues=instance
      
    def setAttrVal(self,AttributeIndex):
        self.value=self.attrValues[AttributeIndex]
        
    def display(self):
        self.attrValues


class Attribute:
    def __init__(self,attribute,attributeIndex):
        self.name=attribute[0]
        self.values=attribute[1]
        self.index=attributeIndex
        self.numberOfInstancesWithValue = []
        self.numberOfPositiveInstancesWithValue = []
        for value in self.values:
            self.numberOfInstancesWithValue.append(0)
            self.numberOfPositiveInstancesWithValue.append(0)

def predictedClass(testInstance,attributes,n):
    probabilitiesOfYgivenX = []
    for j in range(len(attributes[-1].values)):
        probabilityOfXgivenY = 1.0
        probabilityOfY = (attributes[-1].numberOfInstancesWithValue[j]+1)/float(n+2)
#         print probabilityOfY
#         probabilityOfYprime = (attributes[-1].numberOfInstancesWithValue[1]+1)/float(attributes[-1].numberOfInstancesWithValue[0]+attributes[-1].numberOfInstancesWithValue[1]+2) #rm
#         probabilityOfXgivenYprime = 1.0 #rm
        for i in range(len(attributes)-1):
            if j==0:
                numberOfInstancesWithYandX = attributes[i].numberOfPositiveInstancesWithValue[attributes[i].values.index(testInstance[i])] + 1
            else :
                numberOfInstancesWithYandX = attributes[i].numberOfInstancesWithValue[attributes[i].values.index(testInstance[i])] - attributes[i].numberOfPositiveInstancesWithValue[attributes[i].values.index(testInstance[i])] + 1
            numberOfInstancesWithY = attributes[-1].numberOfInstancesWithValue[j] + len(attributes[i].values)
#             print 'prob of Xi',numberOfInstancesWithYandX/float(numberOfInstancesWithY)
#             print 'num of instances with x =',attributes[i].name,'and y =',j,'is',numberOfInstancesWithYandX
#             print 'num of y with value',j,'is',attributes[-1].numberOfInstancesWithValue[j]
            probabilityOfXgivenY *= numberOfInstancesWithYandX/float(numberOfInstancesWithY)
#             print probabilityOfXgivenY
        probabilitiesOfYgivenX.append(probabilityOfY*probabilityOfXgivenY)
            
#     print probabilitiesOfYgivenX
    s = sum(probabilitiesOfYgivenX)
#     print s
    for i in range(len(probabilitiesOfYgivenX)):
        probabilitiesOfYgivenX[i] = probabilitiesOfYgivenX[i]/s
#             numberOfInstancesWithYprimeandX = attributes[i].numberOfPositiveInstancesWithValue[attributes[i].values.index(testInstance[i])] + 1
#             numberOfInstancesWithYprime = attributes[-1].numberOfInstancesWithValue[1] + len(attributes[i].values)
#             probabilityOfXgivenYprime *= numberOfInstancesWithYprimeandX/float(numberOfInstancesWithYprime)
        
#     print probabilityOfY,probabilityOfYprime,probabilityOfXgivenY,probabilityOfXgivenYprime
#     print probabilitiesOfYgivenX
    return probabilitiesOfYgivenX.index(max(probabilitiesOfYgivenX))
def main():
    attributes=[]           #list of training instance objects
    for attribute in trainingData['attributes']:
        attributeIndex = trainingData['attributes'].index(attribute)
        attributeObj = Attribute(attribute,attributeIndex)
        attributes.append(attributeObj)
    
    trainingInstances=[]    #list of training instance objects
    for instance in trainingData['data']:
        objInstance=trainInst(instance)
        for i in range(len(instance)): 
            #precomputing number of instances for every attribute
            attributes[i].numberOfInstancesWithValue[attributes[i].values.index(instance[i])]+=1
            if instance[-1] == attributes[-1].values[0]:
#                 print attributes[i].values
                attributes[i].numberOfPositiveInstancesWithValue[attributes[i].values.index(instance[i])]+=1 
        trainingInstances.append(objInstance)
    
    print len(attributes)
    for attribute in attributes:
        print attribute.name,attribute.values
        print attribute.numberOfInstancesWithValue
        print attribute.numberOfPositiveInstancesWithValue
        
    for instance in testData['data']:
        print instance[-1]
        print attributes[-1].values[predictedClass(instance, attributes, len(trainingInstances))]
#         print attributes[-1].values[0] if probabilityOfYgivenX(instance, attributes)>0.5 else attributes[-1].values[1]
    
    
main()