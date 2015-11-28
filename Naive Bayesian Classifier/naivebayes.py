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
    def __init__(self,attribute,attributeIndex,numberOfClasses):
        self.name=attribute[0]
        self.values=attribute[1]
        self.index=attributeIndex
        self.numberOfInstancesWithValue = []
        self.numberOfEachClassInstancesWithValue = []
        self.numberOfInstancesWithValue = [ 0 for value in self.values]
        for i in range(numberOfClasses):
            list = [0 for x in self.numberOfInstancesWithValue]
            self.numberOfEachClassInstancesWithValue.append(list)

def predictClass(testInstance,attributes,n):
    probabilitiesOfYgivenX = []
    for j in range(len(attributes[-1].values)):
        probabilityOfXgivenY = 1.0
        probabilityOfY = (attributes[-1].numberOfInstancesWithValue[j]+1)/float(n+2)
        for i in range(len(attributes)-1):
            numberOfInstancesWithYandX = attributes[i].numberOfEachClassInstancesWithValue[j][attributes[i].values.index(testInstance[i])] + 1
            numberOfInstancesWithY = attributes[-1].numberOfInstancesWithValue[j] + len(attributes[i].values)
            probabilityOfXgivenY *= numberOfInstancesWithYandX/float(numberOfInstancesWithY)
        probabilitiesOfYgivenX.append(probabilityOfY*probabilityOfXgivenY)
            
    s = sum(probabilitiesOfYgivenX)
    probabilitiesOfYgivenX = [p/s for p in probabilitiesOfYgivenX]
    return (attributes[-1].values[probabilitiesOfYgivenX.index(max(probabilitiesOfYgivenX))],max(probabilitiesOfYgivenX))

def main():
    attributes=[]           #list of training instance objects
    numberOfClasses = len(trainingData['attributes'][-1][1])
    for attribute in trainingData['attributes']:
        attributeIndex = trainingData['attributes'].index(attribute)
        attributeObj = Attribute(attribute,attributeIndex,numberOfClasses)
        attributes.append(attributeObj)
    
    trainingInstances=[]    #list of training instance objects
    
    for instance in trainingData['data']:
        objInstance=trainInst(instance)
        for i in range(len(instance)):  #precomputing number of instances for every attribute
            attributes[i].numberOfInstancesWithValue[attributes[i].values.index(instance[i])]+=1
            attributes[i].numberOfEachClassInstancesWithValue[attributes[-1].values.index(instance[-1])][attributes[i].values.index(instance[i])]+=1 
        trainingInstances.append(objInstance)
    
    for attribute in attributes:
        if attribute == attributes[-1]:
            continue
        print 'Attribute Name:',attribute.name
        print 'Parents:',attributes[-1].name,'\n'

    correctCount = 0
    i = 1
#     print 'Sr.\t Actual Class\t Predicted Class'
    for instance in testData['data']:
        predicted = predictClass(instance, attributes, len(trainingInstances))
        if instance[-1] == predicted[0]:
            correctCount +=1
        print 'Actual Class:\t',instance[-1],'\tPredictedClass:',predicted[0],'\tPosterior Probability:',predicted[1]
        i+=1
    
    print 'Total predictions correct =',correctCount,'/',i-1,'Accuracy =',(correctCount/float(i))*100,'%'
main()