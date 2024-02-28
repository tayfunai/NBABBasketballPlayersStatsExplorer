import pandas as pd

url = "https://www.basketball-reference.com/leagues/NBA_" + "2020" + "_per_game.html"
html = pd.read_html(url, header=0)
df = html[0]
raw = df.drop(df[df.Age == 'Age'].index)
print(raw)