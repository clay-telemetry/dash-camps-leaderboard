import pandas as pd


def create_df():
    df = pd.read_csv("assets/data/camp_players_info.csv")
    df = df[
        [
            "first_name",
            "last_name",
            "age",
            "height",
            "weight",
            "class_year",
            "camp_number",
            "position",
            "flexibility_score",
            "angles.shin_to_floor",
            "angles.thigh_to_floor",
            "angles.back_to_floor",
            "scores.shin_to_floor",
            "scores.thigh_to_floor",
            "scores.back_to_floor",
            "grades.shin_to_floor",
            "grades.thigh_to_floor",
            "grades.back_to_floor",
            "s3_bucket",
            "overlay_video",
        ]
    ]
    df = df.rename(
        columns={
            "first_name": "First Name",
            "last_name": "Last Name",
            "age": "Age",
            "height": "Height",
            "weight": "Weight",
            "class_year": "Class",
            "camp_number": "Camp #",
            "position": "Position",
            "flexibility_score": "Flexibility Score",
            "angles.shin_to_floor": "Shin to Floor Angle",
            "angles.thigh_to_floor": "Thigh to Floor Angle",
            "angles.back_to_floor": "Back to Floor Angle",
            "scores.shin_to_floor": "Shin to Floor Score",
            "scores.thigh_to_floor": "Thigh to Floor Score",
            "scores.back_to_floor": "Back to Floor Score",
            "grades.shin_to_floor": "Shin to Floor Grade",
            "grades.thigh_to_floor": "Thigh to Floor Grade",
            "grades.back_to_floor": "Back to Floor Grade",
            "s3_bucket": "S3 Bucket",
            "overlay_video": "Overlay Video",
        }
    )
    return df
