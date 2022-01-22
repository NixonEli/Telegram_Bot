from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters, CallbackQueryHandler, MessageHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, InputMediaAudio
from pytube import YouTube
from bs4 import BeautifulSoup as b
from bs4 import BeautifulSoup

import unicodedata, sys, os, urllib3, pathlib, youtube_dl, requests, pyshorteners, re
import pandas as pd
import time

CONVERSACION=0
CONVERSACION_1=1

def start (update, context):
    bot=context.bot
    chatId=update.message.chat_id
    id_mensajito = update.message.message_id
    username=update.effective_user["first_name"]

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    bot.send_message(
        chat_id=chatId,
        text= "Hola 👋🏼 " + username + " Soy Boxy!. Toca los botones y sigue las instrucciones.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Biblia", callback_data="biblia_menu"), InlineKeyboardButton(text="Música Cristiana", callback_data="musica_cristiana")],
            [InlineKeyboardButton(text="YouTube", callback_data="youtube"), InlineKeyboardButton(text="Ayuda", url="https://telegra.ph/Proyect-B---Comandos-03-30")],
            [InlineKeyboardButton(text="Cerrar Dialogo", callback_data="cerrar_dialogo")]
        ])
        )

def biblia_menu (update, context):
    query = update.callback_query
    bot = context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    query.edit_message_text(
        text="En esta sección esncontraras todo acerca de la Biblia",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Biblia (RVR-1960)", callback_data="biblia"), InlineKeyboardButton(text="Texto del Dia", callback_data="texto_dia")],
            [InlineKeyboardButton(text="Textos Biblicos", callback_data="texto_biblico"), InlineKeyboardButton(text="Preguntas", callback_data="preguntas_biblia")],
            [InlineKeyboardButton(text="Postales", callback_data="postales_cristianos"), InlineKeyboardButton(text="Menú principal", callback_data="menu_principal_bot")]
        ])
    )

def postales_cristianos (update, context):
    query = update.callback_query
    bot = context.bot
    chatId = query.message.chat_id
    id_mensajito = query.message.message_id

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    url = 'https://www.postalescristianas.net/random'

    req = urllib3.PoolManager()
    res = req.request('GET', url)
    soup = BeautifulSoup(res.data, 'html.parser')

    Texto_url = soup.find_all('h1')
    Imagen_url = soup.body.find_all('input')

    Texto = []
    for span in Texto_url:
        Texto = span.getText()

    Imagen = []
    for span in Imagen_url:
        Imagen.append(span.get('value'))

    Texto = Texto
    Imagen = Imagen[3]

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    query.edit_message_text(
        text=f"[{str(Texto)}]({Imagen})",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Actualizar", callback_data="postales_cristianos"), InlineKeyboardButton(text="Volver al menú", callback_data="menu_principal_bot")]
        ])
    )

def postales_cristianos_2 (update, context):
    bot = context.bot
    chatId = update.message.chat_id
    id_mensajito = update.message.message_id

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    url = 'https://www.postalescristianas.net/random'

    req = urllib3.PoolManager()
    res = req.request('GET', url)
    soup = BeautifulSoup(res.data, 'html.parser')

    Texto_url = soup.find_all('h1')
    Imagen_url = soup.body.find_all('input')

    Texto = []
    for span in Texto_url:
        Texto = span.getText()

    Imagen = []
    for span in Imagen_url:
        Imagen.append(span.get('value'))

    Texto = Texto
    Imagen = Imagen[3]

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    bot.send_message(
        chat_id=chatId,
        text=f"[{str(Texto)}]({Imagen})",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Actualizar", callback_data="postales_cristianos"), InlineKeyboardButton(text="Volver al menú", callback_data="menu_principal_bot")]
        ])
    )

def preguntas_biblia (update, context):
    query = update.callback_query
    bot = context.bot
    chatId = query.message.chat_id
    id_mensajito = query.message.message_id

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    url = 'https://www.gotquestions.org/Espanol/'
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Preguntas = []
    for tag in soup.findAll('a', href=True):
        Preguntas.append(tag.getText())

    Preguntas = Preguntas[24:55]

    Preguntas_envio = []
    for i in range(0, len(Preguntas)):
        Preguntas_envio.append(str(i + 1) + '. ' + Preguntas[i])

    Preguntas_opcion = '\n'.join(Preguntas_envio)

    query.edit_message_text(
        text="A continuación envié el número del tema." + '\n' + '\n' + Preguntas_opcion,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Volver al menú principal", callback_data="menu_principal_bot")]
        ])
    )

    return CONVERSACION

def respuesta_preguntas (update, context):
    username = update.effective_user["first_name"]
    Texto = int(update.message.text)
    bot = context.bot
    chatId = update.message.chat_id
    id_mensajito = update.message.message_id

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    url = 'https://www.gotquestions.org/Espanol/'
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls = []
    Preguntas = []
    for tag in soup.findAll('a', href=True):
        Urls.append(tag['href'])
        Preguntas.append(tag.getText())

    Urls = Urls[24:55]
    Preguntas = Preguntas[24:55]

    Urls = Urls[Texto - 1]
    Preguntas = Preguntas[Texto - 1]

    url = 'https://www.gotquestions.org/Espanol/' + Urls
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls_Preguntas = []
    Preguntas_Preguntas = []
    for tag in soup.findAll('a', href=True):
        Urls_Preguntas.append(tag['href'])
        Preguntas_Preguntas.append(tag.getText())

    Urls_Preguntas = Urls_Preguntas[15:]
    Preguntas_Preguntas = Preguntas_Preguntas[15:]

    Temporal = {'ID': [str(chatId)], 'PREGUNTA': [Preguntas], 'ENLACE': [Urls], 'NUMERO': [str(Texto)]}
    Nombre_Librito = str(chatId) + '_' + 'Temporal.csv'
    df = pd.DataFrame(data=Temporal)
    df.to_csv(Nombre_Librito, index=False)

    Final = ''
    for i in range(0, len(Preguntas_Preguntas)):
        if Preguntas_Preguntas[i].__contains__('Retornar a la página inicial de Español'):
            Final = i

    Urls_Preguntas = Urls_Preguntas[7:Final]
    Preguntas_Preguntas = Preguntas_Preguntas[7:Final]

    Preguntas_envio = []
    for i in range(0, len(Preguntas_Preguntas)):
        Preguntas_envio.append(str(i + 1) + '. ' + Preguntas_Preguntas[i])

    keyboard1 = []
    texto_caption = ''
    if len(Preguntas_envio) > 30:
        Preguntas_envio = Preguntas_envio[0:30]
        keyboard1.append([InlineKeyboardButton(text="Siguiente", callback_data="preg_next")])
        keyboard1.append([InlineKeyboardButton(text="Volver al menú principal", callback_data="menu_principal_bot")])
    else:
        keyboard1.append([InlineKeyboardButton(text="Volver al menú principal", callback_data="menu_principal_bot")])

    reply_markupp = InlineKeyboardMarkup(keyboard1)

    Preguntas_opcion = '\n'.join(Preguntas_envio)

    bot.edit_message_text(
        chat_id=chatId,
        message_id=id_mensajito - 1,
        text=Preguntas + '\n' + '\n' + Preguntas_opcion,
        reply_markup=reply_markupp
    )

    return CONVERSACION_1

def respuesta_preguntas_respuesta (update, context):
    username = update.effective_user["first_name"]
    Texto = int(update.message.text)
    bot = context.bot
    chat = update.message.chat
    chatId = update.message.chat_id
    id_mensajito = update.message.message_id

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)
    bot.delete_message(chat_id=chatId, message_id=id_mensajito-2)
    bot.sendChatAction(chat_id=chatId, action="upload_document", timeout=None)

    Buscar_Dato = str(chatId) + '_Temporal.csv'
    datos = pd.read_csv(Buscar_Dato, header=0)
    Tema_numero = datos.values.tolist()[0][3]

    url = 'https://www.gotquestions.org/Espanol/'
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls = []
    Preguntas = []
    for tag in soup.findAll('a', href=True):
        Urls.append(tag['href'])
        Preguntas.append(tag.getText())

    Urls = Urls[24:55]
    Preguntas = Preguntas[24:55]

    Urls = Urls[Tema_numero - 1]
    Preguntas_0 = Preguntas[Tema_numero - 1]

    url = 'https://www.gotquestions.org/Espanol/' + Urls
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls_Preguntas = []
    Preguntas_Preguntas = []
    for tag in soup.findAll('a', href=True):
        Urls_Preguntas.append(tag['href'])
        Preguntas_Preguntas.append(tag.getText())

    Urls_Preguntas = Urls_Preguntas[15:]
    Preguntas_Preguntas = Preguntas_Preguntas[15:]

    Final = ''
    for i in range(0, len(Preguntas_Preguntas)):
        if Preguntas_Preguntas[i].__contains__('Retornar a la página inicial de Español'):
            Final = i

    Urls = Urls_Preguntas[7:Final]
    Preguntas = Preguntas_Preguntas[7:Final]

    Urls = Urls[Texto - 1]
    Preguntas1 = Preguntas[Texto - 1]

    url = 'https://www.gotquestions.org/Espanol/' + Urls
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls_Preguntas = []
    for tag in soup.findAll('a', href=True):
        Urls_Preguntas.append(tag['href'])

    Audio = ''
    for i in range(0, len(Urls_Preguntas)):
        if Urls_Preguntas[i].__contains__('mp3'):
            Audio = i

    try:
        Audio_link = 'https://www.gotquestions.org/Espanol/' + Urls_Preguntas[Audio]
    except:
        pass

    Ruta_txt = 0
    for i in range(0, len(Urls_Preguntas)):
        if Urls_Preguntas[i].__contains__('Printer'):
            Ruta_txt = i

    s = pyshorteners.Shortener()
    try:
        Audio_envio = s.dagd.short(Audio_link)
    except:
        Audio_envio = 'Sin Audio'

    url = 'https://www.gotquestions.org/Espanol/' + Urls_Preguntas[Ruta_txt]
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Textito = []
    for tag in soup.find_all('body'):
        Textito.append(tag.getText())

    Textito = Textito[0].replace('\n', '\n\n')
    Textito = Textito.split('\n')
    Textito = Textito[8:(len(Textito) - 4)]
    Textito = '\n'.join(Textito)

    my_file = open(Preguntas_0 + '.txt', "w+")
    my_file.write(Textito)
    my_file.close()

    Buscar_Dato = str(chatId) + '_Temporal.csv'
    os.remove(Buscar_Dato)

    Documento = Preguntas_0 + '.txt'
    ruta_arch = pathlib.Path().absolute()
    Archivo_Envio = os.path.join(ruta_arch, Documento)

    chat.send_document(
        document=open(Archivo_Envio, "rb"),
        caption=Preguntas_0 + '\n' + Preguntas1,
        #reply_markup = InlineKeyboardMarkup([
            #[InlineKeyboardButton(text="Volver al menú principal", callback_data="menu_principal_bot")]
        #])
    )

    if Audio_envio == 'Sin Audio':
        pass
    else:
        bot.send_message(
            chat_id=chatId,
            text='Escucha el mensaje:' + '\n' + Audio_envio)

    os.remove(Preguntas_0 + '.txt')
    return ConversationHandler.END

