
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

# trainingData = arff.load(open('lymph_train.arff.txt', 'rb'))
# testData = arff.load(open('lymph_test.arff.txt','rb'))

class TrainingInstance:
    def __init__(self, instance):
        self.attrValues = instance

class Attribute:
    def __init__(self,attribute):
        self.name = attribute[0]
        self.values = attribute[1]

class Edge:
    def __init__(self,src,dst,w):
        self.src = src
        self.dst = dst
        self.w = w


def getMST(adjacencyMatrix):
    MST = []
    included = [False for each in adjacencyMatrix[0]]
    Vnew = []
    Vnew.append(0)
    included[0] = True
    while len(Vnew) < len(adjacencyMatrix[0]):
        uEdges = []
        for u in Vnew:
            for v,weight in enumerate(adjacencyMatrix[u]):
                if included[v] == False :
                    uvEdge = Edge(u,v,weight)
                    uEdges.append(uvEdge)
        uEdges.sort(key=lambda x : x.w, reverse=True)
        for edge in uEdges:
            if included[edge.dst] != True:
                MST.append(edge)
                Vnew.append(edge.dst)
                included[edge.dst] = True
                break
    return MST

def makePredictions(MST,testInstances,trainingInstances,attributes):
    parents = [[] for each in attributes]
    for i in range(len(attributes)):
        for edge in MST:
            if edge.dst == i:
                parents[i].append(edge.src)
    for i,atr in enumerate(attributes):
        if atr == attributes[-1]:
            continue
        print 'Attribute Name:',atr.name,'\t'
        for p in parents[i]:
            print 'Parents:',attributes[p].name,
        print attributes[-1].name,'\n'
    predictions = []
#     product = 1
#     for i,attribute in enumerate(attributes):
#         if attribute == attributes[-1]:
#             continue
#         for value in attribute.values:
#             if len(parents[i]) > 0:
#                 for parent in parents[i]:
#                     for x in attributes[parent].values:
#                         for cls in attributes[-1].values:
#                             Nvpx = 0
#                             Npx = 0
#                             for inst in trainingInstances:
#                                 if inst[i] == value and inst[parent] == x and inst[-1] == cls:
#                                     Nvpx += 1
#                                 if inst[parent] == x and inst[-1] == cls:
#                                     Npx += 1
#                             prob = (Nvpx+1)/float(Npx+len(attribute.values))
#                             product *= prob
#             else:
#                     for cls in attributes[-1].values:
#                         Nvpx = 0
#                         Npx = 0
#                         for inst in trainingInstances:
#                             if inst[i] == value and inst[-1] == cls:
#                                 Nvpx += 1
#                             if inst[-1] == cls:
#                                 Npx += 1
#                         prob = (Nvpx+1)/float(Npx+len(attribute.values))
#                         product *= prob
    for testinstance in testInstances:
        PofXiGivenParentsAndY = []
        for yvalue in attributes[-1].values:
            numOfInstancesY = 0
            product = 1.0
            for i in range(len(attributes)-1):     
                instancesCount = 0
                numOfInstancesYandParents = 0
                for traininstance in trainingInstances:
                    if traininstance[i] == testinstance[i]:
                        if len(parents[i]) > 0:
                            for parent in parents[i]:
                                if traininstance[parent] == testinstance[parent] and traininstance[-1] == yvalue:
                                    instancesCount += 1
                        else:
                            if traininstance[-1] == yvalue:
                                instancesCount += 1
                    if len(parents[i]) > 0:
                        for parent in parents[i]:
                            if traininstance[parent] == testinstance[parent] and traininstance[-1] == yvalue:
                                numOfInstancesYandParents += 1
                    else:
                        if traininstance[-1] == yvalue:
                            numOfInstancesYandParents += 1
                    if traininstance[-1] == yvalue:
                        numOfInstancesY += 1
                product *= float(instancesCount+1)/(numOfInstancesYandParents+len(attributes[i].values))
            PofXiGivenParentsAndY.append(product*(float(numOfInstancesY+1)/(len(trainingInstances)+2)))
        PofXiGivenParentsAndY = [each/sum(PofXiGivenParentsAndY) for each in PofXiGivenParentsAndY]
        print 'Actual Class:\t',testinstance[-1],'\t\tPredicted Class:',attributes[-1].values[PofXiGivenParentsAndY.index(max(PofXiGivenParentsAndY))],'\tPosterior Probability:',max(PofXiGivenParentsAndY)
        predictions.append(attributes[-1].values[PofXiGivenParentsAndY.index(max(PofXiGivenParentsAndY))])
    return predictions
    
    
    

