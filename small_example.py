import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

df = px.data.gapminder().query("year == 2007")

fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent", log_x=True)

app.layout = html.Div([
    html.H1("Life Expectancy vs GDP"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)
