import os
import redis

class Carteiro():

    def __init__(self, id, pacote):
        self.user_id = str(id)
        self.pacote = bytes(str(pacote), 'ascii')
        self.redis_bd = redis.Redis()
        self.user_dict = self.redis_bd.hgetall(self.user_id)

    def guardar_status_encomenda(self, status):
    
        if self.redis_bd.exists(self.user_id):
            self.user_dict[self.pacote] = status
            self.redis_bd.hmset(self.user_id, self.user_dict)
        else:
            novo_user_dict = {self.pacote: status}
            self.redis_bd.hmset(self.user_id, novo_user_dict)
    
    def ler_carta(self):
        carta = self.user_dict.get(self.pacote)
        carta = carta.decode(encoding='UTF-8')
        return carta

    def roubar_pacote(self):
        if self.pacote in self.user_dict:
            if len(self.user_dict) == 1:
                self.redis_bd.delete(self.user_id)
            else:
                del self.user_dict[self.pacote]
                self.redis_bd.hmset(self.user_id, self.user_dict)
        else:
            raise ValueError('codigo nao existente na base de dados')

    def checar_existencia_pacote(self):
        return self.user_dict.get(self.pacote)