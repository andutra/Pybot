#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters # pip install python-telegram-bot
import logging, sys
import os
import random



API_TOKEN = os.environ['PyBotApi']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Function called when /start is sended to bot
def start(update, context):
    msg = update.message.reply_text("Ola como posso te ajudar?")

#Function called when the Pybot name is said
def call_my_name(update, context):
    print("Alguém disse meu nome")
    frases = [u'\U0001F610' + " Sem tempo irmão", "Olá eu sou o bot que auxilia nesse grupo, tudo bem?"]
    idx = random.randint(0,len(frases)-1)
    #msg = bot.reply_to(message, u'\U0001F610' + " Sem tempo irmão")
    try:
       update.message.reply_text(frases[idx])
    except Exception as e:
       print(str(e))
       return 0

#Function called when 'Hello World' is said 
def hello_world(update, context):
    try:
        update.message.reply_text("Opa, eu sei fazer um Hello World.\nprint(\"Hello World\")")
    except Exception as e:
        print(str(e))
        return 0
      
#Function called when 'O que é uma variável' is said 
def variavel(update, context):
    try:
        update.message.reply_text("Uma variável pode ser imaginada como um \"caixa\" para armazenar valores de dados." + \
        "Esta caixa só pode armazenar um único valor por vez. No entanto, o valor armazenado na caixa pode mudar inúmeras" + \
        "vezes durante a execução do algoritmo. Em um ambiente computacional de verdade, a caixa correspondente a uma variável" + \
        "é uma posição da memória do computador.")
    except Exception as e:
        print(str(e))
        return 0

#Function called when 'O que é uma string' is said       
def string_reply(update, context):
    try:
        update.message.reply_text("Uma string é uma cadeia ou sequência de caracteres, ela pode ser entendida como uma lista" + \
                                  " de caracteres utilizada para representar uma palavra, frase ou texto em um programa.\n" + \
                                 "Por exemplo, 'abcde', é um lista que contém os caracteres 'a', 'b', 'c','d' e 'e'\n." + \
                                 "Veja aqui uma explicação bem completa: https://pt.wikipedia.org/wiki/Cadeia_de_caracteres")
    except Exception as e:
        print(str(e))
        return 0
      
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

#Function called when a new member enter to the group
def welcome(update, dsp):
    for new_user_obj in update.message.new_chat_members:
        new_user = ""
        try:
            new_user = "@" + new_user_obj['username']
        except Exception as e:
            new_user = new_user_obj['first_name'];

        message_list = ["Seja bem vindo {{username}}" 
                        ,"Olá {{username}} espero que você possa aprender muito nesse grupo"
                        ,"Que bom que você entrou {{username}}, vamos todos aprender muito!"
                       ] 
        chat_id = update.message.chat.id
        message_rnd = random.choice(message_list)

        dsp.bot.sendMessage(chat_id=chat_id, text=message_rnd.replace("{{username}}",str(new_user)), parse_mode='HTML')



def main():
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
    # prices = client.get_all_tickers()
    while True:
        try:
            print("Iniciando Pybot...")
            updater = Updater(API_TOKEN, use_context=True)
            # Get the dispatcher to register handlers
            dp = updater.dispatcher

            #Add command handler
            cmds = {"start": start}

            for cmd in cmds.items():
                dp.add_handler(CommandHandler(cmd[0], cmd[1]))

            rgxHandlers = {"[Hh]ello [Ww]orld": hello_world 
                           ,"[Oo] que ([eé]|s[aã]o)( uma)? [Vv]ari[aá]ve[l|is]": variavel
                           ,"[Oo] que ([eé]|s[aã]o)( uma)? [Ss]tring": string_reply
                           ,"(^|\W)[Pp]y[Bb]ot(\W|$)": call_my_name
                          }
            
            for handler in rgxHandlers.items():
                dp.add_handler(MessageHandler(Filters.regex(handler[0]), handler[1]))

            #add a handler to find new users on chat
            dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

            # log all errors
            dp.add_error_handler(error)

            #Polling
            # Start the Bot
            updater.start_polling()

            # Run the bot until you press Ctrl-C or the process receives SIGINT,
            # SIGTERM or SIGABRT. This should be used most of the time, since
            # start_polling() is non-blocking and will stop the bot gracefully.
            updater.idle()


        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()

        except Exception as e:
            print(str(e))
            sys.exit()




if __name__ == '__main__':
    main()


