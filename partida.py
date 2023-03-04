import streamlit as st 
import mysql.connector
import pandas as pd
# Set up a connection to the MySQL database
mydb = mysql.connector.connect(
  host= st.secrets.host,
  user=st.secrets.user,
  password=st.secrets.password,
  database=st.secrets.database
)

def get_home_shooting(mydb):
    # Create a cursor object to execute SQL queries
    mycursor = mydb.cursor()

    # Define a SQL query to retrieve data from the database
    query = "SELECT * FROM TMHomeShooting WHERE last_updated_at >= '2023-03-03';"

    # Execute the query and fetch the results
    mycursor.execute(query)
    result = mycursor.fetchall()

    # Convert the result into a Pandas DataFrame
    df = pd.DataFrame(result, columns=[i[0] for i in mycursor.description])
    return df


def get_home_miscellaneuos(mydb):
    # Create a cursor object to execute SQL queries
    mycursor = mydb.cursor()

    # Define a SQL query to retrieve data from the database
    query = "SELECT * FROM TMMiscellaneous WHERE last_updated_at >= '2023-03-03';"

    # Execute the query and fetch the results
    mycursor.execute(query)
    result = mycursor.fetchall()

    # Convert the result into a Pandas DataFrame
    df = pd.DataFrame(result, columns=[i[0] for i in mycursor.description])
    return df


def get_home_defensive(mydb):
    # Create a cursor object to execute SQL queries
    mycursor = mydb.cursor()

    # Define a SQL query to retrieve data from the database
    query = "SELECT * FROM TMDefensive WHERE last_updated_at >= '2023-03-03';"

    # Execute the query and fetch the results
    mycursor.execute(query)
    result = mycursor.fetchall()

    # Convert the result into a Pandas DataFrame
    df = pd.DataFrame(result, columns=[i[0] for i in mycursor.description])
    return df
def get_home_passing(mydb):
    # Create a cursor object to execute SQL queries
    mycursor = mydb.cursor()

    # Define a SQL query to retrieve data from the database
    query = "SELECT * FROM TMPassing WHERE last_updated_at >= '2023-03-03';"

    # Execute the query and fetch the results
    mycursor.execute(query)
    result = mycursor.fetchall()

    # Convert the result into a Pandas DataFrame
    df = pd.DataFrame(result, columns=[i[0] for i in mycursor.description])
    return df

def get_home_pass_types(mydb):
    # Create a cursor object to execute SQL queries
    mycursor = mydb.cursor()

    # Define a SQL query to retrieve data from the database
    query = "SELECT * FROM TMPassTypes WHERE last_updated_at >= '2023-03-03';"

    # Execute the query and fetch the results
    mycursor.execute(query)
    result = mycursor.fetchall()

    # Convert the result into a Pandas DataFrame
    df = pd.DataFrame(result, columns=[i[0] for i in mycursor.description])
    return df
def ultimos5jogos(df):
    '''
    df - onde estão os dados
    time - time que você quer ver os últimos 5 jogos
    '''
    return df.iloc[-5:][['gls', 'sot', 'yellow_card', 'offsides', 'corners']]


