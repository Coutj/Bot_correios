import os
import interface_telegram
import read_html
from carteiro import Carteiro
import redis

def limpar_base_de_dados():
    lista_usuarios = listar_usuarios()
    status_possiveis = open('status_possiveis', 'r').readlines()

    for usuario in lista_usuarios:
        for pacote in usuario.get('pacotes'):
            jorge_carteiro = Carteiro(usuario.get('id'), pacote)
            status_base = jorge_carteiro.ler_carta()
            for item in status_possiveis:
                if item in status_base:
                    mensagem = "O pacote {0} foi removido da nossa base de dados pois: '{1}'".format(pacote, item)
                    jorge_carteiro.roubar_pacote()
                    interface_telegram.avisar_usuario(usuario.get('id'), mensagem)
                    
def listar_usuarios():
    lista_usuarios = [item.decode(encoding="UTF8") for item in redis_bd.keys()]
    lista_usuarios_pacotes = list()
    for usuario in lista_usuarios:
        pacotes = {item.decode('UTF8') for item in redis_bd.hgetall(usuario)}
        lista_usuarios_pacotes.append({'id': usuario, 'pacotes': pacotes})

    return lista_usuarios_pacotes

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
                    tiao_carteiro.guardar_status_encomenda(status_novo)
                    msg = "Atualização da encomenda: {0}".format(pacote) + '\n\n' + status_novo
                    interface_telegram.avisar_usuario(usuario.get('id'), msg)
            except:
                pass

def status_mudou(id, pacote, status_novo):
    tiao_carteiro = Carteiro(id, pacote)
    status_antigo = tiao_carteiro.ler_carta()
    if status_antigo == status_novo:
        return False
    else:
        return True

if __name__ == "__main__":
    redis_bd = redis.Redis()
    atualizar_encomendas()
    limpar_base_de_dados()
    
    