def preg_next (update, context):
    query = update.callback_query
    Texto = query.message.text
    bot = context.bot
    chatId = query.message.chat_id
    id_mensajito = query.message.message_id

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    url = 'https://www.gotquestions.org/Espanol/'
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls = []
    Preguntas = []
    for tag in soup.findAll('a', href=True):
        Urls.append(tag['href'])
        Preguntas.append(tag.getText())

    Urls = Urls[24:55]
    Preguntas = Preguntas[24:55]

    Buscar_Dato = str(chatId) + '_Temporal.csv'
    datos = pd.read_csv(Buscar_Dato, header=0)
    Tema_numero = datos.values.tolist()[0][3]

    Urls = Urls[Tema_numero - 1]
    Preguntas = Preguntas[Tema_numero - 1]

    url = 'https://www.gotquestions.org/Espanol/' + Urls
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls_Preguntas = []
    Preguntas_Preguntas = []
    for tag in soup.findAll('a', href=True):
        Urls_Preguntas.append(tag['href'])
        Preguntas_Preguntas.append(tag.getText())

    Urls_Preguntas = Urls_Preguntas[15:]
    Preguntas_Preguntas = Preguntas_Preguntas[15:]

    Final = ''
    for i in range(0, len(Preguntas_Preguntas)):
        if Preguntas_Preguntas[i].__contains__('Retornar a la página inicial de Español'):
            Final = i

    Urls_Preguntas = Urls_Preguntas[7:Final]
    Preguntas_Preguntas = Preguntas_Preguntas[7:Final]

    Preguntas_envio = []
    for i in range(0, len(Preguntas_Preguntas)):
        Preguntas_envio.append(str(i + 1) + '. ' + Preguntas_Preguntas[i])

    Inicio = Texto.split('\n')
    Inicio = Inicio[len(Inicio)-1].split()[0]
    Inicio = int(Inicio.replace('.', ''))

    Preguntas_envio = Preguntas_envio[Inicio:]

    keyboard1 = []
    if len(Preguntas_envio) > 30:
        Preguntas_envio = Preguntas_envio[0:30]
        keyboard1.append([InlineKeyboardButton(text="Anterior", callback_data="preg_back"), InlineKeyboardButton(text="Siguiente", callback_data="preg_next")])
        keyboard1.append([InlineKeyboardButton(text="Volver al menú principal", callback_data="menu_principal_bot")])
    else:
        Preguntas_envio = Preguntas_envio[0:]
        keyboard1.append([InlineKeyboardButton(text="Anterior", callback_data="preg_back")])
        keyboard1.append([InlineKeyboardButton(text="Volver al menú principal", callback_data="menu_principal_bot")])

    reply_markupp = InlineKeyboardMarkup(keyboard1)

    Preguntas_opcion = '\n'.join(Preguntas_envio)

    query.edit_message_text(
        text=Preguntas + '\n' + '\n' + Preguntas_opcion,
        reply_markup=reply_markupp
    )

    return CONVERSACION_1

def preg_back (update, context):
    query = update.callback_query
    Texto = query.message.text
    bot = context.bot
    chatId = query.message.chat_id
    id_mensajito = query.message.message_id

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    url = 'https://www.gotquestions.org/Espanol/'
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls = []
    Preguntas = []
    for tag in soup.findAll('a', href=True):
        Urls.append(tag['href'])
        Preguntas.append(tag.getText())

    Urls = Urls[24:55]
    Preguntas = Preguntas[24:55]

    Buscar_Dato = str(chatId) + '_Temporal.csv'
    datos = pd.read_csv(Buscar_Dato, header=0)
    Tema_numero = datos.values.tolist()[0][3]

    Urls = Urls[Tema_numero - 1]
    Preguntas = Preguntas[Tema_numero - 1]

    url = 'https://www.gotquestions.org/Espanol/' + Urls
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls_Preguntas = []
    Preguntas_Preguntas = []
    for tag in soup.findAll('a', href=True):
        Urls_Preguntas.append(tag['href'])
        Preguntas_Preguntas.append(tag.getText())

    Urls_Preguntas = Urls_Preguntas[15:]
    Preguntas_Preguntas = Preguntas_Preguntas[15:]

    Final = ''
    for i in range(0, len(Preguntas_Preguntas)):
        if Preguntas_Preguntas[i].__contains__('Retornar a la página inicial de Español'):
            Final = i

    Urls_Preguntas = Urls_Preguntas[7:Final]
    Preguntas_Preguntas = Preguntas_Preguntas[7:Final]

    Preguntas_envio = []
    for i in range(0, len(Preguntas_Preguntas)):
        Preguntas_envio.append(str(i + 1) + '. ' + Preguntas_Preguntas[i])

    Inicio = Texto.split('\n')
    Inicio = Inicio[2].split()[0]
    Inicio = int(Inicio.replace('.', ''))

    #Preguntas_envio = Preguntas_envio[Inicio-30:]

    keyboard1 = []
    if Inicio == 31:
        Preguntas_envio = Preguntas_envio[0:30]
        keyboard1.append([InlineKeyboardButton(text="Siguiente", callback_data="preg_next")])
        keyboard1.append([InlineKeyboardButton(text="Volver al menú principal", callback_data="menu_principal_bot")])
    else:
        Preguntas_envio = Preguntas_envio[Inicio-31:Inicio-1]
        keyboard1.append([InlineKeyboardButton(text="Anterior", callback_data="preg_back"), InlineKeyboardButton(text="Siguiente", callback_data="preg_next")])
        keyboard1.append([InlineKeyboardButton(text="Volver al menú principal", callback_data="menu_principal_bot")])

    reply_markupp = InlineKeyboardMarkup(keyboard1)

    Preguntas_opcion = '\n'.join(Preguntas_envio)

    query.edit_message_text(
        text=Preguntas + '\n' + '\n' + Preguntas_opcion,
        reply_markup=reply_markupp
    )

    return CONVERSACION_1

def texto_dia (update, context):
    query = update.callback_query
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    html = requests.get('https://dailyverses.net/es/rvr60')
    content = html.content
    soup = b(content, "lxml")
    cita = soup.find("a", {"class":"vc"}).text
    texto = soup.find("span", {"class":"v1"}).text

    query.edit_message_text(
        text=cita + '\n' + texto,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Volver al menú principal", callback_data="menu_principal_bot")]
        ])
    )

def texto_diario (update, context):
    bot = context.bot
    chatId = update.message.chat_id
    id_mensajito = update.message.message_id

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    html = requests.get('https://dailyverses.net/es/rvr60')
    content = html.content
    soup = b(content, "lxml")
    cita = soup.find("a", {"class": "vc"}).text
    texto = soup.find("span", {"class": "v1"}).text

    bot.send_message(
        chat_id=chatId,
        text=cita + '\n' + '\n' + texto
    )

def texto_aleatorio (update, context):
    bot = context.bot
    chatId = update.message.chat_id
    id_mensajito = update.message.message_id

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    html = requests.get('https://dailyverses.net/es/versiculo-de-la-biblia-al-azar/rvr60')
    content = html.content
    soup = b(content, "lxml")
    cita = soup.find("a", {"class": "vc"}).text
    texto = soup.find("span", {"class": "v1"}).text

    bot.send_message(
        chat_id=chatId,
        text=cita + '\n' +  '\n' + texto,
    )

def texto_biblico (update, context):
    query = update.callback_query
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    html = requests.get('https://dailyverses.net/es/versiculo-de-la-biblia-al-azar/rvr60')
    content = html.content
    soup = b(content, "lxml")
    cita = soup.find("a", {"class":"vc"}).text
    texto = soup.find("span", {"class":"v1"}).text

    query.edit_message_text(
        text=cita + '\n' + texto,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Actualizar", callback_data="texto_biblico"), InlineKeyboardButton(text="Volver al menú principal", callback_data="menu_principal_bot")]
        ])
    )

