import PySimpleGUI as sg

MAX_DISPLAY_SIZE = (800, 600)

def get_layout():
    left_col = [
        [sg.Text('Imagem Original')],
        [sg.Image(key='-ORIGINAL-', size=MAX_DISPLAY_SIZE)],
    ]

    right_col = [
        [sg.Text('Imagem Processada')],
        [sg.Image(key='-EDITADA-', size=MAX_DISPLAY_SIZE)],
    ]

    layout = [
        [sg.Column(left_col), sg.Column(right_col)],
        [sg.Button('Carregar Imagem'), sg.Button('Salvar Imagem'), sg.Button('Limpar Filtros')],
        [sg.Button('Escala de Cinza'), sg.Button('Inversão de Cores'),
         sg.Button('Aumento de Contraste'), sg.Button('Desfoque'),
         sg.Button('Nitidez'), sg.Button('Detecção de Bordas')],
        [sg.Text('Rotação (graus):'), sg.Input('0', size=(5,1), key='-ANGULO-'), sg.Button('Rotacionar')],
        [sg.Text('Redimensionar - Largura:'), sg.Input('300', size=(5,1), key='-LARG-'),
         sg.Text('Altura:'), sg.Input('300', size=(5,1), key='-ALT-'), sg.Button('Redimensionar')],
    ]

    return layout
