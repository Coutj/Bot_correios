import os
from pathlib import Path
import telegram
import read_html
from carteiro import Carteiro

def listar_usuarios():
    lista_usuarios = list()
    for usuario in endereco_usuarios.iterdir():
        lista_pacotes = tuple()
        for pacote in usuario.iterdir():
            lista_pacotes += (pacote.name,)
    
        lista_usuarios.append({'id': usuario.name, 'pacotes': lista_pacotes})

    return lista_usuarios

def atualizar_encomendas():

    lista_usuarios = listar_usuarios()
    for usuario in lista_usuarios:
        lista_pacotes = usuario.get('pacotes')
        for pacote in lista_pacotes:
            try:
                status_novo = read_html.procurar_encomendas(pacote)
                teve_mudanca = status_mudou(usuario.get('id'), pacote, status_novo)
                if teve_mudanca == True:
                    tiao_carteiro = Carteiro(usuario.get('id'), pacote)
                    tiao_carteiro.escrever_carta(status_novo)
                    avisar_usuario(usuario.get('id'), pacote, status_novo)
            except Exception as e:
                print(e)

def status_mudou(id, pacote, status_novo):
    tiao_carteiro = Carteiro(id, pacote)
    status_antigo = tiao_carteiro.ler_carta()
    print(status_antigo)
    print(status_novo)
    if status_antigo == status_novo:
        return False
    else:
        return True


def avisar_usuario(id, pacote, status_encomenda):
    bot = telegram.Bot(token=os.environ['BOT_TOKEN'])
    id = int(id)
    msg = "atualização da encomenda {0}".format(pacote)
    bot.send_message(chat_id=id, text=msg)
    bot.send_message(chat_id=id, text=status_encomenda)

if __name__ == "__main__":
    endereco_usuarios = Path("./pacotes/")
    atualizar_encomendas()
    