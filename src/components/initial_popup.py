import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


paragraph1 = """
    Telemetry Sports is a trusted advisor to over 50 NFL and NCAA® teams 
    providing quality sports data technology that produces efficient and 
    winning results. Known for swift and reliable response solutions—Telemetry 
    Sports offers organizations hands-on support built under their own unique 
    banner. 
        """

paragraph2 = """    
    We’re thrilled to announce the acquisition of Telemetry Sports by Teamworks — expanding our capabilities to better serve the unique needs of college football programs.
        """


initial_popup = html.Div(
    children=[
        dmc.Modal(
            id="initial-popup",
            zIndex=10000,
            size="65%",
            children=[
                dmc.Stack([
                    dmc.Anchor(
                        dmc.Image(
                            src="assets/images/teamworks-wordmark.svg",
                            style={"width": "100%", "height": "100%",
                                   "transform": "scale(1.8)"}
                        ), align="center", href="https://teamworks.com"
                    ),
                    dmc.Text("Formerly Known as...",
                             color="grey", size="md", style={"font-style": "italic"}),
                    dmc.Anchor(
                        dmc.Image(
                            src="assets/images/ts-Wordmark-RGB-White.svg",
                            style={"width": "100%", "transform": "scale(0.9)"}
                        ), align="center", href="https://telemetrysports.com"
                    ),
                    html.Br(),
                    dmc.Title("WHO WE ARE", color="#18639d",
                              order=1, ta="center"),
                    dmc.Text(paragraph1, color="white", size="lg",
                             ta='center', style={"width": "85%", "align-items": "center", "justify-content": "center"}),
                    dmc.Text(paragraph2, color="white", size="lg", ta="center", style={
                             "width": "85%", "ailgn-items": "center", "justify-content": "center"}),
                    html.Br(),
                    dmc.Title("Contact Information", order=2,
                              ta="center", color="white"),
                    dmc.Divider(style={"width": 220},
                                color="white"),
                    dmc.Group([
                        dmc.Image(
                            src="assets/images/_thp6137-edit_720.jpg", style={"width": "15%"}),
                        dmc.Stack([
                            dmc.Text("Jay Hood", color="white", size="lg",
                                     style={"font-weight": "bold"}),
                            dmc.Text("Sales Rep & Product Expert",
                                     color="white", size="md"),
                            dmc.Group([
                                html.Div(DashIconify(icon="formkit:email",
                                                     color="#18639d", width=20)),
                                dmc.Text("jay@telemetry.fm",
                                         color="white", size="md")
                            ],  align="center",),
                            dmc.Group([
                                html.Div(DashIconify(
                                    icon="heroicons:phone-solid", color="#18639d", width=20)),
                                dmc.Text("(765) 717-5540",
                                         color="white", size="md"),
                            ], align="center")
                        ]),
                    ], align="center", style={"align-items": "center", "justify-content": "center"}),
                ], align="center")
            ],
            opened=True,
            overlayColor="lightgray",
            centered=True,
            styles={"modal": {"backgroundColor": "#011627",
                              "box-shadow": "3px 3px 5px grey",
                              "border-radius": "15px 15px 15px 15px"}},
        ),
    ],
)
