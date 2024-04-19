# Importing necessary libraries
import dash
import pandas as pd
from dash import dcc, html, Input, Output, State, dash_table

# # Sample DataFrame of soccer players and stats
# df = pd.DataFrame({
#     "Name": ["Lionel Messi", "Cristiano Ronaldo", "Neymar Jr.", "Kylian Mbappé", "Robert Lewandowski",
#              "Mohamed Salah", "Sadio Mané", "Harry Kane", "Kevin De Bruyne", "Luka Modric",
#              "Sergio Ramos", "Virgil van Dijk", "Jan Oblak", "Alisson Becker", "Thiago Silva"],
#     "Age": [34, 36, 29, 23, 33, 29, 29, 28, 30, 36, 35, 30, 28, 29, 37],
#     "Nationality": ["Argentina", "Portugal", "Brazil", "France", "Poland",
#                     "Egypt", "Senegal", "England", "Belgium", "Croatia",
#                     "Spain", "Netherlands", "Slovenia", "Brazil", "Brazil"],
#     "Club": ["Paris Saint-Germain", "Manchester United", "Paris Saint-Germain", "Paris Saint-Germain", "Bayern Munich",
#              "Liverpool", "Liverpool", "Tottenham Hotspur", "Manchester City", "Real Madrid",
#              "Paris Saint-Germain", "Liverpool", "Atlético Madrid", "Liverpool", "Chelsea"],
#     "Goals": [32, 30, 20, 25, 28, 21, 18, 23, 15, 8, 5, 3, 0, 0, 2],
#     "Assists": [10, 8, 12, 9, 5, 7, 10, 5, 20, 10, 1, 2, 0, 0, 1]
# })


df = pd.read_csv("assets/data/camp_players_info.csv")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    children=[
        html.H1("INP Stats"),
        # Search bar for filtering/sorting the table
        dcc.Input(id="search-input", type="text", placeholder="Search..."),
        # Table displaying soccer players stats
        dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            row_selectable="single",  # Allow selecting only one row at a time
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
        ),
        # Popup for advanced player info
        html.Div(id="player-popup"),
    ]
)


# Define callback to display player popup
@app.callback(
    [Output("player-popup", "children"), Output("player-popup", "style")],
    [Input("table", "selected_rows"), Input("search-input", "value")],
    [State("table", "data")],
)
def display_player_popup(selected_rows, search_value, data):
    filtered_data = data
    if search_value:
        filtered_data = [
            row for row in filtered_data if search_value.lower() in str(row).lower()
        ]

    if selected_rows:
        selected_player = data[selected_rows[0]]
        return html.Div(
            id="player-popup-content",
            children=[
                html.H2(selected_player["person_name"]),
                html.P(f"Age: {selected_player['age']}"),
                html.P(f"Height: {selected_player['height']}"),
                html.P(f"Weight: {selected_player['weight']}"),
                html.P(f"Camp #: {selected_player['camp_number']}"),
                html.P(f"Class: {selected_player['class_year']}"),
            ],
            style={"border": "thin lightgrey solid", "padding": "10px"},
        ), {"display": "block"}
    else:
        return html.Div(), {"display": "none"}


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)  # hot reloading enabled
