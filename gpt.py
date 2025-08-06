from PIL import Image
import pytesseract
import pandas as pd
import re

def processar_imagem():
    image_path = '/home/jardel/PycharmProjects/MenuScan/image/image1.png'
    img = Image.open(image_path)

    # Use OCR to extract text
    text = pytesseract.image_to_string(img, lang='por')

    # Split text into lines
    lines = text.split('\n')

    lines = [line.strip() for line in text.split('\n') if line.strip()]

    lines[:50]

    raw_text = " ".join(lines)


if __name__ == '__main__':
    processar_imagem()
