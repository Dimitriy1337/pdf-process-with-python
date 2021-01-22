import os

from PyPDFForm import PyPDFForm

PATH_TO_DOWNLOADED_SAMPLE_PDF_FORM = os.path.join(
    os.path.expanduser("~/Downloads"), "sample_template.pdf"
)  # Change this to where you downloaded the sample PDF form

PATH_TO_SAMPLE_TTF_FONT_FILE = os.path.join(
    os.path.expanduser("~/Downloads"), "LiberationSerif-Regular.ttf"
)  # Change this to where you downloaded the sample font file

PATH_TO_FILLED_PDF_FORM = os.path.join(
    os.path.expanduser("~"), "output.pdf"
)  # Change this to where you wish to put your filled PDF form

with open(PATH_TO_SAMPLE_TTF_FONT_FILE, "rb+") as font:
    PyPDFForm.register_font("LiberationSerif-Regular", font.read())

with open(PATH_TO_DOWNLOADED_SAMPLE_PDF_FORM, "rb+") as template:
    filled_pdf = PyPDFForm(
        template.read(), simple_mode=False, global_font="LiberationSerif-Regular",
    ).fill(
        {
            "test": "test_1",
            "check": True,
            "test_2": "test_2",
            "check_2": False,
            "test_3": "test_3",
            "check_3": True,
        },
    )

    with open(PATH_TO_FILLED_PDF_FORM, "wb+") as output:
        output.write(filled_pdf.stream)
