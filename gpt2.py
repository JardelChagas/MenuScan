import cv2
import pytesseract
import pandas as pd
import re
from PIL import Image

if __name__ == '__main__':
    # Caminho da imagem
    image_path = '/home/jardel/PycharmProjects/MenuScan/image/image1.png'

    # Pré-processamento da imagem para melhorar OCR
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cv2.imwrite("processed_cardapio.jpg", gray)

    # OCR para extrair texto
    text = pytesseract.image_to_string(Image.open("processed_cardapio.jpg"), lang="por")

    # Divide em linhas
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Tenta identificar colunas com base em padrões (datas)
    columns = []
    rows = []

    # Identifica cabeçalhos com datas (ex: 4-ago, 5-ago...)
    header_line = [line for line in lines if re.search(r"\d{1,2}-\w+", line.lower())]
    if header_line:
        header_parts = re.findall(r"\d{1,2}-\w+", header_line[0])
        columns = ["Item"] + header_parts

    # Monta estrutura básica
    current_section = None
    for line in lines:
        # Detecta se é seção (ex: "CAFÉ DA MANHÃ", "ALMOÇO", "JANTAR")
        if re.search(r"CAFÉ|ALMOÇO|JANTAR", line.upper()):
            current_section = line
        elif ":" not in line and current_section:
            # Pode ser um item
            rows.append([current_section, line])

    # Cria DataFrame simples com os dados brutos
    df = pd.DataFrame(rows, columns=["Seção", "Conteúdo"])

    # Salva CSV
    df.to_csv("cardapio_extraido.csv", index=False)
    print("Arquivo salvo como cardapio_extraido.csv")
