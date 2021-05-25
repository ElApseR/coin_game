import dash
import dash_table
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from brownian import Brownian
import argparse

# prepare argparse
parser = argparse.ArgumentParser(description="Args of dash")
parser.add_argument("--max_round", type=int, default=60)
args = parser.parse_args()

# get params
max_round = args.max_round

# minmax value for axis range
max_y = 100
min_y = 100

# read csv for table data
df = pd.read_csv("wishlist.csv").assign(coin_price=100, ranking=1)

# define brownians. not efficient but small people will play
coin_brownian_all = {}
for coin_name in df.loc[:, "coin"]:
    coin_brownian_all[coin_name] = Brownian(seed_value=coin_name).stock_price(
        deltaT=max_round
    )

# define app layout
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        html.H1(children="Coin Market"),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="live-graph", animate=True), className="six columns"
                ),
                html.Div(
                    dash_table.DataTable(
                        id="coin-table",
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict("records"),
                        style_data_conditional=[
                            {
                                "if": {
                                    "filter_query": "{ranking} <= 5",
                                },
                                "backgroundColor": "#1F77B4",
                                "color": "white",
                            },
                            {
                                "if": {
                                    "filter_query": "{ranking} > 5",
                                },
                                "backgroundColor": "#FF7F0E",
                                "color": "white",
                            },
                        ],
                    ),
                    className="six columns",
                ),
            ],
            className="row",
        ),
        dcc.Interval(id="graph-update", interval=2000, n_intervals=0),
    ]
)


@app.callback(
    Output("live-graph", "figure"),
    Output("coin-table", "data"),
    [Input("graph-update", "n_intervals")],
)
def update_graph_scatter(n):
    global max_y, min_y, coin_brownian_all, df
    data_list = []
    current_coin_price = {}
    x_list = list(range(n + 1))
    for coin_name, prices in coin_brownian_all.items():
        # update price
        y_list = prices[: (n + 1)]

        # reset minmax
        last_y = y_list[-1]
        if last_y > max_y:
            max_y = last_y
        elif last_y < min_y:
            min_y = last_y

        # define data to draw
        data_list.append(
            plotly.graph_objs.Scatter(
                x=x_list, y=y_list, name=coin_name, mode="lines+markers"
            )
        )

        # update last price
        current_coin_price[coin_name] = last_y

    # update coin price as current price
    df.loc[:, "coin_price"] = df.coin.map(current_coin_price)
    df = (
        df.sort_values(by="coin_price", ascending=False)
        .reset_index(drop=True)
        .assign(ranking=np.arange(df.shape[0]) + 1)
    )

    return (
        {
            "data": data_list,
            "layout": go.Layout(
                xaxis=dict(range=[0, n + 1]),
                yaxis=dict(range=[min_y, max_y]),
            ),
        },
        df.to_dict("records"),
    )


if __name__ == "__main__":
    app.run_server(debug=True)
