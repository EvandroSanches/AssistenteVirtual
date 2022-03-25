import traceback
#IMPORTS
#--------------------------------------------------------------------


#INICIO DA FUNCAO
def load_cmds(dic_cmds):
#FUNCAO PARA CARREGAR COMANDOS DE ARQUIVO TXT EXTERNO EM UM DICIONARIO
    lines = open('Chats/cmds.txt','r').readlines()

    for line in lines:
        line = line.replace('\n','')
        parts = line.split('\t')
        dic_cmds.update({parts[0]:parts[1]})
    #espacos em branco no final do arquivo de comando pode gerar erro
#FIM DA FUNCAO load_cmds()
#--------------------------------------------------------------------


#INICIO DA FUNCAO VERIFICA_CMD
def verifica_cmd(speech,dic_cmds):
#FUNCAO PRA VEREFICAR QUAL COMANDO ESTA SENDO DADO

    google_keywords = ['pesquise por', 'pesquisar por', 'pesquisar ']
    Wiki_keywords = ['o que é ', 'quem é ', 'quem foi ', 'qual é a definição ', 'defina ','quem foram ', 'quem são ','quais são'
        , 'quais foram', 'qual é', 'o que são']
    Full_Search_keywords = ['pesquisa completa por']
    keywords_open = ['abrir ', 'executar ', 'iniciar ']

    try:
        for key in keywords_open:
            if speech.startswith(key):
                cmd_type = 'open'
                text = str(speech)
                text = text.replace(key, '')
                text = text.strip()
                return run_cmd(cmd_type,text)

        for key in Wiki_keywords:
            if speech.startswith(key):
                cmd_type = 'wikipedia'
                return run_cmd(cmd_type,speech)


        for key in google_keywords:
            if speech.startswith(key):
                text = str(speech)
                text = text.replace(key,'')
                cmd_type = 'pesquisa'
                return run_cmd(cmd_type,text)

        for key in Full_Search_keywords:
            if speech.startswith(key):
                text = str(speech)
                text = text.replace(key, '')
                cmd_type = 'pesquisaFull'
                return run_cmd(cmd_type, text)

        cmd_type = dic_cmds[speech]

        return run_cmd(cmd_type, speech)

    except:
        tb = traceback.format_exc()


#FIM DA FUNCAO VERIFICA_CMD
#--------------------------------------------------------------------


#INICIO DA FUNCAO
def setvoice(speaker):
#FUNCAO PARA CONFIGURAR IDIOMA DA VOZ

    voices = speaker.getProperty('voices')
    speaker.setProperty('rate',194)
    speaker.setProperty('volume',1.0)
    for voice in voices:

        if voice.name == 'brazil':
            speaker.setProperty('voice', voice.id)
#FIM DA FUNCAO setvoice()
#--------------------------------------------------------------------


#INICIO DA FUNCAO
def speak(speaker,text):
#FUNCAO DE FALA
    speaker.say(text)
    speaker.runAndWait()
#FIM DA FUNCAO speak()
#--------------------------------------------------------------------


#INICIO DA FUNCAO
def evaluate(text):
#FUNCAO PARA FORMATAR FALA DO MICROFONE

    t = str(text)
    t = t.lower()
    t = t.replace('mari','')
    t = t.replace('mary','')
    t = t.strip()
    return t
#FIM DA FUNCAO evaluate()
#--------------------------------------------------------------------


