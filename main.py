import PySimpleGUI as sg
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

# Converter imagem para formato de exibição no PySimpleGUI
def imagem_para_bytes(imagem):
    if len(imagem.shape) == 2:
        imagem = cv2.cvtColor(imagem, cv2.COLOR_GRAY2RGB)
    else:
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(imagem)
    with BytesIO() as output:
        im.save(output, format="PNG")
        return output.getvalue()

# Filtros
def filtro_cinza(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

def filtro_inverter(imagem):
    return cv2.bitwise_not(imagem)

def filtro_contraste(imagem):
    lab = cv2.cvtColor(imagem, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0)
    cl = clahe.apply(l)
    final = cv2.merge((cl, a, b))
    return cv2.cvtColor(final, cv2.COLOR_LAB2BGR)

def filtro_desfoque(imagem):
    return cv2.GaussianBlur(imagem, (7, 7), 0)

def filtro_nitidez(imagem):
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    return cv2.filter2D(imagem, -1, kernel)

def filtro_bordas(imagem):
    return cv2.Canny(imagem, 100, 200)

# Transformações
def rotacionar(imagem, angulo):
    (h, w) = imagem.shape[:2]
    centro = (w // 2, h // 2)
    matriz = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    return cv2.warpAffine(imagem, matriz, (w, h))

def redimensionar(imagem, largura, altura):
    return cv2.resize(imagem, (largura, altura))

# Interface
layout = [
    [sg.Text("Visualizador de Imagens", font=("Helvetica", 16))],
    [sg.Button("Carregar Imagem"), sg.Button("Salvar Imagem")],
    [sg.Button("Escala de Cinza"), sg.Button("Inverter Cores"),
     sg.Button("Contraste"), sg.Button("Desfoque"),
     sg.Button("Nitidez"), sg.Button("Detecção de Bordas")],
    [sg.Text("Rotação (graus):"), sg.Input("0", size=(5,1), key="-ANGULO-"), sg.Button("Aplicar Rotação")],
    [sg.Text("Redimensionar - Largura:"), sg.Input("300", size=(5,1), key="-LARG-"),
     sg.Text("Altura:"), sg.Input("300", size=(5,1), key="-ALT-"), sg.Button("Aplicar Redimensionamento")],
    [sg.Image(key="-ORIGINAL-"), sg.Image(key="-EDITADA-")]
]

janela = sg.Window("Visualizador de Imagens", layout, resizable=True)

imagem_original = None
imagem_editada = None

while True:
    evento, valores = janela.read()
    if evento == sg.WIN_CLOSED:
        break

    if evento == "Carregar Imagem":
        caminho = sg.popup_get_file("Escolha a imagem", file_types=(("Imagens", "*.png;*.jpg;*.jpeg"),))
        if caminho:
            imagem_original = cv2.imread(caminho)
            imagem_editada = imagem_original.copy()
            janela["-ORIGINAL-"].update(data=imagem_para_bytes(imagem_original))
            janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Salvar Imagem" and imagem_editada is not None:
        salvar = sg.popup_get_file("Salvar como", save_as=True, file_types=(("PNG", "*.png"),))
        if salvar:
            if len(imagem_editada.shape) == 2:
                imagem_editada = cv2.cvtColor(imagem_editada, cv2.COLOR_GRAY2BGR)
            cv2.imwrite(salvar, imagem_editada)
            sg.popup("Imagem salva com sucesso!")

    elif evento == "Escala de Cinza" and imagem_editada is not None:
        imagem_editada = filtro_cinza(imagem_editada)
        janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Inverter Cores" and imagem_editada is not None:
        imagem_editada = filtro_inverter(imagem_editada)
        janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Contraste" and imagem_editada is not None:
        imagem_editada = filtro_contraste(imagem_editada)
        janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Desfoque" and imagem_editada is not None:
        imagem_editada = filtro_desfoque(imagem_editada)
        janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Nitidez" and imagem_editada is not None:
        imagem_editada = filtro_nitidez(imagem_editada)
        janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Detecção de Bordas" and imagem_editada is not None:
        imagem_editada = filtro_bordas(imagem_editada)
        janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Aplicar Rotação" and imagem_editada is not None:
        try:
            angulo = float(valores["-ANGULO-"])
            imagem_editada = rotacionar(imagem_editada, angulo)
            janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))
        except:
            sg.popup_error("Erro ao aplicar rotação. Verifique o valor do ângulo.")

    elif evento == "Aplicar Redimensionamento" and imagem_editada is not None:
        try:
            largura = int(valores["-LARG-"])
            altura = int(valores["-ALT-"])
            imagem_editada = redimensionar(imagem_editada, largura, altura)
            janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))
        except:
            sg.popup_error("Erro ao redimensionar. Verifique os valores.")

janela.close()
z