from dash import html


def set_grade(grade, scoreGrade):

    # Green 1bcc67 A
    # Light G a9fc7c B
    # Yellow FFEA00 C
    # Orange FFA500 D
    # Red FF0000 F
    background_color = "#000000"
    font_color = "#FFFFFF"
    border_color = "#000000"

    if scoreGrade == "grade":
        if "A" in grade:
            background_color = "#1bcc67"
            font_color = "black"
        elif "B" in grade:
            background_color = "#a9fc7c"
            font_color = "black"
        elif "C" in grade:
            background_color = "#FFEA00"
            font_color = "black"
        elif "D" in grade:
            background_color = "#FFA500"
            font_color = "black"
        elif "F" in grade:
            background_color = "#FF0000"
            font_color = "black"

        return html.H3(
            f"{grade}",
            style={
                "background-color": background_color,
                "color": font_color,
                "border-radius": "5px",
                "text-align": "center",
                "width": "30%",
            },
        )
    elif scoreGrade == "score":
        if grade >= 80:
            background_color = "#1bcc67"
            font_color = "black"
        elif grade >= 60:
            background_color = "#a9fc7c"
            font_color = "black"
        elif grade >= 40:
            background_color = "#FFEA00"
            font_color = "black"
        elif grade >= 20:
            background_color = "#FFA500"
            font_color = "black"
        elif grade < 20:
            background_color = "#FF0000"
            font_color = "black"

        return html.H3(
            f"{grade}",
            style={
                "background-color": background_color,
                "color": font_color,
                "border-radius": "5px",
                "text-align": "center",
                "width": "30%",
            },
        )
    elif scoreGrade == "flex":
        if grade >= 80:
            border_color = "#1bcc67"
        elif grade >= 60:
            border_color = "#a9fc7c"
        elif grade >= 40:
            border_color = "#FFEA00"
        elif grade >= 20:
            border_color = "#FFA500"
        elif grade < 20:
            border_color = "FF0000"

        return html.H2(
            f"{grade}",
            style={
                "border-color": border_color,
                "border-style": "solid",
                "border-radius": "5px",
                "text-align": "center",
                "color": "#ffffff",
                "width": "25%",
            }
        )
