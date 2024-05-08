#Importando bibliotecas necessárias

import folium
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import inflection
from forex_python.converter import CurrencyRates
from streamlit.components.v1 import html
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from folium.plugins import Fullscreen
from PIL import Image 
from datetime import datetime


st.set_page_config(
       page_title = 'Welcome',
       page_icon='🥑')

# Funções


# O Mapa

def restaurant_maps(df):

    # Calculando a média da nota antes de aplicar qualquer filtro
    mean_rating = df['aggregate_rating'].mean()

    df_aux = (df.loc[:,['country_code','city','cuisines','average_cost_for_two','locality','restaurant_name','address','aggregate_rating','rating_text','votes',
                         'latitude',
                         'longitude',
                         'restaurant_id']].
              groupby(['average_cost_for_two','rating_text','votes','country_code','city','cuisines','locality','aggregate_rating']).
              agg({'latitude':'median',
                   'longitude':'median',
                   'restaurant_id':'count'}).
              reset_index())

    map = folium.Map()

    # Criando um marcador de cluster
    marker_cluster = MarkerCluster().add_to(map)

    for index, location_info in df_aux.iterrows():
        popup_html = f"<b>Cuisines :</b>{location_info['cuisines']}<br>"\
                     f"<b>Price for two :</b> ${location_info['average_cost_for_two']:.1f}<br>"\
                     f"<b>Comments : </b>{location_info['rating_text']}<br>"\
                     f"<b>Votes : </b>{location_info['votes']}<br>"\
                     f"<b> Avg Rating : </b> {location_info['aggregate_rating']}"

        # Determinando a cor com base na nota média
        rating = location_info['aggregate_rating']

        if rating >= 4.5:
            color = 'green'
        elif rating >= 4.0:
            color = 'blue'
        elif rating >= 3.0 and rating < 4.0:
            color = 'yellow'
        elif rating >= 2.0:
            color = 'red'
        elif rating > 0.0:
            color = 'red'
        elif rating == 0:
            color = 'gray'
        else:
            color = 'green'
    
        popup = folium.Popup(popup_html, max_width=300)

        # Substituindo o ícone padrão por um ícone de restaurante
        icon = folium.Icon(icon='cutlery', prefix='fa', color=color)
        if 'Home-made' in location_info['cuisines']:
            icon = folium.Icon(icon='home', prefix='fa', color=color)
        folium.Marker([location_info['latitude'], location_info['longitude']], popup=popup, icon=icon).add_to(marker_cluster)

    # Adicionando o botão de tela cheia (fullscreen)
    FullscreenBtn = Fullscreen()
    map.add_child(FullscreenBtn)

    folium_static(map, width=1024, height=600)
    return None


# Função que indica as cores com base no código do Dataframe
COLORS = {
                "3F7E00": "darkgreen",
                "5BA829": "green",
                "9ACD32": "lightgreen",
                "CDD614": "orange",
                "FFBA00": "red",
                "CBCBC8": "darkred",
                "FF7800": "orange",
                }
def color_name(color_code):
    return COLORS[color_code]


# Função que indica os países com base no código do Dataframe
COUNTRIES = {
                1: "India",
                14: "Australia",
                30: "Brazil",
                37: "Canada",
                94: "Indonesia",
                148: "New Zeland",
                162: "Philippines",
                166: "Qatar",
                184: "Singapure",
                189: "South Africa",
                191: "Sri Lanka",
                208: "Turkey",
                214: "United Arab Emirates",
                215: "England",
                216: "United States of America",
                }

def country_name(country_id):
    return COUNTRIES.get(country_id,'Unknowmn')

# Função para classificar o nivel da culinária com base da numeração 1, 2, 3 e 4 
def create_price_type(price_range):
    if price_range == 1:
        return "Cheap"
    elif price_range == 2:
        return "Normal"
    elif price_range == 3:
        return "Expensive"
    else:
        return "Gourmet"
    
# Função para classificar como sim e como não as colunas de 1 e 0.
def yes_no(dataframe):
    num = dataframe
    if num == 1:
        return 'Yes'
    else:
        return 'No'

    
