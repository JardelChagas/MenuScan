import requests

def api_processar_imagem():
    api_url = 'https://api.api-ninjas.com/v1/imagetotext'
    image_file_descriptor = open('/home/jardel/PycharmProjects/MenuScan/image/image1.png', 'rb')
    files = {'image': image_file_descriptor}
    r = requests.post(api_url, files=files, headers={'X-Api-Key': '/iNtdbywh4WWs64vexRvvQ==4w8nq2o1DF8KmXjx'})

    dados_limpos = [{'text': item['text']} for item in r.json()]

    print(dados_limpos)


if __name__ == '__main__':
    api_processar_imagem()