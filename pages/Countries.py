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
       page_title = 'Countries',
       page_icon='🗺️')

# Funções

# Restaurantes por País
#Quantidade de restaurantes registrados por país
def countries_rest(df):
    paises_02 = (df.loc[:,['country_code','restaurant_id']].
                 groupby('country_code').
                 count().
                 reset_index())   
    paises_02 = paises_02.sort_values(by='restaurant_id', ascending=False).reset_index(drop=True)
    paises_02 = paises_02.rename(columns={'country_code':'Countries','restaurant_id':'Restaurants'})
    #paises_02 = paises_02.head(6)
    paises_02['Rotulo'] = paises_02['Restaurants']

    fig = px.bar(paises_02, x='Countries', y='Restaurants', text='Rotulo')
    fig.update_traces(hovertemplate='<b>%{x}</b><br>' + 
                                    'Cities: %{y}<br>')

    return fig

# País com mais cidades
#1 Qual o nome do país que possui mais cidades registradas?
def countries_citi(df):
    paises_01 = df.loc[:,['city','country_code']].groupby('country_code').nunique().reset_index()
    paises_01 = paises_01.sort_values(by='city', ascending=False).reset_index(drop=True)
    paises_01 = paises_01.rename(columns={'country_code':'Countries','city':'Cities'})
    paises_01['Rotulo'] = paises_01['Cities']

    fig = px.bar(paises_01, x='Countries', y='Cities', text='Rotulo', custom_data=['Cities'])
    fig.update_traces(hovertemplate='<b>%{x}</b><br>' + 
                                    'Cities: %{y}<br>')

    return fig

# Media maior nota registrada por pais
#10 Qual o nome do país que possui, na média, a maior nota média registrada?
def countries_mean(df):
    paises_10 = (df.loc[:,['country_code','votes']].
                        groupby('country_code').
                        agg({'votes':'mean'}).
                        reset_index())
    paises_10 = paises_10.sort_values(by= 'votes', ascending= False).reset_index(drop=True)
    paises_10 = paises_10.rename(columns={'country_code':'Countries','votes':'Rating mean'})
    paises_10 = paises_10.head(6)
    paises_10['Rotulo'] = paises_10['Rating mean'].map('{:.2f}'.format)

    fig = px.bar(paises_10, x='Countries', y='Rating mean', text='Rotulo')
    fig.update_traces(hovertemplate='')

    return fig

# Preço para 2 
#11 Qual a média de preço de um prato para dois por país?
def countries_two(df):
    paises_11 = df.groupby('country_code')['average_cost_for_two'].mean().reset_index()
    paises_11 = paises_11.sort_values(by='average_cost_for_two',ascending=False).reset_index(drop=True)
    paises_11 = paises_11.rename(columns={'country_code':'Countries','average_cost_for_two':'For two people'})
    paises_11 = paises_11.head(6)
    paises_11['Rotulo'] = paises_11['For two people'].map('{:.2f}'.format)

    fig = px.bar(paises_11, x='Countries', y='For two people', text='Rotulo')
    fig.update_traces(hovertemplate='')

    return fig

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
st.header('Country View', divider='blue') # Título 
image = Image.open('food.png')
st.sidebar.image( image, width = 250)
st.sidebar.write('<span style="font-size: medium;">Leonardo Rosa </span> <span style="font-size: small;">:blue[ |  Data Scientist]</span>', unsafe_allow_html=True)
st.sidebar.markdown("""___""")

# st.write('## Find your favorite restaurant !' ) # Subtítulo

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

# Crítica 

# Definição dos intervalos e rótulos correspondentes
intervals = [(4.6, 'Excelente'), (4.1, 'Bom'), (3.1, 'Regular'), (2.1, 'Ruim'), (0.1, 'Péssimo'), (0.0, 'Não avaliado')]
labels = [label for _, label in intervals]


selected_rating_labels = st.sidebar.multiselect(
    'Select the Rating:',
    ['Select All'] + labels,
    default=['Select All']
)
if 'Select All' in selected_rating_labels:
    selected_rating_labels = labels
    
selected_rating_values = [interval[0] for interval in intervals if interval[1] in selected_rating_labels]

# Chamando os filtro 

linhas_selecionadas01 = df['country_code'].isin(country_options)
df = df.loc[linhas_selecionadas01,:]

df = df[df['aggregate_rating'].isin(selected_rating_values)]

# Final sidebar

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Comunidade DS')

# Gráficos

with st.container(): 

            st.subheader('The quantity of registered restaurants per country')
            fig = countries_rest(df)
            st.plotly_chart(fig,use_container_width = True)
               
with st.container(): 

            st.subheader('The quantity of registered cities per country')
            fig = countries_citi(df)
            st.plotly_chart(fig,use_container_width = True)
            
with st.container(): 
    
        st.markdown("""___""")
        col1,col2 = st.columns(2)
            
        with col1:

            st.markdown('##### Average ratings made per city')
            fig = countries_mean(df)
            st.plotly_chart(fig,use_container_width = True)
            
        with col2:

            st.markdown('##### Average dish price for two people')
            fig = countries_two(df)
            st.plotly_chart(fig,use_container_width = True)

            
