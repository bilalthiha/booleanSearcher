# booleanSearcher
This program performs Boolean Search on an inverted index
AUTHOR: Bilal Ansari @ Ye Thi Ha

==========DESCRIPTION=============

This python program (booleanSearcher) implements the search component of an information retrieval system.

Input to the program:
1. Search query 
2. File path of the inverted index file
3. Boolean operation type (1 for AND, 2 for OR, 3 for AND)
4. Compression type (0 for No Compression, 1 for Dictionary-As-String)

Output of the program: A text file containing search query results, out_queryResult.txt.

==========ENVIRONMENT SET-UP=============

1. Download this package (booleanSearcher) from GitHub (easy as a zip file). Save and unzip it in a preferred directory in your machine (e.g "C:\Test\booleanSearch") 
2. Note: An example input inverted index is available in the package as "out_invertedIndex.zip" for use.
3. Install Python 3.8.0 or above from https://www.python.org/downloads/.
4. Install Natural Language Toolkit from https://www.nltk.org/ Note: A reference tutorial of NLTK can be found in this YouTube video. https://www.youtube.com/watch?v=FLZvOKSCkxY

==========HOW TO RUN THE PROGRAM=============

1. Launch the command line. E.g For Windows, press Window Key + R on keyboard and then type 'cmd'
2. Change current directory in the command line to the python path of this package. E.g for Windows "cd C:\Test\booleanSearcher"
3. Get the path of python installation on your machine. E.g For Windows, "C:\Users\YourUserId\AppData\Local\Programs\Python\Python38-32"
4. Run this python program. E.g For Windows, "C:\Users\YourUserId\AppData\Local\Programs\Python\Python38-32\python searcherMain.py"
5. Find the program output file which contains the query results and statistics under the same path as the program. E.g "C:\Test\booleanSearcher\out_queryResult.txt"