def menu (update, context):
    bot=context.bot
    query = update.callback_query
    chatId = query.message.chat_id
    id_mensajito = query.message.message_id

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)
    bot.delete_message(chat_id=chatId, message_id=id_mensajito)

    bot.send_message(
        chat_id=chatId,
        text= "Toca los botones y sigue las instrucciones.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Biblia", callback_data="biblia_menu"), InlineKeyboardButton(text="Música Cristiana", callback_data="musica_cristiana")],
            [InlineKeyboardButton(text="YouTube", callback_data="youtube"), InlineKeyboardButton(text="Ayuda", url="https://telegra.ph/Proyect-B---Comandos-03-30")],
            [InlineKeyboardButton(text="Cerrar Dialogo", callback_data="cerrar_dialogo")]
        ])
    )

    return ConversationHandler.END

def biblia (update, context):
    query = update.callback_query
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    query.edit_message_text(
        text= "Elige una opcion.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Antiguo Testamento", callback_data="testamentoantiguo_menu"), InlineKeyboardButton(text="Nuevo Testamento", callback_data="testamento_nuevo_menu")],
            [InlineKeyboardButton(text="Menu principal", callback_data="menu_principal_bot")]
        ])
    )

def antiguo_testamento (update, context):
    query = update.callback_query
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    datos = pd.read_csv('Libros_Biblia.csv', header=0)
    libros = datos['LIBRO'].iloc[0:13]
    libros2 = datos['LIBRO'].iloc[13:26]
    libros3 = datos['LIBRO'].iloc[26:39]

    libri = []
    libri2 = []
    libri3 = []

    for i in libros:
        libri.append(i)

    for i in libros2:
        libri2.append(i)

    for i in libros3:
        libri3.append(i)

    Lista_general = {'LIBRO1': libri, 'LIBRO2': libri2, 'LIBRO3': libri3}
    df = pd.DataFrame(data=Lista_general)

    keyboard1 = []
    for i, i2, i3 in df.values:
        keyboard1.append([InlineKeyboardButton(text=i, callback_data="id_" + i), InlineKeyboardButton(text=i2, callback_data="id_" + i2), InlineKeyboardButton(text=i3, callback_data="id_" + i3)])


    keyboard1.append([InlineKeyboardButton(text="Regresar a Biblia", callback_data="menu_biblia"), InlineKeyboardButton(text="Menu Principal", callback_data="menu_principal_bot")])

    reply_markup = InlineKeyboardMarkup(keyboard1)

    query.edit_message_text(
        text= "El Antiguo Testamento fue escrito entre 1400 y 430 a.c., principalmente en hebreo.",
        reply_markup=reply_markup
    )

def id_Biblia (update, context):
    query = update.callback_query
    identificador_testamento = query.message.text
    bot=context.bot
    chatId = query.message.chat_id

    Falta_tilde = query.data[3:].lower().replace(' ','-')
    Libro_Biblico_buscado = query.data[3:]
    caracteres = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
    Sin_tilde = unicodedata.normalize('NFD', Falta_tilde).translate(caracteres)
    correcto = 'https://www.bibliaonlinerv1960.com/' + Sin_tilde + '/'

    res = requests.get(correcto)
    soup = BeautifulSoup(res.content, 'html.parser')
    chanDate = soup.find_all('tbody')

    for span in chanDate:
        texto = span.getText()

    Last = int(texto.split().pop())

    keyboard1 = []
    if Last > 99:
        for i in range(0, 75, 5):
            keyboard1.append([InlineKeyboardButton(text=str(i + 1), callback_data="ca_" + str(i + 1)), InlineKeyboardButton(text=str(i + 2), callback_data="ca_" + str(i + 2)), InlineKeyboardButton(text=str(i + 3), callback_data="ca_" + str(i + 3)), InlineKeyboardButton(text=str(i + 4), callback_data="ca_" + str(i + 4)),InlineKeyboardButton(text=str(i + 5), callback_data="ca_" + str(i + 5))])

        keyboard1.append([InlineKeyboardButton(text="Siguiente", callback_data="siguiente")])

    else:
        for i in range(0, Last, 5):
            keyboard1.append([InlineKeyboardButton(text=str(i+1), callback_data="ca_" + str(i+1)), InlineKeyboardButton(text=str(i+2), callback_data="ca_" + str(i+2)), InlineKeyboardButton(text=str(i+3), callback_data="ca_" + str(i+3)), InlineKeyboardButton(text=str(i+4), callback_data="ca_" + str(i+4)), InlineKeyboardButton(text=str(i+5), callback_data="ca_" + str(i+5))])

    if Last < 99:
        if len(keyboard1) * 5 > Last:
            inicio = Last + 1
            final = len(keyboard1) * 5
            ubicacion = len(keyboard1) - 1

            for i in range(inicio, final + 1):
                keyboard1[ubicacion].remove(InlineKeyboardButton(text=str(i), callback_data="ca_" + str(i)))

    filtro_testamento = identificador_testamento [3:4]

    if filtro_testamento == 'A':
        keyboard1.append([InlineKeyboardButton(text="Regresar a libros", callback_data="testamentoantiguo_menu"), InlineKeyboardButton(text="Regresar a biblia", callback_data="menu_biblia")])
        para_identificar = 'Antiguo Testamento'
    else:
        keyboard1.append([InlineKeyboardButton(text="Regresar a libros", callback_data="testamento_nuevo_menu"), InlineKeyboardButton(text="Regresar a biblia", callback_data="menu_biblia")])
        para_identificar = 'Nuevo Testamento'

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    reply_markupp = InlineKeyboardMarkup(keyboard1)
    query.edit_message_text(
        text=para_identificar + ' ' + Libro_Biblico_buscado,
        reply_markup=reply_markupp
    )

def siguiente (update, context):
    query = update.callback_query
    identificador_libro = query.message.text
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    keyboard1 = []
    for i in range(75, 150, 5):
        keyboard1.append([InlineKeyboardButton(text=str(i + 1), callback_data="ca_" + str(i + 1)), InlineKeyboardButton(text=str(i + 2), callback_data="ca_" + str(i + 2)), InlineKeyboardButton(text=str(i + 3), callback_data="ca_" + str(i + 3)), InlineKeyboardButton(text=str(i + 4), callback_data="ca_" + str(i + 4)), InlineKeyboardButton(text=str(i + 5), callback_data="ca_" + str(i + 5))])

    keyboard1.append([InlineKeyboardButton(text="Atras", callback_data="Atras")])

    keyboard1.append([InlineKeyboardButton(text="Regresar a libros", callback_data="testamentoantiguo_menu"), InlineKeyboardButton(text="Regresar a biblia", callback_data="menu_biblia")])

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    reply_markupp = InlineKeyboardMarkup(keyboard1)
    query.edit_message_text(
        text=identificador_libro,
        reply_markup=reply_markupp
    )

def Atras (update, context):
    query = update.callback_query
    identificador_libro = query.message.text
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    keyboard1 = []
    for i in range(0, 75, 5):
        keyboard1.append([InlineKeyboardButton(text=str(i + 1), callback_data="ca_" + str(i + 1)), InlineKeyboardButton(text=str(i + 2), callback_data="ca_" + str(i + 2)), InlineKeyboardButton(text=str(i + 3), callback_data="ca_" + str(i + 3)), InlineKeyboardButton(text=str(i + 4), callback_data="ca_" + str(i + 4)), InlineKeyboardButton(text=str(i + 5), callback_data="ca_" + str(i + 5))])

    keyboard1.append([InlineKeyboardButton(text="Siguiente", callback_data="siguiente")])

    keyboard1.append([InlineKeyboardButton(text="Regresar a libros", callback_data="testamentoantiguo_menu"), InlineKeyboardButton(text="Regresar a biblia", callback_data="menu_biblia")])

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    reply_markupp = InlineKeyboardMarkup(keyboard1)
    query.edit_message_text(
        text=identificador_libro,
        reply_markup=reply_markupp
    )

def nuevo_testamento (update, context):
    query = update.callback_query
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    datos = pd.read_csv('Libros_Biblia.csv', header=0)
    libros = datos['LIBRO'].iloc[39:48]
    libros2 = datos['LIBRO'].iloc[48:57]
    libros3 = datos['LIBRO'].iloc[57:66]

    libri = []
    libri2 = []
    libri3 = []

    for i in libros:
        libri.append(i)

    for i in libros2:
        libri2.append(i)

    for i in libros3:
        libri3.append(i)

    Lista_general = {'LIBRO1': libri, 'LIBRO2': libri2, 'LIBRO3': libri3}
    df = pd.DataFrame(data=Lista_general)

    keyboard1 = []
    for i, i2, i3 in df.values:
        keyboard1.append([InlineKeyboardButton(text=i, callback_data="id_" + i), InlineKeyboardButton(text=i2, callback_data="id_" + i2), InlineKeyboardButton(text=i3, callback_data="id_" + i3)])


    keyboard1.append([InlineKeyboardButton(text="Regresar a Biblia", callback_data="menu_biblia"), InlineKeyboardButton(text="Menu Principal", callback_data="menu_principal_bot")])

    reply_markup = InlineKeyboardMarkup(keyboard1)
    query.edit_message_text(
        text= "El Nuevo Testamento fue aproximadamente del año 45 al 95 d.c., fue escrito en el Griego Koiné.",
        reply_markup=reply_markup
    )

