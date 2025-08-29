import os
import subprocess
import telebot
import glob
from dotenv import load_dotenv


def Key_botTelegram():
    load_dotenv()
    return os.getenv("API_KEY_BOTTELEGRAM")

Key_botTelegram = Key_botTelegram()

bot=telebot.TeleBot(Key_botTelegram)

@bot.message_handler(['start'])
def start(message:telebot.types.Message):
    bot.reply_to(message, 'olá')
    bot.reply_to(message, 'envie a imagem que sera utilizada')

@bot.message_handler(content_types=['photo'])
def handle_image(message: telebot.types.Message):
    # pega o arquivo da foto
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # salva no PC
    with open("./image/image1.png", "wb") as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Imagem recebida e salva ✅")

    result = subprocess.run(
        ["python3", "main.py"],  # pode passar o caminho da imagem como argumento
        capture_output=True, text=True
    )
    arquivos = glob.glob("./sheets/*.csv")
    if arquivos:
        arquivo_recente = max(arquivos, key=os.path.getmtime)

        with open(arquivo_recente, "rb") as f:
            bot.send_document(message.chat.id, f, caption="📊 Aqui está o CSV gerado ✅")

bot.infinity_polling()