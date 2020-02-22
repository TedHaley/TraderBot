import requests
import datetime
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd

# API Requests for news div
news_requests = requests.get(
    "https://newsapi.org/v2/top-headlines?sources=bloomberg&apiKey=da8e2e705b914f9f86ed2e9692e66012"
)

stock_api_base = "https://cloud.iexapis.com/"


# API Call to update news
def update_news(news_requests=news_requests):
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url"]])
    max_rows = 10

    return html.Div(
        children=[
            html.Div(
                children=[
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H4(className="p-news",
                                        children="Headlines:",
                                        style={'color': 'dark grey',
                                               'fontSize': 30,
                                               }
                                        ),
                            ),

                            dbc.Col(html.P(className="p-news float-right",
                                           children="Last update : "
                                                    + datetime.datetime.now().strftime("%H:%M:%S"),
                                           style={'color': 'grey',
                                                  'fontSize': 12,
                                                  }
                                           ),
                                    align="end"
                                    ),
                        ]
                    ),
                ],
            ),
            html.Div(
                children=[
                    dbc.Card(
                        html.A(
                            className="td-link",
                            children=df.iloc[i]["title"],
                            href=df.iloc[i]["url"],
                            target="_blank",
                            style={'color': 'grey',
                                   'fontSize': 12,
                                   'marginBottom': '5px',
                                   'marginTop': '5px',
                                   'marginLeft': '5px',
                                   'marginRight': '5px'}
                        ),
                        color="secondary",
                        outline=True,
                        inverse=True,
                        style={'marginBottom': '5px'}
                    ) for i in range(min(len(df), max_rows))
                ],
            )
        ],
    )


if __name__ == "__main__":
    update_news()