def id_capitulos (update, context):
    query = update.callback_query
    libro_a_buscar = query.message.text

    if libro_a_buscar.split()[0] == 'Antiguo':
        libro = libro_a_buscar[19:]
        Direc = 'AntiguoTestamento'
    else:
        libro = libro_a_buscar[17:]
        Direc = 'NuevoTestamento'

    bot=context.bot
    chatId = query.message.chat_id

    Falta_tilde = libro.replace(' ', '')
    capitulo_buscado = query.data[3:]
    caracteres = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
    Sin_tilde = unicodedata.normalize('NFD', Falta_tilde).translate(caracteres)
    correcto = 'http://www.encinardemamre.com//RV1960/' + Direc + '/' + Sin_tilde + '/' + Sin_tilde + capitulo_buscado + '.htm'

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    res = requests.get(correcto)
    soup = BeautifulSoup(res.content, 'html.parser')

    Envio = []
    for tag in soup.findAll('font'):
        Envio.append(tag.getText())

    Envio = '\n'.join(Envio)
    Envio = Envio.replace('\n', '')
    Envio = Envio.split(str(capitulo_buscado + ':'))
    Envio.pop(0)

    Cant = len(Envio)                   # Cantidad de versiculos

    Versiculos_Envio = []
    if Cant > 20:
        for i in range(0, 20):
            Versiculos_Envio.append(Envio[i])

    else:
        for i in range(0, len(Envio)):
            Versiculos_Envio.append(Envio[i])

    identificar_testamento = libro_a_buscar.split()[0]

    if identificar_testamento == 'Antiguo':
        back = 'testamentoantiguo_menu'
    else:
        back = 'testamento_nuevo_menu'

    keyboard1 = []
    if Cant > 20:
        Versiculos_texto = '\n' + '\n'.join(Versiculos_Envio)

        keyboard1.append([InlineKeyboardButton(text="Enviar Lectura", callback_data="compartir_ver"), InlineKeyboardButton(text="Lectura 🔉", callback_data="predicacion_voz"), InlineKeyboardButton(text="Versiculos ➡️", callback_data="versiculos_next")])
        keyboard1.append([InlineKeyboardButton(text="Volver a Capitulos", callback_data="regreso_capitulos"), InlineKeyboardButton(text="Volver a Libros", callback_data=back)])

    else:
        Versiculos_texto = '\n' + '\n'.join(Versiculos_Envio)
        keyboard1.append([InlineKeyboardButton(text="Enviar Lectura", callback_data="compartir_ver"), InlineKeyboardButton(text="Lectura 🔉", callback_data="predicacion_voz")])
        keyboard1.append([InlineKeyboardButton(text="Volver a Capitulos", callback_data="regreso_capitulos"), InlineKeyboardButton(text="Volver a Libros", callback_data=back)])

    reply_markup = InlineKeyboardMarkup(keyboard1)

    query.edit_message_text(
        parse_mode="HTML",
        text = libro_a_buscar + ' Capitulo ' + ' ' + capitulo_buscado + ' ' + '\n' + Versiculos_texto,
        reply_markup = reply_markup
    )

def versiculos_next (update, context):
    query = update.callback_query
    bot=context.bot
    chatId = query.message.chat_id
    libro_a_buscar = query.message.text
    versiculo_siguiente = int(libro_a_buscar.split('\n').pop().split(' ')[0])

    if libro_a_buscar.split()[0] == 'Antiguo':
        Direc = 'AntiguoTestamento'
    else:
        Direc = 'NuevoTestamento'

    if len(libro_a_buscar.split()[2]) == 1:
        libro = libro_a_buscar.split()[0] + ' ' + libro_a_buscar.split()[1] + ' ' + libro_a_buscar.split()[2] + ' ' + libro_a_buscar.split()[3] + ' ' + libro_a_buscar.split()[4] + ' ' + libro_a_buscar.split()[5]
        Tilde = libro_a_buscar.split()[2] + libro_a_buscar.split()[3]
        Capit = libro_a_buscar.split()[5]

    else:
        libro = libro_a_buscar.split()[0] + ' ' + libro_a_buscar.split()[1] + ' ' + libro_a_buscar.split()[2] + ' ' + libro_a_buscar.split()[3] + ' ' + libro_a_buscar.split()[4]
        Tilde = libro_a_buscar.split()[2]
        Capit = libro_a_buscar.split()[4]

    Falta_tilde = Tilde.replace(' ', '')
    capitulo_buscado = Capit
    caracteres = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
    Sin_tilde = unicodedata.normalize('NFD', Falta_tilde).translate(caracteres)
    correcto = 'http://www.encinardemamre.com//RV1960/' + Direc + '/' + Sin_tilde + '/' + Sin_tilde + capitulo_buscado + '.htm'

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    res = requests.get(correcto)
    soup = BeautifulSoup(res.content, 'html.parser')

    Envio = []
    for tag in soup.findAll('font'):
        Envio.append(tag.getText())

    Envio = '\n'.join(Envio)
    Envio = Envio.replace('\n', '')
    Envio = Envio.split(str(capitulo_buscado + ':'))
    Envio.pop(0)

    Envio = Envio[versiculo_siguiente:]     #Envio listo
    Cant = len(Envio)                       #Cantidad de versiculos

    Versiculos_Envio = []
    if Cant > 20:
        for i in range(0, 20):
            Versiculos_Envio.append(Envio[i])

    else:
        for i in range(0, len(Envio)):
            Versiculos_Envio.append(Envio[i])

    identificar_testamento = libro_a_buscar.split()[0]

    if identificar_testamento == 'Antiguo':
        back = 'testamentoantiguo_menu'
    else:
        back = 'testamento_nuevo_menu'

    keyboard1 = []
    if Cant > 20:
        keyboard1.append([InlineKeyboardButton(text="⬅️ Versiculos", callback_data="versiculos_back"), InlineKeyboardButton(text="Enviar Lectura", callback_data="compartir_ver"), InlineKeyboardButton(text="Versiculos ➡️", callback_data="versiculos_next")])
        keyboard1.append([InlineKeyboardButton(text="Volver a Capitulos", callback_data="regreso_capitulos"), InlineKeyboardButton(text="Lectura 🔉", callback_data="predicacion_voz"), InlineKeyboardButton(text="Volver a Libros", callback_data=back)])
        Versiculos_texto = '\n' + '\n'.join(Versiculos_Envio)
    else:
        keyboard1.append([InlineKeyboardButton(text="⬅️ Versiculos", callback_data="versiculos_back"), InlineKeyboardButton(text="Enviar Lectura", callback_data="compartir_ver")])
        keyboard1.append([InlineKeyboardButton(text="Volver a Capitulos", callback_data="regreso_capitulos"), InlineKeyboardButton(text="Lectura 🔉", callback_data="predicacion_voz"), InlineKeyboardButton(text="Volver a Libros", callback_data=back)])
        Versiculos_texto = '\n' + '\n'.join(Versiculos_Envio)

    reply_markup = InlineKeyboardMarkup(keyboard1)

    query.edit_message_text(
        parse_mode="HTML",
        text = libro + '\n' + Versiculos_texto,
        reply_markup = reply_markup
    )

def versiculos_back (update, context):
    query = update.callback_query
    bot=context.bot
    chatId = query.message.chat_id
    libro_a_buscar = query.message.text
    Ultimo_Versiculo = int(libro_a_buscar.split('\n')[2].split(' ')[0]) - 1 #Versiculo hasta donde llegar -1

    if libro_a_buscar.split()[0] == 'Antiguo':
        Direc = 'AntiguoTestamento'
    else:
        Direc = 'NuevoTestamento'

    if len(libro_a_buscar.split()[2]) == 1:
        libro = libro_a_buscar.split()[0] + ' ' + libro_a_buscar.split()[1] + ' ' + libro_a_buscar.split()[2] + ' ' + libro_a_buscar.split()[3] + ' ' + libro_a_buscar.split()[4] + ' ' + libro_a_buscar.split()[5]
        Tilde = libro_a_buscar.split()[2] + libro_a_buscar.split()[3]
        Capit = libro_a_buscar.split()[5]

    else:
        libro = libro_a_buscar.split()[0] + ' ' + libro_a_buscar.split()[1] + ' ' + libro_a_buscar.split()[2] + ' ' + libro_a_buscar.split()[3] + ' ' + libro_a_buscar.split()[4]
        Tilde = libro_a_buscar.split()[2]
        Capit = libro_a_buscar.split()[4]

    Falta_tilde = Tilde.replace(' ', '')
    capitulo_buscado = Capit
    caracteres = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
    Sin_tilde = unicodedata.normalize('NFD', Falta_tilde).translate(caracteres)
    correcto = 'http://www.encinardemamre.com//RV1960/' + Direc + '/' + Sin_tilde + '/' + Sin_tilde + capitulo_buscado + '.htm'

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    res = requests.get(correcto)
    soup = BeautifulSoup(res.content, 'html.parser')

    Envio = []
    for tag in soup.findAll('font'):
        Envio.append(tag.getText())

    Envio = '\n'.join(Envio)
    Envio = Envio.replace('\n', '')
    Envio = Envio.split(str(capitulo_buscado + ':'))
    Envio.pop(0)

    Envio = Envio[Ultimo_Versiculo - 20:Ultimo_Versiculo]       #Envio listo
    Cant = len(Envio)                                           #Cantidad de versiculos

    Versiculos_Envio = []
    if Cant > 20:
        for i in range(0, 20):
            Versiculos_Envio.append(Envio[i])

    else:
        for i in range(0, len(Envio)):
            Versiculos_Envio.append(Envio[i])

    identificar_testamento = libro_a_buscar.split()[0]

    if identificar_testamento == 'Antiguo':
        back = 'testamentoantiguo_menu'
    else:
        back = 'testamento_nuevo_menu'

    keyboard1 = []
    if Ultimo_Versiculo - 20 > 0 :
        keyboard1.append([InlineKeyboardButton(text="⬅️ Versiculos", callback_data="versiculos_back"), InlineKeyboardButton(text="Enviar Lectura", callback_data="compartir_ver"), InlineKeyboardButton(text="Versiculos ➡️", callback_data="versiculos_next")])
        keyboard1.append([InlineKeyboardButton(text="Volver a Capitulos", callback_data="regreso_capitulos"), InlineKeyboardButton(text="Lectura 🔉", callback_data="predicacion_voz"), InlineKeyboardButton(text="Volver a Libros", callback_data=back)])
        Versiculos_texto = '\n' + '\n'.join(Versiculos_Envio)
    else:
        keyboard1.append([InlineKeyboardButton(text="Enviar Lectura", callback_data="compartir_ver"), InlineKeyboardButton(text="Versiculos ➡️", callback_data="versiculos_next")])
        keyboard1.append([InlineKeyboardButton(text="Volver a Capitulos", callback_data="regreso_capitulos"), InlineKeyboardButton(text="Lectura 🔉", callback_data="predicacion_voz"), InlineKeyboardButton(text="Volver a Libros", callback_data=back)])
        Versiculos_texto = '\n' + '\n'.join(Versiculos_Envio)

    reply_markup = InlineKeyboardMarkup(keyboard1)

    query.edit_message_text(
        parse_mode="HTML",
        text = libro + '\n' + Versiculos_texto,
        reply_markup = reply_markup
    )

