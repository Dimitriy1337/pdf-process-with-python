# PyPDFForm

PyPDFForm is a pure-python library for PDF form processing. 
It allows filling a PDF form by creating a python dictionary that matches its annotation names 
for elements such as text fields and checkboxes. It also supports other drawing image and merging multiple 
PDFs together.

## Installing

Install using  [pip](https://pip.pypa.io/en/stable/quickstart/):

`````commandline
pip install -i https://test.pypi.org/simple/ PyPDFForm
`````

## Quick Example

You can find a sample PDF form from [here](https://github.com/chinapandaman/PyPDFForm/blob/master/pdf_samples/sample_template.pdf). Download it and try:

````python
import os

from PyPDFForm import PyPDFForm

PATH_TO_DOWNLOADED_SAMPLE_PDF_FORM = os.path.join(
    os.path.expanduser("~"), "sample_template.pdf"
)  # Change this to where you downloaded the sample PDF form

PATH_TO_FILLED_PDF_FORM = os.path.join(
    os.path.expanduser("~"), "output.pdf"
)  # Change this to where you wish to put your filled PDF form

with open(PATH_TO_DOWNLOADED_SAMPLE_PDF_FORM, "rb+") as template:
    filled_pdf = PyPDFForm(template.read(), simple_mode=False).fill(
        {
            "test": "test_1",
            "check": True,
            "test_2": "test_2",
            "check_2": False,
            "test_3": "test_3",
            "check_3": True,
        },
        font_size=20,
    )

    with open(PATH_TO_FILLED_PDF_FORM, "wb+") as output:
        output.write(filled_pdf.stream)
````

After running the above code snippet you can find `output.pdf` at the location you specified 
and it should look like [this](https://github.com/chinapandaman/PyPDFForm/blob/master/pdf_samples/sample_filled_font_20.pdf).

## Documentation

(WIP)
