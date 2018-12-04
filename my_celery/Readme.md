Required python libraries are
Wand (for wand installation you need ImageMagic 6.9.x.x) NOTE: ImageMagic 7.xxx will not work for wand.
pytesseract (You will need to install tesseract and add enviroment path for tesseract)
OpenCV for python.
pyPDF2

To Test Pdf Mining USE:
Put invoice pdf with name "invoice" in same folder.
run test=minedPdf.py
collect JSON script fron same folder or check the output printed in the console.

In future work, a program will be written to convert multi page PDF to single page many PDFs for text extraction.