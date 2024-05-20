from dash import dash_table

from utils import create_df

# Load the data & format the df
df = create_df()

table = (
    dash_table.DataTable(
        id="table",
        columns=[
            (
                {"name": i, "id": i, "type": "numeric"}
                if i in ["Age", "Height", "Weight", "Camp #"]
                else {"name": i, "id": i}
            )
            for i in df.columns
        ],
        data=df.to_dict("records"),
        sort_action="native",
        filter_action="native",
        sort_mode="multi",
        page_size=100,
        style_as_list_view=True,
        row_selectable="single",  # Allow selecting only one row at a time
        selected_rows=[],
        style_table={"overflowX": "auto"},  # Horizontal scroll
        style_header={
            "backgroundColor": "lightgrey",
            "fontWeight": "bold",
        },  # Header styling
        style_data={"whiteSpace": "normal", "height": "auto"},  # Row styling
        style_cell={"textAlign": "center", "font-family": "arial"},  # Cell alignment
    ),
)
