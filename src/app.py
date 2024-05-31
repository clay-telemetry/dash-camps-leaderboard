# Importing necessary libraries
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_mantine_components as dmc
import dash_auth
from dash_iconify import DashIconify
import pandas as pd


import components
from utils import create_df

# Load the data & format the df
df = create_df()

df_filter = pd.DataFrame(
    {
        f'{i}': [None] for i in df.columns.values
    }
)


def generate_position_downloads(pos):
    return (dcc.Download(id=f"download-{pos}-xlsx"))


def generate_position_buttons(pos):
    return dmc.Button(children=[dmc.Text(f'{pos}', color="#18639d", style={"width": "5%"})],
                      rightIcon=DashIconify(
                          icon="material-symbols:download", color="#18639d",),
                      id=f"button-export-{pos}", variant="outline",
                      style={"border-color": "#18639d"})


# usernames and passwords
VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world',
    'user': 'password'
}

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# authorization
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = dmc.MantineProvider(
    html.Div(
        children=[
            components.initial_popup,
            components.header,
            dmc.Container(
                fluid=True,
                children=[
                    dmc.Title(
                        "UINDY CAMP PLAYER FLEXIBILITY RESULTS",
                        order=1,
                        align="center",
                        color="#1e2f3f",
                        weight="bold",
                        p=15,
                        style={"fontFamily": "arial", "font-style": "italic"},
                        td="underline",
                    ),
                    html.Br(),
                    # Table displaying player stats
                    dmc.Group([
                        dcc.Input(id="search-input", type="text", placeholder="Search by player name...", style={
                            'width': '15%', 'textAlign': 'left', 'color': '#1e2f3f', 'lineHeight': '25px'}),
                        dmc.Text(
                            " * CLICK ON A PLAYER BELOW TO VIEW SQUAT VIDEO AND SCORES * ", color="green", style={
                                "font-style": "italic"}, size="md"),
                        dmc.Group(children=[i for i in (generate_position_downloads(i)
                                                        for i in ['DB', 'DL', 'LB', 'OL', 'QB', 'RB', 'TE', 'WR'])],
                                  ),
                        dmc.Group(children=[i for i in (generate_position_buttons(
                            i) for i in ['DB', 'DL', 'LB', 'OL', 'QB', 'RB', 'TE', 'WR'])],
                            position="flex-end",
                            style={"align-items": "flex-end",
                                   "justify-content": "flex-end",
                                   "width": "55%"}
                        ),
                    ]),
                    html.Br(),
                    html.Div([
                        # "table" with only headers and dropdowns
                        dash_table.DataTable(
                            id="table-filter",
                            columns=[
                                {"name": i, "id": i, "presentation": "dropdown"}
                                for i in df_filter.columns if i != "S3 Bucket" and i != "Overlay Video"
                                and i != "Height" and i != "Weight"
                            ],
                            data=df_filter.to_dict("records"),
                            cell_selectable=False,
                            style_as_list_view=True,
                            editable=True,
                            dropdown={
                                col: {
                                    "options": [
                                        {"label": str(i), "value": str(i)}
                                        for i in sorted(df[col].unique())
                                    ],
                                }
                                for col in df.columns if col == "Class" or col == "Position"
                            },
                            sort_action="custom",
                            sort_by=[],
                            sort_mode="multi",
                            style_header={
                                "backgroundColor": "#18639d",
                                "fontWeight": "bold",
                                "font-family": "arial",
                                "color": "white",
                                "lineHeight": "30px",
                                'minWidth': '170px', 'width': '170px', 'maxWidth': '170px',
                                "textAlign": "center",
                            },
                            style_data={
                                "font-family": "arial",
                            },
                            css=[
                                {
                                    "selector": ".dash-spreadsheet .Select-option",
                                    "rule": "color: #1e2f3f",
                                },
                                {
                                    "selector": ".dash-spreadsheet .Select-control:hover .Select-arrow",
                                    "rule": "border-top-color: #1e2f3f"
                                },
                                {
                                    "selector": ".dash-spreadsheet th:hover .column-header--sort",
                                    "rule": "color: #1e2f3f"
                                },
                                {
                                    "selector": ".dash-spreadsheet .Select:hover .Select-clear",
                                    "rule": "color: #1e2f3f"
                                }
                            ],
                        ),
                        dash_table.DataTable(
                            # table with all rows/cells
                            id="table-data",
                            columns=[
                                (
                                    {"name": i, "id": i, "type": "numeric"}
                                    if i in ["Age", "Height", "Weight", "Camp #"]
                                    else {"name": i, "id": i}
                                )
                                for i in df.columns if i != "S3 Bucket" and i != "Overlay Video" and i != "Height" and i != "Weight"
                            ],
                            data=df.to_dict("records"),
                            sort_action="custom",
                            sort_by=[],
                            sort_mode="multi",
                            page_size=100,
                            style_as_list_view=True,
                            cell_selectable=True,
                            selected_rows=[],
                            style_filter={
                                "backgroundColor": "#18639d25", "lineHeight": "30px"},
                            style_data_conditional=[
                                {
                                    "if": {"column_id": "First Name"},
                                    "font-weight": "bold"
                                },
                                {
                                    "if": {"column_id": "Last Name"},
                                    "font-weight": "bold"
                                },
                                {
                                    "if": {"row_index": "even"},
                                    "backgroundColor": "#18639d25",
                                },
                                {
                                    "if": {
                                        "state": "active"
                                    },
                                    "backgroundColor": "rgba(0, 116, 217, 0.3)",
                                    "border": "1px solid rgb(0, 116, 217)",
                                },
                                {
                                    "if": {
                                        "state": "selected"
                                    },
                                    "backgroundColor": "rgba(0, 116, 217, 0.3)",
                                    "border": "1px solid rgb(0, 116, 217)",
                                },

                            ],  # Striped rows
                            style_data={
                                "whiteSpace": "normal",
                                "height": "auto",
                                "lineHeight": "50px",
                                'minWidth': '170px', 'width': '170px', 'maxWidth': '170px',
                            },  # Row styling
                            style_cell={
                                "textAlign": "center",
                                "font-family": "arial",
                            },  # Cell alignment
                            css=[{"selector": "tr:first-child",
                                  "rule": "display: none", }, ],
                        )
                    ], style={"overflowX": "auto"}),

                    # Popup for advanced player info
                    components.player_popup,
                ],
            ),
            html.Br(),
            components.footer,
        ]
    )
)


