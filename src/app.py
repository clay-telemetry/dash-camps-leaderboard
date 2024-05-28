# Importing necessary libraries
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_mantine_components as dmc
import dash_auth
from dash_iconify import DashIconify


import components
#from src.utils import create_df
from utils import create_df

# Load the data & format the df
df = create_df()

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
                            " * CLICK ON A PLAYER BELOW TO VIEW SQUAT VIDEO AND SCORES * ", color="green", style={"font-style": "italic"}, size="lg"),
                    ]),
                    html.Br(),
                    dash_table.DataTable(
                        id="table",
                        columns=[
                            (
                                {"name": i, "id": i, "type": "numeric"}
                                if i in ["Age", "Height", "Weight", "Camp #"]
                                else {"name": i, "id": i}
                            )
                            for i in df.columns if i != "S3 Bucket" and i != "Overlay Video"
                        ],
                        data=df.to_dict("records"),
                        sort_action="custom",
                        sort_by=[],
                        filter_action="native",
                        sort_mode="multi",
                        page_size=100,
                        style_as_list_view=True,
                        cell_selectable=True,
                        selected_rows=[],
                        style_table={"overflowX": "auto"},  # Horizontal scroll
                        style_filter={
                            "backgroundColor": "#18639d25", "lineHeight": "30px"},
                        style_header={
                            "backgroundColor": "#18639d",
                            "fontWeight": "bold",
                            "color": "white",
                            "lineHeight": "30px",

                        },  # Header styling
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

                        ],  # Striped rows
                        style_data={
                            "whiteSpace": "normal",
                            "height": "auto",
                            "lineHeight": "50px",
                            'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                        },  # Row styling
                        style_cell={
                            "textAlign": "center",
                            "font-family": "arial",
                        },  # Cell alignment
                    ),
                    # Popup for advanced player info
                    components.player_popup,
                ],
            ),
            # TODO add footer
            html.Br(),
            components.footer,
        ]
    )
)


# custom sort
@ app.callback(
    Output('table', "data", allow_duplicate=True),
    Input('table', "sort_by"),
    prevent_initial_call=True)
def update_table(sort_by):
    if len(sort_by):
        dff = df.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = df

    return dff.to_dict('records')


# Define callback to display player popup on cell click and highlight selected row
@app.callback(
    Output("player-popup", "opened"),
    Output("table", "style_data_conditional"),
    Output("player-popup", "children"),
    Input("table", "selected_cells"),
    Input("table", "active_cell"),
    State("table", "data"),
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

        # age = selected_player["Age"]
        video = f"https://{s3_bucket}.s3.amazonaws.com/{overlay}"
        # Title shoudl be the player name and base info
        # player_name_title = (
        #     f"{selected_player['First Name']} {selected_player['Last Name']}"
        # )
        # camp_number = html.Div(
        #     id="camp-number",
        #     children=[
        #         html.P(f"{camp_num}")
        #     ],
        #     style={"font-size": "1.5em", "font-weight": "bold", "background-color": "lightgrey" })

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
                    html.H1(
                        f"#{camp_num} | YR: {class_year} | POS: {pos} | HT: {ht} | WT: {wt}",
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
            },
        )

        # player_grades_table = dmc.SimpleGrid(
        #             cols=2,
        #             spacing="xs",
        #             verticalSpacing="xs",
        #             children=[
        #                 html.Div(children=[html.H3("Back to Floor Grade:", style={"color": "#ffffff", "text-align": "center"})]),
        #                 html.Div(children=[components.set_grade(back_grade, "grade")]),
        #                 html.Div(children=[html.H3("Shin to Floor Grade:", style={"color": "#ffffff", "text-align": "center"})]),
        #                 html.Div(children=[components.set_grade(shin_grade, "grade")]),
        #                 html.Div(children=[html.H3("Thigh to Floor Grade:", style={"color": "#ffffff", "text-align": "center"})]),
        #                 html.Div(children=[components.set_grade(thigh_grade, "grade")]),
        #             ],
        #             style={"background-color": "#1e2f3f", "padding": "10px", "border-radius": "5px", "font-family": "arial", "margin-top": "40px", "box-shadow": "rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px,rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px"}
        # )

        div_styling = {
            "color": "#ffffff",
            "text-align": "center",
            # "border": "1px solid red",
            "width": "150%",
            "height": "100%",
            "display": "flex",
            "align-items": "center",
            "justify-content": "center",
            "margin": "0px",
        }
        score_styling = {
            # "border": "1px solid red",
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
                # html.H2(f"Flexibility Grade: {flex_score}", style={"text-align": "center", "color": "#ffffff"}),
                # player_grades_table,
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
            },
        )

        logo_div = html.Div(
            id="logo",
            children=[
                dmc.Stack([
                    dmc.Anchor(
                        dmc.Image(
                            src="src/assets/images/TS-Horizontal-RGB-Inverse.svg"),
                        href="https://telemetrysports.com/",
                        style={'align-items': 'center',
                               'justify-content': 'center',
                               # 'height': 'auto',
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
                            # height=500,
                            width="40%",
                            id="video_player",
                            src=video,
                            autoPlay=False,
                            style={"margin-right": "8px"},
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


@ app.callback(Output("table", "data"), [Input("search-input", "value")])
def update_table_search(search_value):
    if search_value:
        filtered_data = df[
            # df.apply(
            #     lambda row: search_value.lower() in " ".join(row.astype(str)).lower(),
            #     axis=1,
            # )
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
