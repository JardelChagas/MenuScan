from PIL import Image
import pytesseract
from tkinter import filedialog, messagebox

def processar_imagem():
    file_path = '/home/jardel/PycharmProjects/MenuScan/image/image1.png'

    try:

        imagem = Image.open(file_path)
        texto_extraido = pytesseract.image_to_string(imagem, lang='por')  # Usa OCR em português

        if not texto_extraido.strip():
            messagebox.showwarning("Aviso", "Nenhum texto encontrado na imagem.")
            return

        # Salvar no banco
        # conn = sqlite3.connect('cardapio.db')
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO cardapio (texto) VALUES (?)", (texto_extraido,))
        # conn.commit()
        # conn.close()
        print(texto_extraido)
        #messagebox.showinfo("Sucesso", "Texto extraído e salvo com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar a imagem: {e}")
        print(e)

if __name__ == '__main__':
    processar_imagem()
