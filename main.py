import streamlit as st 
import mysql.connector
import pandas as pd
from partida import main
st.markdown('<h1 styl1324790e = "border-radius: 50px; color: #FFFFFF;text-align:center;text-transform: uppercase; background:-webkit-linear-gradient(#1088ff,#0bd6d4);"> Premier League - Databet </h1>',unsafe_allow_html=True)
st.text("")
st.text("")
# Print the DataFrame to the console
list_pages = ["", "Analise Tabela",'Analise Partidas']
st.sidebar.markdown("<h3 style='color:#1088ff; text-align:center;'> Navegação </h3>",unsafe_allow_html=True)
st.sidebar.text("")
st.sidebar.markdown("<h5 style='color:#1088ff; text-align:center;'> Escolha qual página ira acessar </h5>",unsafe_allow_html=True)
selection = st.sidebar.selectbox("", list_pages)
if selection == 'Analise Tabela':
	pass
elif selection == 'Analise Partidas':
    st.markdown('<h1 styl1324790e = "border-radius: 50px; color: #FFFFFF;text-align:center;text-transform: uppercase; background:-webkit-linear-gradient(#1088ff,#0bd6d4);"> Premier League - Databet </h1>',unsafe_allow_html=True)

    main()
