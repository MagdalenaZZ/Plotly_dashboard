import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load dataset
df = px.data.gapminder()

# Initialize app
app = dash.Dash(__name__)
server = app.server  # for deployment

# App layout
app.layout = html.Div([
    html.H1("🌍 Global Development Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Choose a continent:"),
        dcc.Dropdown(
            id="continent-dropdown",
            options=[{"label": c, "value": c} for c in df["continent"].unique()],
            value="Europe",
            clearable=False,
            style={"width": "300px"}
        ),
    ], style={"padding": "10px"}),

    html.Div([
        html.Label("Select a year:"),
        dcc.Slider(
            id="year-slider",
            min=df["year"].min(),
            max=df["year"].max(),
            step=5,
            marks={str(year): str(year) for year in df["year"].unique()},
            value=2007
        ),
    ], style={"padding": "20px"}),

    html.Div([
        html.Div(id="summary-box", style={
            "padding": "10px", "backgroundColor": "#f0f0f0",
            "borderRadius": "8px", "marginBottom": "20px",
            "textAlign": "center", "fontSize": "18px"
        }),
        dcc.Graph(id="scatter-plot")
    ])
])

# Callbacks
@app.callback(
    [Output("scatter-plot", "figure"),
     Output("summary-box", "children")],
    [Input("continent-dropdown", "value"),
     Input("year-slider", "value")]
)
def update_graph(continent, year):
    filtered = df[(df["continent"] == continent) & (df["year"] == year)]

    fig = px.scatter(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="country",
        hover_name="country",
        log_x=True,
        title=f"{continent} in {year}",
        size_max=60
    )

    avg_life = round(filtered["lifeExp"].mean(), 1)
    avg_gdp = round(filtered["gdpPercap"].mean(), 1)

    summary = f"📊 Avg Life Expectancy: {avg_life} years | 💰 Avg GDP: ${avg_gdp}"

    return fig, summary

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