def main():
    # Set up a connection to the MySQL database
    mydb = mysql.connector.connect(
    host='151.106.96.201',
    user='u815012393_thiago',
    password='Jesussalva123',
    database="u815012393_thiago"
    )
    home_shooting = get_home_shooting(mydb)
    miscellaneous  = get_home_miscellaneuos(mydb)
    defensive  = get_home_defensive(mydb)
    passing  = get_home_passing(mydb)
    pass_types  = get_home_pass_types(mydb)

    df = home_shooting.merge(miscellaneous,on=['squad', 'match_date', 'competition', 'matchweek', 'match_day', 'venue',
        'result_match','opponent']) 
    df = df.merge(defensive,on=['squad', 'match_date', 'competition', 'matchweek', 'match_day', 'venue',
        'result_match','opponent'])
    df = df.merge(passing,on=['squad', 'match_date', 'competition', 'matchweek', 'match_day', 'venue', 'result_match','opponent'])
    df = df.merge(pass_types,on=['squad', 'match_date', 'competition', 'matchweek', 'match_day', 'venue', 'result_match','opponent'])
   
    cols = []
    count = 1
    for column in df.columns:
        if column == 'gf_x':
            cols.append(f'gf_{count}')
            count+=1
            continue
        cols.append(column)
    df.columns = cols

    cols = []
    count = 1
    for column in df.columns:
        if column == 'ga_x':
            cols.append(f'ga_{count}')
            count+=1
            continue
        cols.append(column)
    df.columns = cols
    df_filtrado = df[['squad', 'match_date', 'competition', 'venue', 'result_match', 'matchweek', 'gf_1', 'ga_1', 'opponent',\
       'gls', 'sh', 'sot', 'sot_percentage', 'g_divided_shot', 'g_divided_sot',
       'fk', 'pk', 'pkatt', 'xG', 'np_xg', 'np_xg_divided_shot',
       'goals_minus_expected_goals', 'np_goals_minus_expected_goals',
       'yellow_card', 'red_card', 'second_yellow_card', 'fouls_commited',
       'fouls_draw', 'offsides', 'crosses', 'interceptions_x', 'tackles_won_x',
       'pk_won', 'pk_conceded', 'own_goals', 'ball_recoveries', 'aerial_won',
       'aeria_lost', 'aerial_won_percentage',  'tackles',
       'tackles_won_y', 'blocks', 'interceptions_y',
       'tackles_plus_interceptions', 'clearances', 'errors',
       'pass_cmp', 'pass_att', 'pass_cmp_percentage', 'short_pass_cmp',
       'short_pass_att', 'short_pass_cmp_percentage', 'medium_pass_cmp',
       'medium_pass_att', 'medium_pass_cmp_percentage', 'long_pass_cmp',
       'long_pass_att', 'long_pass_cmp_percentage', 'ast', 'xAG', 'xA', 'kp','pass_live', 'pass_dead', 'pass_fk', 'pass_tb',
       'pass_crosses', 'pass_throw_in', 'pass_corner_kicks', 'corner_kicks_in',
       'corner_outswinging', 'corner_straight'
       ]]
    df_filtrado['corners'] = df_filtrado['corner_kicks_in'] + df_filtrado['corner_outswinging'] + df_filtrado['corner_straight']
    st.write(df_filtrado)
    squads = df_filtrado['squad'].unique().tolist()
    squads.insert(0, '')
    home_team = st.selectbox('Time Casa', squads)
    away_team = st.selectbox('Time Visitante', squads)
    casa_fora = st.selectbox('Casa/Visitante', ['','Home','Away'])
    df_home_team_full = None 
    df_away_team_full = None 
    df_home_team_venue = None 
    df_away_team_venue = None
    if home_team != '':
        df_home_team_full = df_filtrado.query(f"squad == '{home_team}'")
        if casa_fora == 'Home':
            df_home_team_venue = df_home_team_full.query(f"venue == '{casa_fora}'")
        elif casa_fora == 'Away':
            df_home_team_venue = df_home_team_full.query(f"venue == '{casa_fora}'")
    if away_team != '':
        df_away_team_full = df_filtrado.query(f"squad == '{away_team}'")
        if casa_fora == 'Home':
            df_away_team_venue =  df_away_team_full.query(f"venue == 'Away'")
        else:
            df_away_team_venue =  df_away_team_full.query(f"venue == 'Home'")
    col1, col2 = st.columns(2)
    with col1: 
        st.write(f'ultimos 5 jogos time {home_team}')
        st.write(ultimos5jogos(df_home_team_full))
        st.write(f'ultimos 5 jogos {casa_fora} do time {home_team}')
        st.write(ultimos5jogos(df_home_team_venue))
        st.write()
        st.write()
        st.write("Analise Quantis Gerais")
        cols = ['gls','sot','yellow_card','corners']
        ultimos_jogos = ultimos5jogos(df_home_team_full)
        ultimos_jogos = ultimos_jogos[cols].quantile([.1,.25,.5,.75,.90,.99])
        ultimos_jogos.index = ['Safezão +', 'Safe', 'Risco','Arriscado',"Arriscado D+", 'Lunatico']
        st.write(ultimos_jogos)

       
    with col2:
        st.write(f'ultimos 5 jogos time {away_team}')
        st.write(ultimos5jogos(df_away_team_full))
        if casa_fora == 'Home':
            st.write(f'ultimos 5 jogos Away do time {away_team}')
        if casa_fora == 'Away':
            st.write(f'ultimos 5 jogos Home do time {away_team}')
        st.write(ultimos5jogos(df_away_team_venue))
        st.write()
        st.write()
        st.write("Analise Quantis Gerais")
        cols = ['gls','sot','yellow_card','corners']
        ultimos_jogos = ultimos5jogos(df_away_team_full)
        ultimos_jogos = ultimos_jogos[cols].quantile([.1,.25,.5,.75,.90,.99])
        ultimos_jogos.index = ['Safezão +', 'Safe', 'Risco','Arriscado',"Arriscado D+", 'Lunatico']
        st.write(ultimos_jogos)

