import dash_mantine_components as dmc 
from dash import html        


player_popup = html.Div(
    children=[
        dmc.Modal(title="test", id="player-popup", zIndex=10000,size="65%", children=[], opened=False, overlayColor="lightgray", styles={"modal": {"backgroundColor": "#011627"}}),
    ],
    # style={"background-color": "#011627"} 

)
