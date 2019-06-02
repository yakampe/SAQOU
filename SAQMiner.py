
import sys
import easygui
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator
from tkinter import Tk
from tkinter.filedialog import askopenfilename

printQuestion = False
printAnswer = False
stillPrinting = False
questionNumber = 0
question = ""
answer = ""
options = []

def showMessage(message, boxtitle, buttons):
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

fp = open(my_file, "rb")
parser = PDFParser(fp)
document = PDFDocument(parser)
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)




questionNumberEntry = int(easygui.enterbox(msg="Where did you get to", default="0"))

for page in PDFPage.create_pages(document):


    interpreter.process_page(page)

    layout = device.get_result()

    for (objNo, lt_obj) in enumerate(layout):

        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine) or printQuestion or printAnswer:

                        #If printing answer - will stop and look for question start if the next layout object starts with a digit.                        
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

                        #If printing question - will stop when layout object has answer in the body.
                        try:
                            if printQuestion:

                                if "Answer" in lt_obj.get_text():
                                    printQuestion = False
                                    printAnswer = True
                                    if questionNumber >= questionNumberEntry:
                                        options = ["Get Answer","Quit"]
                                        showMessage(question, questionNumber, options)
                                    answer = ""
                                   
                                else:
                                    question += lt_obj.get_text()

                        except:
                            continue

                        #Look for start of the question
                        try:
                            if "SAQ " in lt_obj.get_text():
                                question = ""
                                questionNumber += 1
                                printQuestion = True

                        except:
                            continue

fp.close()
