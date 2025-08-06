import cv2
import pytesseract
from pytesseract import Output
import pandas as pd

def processar_imagem():

    image = cv2.imread('/home/jardel/PycharmProjects/MenuScan/image/image1.png')

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    data = pytesseract.image_to_data(thresh, output_type=Output.DICT)

    text = ""
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 80:
            text += data['text'][i] + " "
        if i > 0 and data['block_num'][i] != data['block_num'][i - 1]:
            text += "\n"

    print(text)
    rows = []
    current_row = []
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:
            current_row.append(data['text'][i])
        if i > 0 and data['line_num'][i] != data['line_num'][i - 1]:
            rows.append(current_row)
            current_row = []

    df = pd.DataFrame(rows)
    print(df)


if __name__ == '__main__':
    processar_imagem()
