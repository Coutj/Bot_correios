import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import read_html
import carteiro




def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Digite o código de rastreamento do pacote")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Você também pode remover um pacote digitando '/remover <pacote>'")

def receber_pacotes(update, context):
    codigo = formatar_codigo(update.message.text)
    try:
        validar_codigo(codigo)
        mensagem = checar_status(update.message.text, update.effective_chat.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Verificaremos o seu pacote a cada 1h, nao seja afobado.')
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=e.args)

def checar_status(pacote, id):
    joao_carteiro = carteiro.Carteiro(id, pacote)
    try:
        status_encomenda = read_html.procurar_encomendas(pacote)
        joao_carteiro.guardar_status_encomenda(status_encomenda)
        return status_encomenda
    except:
        return "Não foi possível acessar o site dos correios"

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


if __name__ == "__main__":

    token_bot_path = "/home/juan/Documents/Telegram/token"
    token_bot = str(open(token_bot_path, "r").readline()).replace("\n", "")

    updater = Updater(token=token_bot, use_context=True)
    bot = telegram.Bot(token=token_bot)
    dispatcher = updater.dispatcher    

    updater.start_polling()

    start_handler = CommandHandler('start', start)
    receber_mensagem_handler = MessageHandler(Filters.text & (~Filters.command), receber_pacotes)
    remover_pacote_handler = CommandHandler('remover', remover_pacote) 

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(receber_mensagem_handler)
    dispatcher.add_handler(remover_pacote_handler)
