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
                                src="src/assets/images/TS-Wordmark-RGB-White.svg",
                            ),
                            href="https://telemetrysports.com/",
                        )
                    ],
                    position="left",
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
                            size="md",
                        ),
                        dmc.Button(
                            dmc.Anchor(
                                dmc.Text("Pro", color="white"),
                                href="https://telemetrysports.com/pro",
                            ),
                            variant="outline",
                            radius="sm",
                            size="md",
                        ),
                        dmc.Button(
                            dmc.Anchor(
                                dmc.Text("College", color="white"),
                                href="https://telemetrysports.com/college",
                            ),
                            variant="outline",
                            radius="sm",
                            size="md",
                        ),
                        dmc.Button(
                            dmc.Anchor(
                                dmc.Text("Recruit", color="white"),
                                href="https://telemetrysports.com/recruit",
                            ),
                            variant="outline",
                            radius="sm",
                            size="md",
                        ),
                        dmc.Button(
                            dmc.Anchor(
                                dmc.Text("Broadcast", color="white"),
                                href="https://telemetrysports.com/broadcast",
                            ),
                            variant="outline",
                            radius="sm",
                            size="md",
                        ),
                        dmc.Button(
                            dmc.Anchor(
                                dmc.Text("Contact Us", color="white"),
                                href="https://telemetrysports.com/contact",
                            ),
                            variant="outline",
                            radius="sm",
                            size="md",
                        ),
                    ],
                    position="right",
                    spacing="xl",
                ),
            ],
            grow=True,
            p=10,
        )
    ],
    style={"backgroundColor": "#1e2f3f"},
)
