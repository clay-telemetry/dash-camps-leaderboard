import dash_mantine_components as dmc
from dash import html, Output, Input, State, callback

popup = html.Div(
    [
        dmc.Modal(
            title="Centered Modal",
            id="modal-centered",
            centered=True,
            zIndex=10000,
            children=[dmc.Text("This is a vertically centered modal.")],
        ),
        # dmc.Button("Open modal", id="modal-centered-button"),
    ]
)