def regreso_capitulos (update, context):
    query = update.callback_query
    identificador_testamento = query.message.text

    if len(identificador_testamento.split()[2]) == 1:
        libro = identificador_testamento.split()[2] + ' ' + identificador_testamento.split()[3]
    else:
        libro = identificador_testamento.split()[2]

    bot=context.bot
    chatId = query.message.chat_id

    Falta_tilde = libro.lower().replace(' ', '-')
    caracteres = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
    Sin_tilde = unicodedata.normalize('NFD', Falta_tilde).translate(caracteres)
    correcto = 'https://www.bibliaonlinerv1960.com/' + Sin_tilde + '/'

    res = requests.get(correcto)
    soup = BeautifulSoup(res.content, 'html.parser')
    chanDate = soup.find_all('tbody')

    for span in chanDate:
        texto = span.getText()

    Last = int(texto.split().pop())

    keyboard1 = []
    if Last > 99:
        for i in range(0, 75, 5):
            keyboard1.append([InlineKeyboardButton(text=str(i + 1), callback_data="ca_" + str(i + 1)), InlineKeyboardButton(text=str(i + 2), callback_data="ca_" + str(i + 2)), InlineKeyboardButton(text=str(i + 3), callback_data="ca_" + str(i + 3)), InlineKeyboardButton(text=str(i + 4), callback_data="ca_" + str(i + 4)),InlineKeyboardButton(text=str(i + 5), callback_data="ca_" + str(i + 5))])

        keyboard1.append([InlineKeyboardButton(text="Siguiente", callback_data="siguiente")])

    else:
        for i in range(0, Last, 5):
            keyboard1.append([InlineKeyboardButton(text=str(i+1), callback_data="ca_" + str(i+1)), InlineKeyboardButton(text=str(i+2), callback_data="ca_" + str(i+2)), InlineKeyboardButton(text=str(i+3), callback_data="ca_" + str(i+3)), InlineKeyboardButton(text=str(i+4), callback_data="ca_" + str(i+4)), InlineKeyboardButton(text=str(i+5), callback_data="ca_" + str(i+5))])

    if Last < 99:
        if len(keyboard1) * 5 > Last:
            inicio = Last + 1
            final = len(keyboard1) * 5
            ubicacion = len(keyboard1) - 1

            for i in range(inicio, final + 1):
                keyboard1[ubicacion].remove(InlineKeyboardButton(text=str(i), callback_data="ca_" + str(i)))

    filtro_testamento = identificador_testamento.split()[0]

    if filtro_testamento == 'Antiguo':
        keyboard1.append([InlineKeyboardButton(text="Regresar a libros", callback_data="testamentoantiguo_menu"), InlineKeyboardButton(text="Regresar a biblia", callback_data="menu_biblia")])
        para_identificar = 'Antiguo Testamento'
    else:
        keyboard1.append([InlineKeyboardButton(text="Regresar a libros", callback_data="testamento_nuevo_menu"), InlineKeyboardButton(text="Regresar a biblia", callback_data="menu_biblia")])
        para_identificar = 'Nuevo Testamento'

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    reply_markupp = InlineKeyboardMarkup(keyboard1)
    query.edit_message_text(
        text=para_identificar + ' ' + libro,
        reply_markup=reply_markupp
    )

def predicacion (update, context):
    query = update.callback_query
    botones = query.message.reply_markup.inline_keyboard
    libro_a_buscar = query.message.text
    bot=context.bot
    chatId = query.message.chat_id
    id_mensajito = query.message.message_id

    Texto = libro_a_buscar.split('\n')[0]
    caracteres = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
    Sin_tilde = unicodedata.normalize('NFD', Texto).translate(caracteres)

    if Texto.split()[0] == 'Antiguo':
        Libro_Buscado = Texto[19:].replace(' Capitulo ',' ').split()
        Capitulo = Libro_Buscado.pop()
        Tipo = 'antiguo-testamento'
    else:
        Libro_Buscado = Texto[17:].replace(' Capitulo ',' ').split()
        Capitulo = Libro_Buscado.pop()
        Tipo = 'nuevo-testamento'

    Libro_Buscado = ' '.join(Libro_Buscado)
    caracteres = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
    Libro_Buscado = unicodedata.normalize('NFD', Libro_Buscado).translate(caracteres)

    Correcto = 'https://www.bibliaonlinerv1960.com/' + Tipo + '/'
    res = requests.get(Correcto)
    soup = BeautifulSoup(res.content, 'html.parser')
    chanDate = soup.find_all('td')

    Ubicacion = []
    Libro = []

    for tag in soup.findAll('a', href=True):
        Libro.append(tag.getText())

    for tag in soup.findAll('tr'):
        Ubicacion.append(tag.getText())

    Ubicacion = '\n'.join(Ubicacion).split()

    Libro = Libro[5:]

    if Tipo == 'antiguo-testamento':
        Libro_Biblia = Libro.index(Libro_Buscado) + 1

    else:
        if Libro_Buscado == '2 Pedro':
            Libro_Buscado = ' 2 Pedro'

        Libro_Biblia = Libro.index(Libro_Buscado) + 40

    Predica = 'http://www.lmontt.com/biblia/RVR1960/' + str(Libro_Biblia) + '-' + str(Capitulo) + '.mp3'

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)

    bot.send_audio(
        chat_id=chatId,
        audio=Predica,
        disable_notification=True
    )

    reply_markup_bo = InlineKeyboardMarkup(botones)

    bot.send_message(
        chat_id=chatId,
        text=libro_a_buscar,
        disable_web_page_preview=True,
        reply_markup=reply_markup_bo
    )

def compartir_ver (update, context):
    query = update.callback_query
    botones = query.message.reply_markup.inline_keyboard
    texto_enviar = query.message.text
    bot=context.bot
    chatId = query.message.chat_id
    id_mensajito = query.message.message_id

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)

    bot.send_message(
        chat_id=chatId,
        text=texto_enviar)

    reply_markup_bo = InlineKeyboardMarkup(botones)

    bot.send_message(
        chat_id=chatId,
        text=texto_enviar,
        disable_web_page_preview=True,
        reply_markup=reply_markup_bo
    )

def process_message (update, context):
    bot = context.bot
    chatId = update.message.chat_id
    id_mensajito = update.message.message_id
    text = update.message.text
    text_min = text.lower()
    caracteres = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
    Sin_tilde = unicodedata.normalize('NFD', text).translate(caracteres)
    Sin_tilde_deter = Sin_tilde.lower()
    datos = Sin_tilde_deter.split('\n')

    if Sin_tilde_deter.__contains__('cita biblica'):

        Ubicacion_cita = ''
        ubicadito = ''
        for i in range(0, len(datos), 1):
            if datos[i].__contains__('cita biblica'):
                Ubicacion_cita = Sin_tilde.split('\n')[i]
                ubicadito = i
                break

        enviar_cita = text.split('\n')[ubicadito]
        separar = ''
        if len(Ubicacion_cita.split()[2]) == 1:
            separar = Ubicacion_cita.split()[4]
            separar = separar.split(':')
        else:
            separar = Ubicacion_cita.split()[3]
            separar = separar.split(':')

        capitulo_buscado = separar[0]

        if separar[1].__contains__('-'):
            separar_versiculos = separar[1].split('-')
            ver_ini = separar_versiculos[0]
            ver_fin = separar_versiculos[1]
        else:
            ver_ini = separar[1]
            ver_fin = ver_ini

        if len(Ubicacion_cita.split()[2]) == 1:
            Libro_Tilde = Ubicacion_cita.split()[2] + Ubicacion_cita.split()[3]

        else:
            Libro_Tilde = Ubicacion_cita.split()[2]

        #Se determina si es antiguo o nuevo text
        Falta_tilde = Libro_Tilde.replace(' ', '')
        Correcto = 'http://www.encinardemamre.com//RV1960/AntiguoTestamento/'
        res = requests.get(Correcto)
        soup = BeautifulSoup(res.content, 'html.parser')

        Antiguo_Test = []
        for tag in soup.findAll('a'):
            Antiguo_Test.append(tag.getText().replace('/', ''))

        Antiguo_Test = Antiguo_Test[5:]

        try:
            Posicion = Antiguo_Test.index(Falta_tilde)
            Direc = 'AntiguoTestamento'
        except:
            Direc = 'NuevoTestamento'

        Correcto = 'http://www.encinardemamre.com//RV1960/' + Direc + '/' + Falta_tilde + '/' + Falta_tilde + capitulo_buscado + '.htm'
        res = requests.get(Correcto)
        soup = BeautifulSoup(res.content, 'html.parser')
        chanDate = soup.find_all('td')

        Envio = []
        for tag in soup.findAll('font'):
            Envio.append(tag.getText())

        Envio = '\n'.join(Envio)
        Envio = Envio.replace('\n', '')
        Envio = Envio.split(str(capitulo_buscado + ':'))
        Envio.pop(0)

        Envio_Ver = []
        for i in range(int(ver_ini)-1, int(ver_fin), 1):
            Envio_Ver.append(Envio[i])

        if len(datos) == 1:
            bot.delete_message(chat_id=chatId, message_id=id_mensajito)

        Versiculos_texto = '\n' + '\n'.join(Envio_Ver)

        bot.send_message(
            chat_id=chatId,
            text=enviar_cita + '\n' + Versiculos_texto)


    if text_min.__contains__('boxy'):
        datos = text.split('\n')
        Texto_envio = datos[1:]

        bot.delete_message(chat_id=chatId, message_id=id_mensajito)

        Enviar_texto = '\n'.join(Texto_envio)

        bot.send_message(
            chat_id=chatId,
            disable_notification=True,
            text=Enviar_texto)


    if text_min.__contains__('crear encuesta'):
        datos = text.split('\n')

        opciones = []
        for i in range(0, len(datos[2].split(',')), 1):
            opciones.append(datos[2].split(',')[i].replace(',', ''))

        pregunta = datos[1]
        correcto = int(datos[3])
        respuesta = datos[4]

        bot.delete_message(chat_id=chatId, message_id=id_mensajito)

        bot.send_poll(
            chat_id=chatId,
            question=pregunta,
            options=opciones,
            is_anonymous=False,
            type='quiz',
            correct_option_id=correcto,
            explanation=respuesta
        )

        bot.pin_chat_message(
            chat_id=chatId,
            message_id=id_mensajito + 1,
            disable_notification=True)

