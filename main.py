import ntplib
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from openai import OpenAI
import os
import  base64
import re
import uuid


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
                itens_raw = partesRefeicao[2].strip()

                itens = []
                for item in itens_raw.split(";"):
                    if ":" in item:
                        categoria, valor = item.split(":", 1)
                        itens.append((categoria.strip(), valor.strip()))

                refeicoes.append([data, periodo, itens])

    return refeicoes

def verificarRefeicoes(calendario, refeicoes):
    periodos = ["Café da Manhã", "Almoço", "Jantar"]
    larguraColuna = 34

    def imprimir_categoria_multilinha(categoria, periodo_refeicoes, max_por_linha=2):
        linhas_por_data = []
        for _, itens in periodo_refeicoes:
            valor = next((v for c, v in itens if c == categoria), "")
            itens_split = [x.strip() for x in valor.split(",")]

            # Quebra em pedaços de max_por_linha itens
            linhas = [", ".join(itens_split[i:i+max_por_linha]) for i in range(0, len(itens_split), max_por_linha)]
            linhas_por_data.append(linhas)

        max_linhas = max(len(linhas) for linhas in linhas_por_data)

        for i in range(max_linhas):
            if i == 0:
                print(categoria.ljust(larguraColuna), end="")
            else:
                print("".ljust(larguraColuna), end="")
            for linhas in linhas_por_data:
                if i < len(linhas):
                    print(linhas[i].ljust(larguraColuna), end="")
                else:
                    print("".ljust(larguraColuna), end="")
            print()

    for periodo in periodos:
        periodo_refeicoes = [(dataCardapio, itens) for dataCardapio, p, itens in refeicoes if p.lower() == periodo.lower()]
        if not periodo_refeicoes:
            continue

        print(f"\n{periodo}")

        # Cabeçalho: Categoria + datas

        datas = [data for data, _ in periodo_refeicoes]
        print("Categoria".ljust(larguraColuna), end="")
        for data in datas:
            print(data.ljust(larguraColuna), end="")
        print()

        # Descobre todas as categorias únicas
        categorias = set()
        for _, itens in periodo_refeicoes:
            for categoria, _ in itens:
                categorias.add(categoria)
        categorias = list(categorias)

        # Imprime valores
        for categoria in categorias:
            if categoria.lower() == "acompanhamentos":
                imprimir_categoria_multilinha(categoria, periodo_refeicoes)
            else:
                print(f"{categoria}".ljust(larguraColuna), end="")
                for _, itens in periodo_refeicoes:
                    valor = next((v for c, v in itens if c == categoria), "")
                    print(valor.ljust(larguraColuna), end="")
                print()



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
    return os.getenv('API_KEY_GPT')

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

def gerarTextoCardapio():
    return """
        Quero que você converta tabelas de cardápio em um arquivo CSV exatamente nesse formato:

        O arquivo deve ter três colunas: Dia, Horário, Itens.

        Cada linha representa um período do dia (Café da Manhã, Almoço ou Jantar).

        O campo Dia deve estar no formato AAAA-MM-DD.
        
        O campo Horário deve ter apenas um destes três valores: Café da Manhã, Almoço, Jantar.
        
        O campo Itens deve conter todos os alimentos daquela refeição, no formato: Categoria: valor; Categoria: valor; Categoria: valor.
        """

if __name__ == '__main__':

    texto_cardapio = gerarTextoCardapio()
    cardapio = chamarAPIChatGPT(texto_cardapio)        #DESCOMENTAR QUANDO FOR FAZER UMA CHAMDA REAL A API DO CHAT GPT
    #cardapio= "3d41b058-164e-493b-9237-945aae068898.csv" #COMENTAR QUANDO FOR FAZER UMA CHAMDA REAL A API DO CHAT GPT

    dados = carregarCardapio(cardapio)
    agora = pegar_data_hora_ntp()
    brasil = agora - timedelta(hours=3)
    verificarRefeicoes(brasil, dados)
