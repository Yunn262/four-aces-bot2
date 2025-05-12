import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
import tempfile

st.set_page_config(page_title="Bot Four Aces", layout="centered")

st.title("🤖 Bot Previsor - Four Aces (Bantubet)")
st.write("Carregue um print do jogo com o histórico visível. O bot analisará e recomendará onde clicar.")

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Altere se necessário

uploaded_file = st.file_uploader("📷 Envie o print do jogo", type=["jpg", "png"])

def extrair_cartas_da_imagem(img):
    # Recorte do histórico no lado direito (ajuste conforme necessário)
    largura, altura = img.size
    crop = img.crop((largura - 250, 100, largura, 650))  # ajustar se necessário

    # OCR
    texto = pytesseract.image_to_string(crop, config='--psm 6')
    linhas = texto.split('\n')
    cartas = []
    for linha in linhas:
        partes = linha.strip().split()
        if len(partes) >= 4:
            cartas.append(partes[:4])
    return cartas

def calcular_frequencia(cartas):
    colunas = list(zip(*cartas))
    frequencia = []
    for coluna in colunas:
        contagem = {}
        for simbolo in coluna:
            contagem[simbolo] = contagem.get(simbolo, 0) + 1
        frequencia.append(contagem)
    return frequencia

def recomendar_posicao(freq):
    melhores = []
    for f in freq:
        if f:
            melhores.append(max(f, key=f.get))
        else:
            melhores.append("?")
    return melhores

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem recebida", use_column_width=True)

    with st.spinner("🔍 Analisando imagem..."):
        cartas = extrair_cartas_da_imagem(image)
        freq = calcular_frequencia(cartas)
        recomendacoes = recomendar_posicao(freq)

    st.subheader("📊 Análise de Frequência")
    for i, f in enumerate(freq):
        st.write(f"**Posição {i+1}**: {f}")

    st.subheader("✅ Recomendação")
    melhor_pos = np.argmax([max(f.values()) if f else 0 for f in freq]) + 1
    st.success(f"Clique na **posição {melhor_pos}** (✔️) — símbolo mais frequente: `{recomendacoes[melhor_pos-1]}`")

    st.caption("Observação: análise baseada no histórico visível.")
