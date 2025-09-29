from datetime import datetime

def data_br(data_input):
    '''funcção que converte datetime padrão no padrão BR'''
    data_br = datetime.strptime(data_input, "%Y-%m-%dT%H:%M").strftime("%d/%m/%Y %H:%M")
    return data_br