def ayuda (update, context):
    bot = context.bot
    chatId = update.message.chat_id
    id_mensajito = update.message.message_id
    username = update.effective_user["first_name"]

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    bot.send_message(
        chat_id=chatId,
        text= 'Hola ' + username + ' este bot puede realizar solicitudes a pedido del usuario por ejemplo:' + '\n'
        + '/start al enviar esta palabra el bot respondera con botones los cuales realizan una serie de tareas.' + '\n'
        + 'o tambien puedes escribir directamente "Cita Bíblica Génesis 1:1-2"',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Menu principal", callback_data="menu_principal_bot"), InlineKeyboardButton(text="Cerrar Dialogo", callback_data="cerrar_dialogo")]
        ])
    )

def youtube (update, context):
    query = update.callback_query
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    query.edit_message_text(
        text= "Elije una opción para descargar.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Video", callback_data="video"), InlineKeyboardButton(text="Audio", callback_data="audio")],
            [InlineKeyboardButton(text="Menu principal", callback_data="menu_principal_bot")]
            ])
        )

def musica_cristiana (update, context):
    query = update.callback_query
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    url = 'https://mismp3cristianos.com/'
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls = []
    Artistas = []
    for tag in soup.findAll('a', href=True):
        Urls.append(tag['href'])
        Artistas.append(tag.getText())

    for i in range(2, -1, -1):
        Urls.pop(i)
        Artistas.pop(i)

    for i in range(156, 163, -1):
        Urls.pop(i)
        Artistas.pop(i)

    keyboard1 = []
    for i in range(0, 50, 2):
        keyboard1.append([InlineKeyboardButton(text=Artistas[i], callback_data='AR_' + str(i)), InlineKeyboardButton(text=Artistas[i+1], callback_data='AR_' + str(i+1))])

    keyboard1.append([InlineKeyboardButton(text="Menu Principal", callback_data="menu_principal_bot"), InlineKeyboardButton(text="Siguiente ➡️", callback_data="artistas_next")])

    reply_markup = InlineKeyboardMarkup(keyboard1)

    query.edit_message_text(
        text="Seleccione su artista favorito / Lista 1 - 3",
        reply_markup=reply_markup
    )

def artistas_next (update, context):
    query = update.callback_query
    Siguiente = query.message.text
    numero = int(Siguiente.split()[6])
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    url = 'https://mismp3cristianos.com/'
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls = []
    Artistas = []
    for tag in soup.findAll('a', href=True):
        Urls.append(tag['href'])
        Artistas.append(tag.getText())

    for i in range(2, -1, -1):
        Urls.pop(i)
        Artistas.pop(i)

    for i in range(156, 163, -1):
        Urls.pop(i)
        Artistas.pop(i)


    keyboard1 = []
    Numero_Lista = numero

    if numero == 1:
        Numero_Lista = numero + 1

        for i in range(50, 101, 2):
            keyboard1.append([InlineKeyboardButton(text=Artistas[i], callback_data='AR_' + str(i)), InlineKeyboardButton(text=Artistas[i + 1], callback_data='AR_' + str(i + 1))])

        keyboard1.append([InlineKeyboardButton(text="⬅️ Atras", callback_data="artistas_back"), InlineKeyboardButton(text="Siguiente ➡️", callback_data="artistas_next")])
        keyboard1.append([InlineKeyboardButton(text="Menu Principal", callback_data="menu_principal_bot")])

    if numero == 2:
        Numero_Lista = numero + 1

        for i in range(102, 155, 2):
            keyboard1.append([InlineKeyboardButton(text=Artistas[i], callback_data='AR_' + str(i)), InlineKeyboardButton(text=Artistas[i + 1], callback_data='AR_' + str(i + 1))])

        keyboard1.append([InlineKeyboardButton(text=Artistas[156], callback_data='AR_' + str(156))])
        keyboard1.append([InlineKeyboardButton(text="Menu Principal", callback_data="menu_principal_bot"), InlineKeyboardButton(text="⬅️ Atras", callback_data="artistas_back")])

    reply_markup = InlineKeyboardMarkup(keyboard1)

    query.edit_message_text(
        text='Seleccione su artista favorito / Lista ' + str(Numero_Lista) + ' - 3',
        reply_markup=reply_markup
    )

def artistas_back (update, context):
    query = update.callback_query
    Siguiente = query.message.text
    numero = int(Siguiente.split()[6])
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    url = 'https://mismp3cristianos.com/'
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls = []
    Artistas = []
    for tag in soup.findAll('a', href=True):
        Urls.append(tag['href'])
        Artistas.append(tag.getText())

    for i in range(2, -1, -1):
        Urls.pop(i)
        Artistas.pop(i)

    for i in range(156, 163, -1):
        Urls.pop(i)
        Artistas.pop(i)


    keyboard1 = []
    Numero_Lista = numero

    if numero == 3:
        Numero_Lista = numero - 1

        for i in range(50, 101, 2):
            keyboard1.append([InlineKeyboardButton(text=Artistas[i], callback_data='AR_' + str(i)), InlineKeyboardButton(text=Artistas[i + 1], callback_data='AR_' + str(i + 1))])

        keyboard1.append([InlineKeyboardButton(text="⬅️ Atras", callback_data="artistas_back"), InlineKeyboardButton(text="Siguiente ➡️", callback_data="artistas_next")])
        keyboard1.append([InlineKeyboardButton(text="Menu Principal", callback_data="menu_principal_bot")])

    if numero == 2:
        Numero_Lista = numero - 1

        for i in range(0, 50, 2):
            keyboard1.append([InlineKeyboardButton(text=Artistas[i], callback_data='AR_' + str(i)), InlineKeyboardButton(text=Artistas[i + 1], callback_data='AR_' + str(i + 1))])

        keyboard1.append([InlineKeyboardButton(text="Menu Principal", callback_data="menu_principal_bot"), InlineKeyboardButton(text="Siguiente ➡️", callback_data="artistas_next")])

    reply_markup = InlineKeyboardMarkup(keyboard1)

    query.edit_message_text(
        text='Seleccione su artista favorito / Lista ' + str(Numero_Lista) + ' - 3',
        reply_markup=reply_markup
    )

