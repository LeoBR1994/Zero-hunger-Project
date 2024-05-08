# Zero-hunger-Project
[Acessar Dashboard]()

# Skills utilizadas:

    Python, (Pandas, Haversine, Map,
    JupterLab
    Streamlit
    Streamlit Cloud
    Github


# Fome Zero

# 1. Problema de Negócio

  Sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra
a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer
utilizando dados!
A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

  O CEO também pediu que fosse gerado um dashboard que permitisse que ele
visualizasse as principais informações das perguntas que ele fez. O CEO precisa
dessas informações o mais rápido possível, uma vez que ele também é novo na
empresa e irá utilizá-las para entender melhor a empresa Fome Zero para conseguir
tomar decisões mais assertivas.
Seu trabalho é utilizar os dados que a empresa Fome Zero possui e responder as
perguntas feitas do CEO e criar o dashboard solicitado.

# 2. O Desafio

O CEO Guerra também foi recém contratado e precisa entender melhor o negócio
para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a
Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da
empresa e que sejam gerados dashboards, a partir dessas análises, para responder
às seguintes perguntas:

## 1. Visão geral

  1. Quantos restaurantes únicos estão registrados?
  2. Quantos países únicos estão registrados?
  3. Quantas cidades únicas estão registradas?
  4. Qual o total de avaliações feitas?
  5. Qual o total de tipos de culinária registrados?


## 2. Premissas assumidas para a análise para os Paises

  1. Qual o nome do país que possui mais cidades registradas?
  2. Qual o nome do país que possui mais restaurantes registrados?
  3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
  4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
  5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
  6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
  7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
  reservas?
  8. Qual o nome do país que possui, na média, a maior quantidade de avaliações
  registrada?
  9. Qual o nome do país que possui, na média, a maior nota média registrada?
  10. Qual o nome do país que possui, na média, a menor nota média registrada?
  11. Qual a média de preço de um prato para dois por país?

## 3. Premissas assumidas para a análise para as Cidades

  1. Qual o nome da cidade que possui mais restaurantes registrados?
  2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
  3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
  4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
  5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
  distintas?
  6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
  reservas?
  7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
  entregas?
  8. Qual o nome da cidade que possui a maior quantidade de restaurantes que
  aceitam pedidos online?

## 4. Premissas assumidas para a análise para os Restaurantes

  1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
  2. Qual o nome do restaurante com a maior nota média?
  3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
  4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
  5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
  6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
  7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
  8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
  possuem um valor médio de prato para duas pessoas maior que as churrascarias
  americanas (BBQ)?

## 5. Premissas assumidas para a análise para os Tipos de Culinária

  1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
  2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
  3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
  4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
  5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
  6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
  7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
  8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?
  9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
  10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?
  11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
  12. Qual o tipo de culinária que possui a maior nota média?
  13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
  online e fazem entregas?

# 3. Estratégia da solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem
as 3 principais visões do modelo de negócio da empresa:

  1. Visão global dos restaurantes cadastrados no data base.
  2. Visão das cidades.
  3. VIsão dos paises.

## 1. Visão global dos restaurantes cadastrados no data base.

  a. Quantidade de paises registados.
  
  b. Quantidade de cidades registadas.
  
  c. Quantidade de restaurantes registados.
  
  d. Quantidade de cozinhas registadas.
  
  e. Quantidade de votos registados.
  
  f. Mapa global.

## 2. Visão das cidades.

  a. As 10 cidades com mais restaurantes no banco de dados.
  
  b. As 7 principais cidades com restaurantes com classificação média acima de 4.
  
  c. As 7 principais cidades com restaurantes com classificação média abaixo de 2,5.
  
  d. Top 10 cidades com restaurantes com diferentes tipos de cozinha.
  
## 3. VIsão dos paises.

  a. A quantidade de restaurantes registrados por país.
  
  b. A quantidade de cidades cadastradas por país.
  
  c. Avaliações médias feitas por cidade.
  
  d. Preço médio do prato para duas pessoas.

  
# 4. Conclusão

  O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.
  Com base nos dados podemos concluir que o número de pedidos avaliados como Excelentes possuem maior concentração na India e nos Estados Unidos, totalizando em 287 opções de restaurantes em 62 cidades, com + de 60 tipos de culinárias diferentes, onde a media do custo de prato para 2, custa aproximadamente em 694.0 rupias indiana (India) e 56.0 dólarres (EUA).

# 5. Projeto

  Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
O painel pode ser acessado através desse link: https://dashboardfood-portifolio.streamlit.app/

# Os Dados

O conjunto de dados que representam o contexto está disponível na plataforma do
Kaggle. O link para acesso aos dados :
https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-datase
t?resource=download&select=zomato.csv
