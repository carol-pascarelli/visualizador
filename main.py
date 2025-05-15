import PySimpleGUI as sg
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

from ui import get_layout
from alteracoes.cinza import apply_cinza
from alteracoes.inversao import apply_inversao
from alteracoes.contraste import apply_contraste
from alteracoes.blur import apply_blur
from alteracoes.sharpen import apply_sharpen
from alteracoes.bordas import apply_bordas
from alteracoes.rotacionar import apply_rotacionar
from alteracoes.redimensionar import apply_redimensionar

def imagem_para_bytes(imagem):
    if len(imagem.shape) == 2:
        imagem = cv2.cvtColor(imagem, cv2.COLOR_GRAY2RGB)
    else:
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(imagem)
    with BytesIO() as output:
        im.save(output, format="PNG")
        return output.getvalue()

janela = sg.Window("Visualizador de Imagens", get_layout(), resizable=True)

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
            img_salvar = imagem_processada
            if len(img_salvar.shape) == 2:
                img_salvar = cv2.cvtColor(img_salvar, cv2.COLOR_GRAY2BGR)
            cv2.imwrite(salvar, img_salvar)
            sg.popup("Imagem salva com sucesso!")

    elif evento == "Limpar Filtros" and imagem_original is not None:
        imagem_processada = imagem_original.copy()
        janela["-PROCESSED-"].update(data=imagem_para_bytes(imagem_processada))

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