def musica_art (update, context):
    query = update.callback_query
    bot=context.bot
    chatId = query.message.chat_id
    artista = query.data[3:]
    Identificar = query.message.chat.type

    url = 'https://mismp3cristianos.com/'
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls = []
    Artistas = []
    for tag in soup.findAll('a', href=True):
        Urls.append(tag['href'])
        Artistas.append(tag.getText())

    for i in range(2, -1, -1):
        Urls.pop(i)
        Artistas.pop(i)

    for i in range(156, 163, -1):
        Urls.pop(i)
        Artistas.pop(i)

    query.edit_message_text(
        text='Se esta generando la lista de canciones espere por favor...')

    artista_buscado = Artistas[int(artista)]

    url = Urls[int(artista)]
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls_Canciones = []
    Nombre_Canciones = []
    for tag in soup.findAll('a', href=True):
        Urls_Canciones.append(tag['href'])
        Nombre_Canciones.append(tag.getText())

    if Nombre_Canciones[4] == 'Tuitear':
        for i in range(4, -1, -1):
            Urls_Canciones.pop(i)
            Nombre_Canciones.pop(i)
    else:
        for i in range(2, -1, -1):
            Urls_Canciones.pop(i)
            Nombre_Canciones.pop(i)

    lista_sin_caracteres = [re.sub('[^\w\s]', '', string).strip() for string in Nombre_Canciones]
    Nombre_Canciones = [string for string in lista_sin_caracteres if string]

    Fin = 0
    for i in range(0, len(Nombre_Canciones), 1):
        if Nombre_Canciones[i].__contains__('mp3') == True:
            Fin = i
            break

    # Urls_cortitas = []
    # for i in range(0, Fin, 1):
    #   s = pyshorteners.Shortener()
    #  Urls_cortitas.append(s.dagd.short(Urls_Canciones[i]))

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    keyboard1 = []
    Envio_canciones_cortas_url = []
    if Fin > 10:
        keyboard1.append([InlineKeyboardButton(text=f"Más de {artista_buscado}", callback_data=f"list_music_next_{artista_buscado}")])
        keyboard1.append([InlineKeyboardButton(text="Reproducir 🎧", callback_data="reproducir_music")])

        for i in range(0, 10, 1):
            Envio_canciones_cortas_url.append(f'[{str(i + 1)}. {Nombre_Canciones[i]}]({Urls_Canciones[i]})')
    else:
        keyboard1.append([InlineKeyboardButton(text="Reproducir 🎧", callback_data="reproducir_music")])

        for i in range(0, Fin):
            Envio_canciones_cortas_url.append(f'[{str(i + 1)}. {Nombre_Canciones[i]}]({Urls_Canciones[i]})')

    if Identificar == 'private':
        keyboard1.append([InlineKeyboardButton(text="👤", callback_data="musica_cristiana"), InlineKeyboardButton(text="🗃", callback_data="menu_principal_bot")])
    else:
        pass

    reply_markupp = InlineKeyboardMarkup(keyboard1)

    Canciones_descargar = '\n'.join(Envio_canciones_cortas_url)

    query.edit_message_text(
        text=artista_buscado + '\n' + '\n' + Canciones_descargar,
        parse_mode=ParseMode.MARKDOWN,
        # disable_web_page_preview=True,
        reply_markup=reply_markupp
    )

def list_music_next (update, context):
    query = update.callback_query
    bot = context.bot
    Texto = query.message.text.split('\n')
    chatId = query.message.chat_id
    artista = query.data[16:]
    Identificar = query.message.chat.type

    Total = len(Texto)-1
    Numero_next = Texto[int(Total)].split()[0].replace('.', '')

    url = 'https://mismp3cristianos.com/'
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls = []
    Artistas = []
    for tag in soup.findAll('a', href=True):
        Urls.append(tag['href'])
        Artistas.append(tag.getText())

    for i in range(2, -1, -1):
        Urls.pop(i)
        Artistas.pop(i)

    for i in range(156, 163, -1):
        Urls.pop(i)
        Artistas.pop(i)

    query.edit_message_text(
        text='Se esta generando la lista de canciones espere por favor...')

    artista_id = ''
    for i in range(0, len(Artistas), 1):
        if Artistas[i] == artista:
            artista_id = i
            break

    url = Urls[int(artista_id)]
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls_Canciones = []
    Nombre_Canciones = []
    for tag in soup.findAll('a', href=True):
        Urls_Canciones.append(tag['href'])
        Nombre_Canciones.append(tag.getText())

    if Nombre_Canciones[4] == 'Tuitear':
        for i in range(4, -1, -1):
            Urls_Canciones.pop(i)
            Nombre_Canciones.pop(i)
    else:
        for i in range(2, -1, -1):
            Urls_Canciones.pop(i)
            Nombre_Canciones.pop(i)

    lista_sin_caracteres = [re.sub('[^\w\s]', '', string).strip() for string in Nombre_Canciones]
    Nombre_Canciones = [string for string in lista_sin_caracteres if string]

    Fin = 0
    for i in range(0, len(Nombre_Canciones), 1):
        if Nombre_Canciones[i].startswith(("musica", 'Musica', 'música', 'Música')) == True:
        #if Nombre_Canciones[i].__contains__('mp3') == True:
            Fin = i
            break

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    #Urls_cortitas = []
    #for i in range(0, Fin, 1):
     #   s = pyshorteners.Shortener()
      #  Urls_cortitas.append(s.dagd.short(Urls_Canciones[i]))

    keyboard1 = []
    Envio_canciones_cortas_url = []
    if Fin - int(Numero_next) > 10:
        keyboard1.append([InlineKeyboardButton(text="🔙", callback_data=f"list_music_back_{artista}"),
                          InlineKeyboardButton(text="🎧", callback_data="reproducir_music"),
                          InlineKeyboardButton(text="🔜", callback_data=f"list_music_next_{artista}")])

        for i in range(int(Numero_next), int(Numero_next) + 10, 1):
            Envio_canciones_cortas_url.append(f'[{str(i + 1)}. {Nombre_Canciones[i]}]({Urls_Canciones[i]})')
    else:
        keyboard1.append([InlineKeyboardButton(text="Anterior", callback_data=f"list_music_back_{artista}")])
        keyboard1.append([InlineKeyboardButton(text="Reproducir 🎧", callback_data="reproducir_music")])

        for i in range(int(Numero_next), Fin, 1):
            Envio_canciones_cortas_url.append(f'[{str(i + 1)}. {Nombre_Canciones[i]}]({Urls_Canciones[i]})')

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    if Identificar == 'private':
        keyboard1.append([InlineKeyboardButton(text="👤", callback_data="musica_cristiana"), InlineKeyboardButton(text="🗃", callback_data="menu_principal_bot")])
    else:
        pass

    reply_markupp = InlineKeyboardMarkup(keyboard1)

    Canciones_descargar = '\n'.join(Envio_canciones_cortas_url)

    query.edit_message_text(
        text=artista + '\n' + '\n' + Canciones_descargar,
        parse_mode=ParseMode.MARKDOWN,
        # disable_web_page_preview=True,
        reply_markup=reply_markupp
    )

def list_music_back (update, context):
    query = update.callback_query
    bot = context.bot
    Texto = query.message.text.split('\n')
    chatId = query.message.chat_id
    artista = query.data[16:]
    Identificar = query.message.chat.type

    Total = len(Texto) - 1
    Numero_back = Texto[int(Total)].split()[0].replace('.', '')

    Numero_next = Texto[2].split()[0].replace('.', '')
    Numero_next = int(Numero_next)

    url = 'https://mismp3cristianos.com/'
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls = []
    Artistas = []
    for tag in soup.findAll('a', href=True):
        Urls.append(tag['href'])
        Artistas.append(tag.getText())

    for i in range(2, -1, -1):
        Urls.pop(i)
        Artistas.pop(i)

    query.edit_message_text(
        text='Se esta generando la lista de canciones espere por favor...')

    for i in range(156, 163, -1):
        Urls.pop(i)
        Artistas.pop(i)

    artista_id = ''
    for i in range(0, len(Artistas), 1):
        if Artistas[i] == artista:
            artista_id = i
            break

    url = Urls[int(artista_id)]
    html = requests.get(url)
    content = html.content
    soup = b(content, 'lxml')

    Urls_Canciones = []
    Nombre_Canciones = []
    for tag in soup.findAll('a', href=True):
        Urls_Canciones.append(tag['href'])
        Nombre_Canciones.append(tag.getText())

    if Nombre_Canciones[4] == 'Tuitear':
        for i in range(4, -1, -1):
            Urls_Canciones.pop(i)
            Nombre_Canciones.pop(i)
    else:
        for i in range(2, -1, -1):
            Urls_Canciones.pop(i)
            Nombre_Canciones.pop(i)

    lista_sin_caracteres = [re.sub('[^\w\s]', '', string).strip() for string in Nombre_Canciones]
    Nombre_Canciones = [string for string in lista_sin_caracteres if string]

    Fin = 0
    for i in range(0, len(Nombre_Canciones), 1):
        if Nombre_Canciones[i].startswith(("musica", 'Musica', 'música', 'Música')) == True:
        #if Nombre_Canciones[i].__contains__('mp3') == True:
            Fin = i
            break

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=20)

    #Urls_cortitas = []
    #for i in range(0, Fin, 1):
     #   s = pyshorteners.Shortener()
      #  Urls_cortitas.append(s.dagd.short(Urls_Canciones[i]))

    keyboard1 = []
    Envio_canciones_cortas_url = []
    if int(Numero_next) - 10 > 10:
        keyboard1.append([InlineKeyboardButton(text="🔙", callback_data=f"list_music_back_{artista}"),
                          InlineKeyboardButton(text="🎧", callback_data="reproducir_music"),
                          InlineKeyboardButton(text="🔜", callback_data=f"list_music_next_{artista}")])

        for i in range(int(Numero_next) - 11, int(Numero_next) - 1, 1):
            Envio_canciones_cortas_url.append(f'[{str(i + 1)}. {Nombre_Canciones[i]}]({Urls_Canciones[i]})')
    else:
        keyboard1.append([InlineKeyboardButton(text=f"Más de {artista}", callback_data=f"list_music_next_{artista}")])
        keyboard1.append([InlineKeyboardButton(text="Reproducir 🎧", callback_data="reproducir_music")])

        for i in range(0, int(Numero_next) - 1, 1):
            Envio_canciones_cortas_url.append(f'[{str(i + 1)}. {Nombre_Canciones[i]}]({Urls_Canciones[i]})')

    if Identificar == 'private':
        keyboard1.append([InlineKeyboardButton(text="👤", callback_data="musica_cristiana"), InlineKeyboardButton(text="🗃", callback_data="menu_principal_bot")])
    else:
        pass

    reply_markupp = InlineKeyboardMarkup(keyboard1)

    Canciones_descargar = '\n'.join(Envio_canciones_cortas_url)

    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    query.edit_message_text(
        text=artista + '\n' + '\n' + Canciones_descargar,
        parse_mode=ParseMode.MARKDOWN,
        # disable_web_page_preview=True,
        reply_markup=reply_markupp
    )

