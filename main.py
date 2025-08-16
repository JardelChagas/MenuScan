import ntplib
import os
import base64
import re
import uuid
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from openai import OpenAI

def pegar_data_hora_ntp():
    try:
        cliente = ntplib.NTPClient()
        resposta = cliente.request('pool.ntp.org')
        data_hora = datetime.fromtimestamp(resposta.tx_time, timezone.utc)
        return data_hora
    except Exception as e:
        print("Erro:", e)
        return None

def carregarCardapio(cardapio):
    refeicoes = []
    with open("sheets/"+cardapio, "r", newline="", encoding="utf-8") as arquivoCardapio:
        for i,linha in enumerate(arquivoCardapio):

            if i == 0:
                continue

            linha = linha.strip()

            if not linha:
                continue

            partesRefeicao = linha.split(",", 2)

            if len(partesRefeicao) == 3:
                data = partesRefeicao[0].strip()
                periodo = partesRefeicao[1].strip()
                itens = partesRefeicao[2].strip().replace(";", "\n")
                refeicoes.append([data, periodo, itens])

    return refeicoes

def verificarRefeicoes(calendario, refeicoes):
    data = str(brasil.date())
    hora = brasil.time()

    for dataCardapio, periodo, itens in dados:
        print(f"{periodo, dataCardapio}")
        print(f"{itens}")
        print("-" * 40)

def chamarAPIChatGPT(texto_cardapio):
    api_key_gpt = carregarAPIKeyGPT()
    base64_image = carregarImagem()
    client = OpenAI(api_key=api_key_gpt)

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "system",
                "content": [
                    {"type": "input_text",
                     "text": "Você é um agente capaz de analisar uma imagem e transformar em uma planilha."}
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": texto_cardapio},
                    {"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_image}"},
                ],
            },
        ],
    )

    texto_capturado = limparResultado(response.output_text)
    return criarArquivoCsv(texto_capturado)


def carregarAPIKeyGPT():
    load_dotenv()
    return os.getenv('API_KEY_CHATGPT')

def carregarImagem():
    image_path = "./image/image1.png"
    return encode_image(image_path)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def limparResultado(output_text):
    padrao = r'```(.*?)```'
    resultado = re.search(padrao, output_text, re.DOTALL)
    texto_capturado = ""
    if resultado:
        texto_capturado = resultado.group(1).strip()
        return texto_capturado
    else:
        print("Nenhum texto encontrado entre ```")
        return None

def criarArquivoCsv(texto_capturado):
    nome_arquivo = str(uuid.uuid4()) + ".csv"
    linhas = texto_capturado.split('\n')
    with open("sheets/"+nome_arquivo, 'w', encoding='utf-8') as arquivo:
        for linha in linhas:
            arquivo.write(linha + '\n')

    print(f"Arquivo '{nome_arquivo}' criado com sucesso!")

    arquivo.close()
    return nome_arquivo

def carregarPrompt():
    return """
        Converta a tabela de cardápio que estou enviando para um arquivo CSV no seguinte formato:

        Três colunas: Dia, Horário e Itens.

        A coluna Dia deve estar no formato AAAA-MM-DD.

        A coluna Horário deve ser um dos três valores: Café da Manhã, Almoço ou Jantar.

        A coluna Itens deve conter todos os dados dessa refeição concatenados no formato Categoria: valor; Categoria: valor; ..., mantendo a mesma ordem e nomes de categoria da tabela original.

        Inclua todas as categorias, mesmo que alguma esteja vazia (neste caso, apenas coloque o nome da categoria sem valor).

        Use vírgula como separador de colunas e envolva valores com aspas duplas quando necessário.

        Retorne o CSV começando pelo cabeçalho Dia,Horário,Itens.
        """

if __name__ == '__main__':
    texto_cardapio = carregarPrompt()
    cardapio = chamarAPIChatGPT(texto_cardapio)        #DESCOMENTAR QUANDO FOR FAZER UMA CHAMDA REAL A API DO CHAT GPT
    #cardapio= "bf10a070-9c05-47c9-8c4d-0f9f0588c3fb.csv" #COMENTAR QUANDO FOR FAZER UMA CHAMDA REAL A API DO CHAT GPT

    dados = carregarCardapio(cardapio)
    agora = pegar_data_hora_ntp()
    brasil = agora - timedelta(hours=3)
    verificarRefeicoes(brasil, dados)
