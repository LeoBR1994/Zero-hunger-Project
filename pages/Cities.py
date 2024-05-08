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
       page_title = 'Cities',
       page_icon='🏙️')

# Funções


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
st.header('Cities View', divider='blue') # Título 
image = Image.open('food.png')
st.sidebar.image( image, width = 250)
st.sidebar.write('<span style="font-size: small;">:blue[Comunidade DS]</span>', unsafe_allow_html=True)
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
    

# Chamando os filtro 

linhas_selecionadas01 = df['country_code'].isin(country_options)
df = df.loc[linhas_selecionadas01,:]

# Final sidebar

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Leonardo Rosa')

# Gráficos

with st.container(): 

        st.markdown('##### Top 10 cities with the most restaurants in the database')
         #1 Qual o nome da cidade que possui mais restaurantes registrados?
        def city(df):
            cidade_01 = df.loc[:, ['city', 'restaurant_id']].groupby('city').nunique().reset_index()
            cidade_01 = cidade_01.sort_values(by='restaurant_id', ascending=False).head(10).reset_index(drop=True)
            cidade_01.columns = ['Cities', 'Restaurants']
            fig = px.bar(cidade_01, x='Cities', y='Restaurants', labels={'Cities': 'Cities', 'Restaurants': 'Restaurants'})
            return fig
        
        fig = city(df)
        st.plotly_chart(fig, use_container_width = True)
            
with st.container(): 
    
        st.markdown("""___""")
        col1,col2 = st.columns(2)
            
        with col1:

            st.markdown('##### Top 7 cities with Restaurants with an average rating above 4')
            #2 Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
            def above(df):
                cidade_02 = (df.loc[:,['city','restaurant_id','aggregate_rating']]
                             .groupby(['city'])
                             .count()
                             .rename(columns={'restaurant_id':'Restaurant','aggregate_rating':'Mean rating'})
                             .reset_index())
                cidade_02 = cidade_02[cidade_02['Mean rating'] > 4.0]

                # Renomeie a coluna 'city' para 'Cities'
                cidade_02 = cidade_02.rename(columns={'city': 'Cities'})

                # Ordenar pela coluna 'Mean rating' de forma decrescente
                cidade_02 = cidade_02.sort_values(by='Restaurant', ascending=False).head(6).reset_index(drop=True)

                fig = px.bar(cidade_02, x='Cities', y='Restaurant', labels={'Cities': 'Cities', 'Restaurant': 'Restaurant'})

                return fig
        
            fig = above(df)
            st.plotly_chart(fig, use_container_width = True)


        with col2:

            st.markdown('##### Top 7 cities with Restaurants with an average rating below 2.5')
            #3 Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
            def below(df):
                cidade_02 = (df.loc[:,['city','restaurant_id','aggregate_rating']]
                             .groupby(['city'])
                             .count()
                             .rename(columns={'restaurant_id':'Restaurant','aggregate_rating':'Mean rating'})
                             .reset_index())
                cidade_02 = cidade_02[cidade_02['Mean rating'] < 2.5]

                # Renomeie a coluna 'city' para 'Cities'
                cidade_02 = cidade_02.rename(columns={'city': 'Cities'})

                # Ordenar pela coluna 'Mean rating' de forma decrescente
                cidade_02 = cidade_02.sort_values(by='Restaurant', ascending=False).head(7).reset_index(drop=True)

                fig = px.bar(cidade_02, x='Cities', y='Restaurant', labels={'Cities': 'Cities', 'Restaurant': 'Restaurant'})

                return fig
        
            fig = below(df)
            st.plotly_chart(fig, use_container_width = True)
            
with st.container(): 

        st.markdown('##### Top 10 cities with Restaurants with different types of cuisine')
        #5 Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
        def cusiner(df):
            cidade_05 = df.loc[:,['city','cuisines']].groupby('city').nunique().reset_index()
            cidade_05 = cidade_05.sort_values(by='cuisines', ascending=False).head(10).reset_index(drop=True)
            cidade_05.columns = ['Cities', 'Cuisiners']

            # Plota o gráfico de barras com as cores da coluna 'rating_color'
            fig = px.bar(cidade_05, x='Cities', y='Cuisiners',labels={'Cities': 'Cities', 'Cuisiners': 'Cuisiners'})

            return fig

        fig = cusiner(df)
        st.plotly_chart(fig, use_container_width = True)


            
