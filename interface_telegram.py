import threading
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import read_html
import carteiro


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Digite o código de rastreamento do pacote")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Você também pode remover um pacote digitando '/remover <pacote>'")

def receber_pacotes(update, context):
    codigo = formatar_codigo(update.message.text)
    try:
        validar_codigo(codigo)
        event = threading.Event()
        event.set()
        threading.Thread(target=thread_busca_status, args=(event, update.effective_chat.id, codigo,), daemon=True).start()
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=e.args[0])

def checar_status(id, pacote):
    joao_carteiro = carteiro.Carteiro(id, pacote)
    try:
        status_encomenda = read_html.procurar_encomendas(pacote)
        joao_carteiro.guardar_status_encomenda(status_encomenda)
        bot.send_message(chat_id=int(id), text=status_encomenda)
        bot.send_message(chat_id=int(id), text='Verificaremos o seu pacote a cada 1h, nao seja afobado.')
    except:
        bot.send_message(chat_id=int(id), text='Não foi possível acessar o site dos correios.')
 
def remover_pacote(update, context):
    try:
        pacote = formatar_codigo(context.args[0])
        validar_codigo(pacote)
        carteiro_lalau = carteiro.Carteiro(update.effective_chat.id, pacote)
        if carteiro_lalau.checar_existencia_pacote() == False:
            raise ValueError('codigo nao existente na base de dados')
        else:
            carteiro_lalau.roubar_pacote()
            bot.send_message(update.effective_chat.id, text="O código {0} foi removido".format(pacote))
    except ValueError as e:
        bot.send_message(update.effective_chat.id, text=e.args)

def validar_codigo(codigo):
    if len(codigo) != 13:
        raise ValueError('comprimento invalido.')
    elif codigo.isalnum() == False:
        raise ValueError('codigo deve conter apenas letras e numeros.')

def formatar_codigo(codigo):
    codigo = codigo.replace(" ", "")
    codigo = codigo.upper()
    return codigo

def thread_busca_status(event, id, pacote):
    if event.is_set() == True:
        checar_status(id, pacote)
    event.clear()

def avisar_usuario(id, mensagem):
    id = int(id)
    bot = telegram.Bot(token=os.environ['BOT_TOKEN'])
    bot.send_message(chat_id=id, text=mensagem)

if __name__ == "__main__":

    updater = Updater(token=os.environ['BOT_TOKEN'], use_context=True)
    bot = telegram.Bot(token=os.environ['BOT_TOKEN'])
    dispatcher = updater.dispatcher    

    updater.start_polling()

    start_handler = CommandHandler('start', start)
    receber_mensagem_handler = MessageHandler(Filters.text & (~Filters.command), receber_pacotes)
    remover_pacote_handler = CommandHandler('remover', remover_pacote) 

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(receber_mensagem_handler)
    dispatcher.add_handler(remover_pacote_handler)
