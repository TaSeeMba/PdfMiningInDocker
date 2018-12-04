# Dependencies and running program

## Procedure to install dependent libraries:
1. Install Cmake <br/>
2. Install Visual studio 15 or 17 with C++ compiler <br/>
3. Install ImageMagick 6.9.x.x (Don't install version 7.x.x as it is not compatible with wand) ImageMagic 7.xxx will not work for wand. <br/>
4. Open terminal or cmd and run ```pip install requirements.txt``` to install the dependencies of the application.<br/>

## To Test the Pdf Mining Module, USE: 
i. Put invoice pdf with name "invoice" in same folder. <br/>
ii. run ```python test-minedPdf.py``` in your terminal<br/>
iii. collect JSON script fron same folder or check the output printed in the console. <br/>

In future work, a program will be written to convert multi page PDF to single page many PDFs for text extraction. The current source code only handles single page pdfs

### Output of current program returns a JSON in the following format:
```
{
    "Seller Email": "sales@insightcom",
    "Vat-No": "0158653",
    "Seller address": "Test Town, Test City",
    "Tel#": "010-012-6359",
    "Buyer's Address": "9 2\u2122 Drive, Dave County",
    "Buyer's Name": "Titan Core",
    "Buyer's Account": "TC-07546",
    "Date of purchase": "21/08/2018",
    "Total Price": "2433.40",
    "Item's Billed": [
        {
            "Item":"NLP Platform Credits",
            "UnitCost":"R10",
            "Rate":10,
            "Amount":"R1000"
        }, 
                {
            "Item":"Basic service fee",
            "UnitCost":"R1000",
            "Rate":1,
            "Amount":"R1000"
        },
                        {
            "Item":"Invoice Processing"",
            "UnitCost":"R0.01",
            "Rate":10000,
            "Amount":"R100"
        },                {
            "Item":"Policy Documents Processing",
            "UnitCost":"R0.02",
            "Rate":800,
            "Amount":"R16"
        }
    ]
}
```
