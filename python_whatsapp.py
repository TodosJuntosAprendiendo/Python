#!/usr/bin/python
# -*- coding: utf-8 -*-
# ModuleNotFoundError: No module named 'emoji'
#pip install emoji --upgrade
#En caso de no tener pip intalado
#git clone https://github.com/carpedm20/emoji.git
#cd emoji
#python setup.py install
# Cargar Librerias
#%pip install emoji --upgrade
#%pip install plotly --upgrade


#############################################################
# Hola, te recomendmos suscribirte a todas las redes sociales del proyecto
# Todos Juntos Aprendiendo para más contenido
# Cualquier aporte, corrección, o tema relacionado será bienvenido a
# tjaprendiendo@jmail.
#############################################################

import pandas as pd
import re
import numpy as np
import collections
import emoji
import plotly.express as px #pip3 install plotly --upgrade
import matplotlib.pyplot as plt
from datetime import datetime

#from google.colab import files

#files.upload()

def starts_with_date_time(s):
    # Patron de expreciones regulares para la fecha y la hora
    pattern = '^([0-9])+/([0-9])+/([0-9])+ ([0-9])+:([0-9])+ -' #Hora en México
    result = re.match(pattern, s)
    if result:
        return True
    return False

def find_author(s):
    patterns = [
        '([\w]+):',                        # Nombre
        '([\w]+[\s]+[\w]+):',              # Nombre y apellido
        '([\w]+[\s]+[\w]+[\s]+[\w]+.*):',  # Nombre + 2 apellidos
        '(\+52 1 \d{3} \d{3} \d{4}):',     # Número telefónico (México)
        '([\w]+)[\u263a-\U0001f999]+:',    # Nombre y emoji
        '([\w]+[\s]+[0-9]+):'              # Nombre genérico
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False


parsed_data = []
conversation_path = "WhatsApp Chat with Intercambio Navideño 2022.txt" # chat file
with open(conversation_path, encoding='utf-8') as fp:
    fp.readline() # Skipping first line of the file
    fp.readline()
    while True:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        starts_with_date_time(line)

        try:
          splitLine = line.split(' - ')                # Divide line en dos partes
          dateTime = splitLine[0]                      # La primera parte se guarda en dateTime
          date_time = dateTime.split(',')             # Separa fecha y hora
          date = date_time[0]
          time = date_time[1]

          message = ' '.join(splitLine[1:])            # Autor + mensaje
          find_author(message)                      # Si existe autor
          splitMessage = message.split(': ')       # Separa a partir de ': '
          author = splitMessage[0]                 # La primera parte es author
          message = ' '.join(splitMessage[1:])     # Lo siguiente es el mensaje

        except IndexError:
          pass

        parsed_data.append([date, time, author, message])

df = pd.DataFrame(parsed_data, columns=['Date', 'Time', 'Author', 'Message'])


media = list(df['Message'])
df.info()


dat = list(df['Date'])
num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
       21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
ave = []

for i,k in enumerate(dat):
  j = k.split("/")

  try:
    if float(j[0]) in num:
      pass

  except ValueError:
      ave.append(i)

df.drop(ave, axis=0, inplace=True)
df.reset_index(drop=True, inplace=True)

df["Date"] = pd.to_datetime(df["Date"])

media = list(df['Message'])
ind = []
for i,j in enumerate(media):
  if j == "":
    ind.append(i)

df.drop(ind, axis=0, inplace=True)
df.reset_index(drop=True, inplace=True)

emoji_regexp = u'[\U00002600-\U000026FF]|[\U00002700-\U000027BF]|[\U0001f300-\U0001f5fF]|[\U0001f600-\U0001f64F]|' \
               u'[\U0001f680-\U0001f6FF]'
lista_emoji = re.findall(emoji_regexp, x, re.UNICODE)
len(lista_emoji)

def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.EMOJI_DATA for char in word):
            emoji_list.append(word)

    return emoji_list
# Probamos la función
x = '01/10/18 19:18 - Señora 5: Claudia, puedes reenviar los paquetes, por favor? 🙏🏼 Aún no estaba en el grupo'

print(x)
#df.iloc[3, 3]
#re.findall(r'\X', df.iloc[:, 3])
re.findall(emoji_regexp, x)
split_count(x)


total_messages = df.shape[0]
media_messages = df[df['Message'] == ''].shape[0]
df["emoji"] = df["Message"].apply(split_count)
emojis = sum(df['emoji'].str.len())
URLPATTERN = r'(https?://\S+)'
df['urlcount'] = df.Message.apply(lambda x: re.findall(URLPATTERN, x)).str.len()
links = np.sum(df.urlcount)


print('Mensajes enviados: ', total_messages)
print('Mensajes con emoji: ', media_messages)
print('Emojis: ', emojis)
print('Links enviados: ', links)



media_messages_df = df[df['Message'] == '']
messages_df = df.drop(media_messages_df.index)

