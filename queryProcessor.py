import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import glob
import os
import compressor
import sys

#global for document Ids
minDocId = 1
maxDocId = 7945

#optimization switches
CLEAN_DUPLICATED_INPUT = True
AND_OPERATION_OPTIMIZATION = True


def processQueryText(qryText):
    #1. Tokenize
    tkzr = RegexpTokenizer(r'\w+')
    tokenizedWords = tkzr.tokenize(qryText)
    
    #2. Remove duplicated tokens
    if (CLEAN_DUPLICATED_INPUT):
        uniqueTokens = []
        for j in tokenizedWords:
            if j not in uniqueTokens:
                uniqueTokens.append(j)
    else: #no input cleaning
        uniqueTokens = tokenizedWords
    
    #3. Remove stop words
    stopWords = set(stopwords.words("english"))
    filteredWords=[]
    for w in uniqueTokens:
        if w not in stopWords:
            filteredWords.append(w)
            
    #4. Stem words (create terms)
    ps = PorterStemmer()
    queryTerms = []
    for i in filteredWords:
        queryTerms.append(ps.stem(i))
        
    return queryTerms

    
def operateAND(posting1, posting2):
    p1 = 0
    p2 = 0
    result = []   
    
    while p1 < len(posting1) and p2 < len(posting2):
        if posting1[p1] == posting2[p2]:
            result.append(posting1[p1])
            p1 += 1
            p2 += 1
        elif posting1[p1] > posting2[p2]:
            p2 += 1
        else:
            p1 += 1
    return result
    
def operateOR(posting1, posting2):
    p1 = 0
    p2 = 0
    result = []   
    
    while p1 < len(posting1) and p2 < len(posting2):
        if posting1[p1] == posting2[p2]:
            result.append(posting1[p1])
            p1 += 1
            p2 += 1
        elif posting1[p1] > posting2[p2]:
            result.append(posting2[p2])
            p2 += 1
        else:
            result.append(posting1[p1])
            p1 += 1
    while p1 < len(posting1):
        result.append(posting1[p1])
        p1 += 1
    while p2 < len(posting2):
        result.append(posting2[p2])
        p2 += 1
    return result
    
def operateNOT(posting):    
    global minDocId
    global maxDocId
    i = minDocId
    allDocIds = []
    result = []
    
    #get all doc Ids list
    while (i <= maxDocId):
        allDocIds.append(i)
        i+=1
    
    #result is not docs in posting
    for i in allDocIds:
        if i not in posting:
            result.append(i)  
    return result

def operateBoolean(procQryTxtLst, opType):    
    qryTermFreqDict = {}
    sortedprocQryTxtLst = []    
    posting1 = []
    posting2 = []
    result = []
    
    #input sanity check
    if(opType < 1 or opType > 3):
        print('Provided Boolean operation type ' + str(opType) + ' is unknown. Program ends.')
        sys.exit()
        return result
        
    
    if(AND_OPERATION_OPTIMIZATION):
        #create query term-frequency pairs for processing in ascending order for AND
        for i in procQryTxtLst:
            if i not in qryTermFreqDict.keys():
                qryTermFreqDict[i] = compressor.getDocFreqOfTerm(i) #frequency is first element of docIdList
        
        sortedprocQryTxtLst = sorted(qryTermFreqDict, key=qryTermFreqDict.get)
        #print('Processed and sorted query terms are:')
        #print(sortedprocQryTxtLst)
    else: #no optimization
        sortedprocQryTxtLst = procQryTxtLst
    
    #perform AND, OR, NOT depending on user input
    #handle NOT
    if (opType == 3): #NOT
        if (len(sortedprocQryTxtLst) == 1):
            result = operateNOT(compressor.getDocListOfTerm(sortedprocQryTxtLst[0]))
        else:
            result = []
            print('Invalid number of query words. Please enter only one word for NOT operation. Thank you. Program ends.')
            sys.exit()
        return result
    
    
    #handle AND, OR
    if (len(sortedprocQryTxtLst) < 2):
        result = []
        print('Invalid number of query words. Please enter at least two words for AND/OR operation. Thank you. Program ends.') 
        sys.exit()
        return result
    else:    
        term1 = sortedprocQryTxtLst.pop(0)
        posting1 = compressor.getDocListOfTerm(term1)        
        
        while(sortedprocQryTxtLst != []):        
            term2 = sortedprocQryTxtLst.pop(0)
            posting2 = compressor.getDocListOfTerm(term2)
            
            if (opType == 1): #AND
                posting1 = operateAND(posting1, posting2)
            else: #OR opType == 2
                posting1 = operateOR(posting1, posting2)   
        result = posting1        
    return result
    
def getOpTypeText(opType):
    opTypeText = ''
    if (opType == 1):
        opTypeText = 'AND'
    elif (opType == 2):
        opTypeText = 'OR'
    elif (opType == 3):
        opTypeText = 'NOT'
    else:
        opTypeText = 'Invalid'
    return opTypeText

def outputQueryResult(qryText, comprMode, opType, docLst, descFileName, ttlTime):    
    resultFile = open(descFileName, 'w', encoding ='utf-8')
    #update search time
    resultFile.write('Time taken for search (in seconds): '+ttlTime+ '\n')
    #update compression type used and index size in memory
    resultFile.write('Compression mode used: ' + compressor.getComprModeText(comprMode) + '\n')
    resultFile.write('Index size in memory (in bytes): ' + str(compressor.getIndexSizeInMemory()) + '\n')
    #update query result list (document list)
    resultFile.write('\n\n')
    resultFile.write('For given query operation type: ' + getOpTypeText(int(opType)) + '\n')
    resultFile.write('For given query text: ' + qryText + '\n')
    resultFile.write('Total number of document hits: ' + str(len(docLst)) + '\n')
    resultFile.write('Query Result (document list) is as follows:\n')
    if (docLst == []):
        resultFile.write('Query not found')
    else:
        for i in docLst:
            resultFile.write(str(i) + '.txt' + '\n')
    resultFile.close()

def cleanPrevOutputFiles():
    flName2Del = ''
    #get list of files with 'out_' prefix
    obsFileList = glob.glob("out_*.txt")
    #print(obsFileList)
    while (len(obsFileList) > 0):
        flName2Del = obsFileList.pop(0)
        os.remove(flName2Del)

def cleanGlobalData():
    global minDocId, maxDocId, CLEAN_DUPLICATED_INPUT, AND_OPERATION_OPTIMIZATION
    del minDocId, maxDocId, CLEAN_DUPLICATED_INPUT, AND_OPERATION_OPTIMIZATION
