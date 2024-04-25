# Importing necessary libraries
import dash
from dash import dcc, html, Input, Output, State, dash_table, callback
import dash_mantine_components as dmc

import components


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
                        style={"fontFamily": "ITC Franklin Gothic"},
                    ),
                    # Table displaying player stats
                    components.grid,
                    # dash_table.DataTable(
                    #     id="table",
                    #     columns=[
                    #         {"name": i, "id": i}
                    #         for i in df.columns
                    #         if i not in ["S3 Bucket", "Overlay Video"]
                    #     ],
                    #     data=df.to_dict("records"),
                    #     row_selectable="single",  # Allow selecting only one row at a time
                    #     style_table={"overflowX": "auto"},
                    #     style_cell={"textAlign": "center"},
                    # ),
                    # Popup for advanced player info
                    components.popup,
                ],
            ),
            # TODO add footer
        ]
    )
)


@callback(
    Output("modal-centered", "opened"),
    # Input("modal-centered-button", "n_clicks"),
    Input("table", "selected_rows"),
    State("modal-centered", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    return not opened

# Define callback to display player popup
# @app.callback(
#     Output("player-popup", "opened"),
#     Output("player-popup", "title"),
#     Output("player-popup", "children"),
#     Input("table", "selected_rows"),
#     State("table", "data"),
#     State("player-popup", "opened"),
#     prevent_initial_call=True,
# )
# def display_player_popup(selected_rows, data, opened):
#     if selected_rows:
#         selected_player = data[selected_rows[0]]
#         player_name_title = (
#             f"{selected_player['First Name']} {selected_player['Last Name']}"
#         )
#         player_popup = html.Div(
#             id="player-popup-content",
#             children=[
#                 html.P(f"Age: {selected_player['Age']}"),
#                 html.P(f"Height: {selected_player['Height']}"),
#                 html.P(f"Weight: {selected_player['Weight']}"),
#                 html.P(f"Camp #: {selected_player['Camp #']}"),
#                 html.P(f"Class: {selected_player['Class']}"),
#             ],
#             style={"border": "thin lightgrey solid", "padding": "10px"},
#         )
#         return not opened, player_name_title, player_popup
#     else:
#         return not opened, "", html.Div()



# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)  # hot reloading enabled
