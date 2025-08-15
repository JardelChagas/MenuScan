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
        for linha in arquivoCardapio:
            linha = linha.strip()

            if not linha:  # pula linhas vazias
                continue

            partesRefeicao = linha.split(",", 2)

            if len(partesRefeicao) == 3:
                data = partesRefeicao[0].strip()
                periodo = partesRefeicao[1].strip()
                itens = partesRefeicao[2].strip().replace(";", "\n")
                refeicoes.append([data, periodo, itens])

    return refeicoes


if __name__ == '__main__':
    dados = carregarCardapio()
    agora = pegar_data_hora_ntp()
    brasil = agora - timedelta(hours=3)

    data = brasil.date()
    hora = brasil.time()

    for data, periodo, itens in dados:
        print(f"{periodo}")
        print(f"{itens}")
        print("-" * 40)