messages_df['Letter_Count'] = messages_df['Message'].apply(lambda s : len(s))
messages_df['Word_Count'] = messages_df['Message'].apply(lambda s : len(s.split(' ')))
messages_df["MessageCount"]=1

messages_df.head()

l = messages_df.Author.unique()

for i in range(len(l)):
  # Filtering out messages of particular user
  req_df= messages_df[messages_df["Author"] == l[i]]
  # req_df will contain messages of only one particular user
  print(f'Estadísticas de {l[i]} -')
  # shape will print number of rows which indirectly means the number of messages
  print('Mensajes enviados:', req_df.shape[0])
  #Word_Count contains of total words in one message. Sum of all words/ Total Messages will yield words per message
  words_per_message = (np.sum(req_df['Word_Count']))/req_df.shape[0]
  print('Palabras por mensaje:', words_per_message)
  #media conists of media messages
  media = media_messages_df[media_messages_df['Author'] == l[i]].shape[0]
  print('Contenido multimedia enviado:', media)
  # emojis conists of total emojis
  emojis = sum(req_df['emoji'].str.len())
  print('Emojis enviados:', emojis)
  #links consist of total links
  links = sum(req_df["urlcount"])
  print('Links enviados:', links)
  print()

  #Total de Emojis distintos enviados dentro de la conversación
total_emojis_list = list(set([a for b in messages_df.emoji for a in b]))
total_emojis = len(total_emojis_list)
print('Total de Emojis diferentes enviados:',total_emojis)

import collections
total_emojis_list = list([a for b in messages_df.emoji for a in b])
emoji_dict = dict(collections.Counter(total_emojis_list))
emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)

emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])

import plotly.express as px
fig = px.pie(emoji_df, values='count', names='emoji',
             title='Distribución por proporción de Emojis')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()


# Crear lista de autores, para generar gráficos de uso de emoji's por cada autor
l = messages_df.Author.unique()
for i in range(len(l)):
  dummy_df = messages_df[messages_df['Author'] == l[i]]
  total_emojis_list = list([a for b in dummy_df.emoji for a in b])
  emoji_dict = dict(collections.Counter(total_emojis_list))
  emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
  print('Emoji Distribution for', l[i])
  author_emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])
  fig = px.pie(author_emoji_df, values='count', names='emoji')
  fig.update_traces(textposition='inside', textinfo='percent+label')
  fig.show()

messages_df['Author'].value_counts().head(15).plot.barh() # Top 10 de miembros más activos
plt.xlabel('Número de mensajes')
plt.ylabel('Autor')




date_df = messages_df.groupby("Date").sum()
date_df.reset_index(inplace=True)
fig = px.line(date_df, x="Date", y="MessageCount", labels={'Date':'Periodo', 'MessageCount':'No.Mensajes'}, title='Variación de la Actividad dentro del periodo.')
fig.update_xaxes(nticks=20)
fig.show()

def dayofweek(i):
  l = ["Lunes", "Martes", "Miércoes", "Jueves", "Viernes", "Sábado", "Domingo"]
  return l[i];
day_df=pd.DataFrame(messages_df["Message"])
messages_df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
day_df['day_of_date'] = messages_df['Date'].dt.weekday
day_df['day_of_date'] = day_df["day_of_date"].apply(dayofweek)
day_df["messagecount"] = 1
day = day_df.groupby("day_of_date").sum()
day.reset_index(inplace=True)

fig = px.line_polar(day, r='messagecount', theta='day_of_date', line_close=True)
fig.update_traces(fill='toself')
fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0,1500]
    )),
  showlegend=False
)
fig.show()

messages_df['Date'].value_counts().head(10).plot.barh()
plt.xlabel('Número de mensajes')
plt.ylabel('Fecha')


dat = list(messages_df['Time'])
num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
ave = []

for i,k in enumerate(dat):
  j = k.split(":")

  try:
    if float(j[0]) in num:
      pass

  except ValueError:
      ave.append(i)

messages_df.drop(ave, axis=0, inplace=True)
messages_df.reset_index(drop=True, inplace=True)


messages_df['Time'].value_counts().head(10).plot.barh()
plt.xlabel('Número de mensajes')
plt.ylabel('Hora')


import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
stopwords = set(stopwords.words('spanish'))
stopwords.update([ "chingo", "xq","aaay","Jajajaa","perra","kieren","verga","inés"])
stopwords.update(set(["si", "multimedia", "omitido",
    "ra", "ga", "na", "ani", "em", "ki", "ah","ha","la","eh","ne","le"]))
wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)

# Generate a word cloud image
wordcloud = WordCloud(stopwords=stopwords, background_color="white",
                     max_words = 80).generate(text)

# Display the generated image:
# the matplotlib way:
plt.figure( figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear', vmin=12, vmax=20)
plt.axis("off")
plt.show()