# custom filtering with dropdowns and sorting
@app.callback(
    Output("table-data", "data", allow_duplicate=True),
    [Input("table-filter", "data_timestamp"),
     Input('table-filter', 'sort_by'),
     Input('table-filter', 'data'),
     Input('table-data', 'data')],
    prevent_initial_call=True,
)
def update_table_dropdown_sort(timestamp, sort_by, filter_rows, current_data):
    if timestamp is None:
        raise dash.exceptions.PreventUpdate
    data = df.copy()
    cols = data.columns

    for col, value in filter_rows[0].items():
        # filtering
        if value is not None:
            data = data[data.astype(str)[col] == value]
        # sorting
        if len(sort_by):
            dff = data.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )
        else:
            dff = data

    return dff.to_dict("records")


# sort without filter callback
@app.callback(
    Output('table-data', 'data', allow_duplicate=True),
    Input('table-filter', 'sort_by'),
    State('table-data', 'data'),
    prevent_initial_call=True,
)
def sort(sort_by, tabledata):
    data = pd.DataFrame(tabledata)
    if len(sort_by):
        dff = data.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    else:
        dff = data

    return dff.to_dict("records")


# export positions to excel function
def export_to_excel(pos):
    writer = pd.ExcelWriter(f'{pos}_sheet.xlsx', engine='xlsxwriter')
    filtered_df = df[df['Position'] == pos]
    filtered_df = filtered_df.drop(['S3 Bucket', 'Overlay Video'], axis=1)
    filtered_df.to_excel(writer, sheet_name=f'{pos}_Sheet')
    writer.close()
    return dcc.send_file(f'{pos}_sheet.xlsx')


# position group export to excel callbacks
@app.callback(
    Output('download-DB-xlsx', 'data'),
    Input('button-export-DB', 'n_clicks'),
    prevent_initial_call=True
)
def callback_DB(n):
    return export_to_excel("DB")


@app.callback(
    Output('download-DL-xlsx', 'data'),
    Input('button-export-DL', 'n_clicks'),
    prevent_initial_call=True
)
def callback_DL(n):
    return export_to_excel("DL")


@app.callback(
    Output('download-LB-xlsx', 'data'),
    Input('button-export-LB', 'n_clicks'),
    prevent_initial_call=True
)
def callback_LB(n):
    return export_to_excel("LB")


@app.callback(
    Output('download-OL-xlsx', 'data'),
    Input('button-export-OL', 'n_clicks'),
    prevent_initial_call=True
)
def callback_OL(n):
    return export_to_excel("OL")


