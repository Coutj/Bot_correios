import os
from pathlib import Path

class Carteiro():

    def __init__(self, id, pacote):
        self.endereco_usuario = str(id)
        self.pacote = str(pacote)
        self.endereco_dos_correios = Path(Path(__file__).parent / "pacotes")
        self.caixa_de_correio = self.endereco_dos_correios / self.endereco_usuario
        self.endereco_carta = self.caixa_de_correio / self.pacote

    def guardar_status_encomenda(self, status):
    
        if not self.caixa_de_correio.exists():
            self.caixa_de_correio.mkdir()

        self.escrever_carta(status)
    
    def escrever_carta(self, mensagem):
        carta = open(self.endereco_carta.absolute(), "w")
        carta.write(mensagem)
        carta.close()

    def ler_carta(self):
        carta = open(self.endereco_carta.absolute(), "r")
        conteudo_carta = ""
        for line in carta.readlines():
            conteudo_carta += line
        carta.close()
        return conteudo_carta

    def roubar_pacote(self):
        self.endereco_carta.unlink()

    def checar_existencia_pacote(self):
        return self.endereco_carta.exists()