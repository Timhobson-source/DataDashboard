import datetime as dt

import pandas as pd
import plotly.express as px
from dash import html, Dash, dash_table, dcc, Output, Input

app = Dash(
    __name__, external_stylesheets=["app.css"]
)

all_data_types = ['futures', 'options']
colors = {"background": "#011833", "text": "#7FDBFF"}
columns = [
    {'id': 'name', 'name': 'Contract Name'},
    {'id': 'last available date', 'name': 'Last Available Date'},
    {'id': 'days missing', 'name': 'Days Missing'}
]


def get_data(datatype: str):
    latest_date = dt.date.today()

    df = pd.read_csv(f'db/{datatype}_data.csv')
    df.date = pd.to_datetime(df.date)
    data = []
    for contract, contract_data in df.groupby('name'):
        last_date = contract_data.date.max()
        missing = last_date.date() < latest_date
        if missing:
            days_missing = (latest_date - last_date.date()).days
            data.append(
                {
                    'name': contract,
                    'last available date': last_date,
                    'days missing': days_missing
                }
            )

    return data


app.layout = html.Div(
    [
        html.H1("My Data Dashboard - Home"),
        html.H2("Missing data:"),
        html.H3("Futures"),
        dash_table.DataTable(
            id='futures_stable',
            data=get_data('futures'),
            columns=columns,
            style_header={
                'backgroundColor': '#25597f',
                'color': 'white',
                'fontFamily': 'Gill Sans'
            },
            style_table={
                'maxHeight': '50ex',
                'width': '100%',
                'minWidth': '100%',
            },
            style_cell={
                'color': 'black',
                'fontFamily': 'Gill Sans',
                'textAlign': 'center',
                'height': '20px',
                'padding': '2px 4px',
                'whiteSpace': 'inherit',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
        ),
        html.H3("Options"),
        dash_table.DataTable(
            id='option_stable',
            data=get_data('options'),
            columns=columns,
            style_header={
                'backgroundColor': '#25597f',
                'color': 'white',
                'fontFamily': 'Gill Sans'
            },
            style_table={
                'maxHeight': '50ex',
                'width': '100%',
                'minWidth': '100%',
            },
            style_cell={
                'color': 'black',
                'fontFamily': 'Gill Sans',
                'textAlign': 'center',
                'height': '20px',
                'padding': '2px 4px',
                'whiteSpace': 'inherit',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
        ),
        dcc.RadioItems(
            id='pc-missing-piechart-type',
            options=[
                {'label': i, 'value': i}
                for i in ['options', 'futures', 'all']
            ],
            value='all',  # default value
            labelStyle={'display': 'inline-block'},
            className='radio'
        ),
        html.Div(
            dcc.Graph(id="pc-missing-piechart", className="chart")
        )
    ],
    className="container"
)


@app.callback(
    Output('pc-missing-piechart', 'figure'),
    [Input('pc-missing-piechart-type', 'value')]
)
def get_missing_piechart(data_type):
    latest_date = dt.date.today()

    data = []
    for dtype in all_data_types:
        if dtype == data_type or data_type == 'all':
            df = pd.read_csv(f'db/{dtype}_data.csv')
            df.date = pd.to_datetime(df.date)
            for contract, contract_data in df.groupby('name'):
                last_date = contract_data.date.max()
                missing = last_date.date() < latest_date
                status = 'missing' if missing else 'up to date'
                data.append(
                    {
                        'datatype': dtype,
                        'contract': contract,
                        'up_to_date': status
                    }
                )

    fig = px.pie(
        pd.DataFrame(data),
        names='up_to_date',
        title='Percentage Missing Data'
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
