import dash_mantine_components as dmc
from dash_iconify import DashIconify


footer = dmc.Footer(
    height=265,
    children=[
        dmc.Center(
            [
                # left side of footer - logo and socials links
                dmc.Center(
                    dmc.Stack(
                        [
                            dmc.Anchor(
                                dmc.Image(
                                    src="src/assets/images/TS-Vertical-Main-RGB-Inverse.svg",
                                ),
                                href="https://telemetrysports.com/",
                            ),
                            dmc.Group(
                                [
                                    dmc.Anchor(DashIconify(
                                        icon="bxl:twitter", width=30, color="white"), href="https://twitter.com/telemetrysports"),
                                    dmc.Anchor(DashIconify(icon="bxl:instagram", width=30, color="white"),
                                               href="https://www.instagram.com/telemetrysports/?hl=en"),
                                    dmc.Anchor(DashIconify(icon="bxl:linkedin-square", width=30, color="white"),
                                               href="https://www.linkedin.com/company/telemetry-sports/"),
                                    dmc.Anchor(DashIconify(
                                        icon="bxl:tiktok", width=30, color="white"), href="https://www.tiktok.com/@telemetrysports"),
                                ], align="center",
                            )
                        ], align="center",
                    ),
                    style={"width": "20%"},
                ),
                dmc.Divider(orientation="vertical", style={
                            "height": 220}, color="#18639d"),
                # middle footer - links
                dmc.Center(
                    dmc.Stack(
                        [
                            dmc.Title("PRODUCTS", color="#18639d", order=3),
                            dmc.Anchor(
                                dmc.Text("PRO", color="white", weight="bold"),
                                href="https://telemetrysports.com/pro",
                            ),
                            dmc.Anchor(
                                dmc.Text("COLLEGE", color="white",
                                         weight="bold"),
                                href="https://telemetrysports.com/college",
                            ),
                            dmc.Anchor(
                                dmc.Text("RECRUIT", color="white",
                                         weight="bold"),
                                href="https://telemetrysports.com/recruit",
                            ),
                            dmc.Anchor(
                                dmc.Text("BROADCAST", color="white",
                                         weight="bold"),
                                href="https://telemetrysports.com/broadcast",
                            )
                        ], align="center",
                    ),
                    style={"width": "15%"}
                ),
                dmc.Divider(orientation="vertical", style={
                            "height": 220}, color="#18639d"),
                # right side of footer - demo/contact
                dmc.Center(
                    dmc.Stack(
                        [
                            dmc.Text("Ready for a demo?",
                                     color="#18639d", weight="bold"),
                            dmc.Text(
                                "Let's schedule some time and see how we can customize our tools to help you!", color="white", align="center"),
                            dmc.Button(
                                dmc.Anchor(
                                    dmc.Text("CONTACT US", color="white"),
                                    href="https://telemetrysports.com/contact",
                                ),
                                variant="filled",
                                radius="sm",
                                size="md",
                                color="#18639d",
                            )
                        ], align="center",
                    ),
                    style={"width": "20%"}
                )
            ],
            p=10,
        )
    ],
    style={"backgroundColor": "#1e2f3f"},
)
