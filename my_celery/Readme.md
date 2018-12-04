# Dependencies and running program

## Required python libraries are:
1. Wand (for wand installation you need ImageMagic 6.9.x.x) NOTE: ImageMagic 7.xxx will not work for wand. <br/>
2. pytesseract (You will need to install tesseract and add enviroment path for tesseract) <br/>
3. OpenCV for python. <br/>
4. pyPDF2 <br/>

## To Test Pdf Mining USE: 
i. Put invoice pdf with name "invoice" in same folder. <br/>
ii. run test=minedPdf.py <br/>
iii. collect JSON script fron same folder or check the output printed in the console. <br/>

In future work, a program will be written to convert multi page PDF to single page many PDFs for text extraction. The current source code only handles single page pdfs
