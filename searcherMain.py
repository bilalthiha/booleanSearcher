import os
import sys
import queryProcessor
import compressor
from pathlib import Path
import time

#module global
queryText = ''
invIdxFile = ''
procQueryText = [] #list of query terms
docList = [] #program output
outFileName = 'out_queryResult.txt'
compressionMode = '0'
procQueryTextList = ''
startSearchTime = 0
endSearchTime=0
totalSearchTime=0

#=================== Functions =======================
def cleanGlobalData():
    global queryText, invIdxFile, procQueryText, docList, outFileName, compressionMode, procQueryTextList, startSearchTime, endSearchTime, totalSearchTime
    del queryText, invIdxFile, procQueryText, docList, outFileName, compressionMode, procQueryTextList, startSearchTime, endSearchTime, totalSearchTime
#=================== End of Functions =======================

print('\nPlease key in your query:')
queryText = input()

print('\nPlease key in the path to the inverted index file: (e.g C:\Test\index.txt)')
invIdxFile = input()

print('\nPlease key in the Operation Type:\nType 1 for AND\nType 2 for OR\nType 3 for NOT')
operationType = input()

print('\nPlease key in the Compression Mode:\nType 0 for No Compression\nType 1 for Compression (Dictionary-as-a-string)')
compressionMode = input()

#0. Initialization
queryProcessor.cleanPrevOutputFiles()
compressor.setComprMode(int(compressionMode))

#1. Get processed query text
procQueryTextList = queryProcessor.processQueryText(queryText)

#2. Read inverted index file (into local dictionary)
#Get start time for search
startSearchTime = time.time()
compressor.readInvIdxFile(invIdxFile)

#3. Perform Boolean search based on the operation type
docList = queryProcessor.operateBoolean(procQueryTextList, int(operationType))
#Get end time for search
endSearchTime = time.time()
totalSearchTime = endSearchTime-startSearchTime

#4. Store doc list in output query result file
queryProcessor.outputQueryResult(queryText, compressionMode, operationType, docList, outFileName, str(totalSearchTime))
print('\nPlease find the query results in\n' + outFileName + ' under the directory\n' + str(Path.cwd()))

#5. Store Misc Info and DeInit Program
compressor.saveMiscInfo() #save dictionary as string for human reference
compressor.cleanGlobalData()
queryProcessor.cleanGlobalData()
cleanGlobalData()

