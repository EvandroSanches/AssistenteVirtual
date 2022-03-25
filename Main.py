from chatterbot import ChatBot
import speech_recognition as sr
import pyttsx3
import funcoes
import traceback
from pocketsphinx import LiveSpeech
from chatterbot.trainers import ListTrainer




#-----------------------------------------
#Criando Chatbot, Setando sintetizador de voz, Carregando dicionario com comandos em arquivo externo e Treinando Chatbot


bot = ChatBot('Mari',read_only=True,)
speaker = pyttsx3.init('sapi5')
funcoes.setvoice(speaker)
dic_cmds = {}
funcoes.load_cmds(dic_cmds)
r = sr.Recognizer()

trainer = ListTrainer(bot)


#lines = open('Chats/Conversas.txt','r').readlines()

#trainer.train(lines)
#-----------------------------------------

"""lines = open('Chats/treino8.txt','r', encoding='utf-8').readlines()

for line in lines:
    line = line.replace('\n','')
    line = line.lstrip()
    parts = line.split('?')
    
    trainer.train(parts)
"""

#INICIO DA FUNCAO RECOGNIZE_MICROPHONE
def recognize_microphone():
#FUNCAO PRINCIPAL QUE RECONHECE COMANDOS DO MICROFONE E REALIZA O TRATAMENTO DOS MESMO


    with sr.Microphone() as s:
        r.adjust_for_ambient_noise(s,duration=0.5)
        mode = 1
        while True:
            try:
                input("Pressione enter para chamar!!")
                funcoes.speak(speaker, funcoes.call_back())

                if mode == 1: # VERIFICA SE CONFIGURAÇÃO ESTA COMUNICAÇÃO POR TEXTO
                    speech = input("Digite:")

                response = False # VARIAVEL PARA SABER SE É RESPOSTA DO CHATBOT OU COMANDO

                if mode == 0: # VERIFICA SE A COMUNICAÇÃO ESTA POR VOZ
                    print('Fale!')
                    audio = r.listen(s,phrase_time_limit=4)
                    speech = r.recognize_google(audio_data=audio,language='pt-BR')


                fala_tratada = funcoes.evaluate(speech)
                bot_response = bot.get_response(fala_tratada)

                if float(bot_response.confidence) > 0.5: # VERIFICA CONFIANÇA DE RESPOSTAS NA BASE DE DADOS
                    response = True

                else:
                    bot_response = funcoes.verifica_cmd(fala_tratada,dic_cmds) # VERIFICA SE É UM COMANDO
                    if bot_response == None: # SE NÃO FOR UM COMANDO
                        bot_response = bot.get_response(fala_tratada)
                        response = True

                if response:
                    if float(bot_response.confidence) > 0.6:
                        print('Voce: ', speech)
                        print('Mari: ', bot_response)
                        print('------------------------------------------------------------------------')
                        funcoes.speak(speaker, bot_response)
                        #calling()

                    else: # SE NÃO FOR UM COMANDO E NÃO TIVER RESPOSTA NA BASE
                        print('Voce: ', speech)
                        print('Mari: ', 'Desculpe, ainda não sei como responder.')
                        funcoes.speak(speaker, 'Desculpe, ainda não sei como responder.')

                        pergunta = speech # VARIAVEL RECEBE FRASE FORNECIDA PELO USUARIO

                        while speech != 'sim' : # ENQUANTO O USUARIO DISSER ALGO DIFERENTE DE 'SIM'

                            print('Mari: ', 'O que devo responder?')
                            funcoes.speak(speaker, 'O que devo responder?')

                            if mode == 1: # VERIFICAÇÃO DE MODO DE COMUNICAÇÃO
                                chat_resposta = input("Digite:")

                            if mode == 0: # VERIFICAÇÃO DE MODO DE COMUNICAÇÃO
                                print('Fale!')
                                audio = r.listen(s)
                                chat_resposta = r.recognize_google(audio_data=audio, language='pt-BR')

                            speech = funcoes.evaluate(speech)

                            if chat_resposta == 'nada': # SE O USUARIO DISSER 'NADA' PARA A PERGUNTA 'O QUE DEVO RESPONDER' SAI DO LOOP
                                speech = 'sim'

                            else:
                                print('Mari: ',  chat_resposta , ', está correto?.') # CONFIRMAÇÃO DE APRENDIZAGEM
                                funcoes.speak(speaker, chat_resposta + ', está correto?')

                                if mode == 1:
                                    speech = input("Digite:")

                                if mode == 0:
                                    print('Fale!')
                                    audio = r.listen(s)
                                    speech = r.recognize_google(audio_data=audio, language='pt-BR')

                                if speech == 'sim' or speech == 'Sim': # SE CONFIRMADA SERÁ FEITA A APRENDIZAGEM
                                    treino = [pergunta, chat_resposta]
                                    trainer.train(treino)
                                    print('Mari: ', 'Obrigada por me ensinar.')
                                    funcoes.speak(speaker, 'Obrigada por me ensinar.')
                                    print('------------------------------------------------------------------------')
                        #calling()


                else:
                    if(bot_response == 'Modo de digitação iniciado'):
                        mode = 1
                    if(bot_response == 'Modo de fala iniciado'):
                        mode = 0
                    print('Voce: ', speech)
                    print('Mari: ', bot_response)
                    funcoes.speak(speaker, bot_response)
                    print('------------------------------------------------------------------------')
                    #calling()

            except: # CASO DE ERROS NO PROCESSO DE RECONHECIMENTO DE VOZ
                print('erro.')
                funcoes.speak(speaker, 'Desculpe, não consegui entender.')
                tb = traceback.format_exc()
                #calling()


#FIM DA FUNCAO RECOGNIZE_MICROPHONE
#---------------------------------------------------------


#INICIO DA FUNCAO CALLING
def calling():
#FUNCAO PARA OUVIR AUDIO DO MICROFONE EM TEMPO REAL E CHAMAR FUNCAO PRINCIPAL DE COMANDOS POR VOZ

    for phrase in LiveSpeech():
        frase = str(phrase)
        print(frase)
        funcoes.evaluate_live(frase)

        if "hello" in frase:
            recognize_microphone()

#FIM DA FUNCAO CALLING
#---------------------------------------------------------

funcoes.speak(speaker,'Sistema iniciado.')


recognize_microphone()

