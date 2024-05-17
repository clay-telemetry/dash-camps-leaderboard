# Importing necessary libraries
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_mantine_components as dmc

import components
from utils import create_df

# Load the data & format the df
df = create_df()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = dmc.MantineProvider(
    html.Div(
        children=[
            components.header,
            dmc.Container(
                fluid=True,
                children=[
                    dmc.Title(
                        "UIndy Camp Player Flexibility Results",
                        order=1,
                        align="center",
                        color="#6c767a",
                        weight="bold",
                        p=15,
                        style={"fontFamily": "Calibri"},
                    ),
                    # Table displaying player stats
                    dcc.Input(id='search-input', type='text', placeholder='Search...'),
                    html.Br(),
                    dash_table.DataTable(
                        id="table",
                        columns=[
                            {"name": i, "id": i, "type": "numeric"} if i in ["Age", "Height", "Weight", "Camp #"] else {"name": i, "id": i} for i in df.columns
                        ],
                        data=df.to_dict("records"),
                        sort_action="native",
                        filter_action="native",
                        sort_mode='multi',
                        page_size=100,
                        style_as_list_view=True,
                        row_selectable="single",  # Allow selecting only one row at a time
                        selected_rows=[],
                        style_table={'overflowX': 'auto'},  # Horizontal scroll
                        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},  # Header styling
                        style_data={'whiteSpace': 'normal', 'height': 'auto'},  # Row styling
                        style_cell={'textAlign': 'center', 'font-family':'arial'},  # Cell alignment
                    ),
                    # Popup for advanced player info
                    components.player_popup,
                ],
            ),
            # TODO add footer
        ]
    )
)


# Define callback to display player popup
@app.callback(
    Output("player-popup", "opened"),
    Output("player-popup", "title"),
    Output("player-popup", "children"),
    Input("table", "selected_rows"),
    State("table", "data"),
    State("player-popup", "opened"),
    prevent_initial_call=True,
)
def display_player_popup(selected_rows, data, opened):
    if selected_rows:
        selected_player = data[selected_rows[0]]
        first_name = selected_player["First Name"]
        last_name = selected_player["Last Name"]
        camp_num = selected_player["Camp #"]
        s3_bucket = selected_player["S3 Bucket"]
        overlay  = selected_player["Overlay Video"]
        class_year = selected_player["Class"]
        ht = selected_player["Height"]
        wt = selected_player["Weight"]
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
                html.H1(f"{first_name} {last_name}", style={"color": "#ffffff", "width": "100%", "text-align": "center"}),
                html.P(f"{camp_num} | {class_year} | HT: {ht} | WT: {wt}", style={"color": "#ffffff"}),
            ], 

            style={"border": "1px solid yellow","font-family": "arial", "font-color": 'white', "background-color": "#011627", "display": "flex", "flex-direction": "row"}
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
            "width": "100%",
            "height": "50%",
            "display":"flex",
            "align-items": "center",
            "justify-content": "center",
            "margin": "0px",
        }
        score_styling = {
            # "border": "1px solid red",
            "width": "100%",
            "height": "50%",
            "display":"flex",
            "align-items": "center",
            "justify-content": "center",
            "margin": "0px",
        }

        player_scores_table = dmc.SimpleGrid(
                    cols=3,
                    spacing="5px",
                    verticalSpacing="5px",
                    children=[
                        html.Div(children=[html.H3("Back to Floor:")], style=div_styling),
                        html.Div(children=[components.set_grade(back_score, "score")], style=score_styling),
                        html.Div(children=[components.set_grade(back_grade, "grade")], style=score_styling),
                        html.Div(children=[html.H3("Shin to Floor:")],style=div_styling),
                        html.Div(children=[components.set_grade(shin_score, "score")],style=score_styling),
                        html.Div(children=[components.set_grade(shin_grade, "grade")],style=score_styling),
                        html.Div(children=[html.H3("Thigh to Floor:")], style=div_styling),
                        html.Div(children=[components.set_grade(thigh_score, "score")], style=score_styling),
                        html.Div(children=[components.set_grade(thigh_grade, "grade")], style=score_styling),
                    ],
                    style={"background-color": "#1e2f3f", "border-radius": "5px", "font-family": "arial",  "box-shadow": "rgba(0, 0, 0, 0.1) 0px 4px 12px", "border":"1px solid red"}
        )

        player_scores_div = html.Div(
            id="player-scores",
            children=[
                # html.H2(f"Flexibility Grade: {flex_score}", style={"text-align": "center", "color": "#ffffff"}),
                # player_grades_table,
                html.H2(f"Flexibility Score: {flex_score}", style={"text-align": "center", "color": "#ffffff"}),
                html.Div(children=[player_scores_table], style={"padding-top": "10px", "border":"1px solid blue"}),
            ],
            style={  "padding": "10px", "width": "60%", "font-family": "arial", "font-color": 'white'},
        )
       
        

        player_popup = html.Div(
            id="player-popup-content",
            children=[
                html.Video(
                    controls=True,
                    # height=500,
                    width="40%",
                    id='video_player',
                    src=video,
                    autoPlay=False,
                    style={ "margin-right": "8px" },
                ),
                player_scores_div
            ],
            style={"padding": "10px", "display": "flex", "flex-direction": "row", "background-color": "#011627"},
        )
        return not opened,player_header, player_popup
    else:
        return not opened, "", html.Div()


@app.callback(
    Output('table', 'data'),
    [Input('search-input', 'value')]
)
def update_table(search_value):
    if search_value:
        filtered_data = df[df.apply(lambda row: search_value.lower() in ' '.join(row.astype(str)).lower(), axis=1)]
        return filtered_data.to_dict('records')
    else:
        return df.to_dict('records')




# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)  # hot reloading enabled