#INICIO DA FUNCAO
def run_cmd(cmd_type,speech):
#FUNCAO PARA EXECUTAR COMANDOS

    import datetime

    result = None


    if (cmd_type == 'asktime'):
        now = datetime.datetime.now()
        result = 'São '+ str(now.hour) + ' horas e '+ str(now.minute) + ' minutos.'

    elif (cmd_type == 'askdate'):

        mes = {1: 'Janeiro',2: 'Fevereiro',3: 'Março',4: 'Abril',5: 'Maio',
                6: 'Junho',7: 'Julho',8: 'Agosto',9: 'Setembro',10: 'Outubro',
                11: 'Novembro',12: 'Dezembro',}

        dia_semana = {6: 'Domingo',0: 'Segunda',1: 'Terça',2: 'Quarta',3: 'Quinta',
                        4: 'Sexta',5: 'Sábado',}


        now = datetime.datetime.now()
        result = 'Hoje é  '+ dia_semana[now.weekday()] + ' dia '+ str(now.day) + ' de ' + mes[now.month]

    elif (cmd_type == 'wikipedia'):
        result = search_wikipedia(speech)

    elif (cmd_type == 'pesquisa'):
        result = search_google(speech)


    elif (cmd_type == 'pesquisaFull'):
        result = full_search_google(speech)

    elif (cmd_type == 'open'):
        result = OpenSoftware(speech)
        if result == None:
            result = "Não encontrei nenhum programa com o nome de "+speech
    elif (cmd_type == 'digitemode'):
        result = 'Modo de digitação iniciado'

    elif (cmd_type == 'speakmode'):
        result = 'Modo de fala iniciado'

    else:
        result = None

    return result
#FIM DA FUNCAO run_cmd()
#--------------------------------------------------------------------


#INICIO DA FUNCAO SEARCH_WIKIPEDIA
def search_wikipedia(text):
#FUNCAO DE PESQUISA NO WIKIPEDIA

    import wikipedia
    wikipedia.set_lang('pt')
    search = None

    search = wikipedia.search(text)
    text = wikipedia.summary(search[0],sentences=1)

    return text
#FIM DA FUNCAO SEARCH_WIKIPEDIA
#--------------------------------------------------------------------


#INICIO DA FUNCAO SEARCH_GOOGLE
def search_google(text):
#FUNCAO DE PESQUISA NO GOOGLE COM RETORNO DE PAGINA MAIS ACESSADA

    import googlesearch as search
    import webbrowser

    result = None

    result = 'Pesquisando por '+text
    for url in search.search(text, stop=1, lang='pt'):
        webbrowser.open_new_tab(url)


    return result

#FIM DA FUNCAO SEARCH_GOOGLE
#--------------------------------------------------------------------


#INICIO DA FUNCAO SEARCH_GOOGLE
def full_search_google(text):
#FUNCAO DE PESQUISA COMPLETA NO GOOGLE

    import webbrowser

    result = None

    result = 'Pesquisando por '+text
    pesquisa = ('https://www.google.com.br/search?q='+text)
    webbrowser.open(pesquisa)

    return result

#FIM DA FUNCAO SEARCH_GOOGLE
#--------------------------------------------------------------------

#INICIO DA FUNCAO EVALUATE_LIVE
def evaluate_live(text):
#FUNCAO PARA FORMATAR TEXTO DE LIVE_SPEECH
    t = str(text)
    t = t.lower()
    t = t.strip()
    return t
#FIM DA FUNCAO EVALUATE LIVE
#--------------------------------------------------------------------


#INICIO DA FUNCAO CALL_BACK
def call_back():
#FUNCAO PARA GERAR UMA RESPOSTA À CHAMADA DA ASSISTENTE
    from random import randint

    random = randint(0,3)
    dic_call = ['Sim.', 'Do que precisa', 'O que deseja', 'Estou aqui', 'Em que posso ajudar.']
    return dic_call[random]

#FIM DA FUNCAO CALL_BACK
# --------------------------------------------------------------------


#INICIO DA FUNCAO OPENSOFTWARE
def OpenSoftware(text):
#FUNCAO PARA BUSCAR E EXECUTAR PROGRAMA
    import os
    result = ""
    programa = ''
    programas = {'bloco de notas' : 'notepad', 'google' : 'C:\Program Files (x86)\Google\Chrome\Application/chrome', 'word' :
                 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs/Word' , 'excel' : 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs/Excel'
                 , 'lol' : 'C:\Riot Games\Riot Client/RiotClientServices.exe', 'league of legends' : 'C:\Riot Games\Riot Client/RiotClientServices.exe',
                 'paint' : 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories/Paint', 'ferramenta de captura' : 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories/Ferramenta de Captura'}

    try:
        programa = programas[text]
        os.startfile(programa)
        result = "Iniciando "+text
        return result
    except:
        result = "Não consegui encontrar este programa"
        return result
#FIM DA FUNCAO OPENSOFTWARE
# --------------------------------------------------------------------

