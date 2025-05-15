import PySimpleGUI as sg

MAX_DISPLAY_SIZE = (800, 600)

def get_layout():
    left_col = [
        [sg.Text('Imagem Original')],
        [sg.Image(key='-ORIGINAL-', size=MAX_DISPLAY_SIZE)],
    ]

    right_col = [
        [sg.Text('Imagem Processada')],
        [sg.Image(key='-PROCESSED-', size=MAX_DISPLAY_SIZE)],
    ]

    controls = [
        sg.Button('Upar Imagem'),
        sg.Combo([
            'Escala de Cinza',
            'Inversão de Cores',
            'Aumento de Contraste',
            'Desfoque',
            'Nitidez',
            'Detecção de Bordas',
            'Rotação',
            'Redimensionamento'], 
            key='-FILTER-', enable_events=True),
        sg.Button('Aplicar Filtro'),
        sg.Button('Salvar Imagem'),
        sg.Text('Parâmetros:'),
        sg.Input(key='-PARAMS-', size=(10,1)),
    ]

    layout = [
        [sg.Column(left_col), sg.Column(right_col)],
        [controls],
    ]

    return layout
