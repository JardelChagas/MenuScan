import cv2
import pytesseract
import pandas as pd

def processar_imagem():
    # Caminho da imagem
    imagem = cv2.imread('/home/jardel/PycharmProjects/MenuScan/image/image1.png')

    # Pré-processamento
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    _, imagem = cv2.threshold(imagem, 150, 255, cv2.THRESH_BINARY)

    # Extrai texto com formatação de tabela
    custom_oem_psm_config = r'--oem 3 --psm 6'
    texto = pytesseract.image_to_string(imagem, config=custom_oem_psm_config, lang='por')

    # Divide linhas e colunas
    linhas = texto.strip().split('\n')
    dados = [linha.split() for linha in linhas]

    # Cria o DataFrame e salva como CSV
    df = pd.DataFrame(dados)
    df.to_csv("planilha_convertida.csv", index=False, header=False)


if __name__ == '__main__':
    processar_imagem()