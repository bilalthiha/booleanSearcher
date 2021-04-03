import ast
import sys

#dictionary to store inv index in memory
indexDict = {}

#dictionary as string to store inv index in memory
termString = ''
termPtrList = []
postingPtrList = []
currDocPtr = -1 #default invalid


#compression mode
comprMode = 0 #default no compression/dictionary data structure


def setComprMode(mode):
    global comprMode
    comprMode = mode
    if (mode < 0 or mode > 1):
        print('Provided compression mode ' + str(comprMode) +' is unknown. Program ends. Thank you.') 
        sys.exit()    
    
def getComprMode(mode):
    global comprMode
    return comprMode

def getComprModeText(mode):
    global comprMode
    comprModeText = 'None'
    if (getComprMode(mode) == 0):
        comprModeText = 'None (Inverted Index is stored in memory as dictionary)'
    else:
        comprModeText = 'Dictionary-as-a-string'
    return comprModeText
    
#========================= Dictionary Interfaces ================================
def getDocListOfTermInDict(term):
    global indexDict
    dList = []
    if term in indexDict.keys():
        dList = (indexDict[term])[1:]
    else:
        dList = []
    return dList
    
def getDocFreqOfTermInDict(term):
    global indexDict
    dFreq = 0
    if term in indexDict.keys():
        dFreq = (indexDict[term])[0] #first index of doc lis is doc id
    else:
        dFreq = 0
    return dFreq

def getDictSize():
    global indexDict
    size = sys.getsizeof(indexDict)
    return size

def invIdxFile2Dict(flPath):
    currLine = 'init'
    global indexDict
    try:
        invIdxFile = open(flPath, 'r', encoding ='utf-8')
    except FileNotFoundError:
        print('Provided inverted-index file does not exist. Please check file naming or directory. Program ends.')        
        sys.exit()
            
    while(currLine != ''):
        term = ''
        termComponents = []
        lst = []
        currLine = invIdxFile.readline()
        if(currLine != ''):
            term = currLine[:currLine.index(':')]
            termComponents = term.split('\'')
            term = str(termComponents[1]) # the middle one is term [', term, ']
            lst = ast.literal_eval(currLine[(currLine.index(':')+ 1):])
            indexDict[term] = list(lst)
    #print(indexDict)    
    invIdxFile.close()
#=================================================================================

#========================= Dictionary As String Interfaces ================================
def isTermPresentInDictAsString(term):
    global currDocPtr
    global termString
    global termPtrList
    start = 0
    end = 0
    result = False
    for i in termPtrList:
        end = i
        if (term == termString[start:end]):
            result = True
            currDocPtr = termPtrList.index(i)
            break
        start = end            
    return result
    
def getCurrDocPtr():
    global currDocPtr
    return currDocPtr    

def getDocListOfTermInDictAsString(term):
    global postingPtrList
    dList = []
    docPtr = 0
    if (isTermPresentInDictAsString(term)):
        docPtr= getCurrDocPtr()
        dList = (postingPtrList[docPtr])[1:]
    else:
        dList = []
    return dList
    
def getDocFreqOfTermInDictAsString(term):
    global postingPtrList
    dFreq = 0
    docPtr = 0
    if (isTermPresentInDictAsString(term)):
        docPtr= getCurrDocPtr()
        dFreq = (postingPtrList[docPtr])[0]
    else:
        dFreq = []
    return dFreq

def getDictAsStringSize():
    global termString
    global termPtrList
    global postingPtrList
    size = sys.getsizeof(termString) + sys.getsizeof(termPtrList) + sys.getsizeof(postingPtrList)
    return size

def compressDictAsString(invIdxDictFlPath):
    currLine = 'init'
    global termString
    global termPtrList
    global postingPtrList
    
    try:
        invIdxFile = open(invIdxDictFlPath, 'r', encoding ='utf-8')
    except FileNotFoundError:
        print('Provided inverted-index file does not exist. Please check file naming or directory. Program ends.')
        sys.exit() 
            
    while(currLine != ''):
        term = ''
        termPtr = 0        
        postingPtr = 0        
        docLst = []
        currLine = invIdxFile.readline()        
        if(currLine != ''):
            term = currLine[:currLine.index(':')]
            termComponents = term.split('\'')
            #1. Concatenate each term from the inverted index dictionary into string => string
            termString = termString + str(termComponents[1]) # the middle one is term [', term, ']
            
            #2. For each term, calcuate its index in the string (term ptr) and store it in list => 1d list
            termPtr = len(termString)
            termPtrList.append(termPtr)
            
            #3. For each term, get posting (posting ptr) and store it in list => 2d list (list of postings)            
            docLst = ast.literal_eval(currLine[(currLine.index(':')+ 1):])
            postingPtrList.append(docLst)            
            
    invIdxFile.close()
    
def saveDictAsString(dictAsStringIdxFlName):
    global termString
    global termPtrList
    global postingPtrList
    
    outFile = open(dictAsStringIdxFlName, 'w', encoding ='utf-8')
    outFile.write(termString + '\n')
    outFile.write(str(termPtrList) + '\n')
    outFile.write(str(postingPtrList)+ '\n')
    
    outFile.close()
#=================================================================================
    
def getDocListOfTerm(term):    
    docList = []
    if (comprMode == 0): #no compression/dictionary
        docList = getDocListOfTermInDict(term)
    else: #dictAsStringMethod
        docList = getDocListOfTermInDictAsString(term)
    return docList
    
def getDocFreqOfTerm(term):
    docFreq = []
    if (comprMode == 0): #no compression/dictionary
        docFreq = getDocFreqOfTermInDict(term)
    else: #dictAsStringMethod
        docFreq = getDocFreqOfTermInDictAsString(term)
    return docFreq

    
def getIndexSizeInMemory():
    size = 0
    if (comprMode == 0): #no compression/dictionary
        size = getDictSize()
    else: #dictAsStringMethod
        size = getDictAsStringSize()
    return size
    
def readInvIdxFile(inFile):
    if (comprMode == 0): #no compression/dictionary
        invIdxFile2Dict(inFile)
    else: #dictAsStringMethod
        compressDictAsString(inFile)

def saveMiscInfo():
    if (comprMode != 0): #dictAsStringMethod
        saveDictAsString('out_indexDictAsString.txt')
        
def cleanGlobalData():
    global indexDict, termString, termPtrList, postingPtrList, currDocPtr, comprMode
    del indexDict, termString, termPtrList, postingPtrList, currDocPtr, comprMode
    