@app.callback(
    Output('download-QB-xlsx', 'data'),
    Input('button-export-QB', 'n_clicks'),
    prevent_initial_call=True
)
def callback_QB(n):
    return export_to_excel("QB")


@app.callback(
    Output('download-RB-xlsx', 'data'),
    Input('button-export-RB', 'n_clicks'),
    prevent_initial_call=True
)
def callback_RB(n):
    return export_to_excel("RB")


@app.callback(
    Output('download-TE-xlsx', 'data'),
    Input('button-export-TE', 'n_clicks'),
    prevent_initial_call=True
)
def callback_TE(n):
    return export_to_excel("TE")


@app.callback(
    Output('download-WR-xlsx', 'data'),
    Input('button-export-WR', 'n_clicks'),
    prevent_initial_call=True
)
def callback_WR(n):
    return export_to_excel("WR")


# Define callback to display player popup on cell click and highlight selected row
@app.callback(
    Output("player-popup", "opened"),
    Output("table-data", "style_data_conditional"),
    Output("player-popup", "children"),
    Input("table-data", "selected_cells"),
    Input("table-data", "active_cell"),
    State("table-data", "data"),
    State("player-popup", "opened"),
    prevent_initial_call=True,
)
def display_player_popup(selected_cells, active_cell, data, opened):

    style = [
        {
            "if": {
                "column_id": "First Name",
            },
            "font-weight": "bold",
        },
        {
            "if": {
                "column_id": "Last Name",
            },
            "font-weight": "bold",
        },
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#18639d25",
        },
        {
            "if": {
                "state": "active"  # 'active' | 'selected'
            },
            "backgroundColor": "rgba(0, 116, 217, 0.3)",
            "border": "1px solid rgb(0, 116, 217)",
        },
        {
            "if": {
                "state": "selected"  # 'active' | 'selected'
            },
            "backgroundColor": "rgba(0, 116, 217, 0.3)",
            "border": "1px solid rgb(0, 116, 217)",
        },
    ]
    if active_cell != None:
        style.append(
            {
                "if": {"row_index": active_cell["row"]},
                "backgroundColor": "rgba(0, 116, 217, 0.3)",
                "border": "1px solid rgb(0, 116, 217)",
            },
        )

    if selected_cells and active_cell != None:
        selected_player = data[selected_cells[0]['row']]
        first_name = selected_player["First Name"]
        last_name = selected_player["Last Name"]
        camp_num = selected_player["Camp #"]
        s3_bucket = selected_player["S3 Bucket"]
        overlay = selected_player["Overlay Video"]
        class_year = selected_player["Class"]
        ht = selected_player["Height"]
        wt = selected_player["Weight"]
        pos = selected_player["Position"]
        flex_score = selected_player["Flexibility Score"]
        back_grade = selected_player["Back to Floor Grade"]
        shin_grade = selected_player["Shin to Floor Grade"]
        thigh_grade = selected_player["Thigh to Floor Grade"]
        back_score = selected_player["Back to Floor Score"]
        shin_score = selected_player["Shin to Floor Score"]
        thigh_score = selected_player["Thigh to Floor Score"]
        video = f"https://{s3_bucket}.s3.amazonaws.com/{overlay}"

        # Popup should be video of player
        player_header = html.Div(
            id="player-popup-header",
            children=[
                dmc.Group([
                    dmc.Title(
                        f"{first_name} {last_name}", td="underline",
                        style={"color": "#ffffff", "text-align": "center",
                               "width": "100%", "margin": "5px", "font-style": "italic"},
                    ),
                    html.H2(
                        f"#{camp_num} | YR: {class_year} | POS: {pos} | SCHOOL:  | STATE: ",
                        style={"color": "#ffffff", "text-align": "center",
                               "width": "100%", "margin": "5px"},
                    ),
                ], align="center"),
            ],
            style={
                "border-style": "solid",
                "border-color": "#18639d",
                "font-family": "arial",
                "font-color": "white",
                "background-color": "#011627",
                "display": "flex",
                "flex-direction": "row",
                "padding": "10px",
                'minWidth': '400px', 'width': '400px', 'maxWidth': '400px',
                'minHeight': '200px', 'height': '200px', 'maxHeight': '200px',
                "border-radius": "5px"
            },
        )

        div_styling = {
            "color": "#ffffff",
            "text-align": "center",
            "width": "150%",
            "height": "100%",
            "display": "flex",
            "align-items": "center",
            "justify-content": "center",
            "margin": "0px",
        }
        score_styling = {
            "width": "150%",
            "height": "100%",
            "display": "flex",
            "align-items": "center",
            "justify-content": "center",
            "margin": "0px",
        }

        player_scores_table = dmc.SimpleGrid(
            cols=3,
            spacing="5px",
            verticalSpacing="5px",
            children=[
                html.Div(children=[html.H2("Back to Floor:")],
                         style=div_styling),
                html.Div(
                    children=[components.set_grade(back_score, "score")],
                    style=score_styling,
                ),
                html.Div(
                    children=[components.set_grade(back_grade, "grade")],
                    style=score_styling,
                ),
                html.Div(children=[html.H2("Shin to Floor:")],
                         style=div_styling),
                html.Div(
                    children=[components.set_grade(shin_score, "score")],
                    style=score_styling,
                ),
                html.Div(
                    children=[components.set_grade(shin_grade, "grade")],
                    style=score_styling,
                ),
                html.Div(children=[html.H2("Thigh to Floor:")],
                         style=div_styling),
                html.Div(
                    children=[components.set_grade(thigh_score, "score")],
                    style=score_styling,
                ),
                html.Div(
                    children=[components.set_grade(thigh_grade, "grade")],
                    style=score_styling,
                ),
            ],
            style={
                "border-radius": "5px",
                "font-family": "arial",
                "box-shadow": "rgba(0, 0, 0, 0.1) 0px 4px 12px",
                "align-items": "center",
            },
        )

        player_scores_div = html.Div(
            id="player-scores",
            children=[
                dmc.Group(
                    [html.H1("Flexibility Score:", style={"text-align": "center", "color": "#ffffff"}),
                     components.set_grade(flex_score, "flex")], position="center"),
                html.Div(
                    children=[player_scores_table],
                ),
            ],
            style={
                "padding": "10px",
                "font-family": "arial",
                "font-color": "white",
                "border-style": "solid",
                "border-color": "#18639d",
                "background-color": "#011627",
                'minWidth': '400px', 'width': '400px', 'maxWidth': '400px',
                'minHeight': '300px', 'height': '300px', 'maxHeight': '300px',
                "align-items": "center",
                "justify-content": "center",
                "border-radius": "5px"
            },
        )

        logo_div = html.Div(
            id="logo",
            children=[
                dmc.Stack([
                    dmc.Anchor(
                        dmc.Image(
                            src="assets/images/TS-Horizontal-RGB-Inverse.svg"),
                        href="https://telemetrysports.com/",
                        style={'align-items': 'center',
                               'justify-content': 'center',
                               'minHeight': '80px', 'height': '80px', 'maxHeight': '80px',
                               'minWidth': '130px', 'width': '130px', 'maxWidth': '130px'
                               }
                    ),
                    dmc.Button(
                        dmc.Anchor(
                            dmc.Text("Contact Us", color="white"),
                            href="https://telemetrysports.com/contact",
                        ),
                        variant="outline",
                        radius="sm",
                        size="sm",
                        style={"margin-top": "10px",
                               "border-color": "white"}
                    ),
                ], align="center"
                ),
            ],
            style={
                'minWidth': '400px', 'width': '400px', 'maxWidth': '400px',
                'minHeight': '160px', 'height': '160px', 'maxHeight': '160px',
                "align-items": "center",
                "justify-content": "center",
                "padding": "10px",
            },
        )

        player_popup = html.Div(
            id="player-popup-content",
            children=[
                dmc.Group(
                    [
                        html.Video(
                            controls=True,
                            width="40%",
                            id="video_player",
                            src=video,
                            autoPlay=False,
                            style={"margin-right": "8px",
                                   "border-radius": "5px"},
                        ),
                        dmc.Stack([
                            player_header,
                            player_scores_div,
                            logo_div,
                        ])
                    ], position="center",
                ),
            ],
            style={
                "padding": "10px",
                "display": "flex",
                "flex-direction": "row",
                "background-color": "#011627",
            },
        )
        return not opened, style, player_popup
    else:
        return opened, style, html.Div()


# player search bar callback
@ app.callback(Output("table-data", "data"), [Input("search-input", "value")])
def update_table_search(search_value):
    if search_value:
        filtered_data = df[
            df.apply(
                lambda row: search_value.lower() in row["First Name"].lower(
                ) or search_value.lower() in row["Last Name"].lower(),
                axis=1
            )
        ]
        return filtered_data.to_dict("records")
    else:
        return df.to_dict("records")


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)  # hot reloading enabled
