import speech_recognition as sr
import os
import webbrowser
import requests
from bs4 import BeautifulSoup
import pyttsx3
from googlesearch import search

########################################################


# BIBLIOTECA DE PALAVRAS CHAVES PARA PERGUNTAS, DÚVIDAS, QUESTÕES, CURIOSIDADES E ETC

pesquisar_e_sinonimos = {
    'sobre': 1.8,
    'me ajude a encontrar': 1.9,
    'para mim': 1.9,
    'para': 1.9,
    'pesquisar': 1.0,
    'pesquise': 1.0,
    'pesquisa': 1.0,
    'buscar': 1.1,
    'busca': 1.1,
    'busque': 1.1,
    'procurar': 1.2,
    'procura': 1.2,
    'procure': 1.2,
    'encontrar': 1.3,
    'encontre': 1.3,
    'investigar': 1.4,
    'analisar': 1.5,
    'consultar': 1.6,
}

########################################################

# BIBLIOTECA DE PALAVRAS CHAVES PARA INICIAR O PROGRAMA

dic_iniciar_seg = { 
    'cesta': 0,
    'sexta ': 0,
    'sexta-feira': 0,
    'sexta': 0,
}

########################################################

# BIBLIOTECA DE PALAVRAS CHAVES PARA QUESTÕES SOCIAIS (EDUCAÇÃO, PEDI FAVORES ETC)

sociais = {
    'por favor': 1.6,
    'com licença': 1.6,
    'obrigado': 1.7,
    'obrigada': 1.7,
    'por gentileza': 1.6,
    'por obséquio': 1.6,
}

########################################################

# FUNÇÃO QUE INCIA A SEGUNDA-FEIRA (IA)

def inicar_sexta():
    reconhecer = sr.Recognizer()    #GUARDA O VALOR DE RECONHECER VOZ EM VARIAVEL
    with sr.Microphone() as microfone:  # COM ATIVA.MICROFONE COMO MIC (CRIA VARIAVEL MIC)
        reconhecer.adjust_for_ambient_noise(microfone)  # O VALOR DA VARIAVEL RECONHECER E UMA FUNÇÃO DE TIRAR RUIDOS PARA O PARAMETRO (MICROFONE)
        print("SEXTA-FEIRA: Pode falar") # VAI PRINTAR NA TELA PARA O USUARIO PODE FALAR, ASSIM EVITANDO FALAR E NAO CAPTAR
        audio = reconhecer.listen(microfone) # GUARDA O VALOR DO AUDIO (RECONHECE O AUDIO) EM VARIAVEL AUDIO
        texto = reconhecer.recognize_google(audio, language='pt-BR').lower() # TRANSFORMA EM TEXTO PARA A LINGUA PORTUGUESA E ARMAZENA NA VARIAVEL TEXTO
        print(f"Você disse: {texto}") # PRINTA PARA O USUARIO TER CONHECIMENTO DO QUE FOI SALVO DE SUA FALA
        print('----------------------------------------------') # EMBELEZAMENTO
    try:
        if any(palavra in texto for palavra in dic_iniciar_seg): # SE NA VARIAVEL TEXTO TIVER QUALQUER CHAVE DO DICIONARIO VAI INICIAR, CASO CONTRARIO NÃO (NO CASO É PARA INICIAR, CHAMANDO PELO NOME DA IA, COMO O SIRI "HEY SIRI", CASO CONTRARIO NAO CHAMA)
            seg_iniciar_resposta = "Sexta-feira está ativa agora, vamos prosseguir!" # SE FOR ATIVADO O VALOR, VAI SALVAR ESSA RESPOSTA PADRÃO DO SISTEMA EM VARIAVEL
            print(f'{seg_iniciar_resposta.upper()} \nAGUARDE ATÉ A MENSAGEM DE VOZ TERMINAR!')
            print('----------------------------------------------')
            engine = pyttsx3.init()
            engine.setProperty('voice', engine.getProperty('voices')[0].id)
            engine.say(seg_iniciar_resposta)
            engine.runAndWait()
            return True 

    except sr.UnknownValueError:
        seg_iniciar_erro = "Não entendi, tente novamente!"
        engine = pyttsx3.init()
        engine.setProperty('voice', engine.getProperty('voices')[0].id)
        engine.say(seg_iniciar_erro)
        engine.runAndWait()

inicar_sexta_variavel = inicar_sexta()

########################################################

def entender_user_seg():
    seg_iniciada_resposta = "Como posso te ajudar chefe?!"
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[0].id)
    engine.say(seg_iniciada_resposta)
    engine.runAndWait()

    reconhecer = sr.Recognizer()
    with sr.Microphone() as mic:
        reconhecer.adjust_for_ambient_noise(mic)
        print("SEXTA-FEIRA: Pode falar")
        audio = reconhecer.listen(mic)
    try:
        texto = reconhecer.recognize_google(audio, language='pt-BR').lower()
        print(f"VOCÊ DISSE: {texto}")
        print('----------------------------------------------')
        return texto
    except sr.UnknownValueError:
        seg_iniciada_erro = "Não entendi, tente novamente!"
        engine = pyttsx3.init()
        engine.setProperty('voice', engine.getProperty('voices')[0].id)
        engine.say(seg_iniciada_erro)
        engine.runAndWait()
        return ''

def pesquisar_segunda(pesquisarsite):
    segunda_pesquisar_voz = "Você deseja que eu leia, ou te redirecione para a aba? (Responde com leia ou redirecione)"
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[0].id)
    engine.say(segunda_pesquisar_voz)
    engine.runAndWait()

    receconhecer = sr.Recognizer()
    with sr.Microphone() as mic:
        receconhecer.adjust_for_ambient_noise(mic)
        print("SEXTA FEIRA: Pode Falar")
        audio = receconhecer.listen(mic)
        texto = receconhecer.recognize_google(audio, language='pt-BR').lower()
    
    if 'leia' in texto:
        print(f"VOCÊ DISSE: {texto}")
        for url in search(pesquisarsite, num_results=1):
            print('--------------------------------------------------')
            print(f"Pesquisando sobre: {texto}")
            ler_site(url)
    elif 'redirecione' in texto:
        print(f"VOCÊ DISSE: {texto}")
        webbrowser.open(f"https://www.google.com/search?q={pesquisarsite}")



def ler_site(url):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status() 
        sopa = BeautifulSoup(resposta.text, 'html.parser')
        

        paragrafos = sopa.find_all('p')
        
        texto = ' '.join(paragrafo.get_text(strip=True) for paragrafo in paragrafos)

        if texto:
            engine = pyttsx3.init()
            engine.say(texto)
            engine.runAndWait()
        else:
            print("Nenhum parágrafo encontrado.")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o site: {e}")

########################################################

entender_user_seg_variavel = ''
if inicar_sexta_variavel:
    entender_user_seg_variavel = entender_user_seg()

if entender_user_seg_variavel:
    for sinonimo in pesquisar_e_sinonimos:
        if sinonimo in entender_user_seg_variavel:
            procurar_termo = entender_user_seg_variavel.split(sinonimo, 1)[-1].strip()
            if procurar_termo:
                for social in sociais:
                    if procurar_termo.endswith(social):
                        procurar_termo = procurar_termo[:-len(social)].strip()  
                        break  

                procurar_termo = procurar_termo.lstrip(',').strip() 
                pesquisar_segunda(procurar_termo)
            break