# Função para remover os espação dos textos no cabeçalho e também colocar ambas em minúsculas    
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    
    cols_old = list(df.columns)
    cols_old[0] = cols_old[0].capitalize()
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def modelagem(dataframe, country_name, create_price_type, color_name, yes_no):
    
    # Removendo duplicadas do dataframe
    dataframe['duplicada'] = dataframe.groupby('Restaurant ID')['Restaurant ID'].transform('count')
    dataframe = dataframe.loc[dataframe['duplicada'] == 1].copy()

    # Atribuindo as funções dentro do dataframe usando .loc para evitar SettingWithCopyWarning
    dataframe.loc[:, 'Country Code'] = dataframe['Country Code'].map(country_name)
    dataframe.loc[:, 'Price range'] = dataframe['Price range'].map(create_price_type)
    dataframe.loc[:, 'Rating color'] = dataframe['Rating color'].map(color_name)
    dataframe.loc[:, 'Has Table booking'] = dataframe['Has Table booking'].map(yes_no)
    dataframe.loc[:, 'Has Online delivery'] = dataframe['Has Online delivery'].map(yes_no)
    dataframe.loc[:, 'Is delivering now'] = dataframe['Is delivering now'].map(yes_no)
    dataframe.loc[:, 'Switch to order menu'] = dataframe['Switch to order menu'].map(yes_no)

    dataframe = rename_columns(dataframe)

    # Selecionando o primeiro elemento (Palavra) de cada cozinha
    dataframe["cuisines"] = dataframe["cuisines"].astype(str)
    dataframe["cuisines"] = dataframe.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

    # Selecionando o primeiro elemento (Palavra) de cada localidade
    dataframe["locality"] = dataframe["locality"].astype(str)
    dataframe["locality"] = dataframe.loc[:, "locality"].apply(lambda x: x.split(",")[0])

    # Excluindo a coluna 'duplicadas e criando uma copia do dataframe'
    dataframe.drop('duplicada', axis=1, inplace=True)
    
    return dataframe

# Estrutura lógica 

dataframe = pd.read_csv('dataset//zomato.csv')
df = modelagem(dataframe, country_name, create_price_type, color_name, yes_no)

#  Inicio Side Bar
st.header('Analytics Dashboard', divider='red') # Título 
image = Image.open('food.png')
st.sidebar.image( image, width = 250)
st.sidebar.write('</span> <span style="font-size: small;">:blue[Comunidade DS]</span>', unsafe_allow_html=True)
st.sidebar.markdown("""___""")




st.write('## Find your favorite restaurant !' ) # Subtítulo

# Filtros código

#Pais

country = df['country_code'].unique()

if 'Brazil' not in country:
    country = ['Brazil'] + list(country)

country_options = st.sidebar.multiselect(
    'Select the Countries:',
    ['Select All'] + list(country),
    default=['Select All'] 
)

if 'Select All' in country_options:
    country_options = list(country)
    
# Avaliações  ( Criar slicer)

#

# Crítica 

# Definição dos intervalos e rótulos correspondentes
intervals = [(4.6, 'Excelente'), (4.1, 'Bom'), (3.1, 'Regular'), (2.1, 'Ruim'), (0.1, 'Péssimo'), (0.0, 'Não avaliado')]
labels = [label for _, label in intervals]
selected_rating_labels = st.sidebar.multiselect(
    'Select the Rating:',
    ['Select All'] + labels,
    default=['Select All']
)

# Se "Select All" estiver presente, selecionar todos os rótulos de classificação
if 'Select All' in selected_rating_labels:
    selected_rating_values = [interval[0] for interval in intervals]
else:
    # Mapear os rótulos selecionados de volta para os valores numéricos correspondentes
    selected_rating_values = [interval[0] for interval in intervals if interval[1] in selected_rating_labels]

#
# Cidade

city_filtro = df['city'].unique()

if 'Rio de Janeiro' not in city_filtro:
    city_filtro = ['Rio de Janeiro'] + list(city_filtro)

city_filtro_options = st.sidebar.multiselect(
    'Select the City:',
    ['Select All'] + list(city_filtro),
    default=['Select All']
)

if 'Select All' in city_filtro_options:
    city_filtro_options = list(city_filtro)
    
# Culinária

cuisines_filtro = df['cuisines'].unique()

if 'Italian' not in cuisines_filtro:
    cuisines_filtro = ['Italian'] + list(cuisines_filtro)

cuisines_filtro_options = st.sidebar.multiselect(
    'Select the Cuisines:',
    ['Select All'] + list(cuisines_filtro),
    default=['Select All']
)

if 'Select All' in cuisines_filtro_options:
    cuisines_filtro_options = list(cuisines_filtro)
    
# Chamando os filtro 

linhas_selecionadas01 = df['country_code'].isin(country_options)
df = df.loc[linhas_selecionadas01,:]

linhas_selecionadas02 = df['city'].isin(city_filtro_options)
df = df.loc[linhas_selecionadas02,:]

linhas_selecionadas03 = df['cuisines'].isin(cuisines_filtro_options)
df = df.loc[linhas_selecionadas03,:]

df = df[df['aggregate_rating'].isin(selected_rating_values)]

# Final sidebar

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Comunidade DS')

# Gráficos


with st.container(): 
        
        col1,col2,col3,col4,col5,col6 = st.columns(6)
        
        with col1:
            geral_02 = len(df.loc[:,'country_code'].unique())
            col1.metric('Countries',geral_02)
            
        with col2:
            geral_03 = len(df.loc[:,'city'].unique())
            col2.metric('Cities',geral_03)
    
        with col3:
            geral_01 = len(df.loc[:,'restaurant_id'].unique())
            col3.metric('Restaurants',geral_01)
            
            
        with col4:
            geral_05 = len(df.loc[:,'cuisines'].unique())
            col4.metric('Cuisines',geral_05)
            
        with col5:
            geral_04 = df['votes'].sum()
            col5.metric('Popular vote',geral_04)

            
with st.container():
    
    st.markdown("""___""")
    restaurant_maps(df)
