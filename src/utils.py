import pandas as pd
import s3fs


def create_df():
    df = pd.read_csv(
        # "src/assets/data/camp_players_info.csv")
        "s3://scratch.telemetry.fm/ct/CampLeaderboard/camp_players_info.csv")
        # "src/assets/data/ts_office.csv")
        # "src/assets/data/rotated_data.csv")
        # "src/assets/data/EventRegistrationReport.csv", encoding="latin-1")
    df = df[
        [
            "first_name",
            "last_name",
            "height",
            "weight",
            "class_year",
            "school",
            "state",
            "camp_number",
            "position",
            "flexibility_grade",
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
            "height": "Height",
            "weight": "Weight",
            "class_year": "Class",
            "school": "School",
            "state": "State",
            "camp_number": "Camp #",
            "position": "Position",
            "flexibility_grade": "Flexibility Grade",
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
