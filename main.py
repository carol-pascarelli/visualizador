import PySimpleGUI as sg
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

# Importar filtros modularizados
from alteracoes.cinza import apply_cinza
from alteracoes.inversao import apply_inversao
from alteracoes.contraste import apply_contraste
from alteracoes.blur import apply_blur
from alteracoes.sharpen import apply_sharpen
from alteracoes.bordas import apply_bordas
from alteracoes.rotacionar import apply_rotacionar
from alteracoes.redimensionar import apply_redimensionar

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

# Interface gráfica
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
        imagem_editada = apply_cinza(imagem_editada, "")
        janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Inverter Cores" and imagem_editada is not None:
        imagem_editada = apply_inversao(imagem_editada, "")
        janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Contraste" and imagem_editada is not None:
        imagem_editada = apply_contraste(imagem_editada, "")
        janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Desfoque" and imagem_editada is not None:
        imagem_editada = apply_blur(imagem_editada, "")
        janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Nitidez" and imagem_editada is not None:
        imagem_editada = apply_sharpen(imagem_editada, "")
        janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Detecção de Bordas" and imagem_editada is not None:
        imagem_editada = apply_bordas(imagem_editada, "")
        janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))

    elif evento == "Aplicar Rotação" and imagem_editada is not None:
        try:
            angulo = valores["-ANGULO-"]
            imagem_editada = apply_rotacionar(imagem_editada, angulo)
            janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))
        except:
            sg.popup_error("Erro ao aplicar rotação. Verifique o valor do ângulo.")

    elif evento == "Aplicar Redimensionamento" and imagem_editada is not None:
        try:
            largura = valores["-LARG-"]
            altura = valores["-ALT-"]
            imagem_editada = apply_redimensionar(imagem_editada, f"{largura},{altura}")
            janela["-EDITADA-"].update(data=imagem_para_bytes(imagem_editada))
        except:
            sg.popup_error("Erro ao redimensionar. Verifique os valores.")

janela.close()
