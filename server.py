from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
from main import chamarAPIChatGPT, gerarTextoCardapio, carregarImagem  # importa suas funções existentes

app = FastAPI()

# 🔓 Permitir requisições do front-end (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    text: str | None = None
    image: str | None = None  # base64 opcional

@app.post("/chat")
async def chat(request: MessageRequest):
    if request.image:
        # Salva imagem recebida
        image_data = base64.b64decode(request.image.split(",")[1])
        with open("./image/temp.png", "wb") as f:
            f.write(image_data)

        # Processa imagem com GPT
        texto_cardapio = gerarTextoCardapio()
        cardapio = chamarAPIChatGPT(texto_cardapio)
        return {"reply": f"Imagem processada com sucesso! Arquivo gerado: {cardapio}"}

    elif request.text:
        # Aqui você pode colocar lógica para texto (ou chamar outro modelo GPT)
        return {"reply": f"Você disse: {request.text}"}

    else:
        return {"reply": "Nenhuma mensagem recebida."}
