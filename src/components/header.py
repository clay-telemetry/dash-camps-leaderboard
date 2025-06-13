import dash_mantine_components as dmc

header = dmc.Header(
    height=65,
    children=[
        dmc.Group(
            [
                dmc.Group(
                    [
                        dmc.Anchor(
                            dmc.Image(
                                src="assets/images/TS-Wordmark-RGB-White.svg"),
                            href="https://telemetrysports.com/",
                        )
                    ],
                    position="left",
                    style={'align-items': 'center',
                           'display': 'flex', 'width': '10vw'},
                ),
                dmc.Group(
                    [
                        dmc.Anchor(
                            dmc.Button(
                                dmc.Text("About", color="white"),
                                variant="outline",
                                radius="sm",
                                size="sm",
                                style={'width': '6vw'}
                            ),
                            href="https://telemetrysports.com/about",
                        ),
                        dmc.Anchor(
                            dmc.Button(
                                dmc.Text("Pro", color="white"),
                                variant="outline",
                                radius="sm",
                                size="sm",
                                style={'width': '5vw'}
                            ),
                            href="https://telemetrysports.com/nfl/pro",
                        ),
                        dmc.Anchor(
                            dmc.Button(
                                dmc.Text("College", color="white"),
                                variant="outline",
                                radius="sm",
                                size="sm",
                                style={'width': '7vw'}
                            ),
                            href="https://telemetrysports.com/cfb/college",
                        ),
                        dmc.Anchor(
                            dmc.Button(
                                dmc.Text("Recruit", color="white"),
                                variant="outline",
                                radius="sm",
                                size="sm",
                                style={'width': '7vw'}
                            ),
                            href="https://telemetrysports.com/cfb/recruit",
                        ),
                        dmc.Anchor(
                            dmc.Button(
                                dmc.Text("Broadcast", color="white"),
                                variant="outline",
                                radius="sm",
                                size="sm",
                                style={'width': '8vw'}
                            ),
                            href="https://telemetrysports.com/broadcast",
                        ),
                        dmc.Anchor(
                            dmc.Button(
                                dmc.Text("Contact Us", color="white"),
                                variant="outline",
                                radius="sm",
                                size="sm",
                                style={'width': '8vw'}
                            ),
                            href="https://telemetrysports.com/contact",
                        ),
                    ],
                    position="right",
                    style={'display': 'flex', 'flex-direction': 'row',
                           'flex-wrap': 'wrap', 'width': '50vw'}
                ),
            ],
            grow=True,
            p=10,
            style={
                "display": "flex",  # Use Flexbox layout
                "width": "100%",  # Stretch container to 100% of the page width
                "height": "100%",  # Stretch container to 100% of the page width
                "flex-direction": "row",
            },
        )
    ],
    style={"backgroundColor": "#1e2f3f",
           "display": "flex",  # Use Flexbox layout
           # Center the content vertically (top and bottom)
           "align-items": "center",
           "flex-direction": "row",
           "flex-wrap": "wrap",
           "justify-content": "center",
           },
)
