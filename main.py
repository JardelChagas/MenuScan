import ntplib
from datetime import datetime, timezone, timedelta

def pegar_data_hora_ntp():
    try:
        cliente = ntplib.NTPClient()
        resposta = cliente.request('pool.ntp.org')
        data_hora = datetime.fromtimestamp(resposta.tx_time, timezone.utc)
        return data_hora
    except Exception as e:
        print("Erro:", e)
        return None

def carregarCardapio():
    refeicoes = []
    with open("cardapio.csv", "r", newline="", encoding="utf-8") as arquivoCardapio:
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

    if hora.hour == 6 and hora.minute == 00:
        for dataCardapio, periodo, itens in dados:
            if dataCardapio == data and periodo == "Café da Manhã":
                print(f"{periodo}")
                print(f"{itens}")
                print("-" * 40)

    if hora.hour == 11 and hora.minute == 00:
        for dataCardapio, periodo, itens in dados:
            if dataCardapio == data and periodo == "Almoço":
                print(f"{periodo}")
                print(f"{itens}")
                print("-" * 40)

    if hora.hour == 17 and hora.minute == 00:
        for dataCardapio, periodo, itens in dados:
            if dataCardapio == data and periodo == "Jantar":
                print(f"{periodo}")
                print(f"{itens}")
                print("-" * 40)

if __name__ == '__main__':
    dados = carregarCardapio()
    agora = pegar_data_hora_ntp()
    brasil = agora - timedelta(hours=3)

    verificarRefeicoes(brasil, dados)