def reproducir_music (update, context):
    query = update.callback_query
    bot = context.bot
    chatId = query.message.chat_id
    Urls = query.message.entities[0:]
    id_mensajito = query.message.message_id

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    Links = []
    for i in range(0, len(Urls)):
        Links.append(query.message.entities[i].url)

    Envio_varios = list()
    for i in range(0, len(Urls)):
        Envio_varios.append(InputMediaAudio(media=Links[i]))

    bot.send_media_group(
        chat_id=chatId,
        media=Envio_varios,
        disable_notification=True
    )

def video (update, context):
    query = update.callback_query
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    query.edit_message_text(
        text= "Enviame la url del video a descargar.")

    return CONVERSACION

def buscar_video (update, context):
    bot=context.bot
    chatId = update.message.chat_id
    id_mensajito = update.message.message_id
    chat = update.message.chat
    video_url=update.message.text

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)

    bot.edit_message_text(
        chat_id=chatId,
        message_id=id_mensajito - 1,
        text="Su video se esta descargando por favor espere...")

    youtube = YouTube(video_url)
    videoyoutube= youtube.streams.get_highest_resolution().download()

    bot.sendChatAction(chat_id=chatId, action="upload_video", timeout=None)

    bot.delete_message(chat_id=chatId, message_id=id_mensajito-1)
    bot.sendChatAction(chat_id=chatId, action="upload_video", timeout=30)

    chat.send_video(
        video=open(videoyoutube, "rb"),
        caption = "Titulo ..................: " + youtube.title + '\n'
                "Duracion (seg)...: " + str(youtube.length) + '\n'
    )

    os.remove(videoyoutube)
    return ConversationHandler.END

def audio (update, context):
    query = update.callback_query
    bot=context.bot
    chatId = query.message.chat_id
    bot.sendChatAction(chat_id=chatId, action="typing", timeout=None)

    query.edit_message_text(
        text= "Enviame la url del audio a descargar.")

    return CONVERSACION

def buscar_audio (update, context):
    bot=context.bot
    chatId = update.message.chat_id
    chat = update.message.chat
    input_url=update.message.text
    ruta_arch = pathlib.Path().absolute()
    id_mensajito = update.message.message_id

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)

    bot.edit_message_text(
        chat_id=chatId,
        message_id=id_mensajito - 1,
        text="Su audio se esta descargando por favor espere...")

    # Obtenemos el titulo del video
    video_info = youtube_dl.YoutubeDL().extract_info(url=input_url, download=False)
    video_title = video_info['title']
    youtube = YouTube(input_url)


    # Setear las opciones para la descarga del video
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': video_title + ".mp3",  # Seteamos la ubicacion deseada
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    bot.sendChatAction(chat_id=chatId, action="upload_audio", timeout=None)

    # Descargamos el video
    with youtube_dl.YoutubeDL(opciones) as ydl:
        ydl.download([input_url])

    bot.delete_message(chat_id=chatId, message_id=id_mensajito - 1)
    bot.sendChatAction(chat_id=chatId, action="upload_audio", timeout=None)

    enviar = os.path.join(ruta_arch, video_title + ".mp3")

    chat.send_audio(
        audio=open(enviar, "rb"),
        caption="Titulo ..................: " + youtube.title + '\n'
                "Duracion (seg)...: " + str(youtube.length)
    )

    os.remove(enviar)
    return ConversationHandler.END

def cerrar_dialogo (update, context):
    query = update.callback_query
    bot = context.bot
    chatId = query.message.chat_id
    id_mensajito = query.message.message_id

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)

def mensaje_bienvenida (update, context):
    bot = context.bot
    chatId = update.message.chat_id
    Nuevo_Usuario = update.message.new_chat_members[0].first_name
    id_mensajito = update.message.message_id
    Url = 'https://t.me//KitMusic_bot'

    time.sleep(10)
    bot.delete_message(chat_id=chatId, message_id=id_mensajito)

    bot.send_message(
        chat_id=chatId,
        text=f'*Bienvenido {Nuevo_Usuario}*, puedes [interactuar conmigo aqui]({Url})',
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

def chat_voice (update, context):
    bot = context.bot
    chatId = update.message.chat_id
    id_mensajito = update.message.message_id
    Url = bot.exportChatInviteLink(chatId)

    bot.delete_message(chat_id=chatId, message_id=id_mensajito)

    bot.send_message(
        chat_id=chatId,
        text=f'[Únete a nuestro chat de voz]({Url})',
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

def pruebas (update, context):
    bot = context.bot
    chatId = update.message.chat_id

    Url = bot.exportChatInviteLink(chatId)
    bot.send_message(
        chat_id=chatId,
        text=f'[Únete a nuestro chat de voz]({Url})',
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

    print(update)

if __name__ == "__main__":
    token = os.environ['TOKEN']
    updater =  Updater(token=token, use_context=True)
    dp = updater.dispatcher

    #pip install python-telegram-bot -U (Para actualizar la libreria)
    #este es el comando que desencadena el mensaje de entrada
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("texto_diario", texto_diario))
    dp.add_handler(CommandHandler("texto", texto_aleatorio))
    dp.add_handler(CommandHandler("postales", postales_cristianos_2))
    #dp.add_handler(CommandHandler("pruebas", pruebas))

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, mensaje_bienvenida))
    dp.add_handler(MessageHandler(Filters.status_update.voice_chat_started, chat_voice))

    dp.add_handler(CallbackQueryHandler(pattern="biblia_menu", callback=biblia_menu))
    dp.add_handler(CallbackQueryHandler(pattern="cerrar_dialogo", callback=cerrar_dialogo))
    dp.add_handler(CallbackQueryHandler(pattern="testamento_nuevo_menu", callback=nuevo_testamento))
    dp.add_handler(CallbackQueryHandler(pattern="texto_dia", callback=texto_dia))
    dp.add_handler(CallbackQueryHandler(pattern="biblia", callback=biblia))
    dp.add_handler(CallbackQueryHandler(pattern="postales_cristianos", callback=postales_cristianos))

    dp.add_handler(CallbackQueryHandler(pattern="texto_biblico", callback=texto_biblico))
    dp.add_handler(CallbackQueryHandler(pattern="menu_biblia", callback=biblia))
    dp.add_handler(CallbackQueryHandler(pattern="id_", callback=id_Biblia))
    dp.add_handler(CallbackQueryHandler(pattern="testamentoantiguo_menu", callback=antiguo_testamento))
    dp.add_handler(CallbackQueryHandler(pattern="nuevo_testamento", callback=nuevo_testamento))
    dp.add_handler(CallbackQueryHandler(pattern='antiguo_testamento', callback=antiguo_testamento))
    dp.add_handler(CallbackQueryHandler(pattern="youtube", callback=youtube))
    dp.add_handler(CallbackQueryHandler(pattern="siguiente", callback=siguiente))
    dp.add_handler(CallbackQueryHandler(pattern="Atras", callback=Atras))
    dp.add_handler(CallbackQueryHandler(pattern="ca_", callback=id_capitulos))
    dp.add_handler(CallbackQueryHandler(pattern="regreso_capitulos", callback=regreso_capitulos))
    dp.add_handler(CallbackQueryHandler(pattern="versiculos_back", callback=versiculos_back))
    dp.add_handler(CallbackQueryHandler(pattern="versiculos_next", callback=versiculos_next))
    dp.add_handler(CallbackQueryHandler(pattern="musica_cristiana", callback=musica_cristiana))
    dp.add_handler(CallbackQueryHandler(pattern="artistas_next", callback=artistas_next))
    dp.add_handler(CallbackQueryHandler(pattern="artistas_back", callback=artistas_back))
    dp.add_handler(CallbackQueryHandler(pattern="AR_", callback=musica_art))
    dp.add_handler(CallbackQueryHandler(pattern="compartir_ver", callback=compartir_ver))
    dp.add_handler(CallbackQueryHandler(pattern="preg_next", callback=preg_next))
    dp.add_handler(CallbackQueryHandler(pattern="preg_back", callback=preg_back))
    dp.add_handler(CallbackQueryHandler(pattern="list_music_next_", callback=list_music_next))
    dp.add_handler(CallbackQueryHandler(pattern="list_music_back_", callback=list_music_back))
    dp.add_handler(CallbackQueryHandler(pattern="reproducir_music", callback=reproducir_music))
    dp.add_handler(CallbackQueryHandler(pattern="predicacion_voz", callback=predicacion))

    dp.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(pattern='video', callback=video)],
        states={CONVERSACION: [MessageHandler(Filters.text, buscar_video)]},
        fallbacks=[CallbackQueryHandler(pattern="menu_principal_bot", callback=menu)]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(pattern='audio', callback=audio)],
        states={CONVERSACION: [MessageHandler(Filters.text, buscar_audio)]},
        fallbacks=[CallbackQueryHandler(pattern="menu_principal_bot", callback=menu)]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(pattern='preguntas_biblia', callback=preguntas_biblia)],
        states={
            CONVERSACION: [MessageHandler(Filters.text, respuesta_preguntas)],
            CONVERSACION_1: [MessageHandler(Filters.text, respuesta_preguntas_respuesta)]
        },
        fallbacks=[CallbackQueryHandler(pattern="menu_principal_bot", callback=menu)]
    ))

    dp.add_handler(MessageHandler(Filters.text, callback=process_message))
    dp.add_handler(CallbackQueryHandler(pattern="menu_principal_bot", callback=menu))

    updater.start_polling()
    updater.idle()
