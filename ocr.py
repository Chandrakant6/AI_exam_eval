import pymupdf
import os

INPUT_DIR: str = "data/stu_ans_pdf"
OUTPUT_DIR: str = "data/stu_ans_img"

def pdf2img() -> None :
    ''' extract images from student answersheet pdf as page_<numbers>.png '''

    docs = os.listdir(INPUT_DIR)

    for doc in docs:
        doc_obj = pymupdf.open(f"{INPUT_DIR}/{doc}")  # open document

        if not os.path.exists(f"{OUTPUT_DIR}/{doc}"):
            os.makedirs(f"{OUTPUT_DIR}/{doc}")

        for page in doc_obj:  # iterate through the pages
            pix = page.get_pixmap()  # render page to an image
            pix.save(f"{OUTPUT_DIR}/{doc}/page-{page.number:02d}.png")  # store image as a PNG


if __name__ == "__main__":
    pdf2img()
