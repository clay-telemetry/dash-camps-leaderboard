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
                    style={'align-items': 'center', 'display': 'flex', 'width': '10vw'},
                ),
                dmc.Group(
                    [
                        dmc.Button(
                            dmc.Anchor(
                                dmc.Text("About", color="white"),
                                href="https://telemetrysports.com/about",
                            ),
                            variant="outline",
                            radius="sm",
                            size="sm",
                            style={'width': '6vw'}
                        ),
                        dmc.Button(
                            dmc.Anchor(
                                dmc.Text("Pro", color="white"),
                                href="https://telemetrysports.com/pro",
                            ),
                            variant="outline",
                            radius="sm",
                            size="sm",
                            style={'width': '5vw'}
                        ),
                        dmc.Button(
                            dmc.Anchor(
                                dmc.Text("College", color="white"),
                                href="https://telemetrysports.com/college",
                            ),
                            variant="outline",
                            radius="sm",
                            size="sm",
                            style={'width': '7vw'}
                        ),
                        dmc.Button(
                            dmc.Anchor(
                                dmc.Text("Recruit", color="white"),
                                href="https://telemetrysports.com/recruit",
                            ),
                            variant="outline",
                            radius="sm",
                            size="sm",
                            style={'width': '7vw'}
                        ),
                        dmc.Button(
                            dmc.Anchor(
                                dmc.Text("Broadcast", color="white"),
                                href="https://telemetrysports.com/broadcast",
                            ),
                            variant="outline",
                            radius="sm",
                            size="sm",
                            style={'width': '8vw'},
                        ),
                        dmc.Button(
                            dmc.Anchor(
                                dmc.Text("Contact Us", color="white"),
                                href="https://telemetrysports.com/contact",
                            ),
                            variant="outline",
                            radius="sm",
                            size="sm",
                            style={'width': '8vw'},
                        ),
                    ],
                    position="right",
                    style={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'wrap', 'width': '50vw'}
                    #spacing="xl",
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
            "align-items": "center",  # Center the content vertically (top and bottom)
            "flex-direction": "row",
            "flex-wrap": "wrap",
            "justify-content": "center",
    },
)
