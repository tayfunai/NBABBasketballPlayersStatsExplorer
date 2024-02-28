import streamlit as st
import pandas as pd
import seaborn as sns
import base64
import matplotlib.pyplot as plt
import numpy as np

st.title("NBA players Stats Explorer")

st.markdown("""
    This app performs simple webscraping of NBA player stats data
    * **Python Libraries:** base64, pandas, streamlit
    * **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/)
""")

st.title("User Input Features")
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2024))))


# Web scraping of NBA players stats
@st.cache_data
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats


playerstats = load_data(selected_year)

# Sidebar team selection

sorted_unique_time = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('team', sorted_unique_time, sorted_unique_time)

# Sidebar - Position selection

unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data

df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header("Display Player stat's of selected teams")
st.write(
    'Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)


# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806

def filedownloader(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href


st.markdown(filedownloader(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')

    corr = df.select_dtypes(include=[float]).corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        fig, ax = plt.subplots()
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(fig)