def main():
    attributes=[]           #list of training instance objects
    for attribute in trainingData['attributes']:
#         attributeIndex = trainingData['attributes'].index(attribute)
        attributeObj = Attribute(attribute)
        attributes.append(attributeObj)
    
    newTrainingInstances = []
    sumAccuracy=0
    for i in range(4):
        indices = random.sample(range(len(trainingData['data'])),379)
        newTrainingInstances = []
        for i in indices:
            newTrainingInstances.append(trainingData['data'][i])
        
        
        trainingInstances=[]    #list of training instance objects
        
        for instance in newTrainingInstances:
            objInstance=TrainingInstance(instance)
            trainingInstances.append(objInstance)
            
        adjacencyMatrix = [[-1.0 for x in range(len(attributes)-1)] for y in range(len(attributes)-1)]
        visited = [False for x in attributes]
        
        numOfAttributes = len(attributes)-1
        for i in range(numOfAttributes):
            for j in range(i,numOfAttributes):
                if i==j:
                    continue
                mutualInfo = 0.0
                for a in attributes[i].values:
                    for b in attributes[j].values:
                        for c in attributes[-1].values:
                            NoIabc = 0
                            NoIc = 0
                            NoIac = 0
                            NoIbc = 0
                            for instance in trainingInstances:
                                if instance.attrValues[i] == a and instance.attrValues[j] == b and instance.attrValues[-1] == c:
                                    NoIabc +=1
                                if instance.attrValues[-1] == c:
                                    NoIc +=1
                                if instance.attrValues[i] == a and instance.attrValues[-1] == c:
                                    NoIac +=1
                                if instance.attrValues[j] == b and instance.attrValues[-1] == c:
                                    NoIbc +=1
                            numOfAllPossibleValuesOfXi = len(attributes[i].values)
                            numOfAllPossibleValuesOfXj = len(attributes[j].values)
                            numOfAllPossibleValuesOfY = len(attributes[-1].values)
                            numOfAllInstances = len(trainingInstances)
                                
                            PofXiXjGivenY = (NoIabc + 1)/(float(NoIc) + numOfAllPossibleValuesOfXi*numOfAllPossibleValuesOfXj)
                            PofXiXjY = (NoIabc + 1)/(float(numOfAllInstances) + numOfAllPossibleValuesOfXi*numOfAllPossibleValuesOfXj*numOfAllPossibleValuesOfY)
                            PofXiGivenY = (NoIac + 1)/(float(NoIc) + numOfAllPossibleValuesOfXi)
                            PofXjGivenY = (NoIbc + 1)/(float(NoIc) + numOfAllPossibleValuesOfXj)
                            mutualInfo += PofXiXjY*math.log((PofXiXjGivenY/(PofXiGivenY*PofXjGivenY)),2)
                adjacencyMatrix[i][j] = mutualInfo
                adjacencyMatrix[j][i] = mutualInfo
        
        MST = getMST(adjacencyMatrix)
        
    #     for edge in MST:
    #         if edge == MST[0]:
    #             print '{(%d,%d),' %(edge.src,edge.dst),
    #         elif edge != MST[-1]:
    #             print '(%d,%d),' %(edge.src,edge.dst),
    #         else:
    #             print '(%d,%d)}' %(edge.src,edge.dst)
        
        predictions = makePredictions(MST,testData['data'],newTrainingInstances,attributes)
        correctCount = 0 
        for i,instance in enumerate(testData['data']):
            if instance[-1] == predictions[i]:
                correctCount +=1
    #         print i+1,'\t',instance[-1],'\t ',predictions[i]
        
        print 'Total predictions correct =',correctCount,'/',i+1,'Accuracy =',(correctCount/float(i+1))*100,'%'
        sumAccuracy+=(correctCount/float(i+1))*100
        
    avgAccuracy = sumAccuracy/4
    print "average Accuracy =",avgAccuracy
    print len(trainingData['data'])
    print len(newTrainingInstances)

main()