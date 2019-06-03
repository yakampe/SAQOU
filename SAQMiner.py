#pdfTextMiner.py
# Python 2.7.6
# For Python 3.x use pdfminer3k module
# This link has useful information on components of the program
# https://euske.github.io/pdfminer/programming.html
# http://denis.papathanasiou.org/posts/2010.08.04.post.html


''' Important classes to remember
PDFParser - fetches data from pdf file
PDFDocument - stores data parsed by PDFParser
PDFPageInterpreter - processes page contents from PDFDocument
PDFDevice - translates processed information from PDFPageInterpreter to whatever you need
PDFResourceManager - Stores shared resources such as fonts or images used by both PDFPageInterpreter and PDFDevice
LAParams - A layout analyzer returns a LTPage object for each page in the PDF document
PDFPageAggregator - Extract the decive to page aggregator to get LT object elements
'''
import sys
import easygui
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator

from tkinter import Tk
from tkinter.filedialog import askopenfilename

''' This is what we are trying to do:
1) Transfer information from PDF file to PDF document object. This is done using parser
2) Open the PDF file
3) Parse the file using PDFParser object
4) Assign the parsed content to PDFDocument object
5) Now the information in this PDFDocumet object has to be processed. For this we need
   PDFPageInterpreter, PDFDevice and PDFResourceManager
 6) Finally process the file page by page
'''

printQuestion = False
printAnswer = False
stillPrinting = False
questionNumber = 0
questionNumberEntry = 0
question = ""
answer = ""
options = []
pageNumber = -4

def showMessage(message, boxtitle, buttons):
    if typeOfFunction != "Text":
        pressed = easygui.buttonbox(msg=message, title=boxtitle, choices=buttons)
        if pressed == "Quit":
            os._exit(0)
        if pressed == "See Question":
            options = ["See Answer", "Continue", "Quit"]
            showMessage(question, questionNumber, options)
        if pressed == "See Answer":
            options = ["See Question", "Continue", "Quit"]
            showMessage(answer, questionNumber, options)

        
        

Tk().withdraw()
my_file = askopenfilename()
password = ""
extracted_text = ""

# Open and read the pdf file in binary mode
fp = open(my_file, "rb")

# Create parser object to parse the pdf content
parser = PDFParser(fp)

# Store the parsed content in PDFDocument object
document = PDFDocument(parser, password)

# Check if document is extractable, if not abort
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed

# Create PDFResourceManager object that stores shared resources such as fonts or images
rsrcmgr = PDFResourceManager()

# set parameters for analysis
laparams = LAParams()

# Create a PDFDevice object which translates interpreted information into desired format
# Device needs to be connected to resource manager to store shared resources
# device = PDFDevice(rsrcmgr)
# Extract the decive to page aggregator to get LT object elements
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

# Create interpreter object to process page content from PDFDocument
# Interpreter needs to be connected to resource manager for shared resources and device
interpreter = PDFPageInterpreter(rsrcmgr, device)

typeOfFunction = easygui.buttonbox(msg="How do you want to process this PDF?", choices=["Text","GUI"])
if typeOfFunction == "Text":
    textFile = open("SAQs.txt", "w+")

else:
    questionNumberEntry = int(easygui.enterbox("Where did you get to", 0))

PDFPages = PDFPage.create_pages(document)
for page in PDFPages:
    pageNumber += 1

    interpreter.process_page(page)

    layout = device.get_result()

    for (objNo, lt_obj) in enumerate(layout):

        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine) or printQuestion or printAnswer:
                        try:
                            if lt_obj.get_text()[0].isdigit():
                                    printAnswer = False
                                    if len(answer) > 0 and questionNumber >= questionNumberEntry:
                                        options = ["See Question","Next","Quit"]
                                        showMessage(answer, questionNumber, options)
                                        answer = ""
                                        question = ""


                            if printAnswer:
                                if lt_obj.get_text()[0].isalpha() or lt_obj.get_text().startswith("("):
                                   answer += lt_obj.get_text()

                        except:
                            continue

                        try:
                            if printQuestion:

                                if "Answer" in lt_obj.get_text():
                                    printQuestion = False
                                    printAnswer = True
                                    if questionNumber >= questionNumberEntry:
                                        options = ["Get Answer","Quit"]
                                        showMessage(question, questionNumber, options)
                                    answer = ""
                                    textFile.write(question)
                                    textFile.write("\r\n\r\n answer on page " + str(pageNumber)
                                                   + "\r\n-----------------------------------"
                                                   + "\r\n\r\n ")
                                    
                                   
                                else:
                                    question += lt_obj.get_text()

                        except:
                            continue

                        try:
                            if "SAQ " in lt_obj.get_text():
                                question = ""
                                questionNumber += 1
                                printQuestion = True
                                textFile.write("SAQ on page " + str(pageNumber) + "\r\n\r\n ")
                                
                        except:
                            continue
    print("Processed page " + str(pageNumber))
          
textFile.close()
fp.close()
print("Completed")
