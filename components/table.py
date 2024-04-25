import dash_mantine_components as dmc
from dash_mantine_react_table import DashMantineReactTable
from dash import html

from utils import create_df

# Load the data & format the df
df = create_df()

# table = dmc.Table(
#         id="table",
#         data=df.to_dict('records'),
#         # columns=[{'name': col, 'dataIndex': col} for col in df.columns]
#         columns=[
#                 {"name": i, "id": i}
#                 for i in df.columns
#                 if i not in ["S3 Bucket", "Overlay Video"]
#             ],
#         row_selectable="single",
#     )
print(df)


grid = DashMantineReactTable(
        id="table",
        data=df.to_dict("records"),
        columns=[{"accessorKey": i, "header": i} for i in df.columns],
        mrtProps={
            "enableHiding": False,
            "rowSelect": "single",
            "enableColumnFilters": True,
            "initialState": {"density": "sm"},
            "mantineTableProps": {"fontSize": "sm"},
            "mantineTableHeadCellProps": {"style": {"fontWeight": 500}},
        },
        mantineProviderProps={
            "theme": {
                "colorScheme": "light",
            },
        },
    )