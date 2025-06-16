# Importing necessary libraries
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_mantine_components as dmc
import dash_auth
from dash_iconify import DashIconify
import pandas as pd


import src.components as components
from src.utils import create_df

# Load the data & format the df
df = create_df()

# Create filtered dataframes for each year
df_2024 = df[df["Camp Year"] == 2024]
df_2025 = df[df["Camp Year"] == 2025]

df_filter = pd.DataFrame({f"{i}": [None] for i in df.columns.values})

# Create separate filter dataframes for each year
df_filter_2024 = pd.DataFrame({f"{i}": [None] for i in df_2024.columns.values})

df_filter_2025 = pd.DataFrame({f"{i}": [None] for i in df_2025.columns.values})


def generate_position_downloads(pos):
    return dcc.Download(id=f"download-{pos}-xlsx")


def generate_position_buttons(pos):
    return dmc.Button(
        children=[dmc.Text(f"{pos}", color="#18639d", style={"width": "5%"})],
        rightIcon=DashIconify(
            icon="material-symbols:download",
            color="#18639d",
        ),
        id=f"button-export-{pos}",
        variant="outline",
        style={"border-color": "#18639d"},
    )


def create_data_table(df_data, main_table_id, filter_table_id, df_filter):
    # Define numeric columns
    numeric_columns = [
        "Age",
        "Height",
        "Weight",
        "Camp #",
        "Flexibility Score",
        "Back to Floor Score",
        "Shin to Floor Score",
        "Thigh to Floor Score",
    ]

    # Create a single row of empty values for the filter table
    filter_data = [
        {
            col: None
            for col in df_data.columns
            if col != "S3 Bucket" and col != "Overlay Video" and col != "Height" and col != "Weight"
        }
    ]

    return html.Div(
        [
            # Filter table with dropdowns
            dash_table.DataTable(
                id=filter_table_id,  # This is the filter table with dropdowns
                columns=[
                    {"name": i, "id": i, "presentation": "dropdown"}
                    for i in df_filter.columns
                    if i != "S3 Bucket" and i != "Overlay Video" and i != "Height" and i != "Weight"
                ],
                data=df_filter.to_dict("records"),
                cell_selectable=False,
                style_as_list_view=True,
                editable=True,
                dropdown={
                    col: {
                        "clearable": True,
                        "options": [
                            {"label": str(i), "value": str(i)}
                            for i in sorted(
                                df_data[col].dropna().unique(),
                                key=lambda x: (
                                    float(x)
                                    if col in numeric_columns and str(x).replace(".", "", 1).isdigit()
                                    else str(x)
                                ),
                            )
                        ],
                    }
                    for col in df_data.columns
                    if col != "S3 Bucket" and col != "Overlay Video" and col != "Height" and col != "Weight"
                },
                sort_action="custom",
                sort_by=[],
                sort_mode="multi",
                style_table={"minWidth": "100%"},
                style_header={
                    "backgroundColor": "#18639d",
                    "fontWeight": "bold",
                    "font-family": "arial",
                    "color": "white",
                    "lineHeight": "30px",
                    "minWidth": "170px",
                    "width": "170px",
                    "maxWidth": "170px",
                    "textAlign": "center",
                },
                style_data={
                    "font-family": "arial",
                },
                css=[
                    {
                        "selector": ".dash-spreadsheet .Select-option",
                        "rule": "color: #1e2f3f",
                    },
                    {
                        "selector": ".dash-spreadsheet .Select-control:hover .Select-arrow",
                        "rule": "border-top-color: #1e2f3f",
                    },
                    {"selector": ".dash-spreadsheet th:hover .column-header--sort", "rule": "color: #1e2f3f"},
                    {"selector": ".dash-spreadsheet .Select:hover .Select-clear", "rule": "color: #1e2f3f"},
                ],
            ),
            # Main data table
            dash_table.DataTable(
                id=main_table_id,  # This is the main table showing the data
                columns=[
                    (
                        {"name": i, "id": i, "type": "numeric"}
                        if i in ["Age", "Height", "Weight", "Camp #"]
                        else {"name": i, "id": i}
                    )
                    for i in df_data.columns
                    if i != "S3 Bucket" and i != "Overlay Video" and i != "Height" and i != "Weight"
                ],
                data=df_data.to_dict("records"),
                sort_action="custom",
                sort_by=[],
                sort_mode="multi",
                page_size=100,
                page_current=0,
                page_action="custom",
                style_as_list_view=True,
                cell_selectable=True,
                selected_rows=[],
                style_filter={"backgroundColor": "#18639d25", "lineHeight": "30px"},
                style_data_conditional=[
                    {"if": {"column_id": "First Name"}, "font-weight": "bold"},
                    {"if": {"column_id": "Last Name"}, "font-weight": "bold"},
                    {
                        "if": {"row_index": "even"},
                        "backgroundColor": "#18639d25",
                    },
                    {
                        "if": {"state": "active"},
                        "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        "border": "1px solid rgb(0, 116, 217)",
                    },
                    {
                        "if": {"state": "selected"},
                        "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        "border": "1px solid rgb(0, 116, 217)",
                    },
                ],
                style_data={
                    "height": "auto",
                    "lineHeight": "50px",
                    "minWidth": "170px",
                    "width": "170px",
                    "maxWidth": "170px",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                },
                style_cell={
                    "textAlign": "center",
                    "font-family": "arial",
                },
                style_table={"minWidth": "100%", "height": "100%"},
                css=[
                    {
                        "selector": "tr:first-child",
                        "rule": "display: none",
                    },
                    {
                        "selector": ".previous-next-container .page-number .current-page-container input.current-page",
                        "rule": "font-family: arial",
                    },
                ],
            ),
        ],
        style={"overflowX": "auto", "height": "100%"},
    )


# usernames and passwords
VALID_USERNAME_PASSWORD_PAIRS = {
    "adamsd27@msu.edu": "TelemetryRecruit1!",
    "akern@wabash.edu": "TelemetryRecruit1!",
    "alcornta@tiffin.edu": "TelemetryRecruit1!",
    "jdallen2@olivet.edu": "TelemetryRecruit1!",
    "pallgeier@millikin.edu": "TelemetryRecruit1!",
    "jaamos@manchester.edu": "TelemetryRecruit1!",
    "ja3760@columbia.edu": "TelemetryRecruit1!",
    "coachaanderson22@gmail.com": "TelemetryRecruit1!",
    "tandrews1@udayton.edu": "TelemetryRecruit1!",
    "chaseandries11@gmail.com": "TelemetryRecruit1!",
    "carnick@purdue.edu": "TelemetryRecruit1!",
    "dashley2@ashland.edu": "TelemetryRecruit1!",
    "natkins@bsu.edu": "TelemetryRecruit1!",
    "bryan.ault@catapultsports.com": "TelemetryRecruit1!",
    "devin.bacchus@myemail.indwes.edu": "TelemetryRecruit1!",
    "jbanks14@fordham.edu": "TelemetryRecruit1!",
    "abbarr1@butler.edu": "TelemetryRecruit1!",
    "michael.bath@indstate.edu": "TelemetryRecruit1!",
    "jbelfiori@colgate.edu": "TelemetryRecruit1!",
    "lamar.bell@greenville.edu": "TelemetryRecruit1!",
    "stephenbell@augustana.edu": "TelemetryRecruit1!",
    "michael.bellamy@howard.edu": "TelemetryRecruit1!",
    "coachmbellamy@gmail.com": "TelemetryRecruit1!",
    "lberblinger@semo.edu": "TelemetryRecruit1!",
    "daveberkconsulting@gmail.com": "TelemetryRecruit1!",
    "kbeyer01@roosevelt.edu": "TelemetryRecruit1!",
    "bezbra@gvsu.edu": "TelemetryRecruit1!",
    "cjbignell@eiu.edu": "TelemetryRecruit1!",
    "benlblack90@gmail.com": "TelemetryRecruit1!",
    "bblack5@ilstu.edu": "TelemetryRecruit1!",
    "rblackm7@gmail.com": "TelemetryRecruit1!",
    "reginaldblackmon@yahoo.com": "TelemetryRecruit1!",
    "blairzs@tiffin.edu": "TelemetryRecruit1!",
    "dbland1@niu.edu": "TelemetryRecruit1!",
    "bblaney@emich.edu": "TelemetryRecruit1!",
    "blantor2@miamoh.edu": "TelemetryRecruit1!",
    "dbledsoe@defiamce.com": "TelemetryRecruit1!",
    "dbledsoe@defiance.edu": "TelemetryRecruit1!",
    "kjblocker1717@gmail.com": "TelemetryRecruit1!",
    "jared_boddie@taylor.edu": "TelemetryRecruit1!",
    "tboles@niu.edu": "TelemetryRecruit1!",
    "bond@csp.edu": "TelemetryRecruit1!",
    "clbonta@anderson.edu": "TelemetryRecruit1!",
    "kborghardt@roosevelt.edu": "TelemetryRecruit1!",
    "justin.bosch@valpo.edu": "TelemetryRecruit1!",
    "bobbostad66@gmail.com": "TelemetryRecruit1!",
    "ambowen@manchester.edu": "TelemetryRecruit1!",
    "cjb044@bucknell.edu": "TelemetryRecruit1!",
    "akbrady@eiu.edu": "TelemetryRecruit1!",
    "billbrechin@miamioh.edu": "TelemetryRecruit1!",
    "brexhiwj@miamioh.edu": "TelemetryRecruit1!",
    "brechiwj@miamioh.edu": "TelemetryRecruit1!",
    "michael.brewster@valpo.edu": "TelemetryRecruit1!",
    "bbridges094@gmail.com": "TelemetryRecruit1!",
    "cmclarkbroaden@olivet.edu": "TelemetryRecruit1!",
    "bbrohm@gocards.com": "TelemetryRecruit1!",
    "jjbrowde26@wabash.edu": "TelemetryRecruit1!",
    "justinbrowder32@gmail.com": "TelemetryRecruit1!",
    "cdbrown96.cb@gmail.com": "TelemetryRecruit1!",
    "browncd4@miamioh.edu": "TelemetryRecruit1!",
    "keller92@miamioh.edu": "TelemetryRecruit1!",
    "hdbrown@marian.edu": "TelemetryRecruit1!",
    "jbunofsk@carrollu.edu": "TelemetryRecruit1!",
    "kburke77@lakers.mercyhurst.edu": "TelemetryRecruit1!",
    "robertburke10@gmail.com": "TelemetryRecruit1!",
    "jburket@iwu.edu": "TelemetryRecruit1!",
    "jburrell@millikin.edu": "TelemetryRecruit1!",
    "jbush@hillsdale.edu": "TelemetryRecruit1!",
    "grantmcain@hmail.com": "TelemetryRecruit1!",
    "jpcannova@eiu.edu": "TelemetryRecruit1!",
    "mcaputo2@buffalo.edu": "TelemetryRecruit1!",
    "ecarducci@madonna.edu": "TelemetryRecruit1!",
    "jcatanese@millikin.edu": "TelemetryRecruit1!",
    "scavanaugh1s@semo.edu": "TelemetryRecruit1!",
    "championkalani67@gmail.com": "TelemetryRecruit1!",
    "owen.chandler@onu.edu": "TelemetryRecruit1!",
    "braxton.r.chapman@dartmouth.edu": "TelemetryRecruit1!",
    "edcharlebois10@gmail.com": "TelemetryRecruit1!",
    "schase@butler.edu": "TelemetryRecruit1!",
    "coachcchestnut@yahoo.com": "TelemetryRecruit1!",
    "keith.p.clark@dartmouth.edu": "TelemetryRecruit1!",
    "clecidor@upenn.edu": "TelemetryRecruit1!",
    "eliotclough@gmail.com": "TelemetryRecruit1!",
    "bcoad1@marian.edu": "TelemetryRecruit1!",
    "jcoddington@anderson.edu": "TelemetryRecruit1!",
    "collin.coffer@indstate.edu": "TelemetryRecruit1!",
    "21dayvencoleman@gmail.com": "TelemetryRecruit1!",
    "tjcollins2@olivet.edu": "TelemetryRecruit1!",
    "lconard@purdue.edu": "TelemetryRecruit1!",
    "cdconnolly@bsu.edu": "TelemetryRecruit1!",
    "zconowal31@gmail.com": "TelemetryRecruit1!",
    "coopesco@gvsu.edu": "TelemetryRecruit1!",
    "tim.cooper@wmich.edu": "TelemetryRecruit1!",
    "jcordle@ashland.edu": "TelemetryRecruit1!",
    "mcordova@holycross.edu": "TelemetryRecruit1!",
    "kevincorless@aol.com": "TelemetryRecruit1!",
    "cedric.cormier@bsu.edu": "TelemetryRecruit1!",
    "costantinos1@udayton.edu": "TelemetryRecruit1!",
    "ftl-crayton@wiu.edu": "TelemetryRecruit1!",
    "spencer.crisp@indwes.edu": "TelemetryRecruit1!",
    "cruseam@miamioh.edu": "TelemetryRecruit1!",
    "cullisod2@ohiodominican.edu": "TelemetryRecruit1!",
    "jl-curry@wiu.edu": "TelemetryRecruit1!",
    "major_dailey@taylor.edu": "TelemetryRecruit1!",
    "cdavis68@roosevelt.edu": "TelemetryRecruit1!",
    "dalphon.davis@siu.edu": "TelemetryRecruit1!",
    "derek.day@eku.edu": "TelemetryRecruit1!",
    "mr-day3@wiu.edu": "TelemetryRecruit1!",
    "rdeckard@hillsdale.edu": "TelemetryRecruit1!",
    "rdeckard1@marian.edu": "TelemetryRecruit1!",
    "ad825@cornell.edu": "TelemetryRecruit1!",
    "jdelcampo@butler.edu": "TelemetryRecruit1!",
    "rjdemarois@eiu.edu": "TelemetryRecruit1!",
    "jsdenney12@gmail.com": "TelemetryRecruit1!",
    "kmderickson@eiu.edu": "TelemetryRecruit1!",
    "bdessauer@butler.edu": "TelemetryRecruit1!",
    "bdessauer98@gmail.com": "TelemetryRecruit1!",
    "jdidier@sf.edu": "TelemetryRecruit1!",
    "jpdineen@purdue.edu": "TelemetryRecruit1!",
    "jd2327@cornell.edu": "TelemetryRecruit1!",
    "donald.h.dobes@dartmouth.edu": "TelemetryRecruit1!",
    "jacobdopsovic@gmail.com": "TelemetryRecruit1!",
    "tariqdrake23@gmail.com": "TelemetryRecruit1!",
    "adreyer@sf.edu": "TelemetryRecruit1!",
    "matt.drinkall@gmail.com": "TelemetryRecruit1!",
    "dunninis@gvsu.edu": "TelemetryRecruit1!",
    "dunninis@gvs.edu": "TelemetryRecruit1!",
    "dupont@upenn.edu": "TelemetryRecruit1!",
    "kedwards2@olivet.edu": "TelemetryRecruit1!",
    "ekkensba@tiffin.edu": "TelemetryRecruit1!",
    "ellismc@uwosh.edu": "TelemetryRecruit1!",
    "drew.engels2@indwes.edu": "TelemetryRecruit1!",
    "englem@uindy.edu": "TelemetryRecruit1!",
    "kenright@decaturproud.org": "TelemetryRecruit1!",
    "masonespinosa@depauw.edu": "TelemetryRecruit1!",
    "hlether@ilstu.edu": "TelemetryRecruit1!",
    "eric.evans@wmich.edu": "TelemetryRecruit1!",
    "a-feiertag@wiu.edu": "TelemetryRecruit1!",
    "rf6@uakron.edu": "TelemetryRecruit1!",
    "eflaherty1@udayton.edu": "TelemetryRecruit1!",
    "josh_flannery@taylor.edu": "TelemetryRecruit1!",
    "cflecker@defiance.edu": "TelemetryRecruit1!",
    "coachflecker@gmail.com": "TelemetryRecruit1!",
    "beflinn@princeton.edu": "TelemetryRecruit1!",
    "lmf3425@gmail.com": "TelemetryRecruit1!",
    "andrewfosterjr5@gmail.com": "TelemetryRecruit1!",
    "landon.fox@valpo.edu": "TelemetryRecruit1!",
    "rick.fox@centre.edu": "TelemetryRecruit1!",
    "cfunk@hse.k12.in.us": "TelemetryRecruit1!",
    "tyler.funk@indstate.edu": "TelemetryRecruit1!",
    "devvon_gage@georgetowncollege.edu": "TelemetryRecruit1!",
    "agant2@fordham.edu": "TelemetryRecruit1!",
    "agarcia2@lindenwood.esu": "TelemetryRecruit1!",
    "agarcia2@lindenwood.edu": "TelemetryRecruit1!",
    "cgarcia@carrollu.edu": "TelemetryRecruit1!",
    "gardinerss@tiffin.edu": "TelemetryRecruit1!",
    "gerikgarlington59@gmail.com": "TelemetryRecruit1!",
    "cmgeier@eiu.edu": "TelemetryRecruit1!",
    "robert.ghilarducci@valpo.edu": "TelemetryRecruit1!",
    "vg011@bucknell.edu": "TelemetryRecruit1!",
    "gilbertj@wws.k12.in.us": "TelemetryRecruit1!",
    "gilbertj@wabash.edu": "TelemetryRecruit1!",
    "gilbe129@purdue.edu": "TelemetryRecruit1!",
    "dgilbertson4@uakron.edu": "TelemetryRecruit1!",
    "mgoodin@decaturproud.org": "TelemetryRecruit1!",
    "jgrabbe@lindenwood.edu": "TelemetryRecruit1!",
    "ian.grant1@marist.edu": "TelemetryRecruit1!",
    "zachary.grant@siu.edu": "TelemetryRecruit1!",
    "gzonerecruits@gmail.com": "TelemetryRecruit1!",
    "llgreen@mckendree.edu": "TelemetryRecruit1!",
    "twgreene@eiu.edu": "TelemetryRecruit1!",
    "nathan.griffin@siu.edu": "TelemetryRecruit1!",
    "marcguerrero7@icloud.com": "TelemetryRecruit1!",
    "bthaines@iu.edu": "TelemetryRecruit1!",
    "logan.hale@indstate.edu": "TelemetryRecruit1!",
    "ahhaley@purdue.edu": "TelemetryRecruit1!",
    "thequarterbackhouse@gmail.com": "TelemetryRecruit1!",
    "clhall@millikin.edu": "TelemetryRecruit1!",
    "vicqual.hall@bsu.edu": "TelemetryRecruit1!",
    "gibran.hamdan@valpo.edu": "TelemetryRecruit1!",
    "hamerjrl@csp.edu": "TelemetryRecruit1!",
    "bjhammer@bowdoin.edu": "TelemetryRecruit1!",
    "g-hardin@wiu.edu": "TelemetryRecruit1!",
    "ethan.james.325@gmail.com": "TelemetryRecruit1!",
    "michaelharris@upike.edu": "TelemetryRecruit1!",
    "dhass@carthage.edu": "TelemetryRecruit1!",
    "hazellk1@udayton.edu": "TelemetryRecruit1!",
    "dan.hebert@dartmouth.edu": "TelemetryRecruit1!",
    "aheffler@culver.edu": "TelemetryRecruit1!",
    "thefter1@udayton.edu": "TelemetryRecruit1!",
    "javian.henderson@indstate.edu": "TelemetryRecruit1!",
    "jhenderson@indstate.edu": "TelemetryRecruit1!",
    "matthew.henning@wilkes.edu": "TelemetryRecruit1!",
    "ahensell@franklincollege.edu": "TelemetryRecruit1!",
    "sbhickey@butler.edu": "TelemetryRecruit1!",
    "seanbhickey61@gmail.com": "TelemetryRecruit1!",
    "cjhill@manchester.edu": "TelemetryRecruit1!",
    "njholeton@mckendree.edu": "TelemetryRecruit1!",
    "njholeton@mckendree.com": "TelemetryRecruit1!",
    "gholley@carrollu.edu": "TelemetryRecruit1!",
    "rjholmes@butler.edu": "TelemetryRecruit1!",
    "ihorvath@ltu.edu": "TelemetryRecruit1!",
    "chostler@butler.edu": "TelemetryRecruit1!",
    "hudsonc4@miamioh.edu": "TelemetryRecruit1!",
    "darold.hughes@msj.edu": "TelemetryRecruit1!",
    "dylanhyatt03@gmail.com": "TelemetryRecruit1!",
    "jiodence@carthage.edu": "TelemetryRecruit1!",
    "muremovich@butler.edu": "TelemetryRecruit1!",
    "ishmand@wittenberg.edu": "TelemetryRecruit1!",
    "jison@colgate.edu": "TelemetryRecruit1!",
    "mark@gocards.com": "TelemetryRecruit1!",
    "teamjacksonkicking@gmail.com": "TelemetryRecruit1!",
    "derricj@bgsu.edu": "TelemetryRecruit1!",
    "nathaniel.jackson31@gmail.com": "TelemetryRecruit1!",
    "tajecu@gmail.com": "TelemetryRecruit1!",
    "jaglaa99@uwosh.edu": "TelemetryRecruit1!",
    "cjames46@emich.edu": "TelemetryRecruit1!",
    "jack.jarnigan@valpo.edu": "TelemetryRecruit1!",
    "djjelin@northpark.edu": "TelemetryRecruit1!",
    "tmjenkins@mckendree.edu": "TelemetryRecruit1!",
    "johnstc@tiffin.edu": "TelemetryRecruit1!",
    "johnsonandrew223@gmail.com": "TelemetryRecruit1!",
    "cmjohnson5@bsu.edu": "TelemetryRecruit1!",
    "johnsonj29@ohiodominican.edu": "TelemetryRecruit1!",
    "john3584@purdue.edu": "TelemetryRecruit1!",
    "ljjohnson2@anderson.edu": "TelemetryRecruit1!",
    "cjones2@mercyhurst.edu": "TelemetryRecruit1!",
    "darricle.jones@indwes.edu": "TelemetryRecruit1!",
    "ojordan@mst.edu": "TelemetryRecruit1!",
    "kanekm@purdue.edu": "TelemetryRecruit1!",
    "atkarr@purdue.edu": "TelemetryRecruit1!",
    "tkarrasjr@marian.edu": "TelemetryRecruit1!",
    "masonkeelerfootball@gmail.com": "TelemetryRecruit1!",
    "dayne_keller@georgetowncollege.edu": "TelemetryRecruit1!",
    "bkennedy@georgetowncollege.edu": "TelemetryRecruit1!",
    "keegan_kennedy@fas.harvard.edu": "TelemetryRecruit1!",
    "mking1@marian.edu": "TelemetryRecruit1!",
    "connor.kinnett@gmail.com": "TelemetryRecruit1!",
    "jtknowles@butler.edu": "TelemetryRecruit1!",
    "ckoster9899@gmail.com": "TelemetryRecruit1!",
    "gkurzner@emich.edu": "TelemetryRecruit1!",
    "kkuzmuk@franklincollege.edu": "TelemetryRecruit1!",
    "jlamb@fas.harvard.edu": "TelemetryRecruit1!",
    "landersr@wittenberg.edu": "TelemetryRecruit1!",
    "adam_langvardt@taylor.edu": "TelemetryRecruit1!",
    "lauckc@tiffin.edu": "TelemetryRecruit1!",
    "slawanson@gmail.com": "TelemetryRecruit1!",
    "lawsontc1254@gmail.com": "TelemetryRecruit1!",
    "austinleake1@gmail.com": "TelemetryRecruit1!",
    "dlee3@carleton.edu": "TelemetryRecruit1!",
    "leej8@ohiodominican.edu": "TelemetryRecruit1!",
    "jameslee5255@gmail.com": "TelemetryRecruit1!",
    "zrleeds@iu.edu": "TelemetryRecruit1!",
    "coachaleclettl@gmail.com": "TelemetryRecruit1!",
    "parker.lewis@centre.edu": "TelemetryRecruit1!",
    "jlivingston@colgate.edu": "TelemetryRecruit1!",
    "daynellamas@yahoo.com": "TelemetryRecruit1!",
    "louisjim@gvsu.edu": "TelemetryRecruit1!",
    "adam.lovan3404@gmail.com": "TelemetryRecruit1!",
    "jlmadi1@ilstu.edu": "TelemetryRecruit1!",
    "djmang4@gmail.com": "TelemetryRecruit1!",
    "rmanneri@butler.edu": "TelemetryRecruit1!",
    "rorymannering@depauw.edu": "TelemetryRecruit1!",
    "nmantas@carrollu.edu": "TelemetryRecruit1!",
    "smmarks@eiu.edu": "TelemetryRecruit1!",
    "david.marquis@valpo.edu": "TelemetryRecruit1!",
    "martinde@msu.edu": "TelemetryRecruit1!",
    "jalenmasden2022@gmail.com": "TelemetryRecruit1!",
    "karl@gocards.com": "TelemetryRecruit1!",
    "mayzd@miamioh.edu": "TelemetryRecruit1!",
    "mmccarr91@gmail.com": "TelemetryRecruit1!",
    "mmcclana@emich.edu": "TelemetryRecruit1!",
    "trevor.mcconnell@valpo.edu": "TelemetryRecruit1!",
    "rmcelwain@franklincollege.edu": "TelemetryRecruit1!",
    "ryanmcelwain@depauw.edu": "TelemetryRecruit1!",
    "jm4257@columbia.edu": "TelemetryRecruit1!",
    "francismeehan8@gmail.com": "TelemetryRecruit1!",
    "rmelton@culver.edu": "TelemetryRecruit1!",
    "tmendelson64@gmail.com": "TelemetryRecruit1!",
    "metzb@ohio.edu": "TelemetryRecruit1!",
    "josiah.milham@bsu.edu": "TelemetryRecruit1!",
    "nrmiller@mckendree.edu": "TelemetryRecruit1!",
    "alex.mitchell@indstate.edu": "TelemetryRecruit1!",
    "comontgomery@anderson.edu": "TelemetryRecruit1!",
    "tmoore10@niu.edu": "TelemetryRecruit1!",
    "john.morris@bsu.edu": "TelemetryRecruit1!",
    "smorri@bgsu.edu": "TelemetryRecruit1!",
    "jamoss@butler.edu": "TelemetryRecruit1!",
    "drejmuhammad@icloud.com": "TelemetryRecruit1!",
    "mark.murnyack@wilmington.edu": "TelemetryRecruit1!",
    "murph463@miamioh.edu": "TelemetryRecruit1!",
    "pnank77@gmail.com": "TelemetryRecruit1!",
    "andy.navey@yahoo.com": "TelemetryRecruit1!",
    "needham.34@gmail.com": "TelemetryRecruit1!",
    "tjnieka@ilstu.edu": "TelemetryRecruit1!",
    "cj.nightingale@wheaton.edu": "TelemetryRecruit1!",
    "cn328@cornell.edu": "TelemetryRecruit1!",
    "dodea@dartmouth.edu": "TelemetryRecruit1!",
    "moeser@mst.edu": "TelemetryRecruit1!",
    "ogaraco@alma.edu": "TelemetryRecruit1!",
    "kevin.olecki@gmail.com": "TelemetryRecruit1!",
    "olmsteae@wabash.edu": "TelemetryRecruit1!",
    "mayomi.olootujr@bsu.edu": "TelemetryRecruit1!",
    "olsonrya@gvsu.edu": "TelemetryRecruit1!",
    "tomli@emich.edu": "TelemetryRecruit1!",
    "morts1@udayton.edu": "TelemetryRecruit1!",
    "jcostroski@eiu.edu": "TelemetryRecruit1!",
    "ipace@colgate.edu": "TelemetryRecruit1!",
    "kyle.padgett@munciecentral.org": "TelemetryRecruit1!",
    "ggp004@bucknell.edu": "TelemetryRecruit1!",
    "patton15@miamioh.edu": "TelemetryRecruit1!",
    "pawolach@msu.edu": "TelemetryRecruit1!",
    "penrodspeople@gmail.com": "TelemetryRecruit1!",
    "hperry@olivetcollege.edu": "TelemetryRecruit1!",
    "jonperry03@gmail.com": "TelemetryRecruit1!",
    "mpcuskie3@gmail.com": "TelemetryRecruit1!",
    "mpiatkow@emich.edu": "TelemetryRecruit1!",
    "postman@gvsu.edu": "TelemetryRecruit1!",
    "blake.powers@westpoint.edu": "TelemetryRecruit1!",
    "andrew.prevost@valpo.edu": "TelemetryRecruit1!",
    "pricedk@tiffin.edu": "TelemetryRecruit1!",
    "mprince6@emich.edu": "TelemetryRecruit1!",
    "proeselfj@tiffin.edu": "TelemetryRecruit1!",
    "coachrickpurcell@gmail.com": "TelemetryRecruit1!",
    "raglanad@miamioh.edu": "TelemetryRecruit1!",
    "ramseyc@wabash.edu": "TelemetryRecruit1!",
    "rav_73@yahoo.com": "TelemetryRecruit1!",
    "arthur.rayjr@howard.edu": "TelemetryRecruit1!",
    "arthurrayjr@gmail.com": "TelemetryRecruit1!",
    "kennyrayaugustus@gmail.com": "TelemetryRecruit1!",
    "reisertct@tiffin.edu": "TelemetryRecruit1!",
    "jrrejfek@mckendree.edu": "TelemetryRecruit1!",
    "rrelosky@iu.edu": "TelemetryRecruit1!",
    "neal.renna@gmail.com": "TelemetryRecruit1!",
    "chase.rich@msj.edu": "TelemetryRecruit1!",
    "crichardson1@niu.edu": "TelemetryRecruit1!",
    "trichardson@uakron.edu": "TelemetryRecruit1!",
    "ridingsm@wabash.edu": "TelemetryRecruit1!",
    "riesz@miamioh.edu": "TelemetryRecruit1!",
    "riordanj@wabash.edu": "TelemetryRecruit1!",
    "amroberts@manchester.edu": "TelemetryRecruit1!",
    "braelon3411@gmail.com": "TelemetryRecruit1!",
    "andrew.rode@indwes.edu": "TelemetryRecruit1!",
    "jrodriguez@uakron.edu": "TelemetryRecruit1!",
    "rogersdm@tiffin.edu": "TelemetryRecruit1!",
    "chris@nationalpreps.com": "TelemetryRecruit1!",
    "damien.ross@valpo.edu": "TelemetryRecruit1!",
    "royrr12@gmail.edu": "TelemetryRecruit1!",
    "royrr12@gmail.com": "TelemetryRecruit1!",
    "rufenercd@tiffin.edu": "TelemetryRecruit1!",
    "rumseyb@gvsu.edu": "TelemetryRecruit1!",
    "bsander4253@gmail.com": "TelemetryRecruit1!",
    "wsands@sf.edu": "TelemetryRecruit1!",
    "wsands@carthage.edu": "TelemetryRecruit1!",
    "qs-schafer@wiu.edu": "TelemetryRecruit1!",
    "joe.seymour@indstate.edu": "TelemetryRecruit1!",
    "coachwshafer@gmail.com": "TelemetryRecruit1!",
    "wolfgang.shafer@indstate.edu": "TelemetryRecruit1!",
    "patrick.shepard@indstate.edu": "TelemetryRecruit1!",
    "pshepard514@gmail.com": "TelemetryRecruit1!",
    "asherman@sf.edu": "TelemetryRecruit1!",
    "shoemaki@gvsu.edu": "TelemetryRecruit1!",
    "bshort@defiance.edu": "TelemetryRecruit1!",
    "zds@mckendree.edu": "TelemetryRecruit1!",
    "mike.simmonds@indstate.edu": "TelemetryRecruit1!",
    "jssimmon@purdue.edu": "TelemetryRecruit1!",
    "simmon35@miamioh.edu": "TelemetryRecruit1!",
    "nate.simmons@centre.edu": "TelemetryRecruit1!",
    "asiwicki@butler.edu": "TelemetryRecruit1!",
    "lucas.skibba@wilmington.edu": "TelemetryRecruit1!",
    "skibba@rose-hulman.edu": "TelemetryRecruit1!",
    "cmsmith@sf.edu": "TelemetryRecruit1!",
    "dsmith3@marian.edu": "TelemetryRecruit1!",
    "jackson.smith@valpo.edu": "TelemetryRecruit1!",
    "jamillsmith@aol.com": "TelemetryRecruit1!",
    "smithsa@hanover.edu": "TelemetryRecruit1!",
    "twsmithii@eiu.edu": "TelemetryRecruit1!",
    "drew.snouffer1@gmail.com": "TelemetryRecruit1!",
    "snuggsb@uindy.edu": "TelemetryRecruit1!",
    "sokol@rose-hulman.edu": "TelemetryRecruit1!",
    "scottsrnka@depauw.edu": "TelemetryRecruit1!",
    "stambaue@wabash.edu": "TelemetryRecruit1!",
    "mstans@buffalo.edu": "TelemetryRecruit1!",
    "stanton@rose-hulman.edu": "TelemetryRecruit1!",
    "gdstapleton@anderson.edu": "TelemetryRecruit1!",
    "drewsterett@gmail.com": "TelemetryRecruit1!",
    "kdstewa3@ilstu.edu": "TelemetryRecruit1!",
    "tstockton@bsu.edu": "TelemetryRecruit1!",
    "rstokes@hillsdale.edu": "TelemetryRecruit1!",
    "tsstone@manchester.edu": "TelemetryRecruit1!",
    "taylor.stubblefield.ctr@afacademy.af.edu": "TelemetryRecruit1!",
    "studdaja@gvsu.edu": "TelemetryRecruit1!",
    "estults@madonna.edu": "TelemetryRecruit1!",
    "legi@ath.msu.edu": "TelemetryRecruit1!",
    "vinnie.sunseri3@gmail.com": "TelemetryRecruit1!",
    "michael.swider.16@wheaton.edu": "TelemetryRecruit1!",
    "matthew.symmes@valpo.edu": "TelemetryRecruit1!",
    "tafes@tiffin.edu": "TelemetryRecruit1!",
    "tarpeybl@miamioh.edu": "TelemetryRecruit1!",
    "tatetyree@gmail.com": "TelemetryRecruit1!",
    "antoine.taylor08@gmail.com": "TelemetryRecruit1!",
    "austin.taylor@indwes.edu": "TelemetryRecruit1!",
    "carliftaylor@gmail.com": "TelemetryRecruit1!",
    "jetaylor@mckendree.edu": "TelemetryRecruit1!",
    "kteegard@emich.edu": "TelemetryRecruit1!",
    "curtisterry5550@gmail": "TelemetryRecruit1!",
    "coachterry09@gmail.com": "TelemetryRecruit1!",
    "theobaldj26@hanover.edu": "TelemetryRecruit1!",
    "theobald@hanover.edu": "TelemetryRecruit1!",
    "thompsob@carrollu.edu": "TelemetryRecruit1!",
    "at0357317@mckendree.edu": "TelemetryRecruit1!",
    "rtolen@centralstate.edu": "TelemetryRecruit1!",
    "tuckere77@uiu.edu": "TelemetryRecruit1!",
    "nate.vanasperen@valpo.edu": "TelemetryRecruit1!",
    "vanschelvenr1@udayton.edu": "TelemetryRecruit1!",
    "vosst@ohiodominican.edu": "TelemetryRecruit1!",
    "bryan.wade@ic.edu": "TelemetryRecruit1!",
    "lwalker63@davenport.edu": "TelemetryRecruit1!",
    "bwalshstaff@colgate.edu": "TelemetryRecruit1!",
    "coachwalters@purdue.edu": "TelemetryRecruit1!",
    "welshhp@miamioh.edu": "TelemetryRecruit1!",
    "crwelton@manchester.edu": "TelemetryRecruit1!",
    "whitebew@tiffin.edu": "TelemetryRecruit1!",
    "cwhite4@niu.edu": "TelemetryRecruit1!",
    "jacob.white@bsu.edu": "TelemetryRecruit1!",
    "mwhitton01@gmail.com": "TelemetryRecruit1!",
    "kwilk2@uw.edu": "TelemetryRecruit1!",
    "coachtwenty7fb@yahoo.com": "TelemetryRecruit1!",
    "jtwilliams3@anderson.edu": "TelemetryRecruit1!",
    "williamsj@trine.edu": "TelemetryRecruit1!",
    "mwillia6@iwu.edu": "TelemetryRecruit1!",
    "bradwilsonfb@gmail.com": "TelemetryRecruit1!",
    "b-wilson6@wiu.edu": "TelemetryRecruit1!",
    "wilsoncb@purdue.edu": "TelemetryRecruit1!",
    "matty713@gmail.com": "TelemetryRecruit1!",
    "twilson2@ltu.edu": "TelemetryRecruit1!",
    "tlwilson@olivet.edu": "TelemetryRecruit1!",
    "chadwilt06@gmail.com": "TelemetryRecruit1!",
    "dwoodburn@lw210.org": "TelemetryRecruit1!",
    "woosters@gvsu.edu": "TelemetryRecruit1!",
    "coachwoz@ath.msu.edu": "TelemetryRecruit1!",
    "bjyancey@manchester.edu": "TelemetryRecruit1!",
    "ayoung4@iwu.edu": "TelemetryRecruit1!",
    "czarkoskie@gmail.com": "TelemetryRecruit1!",
    "kczenner05@gmail.com": "TelemetryRecruit1!",
    "hoch@telemetry.fm": "TelemetryRecruit1!",
    "paul@telemetry.fm": "TelemetryRecruit1!",
    "andrew@telemetry.fm": "TelemetryRecruit1!",
    "chris@telemetry.fm": "TelemetryRecruit1!",
    "jordan@telemetry.fm": "TelemetryRecruit1!",
    "nate@telemetry.fm": "TelemetryRecruit1!",
    "tyler@telemetry.fm": "TelemetryRecruit1!",
    "ben@telemetry.fm": "TelemetryRecruit1!",
    "cody@telemetry.fm": "TelemetryRecruit1!",
    "wyatt@telemetry.fm": "TelemetryRecruit1!",
    "clay@telemetry.fm": "TelemetryRecruit1!",
    "willie@telemetry.fm": "TelemetryRecruit1!",
    "jay@telemetry.fm": "TelemetryRecruit1!",
    "brayden@telemetry.fm": "TelemetryRecruit1!",
    "chloe@telemetry.fm": "TelemetryRecruit1!",
    "will@telemetry.fm": "TelemetryRecruit1!",
    "alexfagan@usf.edu": "TelemetryRecruit1!",
    "jwwaters@uidaho.edu": "TelemetryRecruit1!",
    "ISU-SycamoreFB@indstate.edu": "TelemetryRecruit1!",
    "bsufootball@bsu.edu": "TelemetryRecruit1!",
    "mdneu2@bsu.edu": "TelemetryRecruit1!",
    "lance.taylor@wmich.edu": "TelemetryRecruit1!",
    "cameron.allen@wmich.edu": "TelemetryRecruit1!",
    "darren.paige@wmich.edu": "TelemetryRecruit1!",
    "fbrecruit@purdue.edu": "TelemetryRecruit1!",
    "natedennison@purdue.edu": "TelemetryRecruit1!",
    "noahjoseph@purdue.edu": "TelemetryRecruit1!",
    "football@msu.edu": "TelemetryRecruit1!",
    "dhicks@ath.msu.edu": "TelemetryRecruit1!",
    "mferrara@iu.edu": "TelemetryRecruit1!",
    "football@ohio.edu": "TelemetryRecruit1!",
    "mattix64@yahoo.com": "TelemetryRecruit1!",
    "fbrecruiting@niu.edu": "TelemetryRecruit1!",
    "awang@niu.edu": "TelemetryRecruit1!",
    "jahnekq@miamioh.edu": "TelemetryRecruit1!",
    "winkelwo@miamioh.edu": "TelemetryRecruit1!",
    "mikeferrarafb@gmail.com": "TelemetryRecruit1!",
    "jcollet2@emich.edu": "TelemetryRecruit1!",
    "brettdietz@depauw.edu": "TelemetryRecruit1!",
    "fbrecruiting@fordham.edu": "TelemetryRecruit1!",
    "fgiufre@fordham.edu": "TelemetryRecruit1!",
    "cburns59@fordham.edu": "TelemetryRecruit1!",
    "alec.pezuti@louisville.edu": "TelemetryRecruit1!",
    "jmarucc@lsu.edu": "TelemetryRecruit1!",
    "brandon.lawson@tennessee.edu": "TelemetryRecruit1!",
    "arw24001@uconn.edu": "TelemetryRecruit1!",
    "latravis.taylor@wku.edu": "TelemetryRecruit1!",
    "cduckett@uakron.edu": "TelemetryRecruit1!",
    "mmacal7@lsu.edu": "TelemetryRecruit1!",
    "TYLER.OLKER@tcu.edu": "TelemetryRecruit1!",
    "bbolin@ia.ua.edu": "TelemetryRecruit1!",
    "grantzy@ucmail.uc.edu": "TelemetryRecruit1!",
    "price3st@ucmail.uc.edu": "TelemetryRecruit1!",
    "rbrosnan@uoregon.edu": "TelemetryRecruit1!",
    "mparis1@walsh.edu": "TelemetryRecruit1!",
    "jfankhauser@walsh.edu": "TelemetryRecruit1!",
}

# Initialize the Dash app
app = dash.Dash(__name__, update_title="Loading Players...", suppress_callback_exceptions=True)
app.title = "Telemetry UIndy Mega Camp"
server = app.server

# authorization
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-7YVQXJ3SRC"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-7YVQXJ3SRC');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

app.layout = dmc.MantineProvider(
    html.Div(
        children=[
            components.initial_popup,
            components.header,
            dmc.Container(
                fluid=True,
                children=[
                    dmc.Title(
                        "UINDY CAMP PLAYER FLEXIBILITY RESULTS",
                        order=1,
                        align="center",
                        color="#1e2f3f",
                        weight="bold",
                        p=15,
                        style={"fontFamily": "arial", "font-style": "italic"},
                        td="underline",
                    ),
                    html.Br(),
                    # Table displaying player stats
                    dmc.Group(
                        [
                            dcc.Input(
                                id="search-input",
                                type="text",
                                placeholder="Search by player name...",
                                style={"width": "15%", "textAlign": "left", "color": "#1e2f3f", "lineHeight": "25px"},
                            ),
                            dmc.Text(
                                " * CLICK ON A PLAYER BELOW TO VIEW SQUAT VIDEO AND SCORES * ",
                                color="green",
                                style={"font-style": "italic"},
                                size="md",
                            ),
                            dmc.Group(
                                children=[
                                    i
                                    for i in (
                                        generate_position_downloads(i)
                                        for i in ["DB", "DL", "LB", "OL", "QB", "RB", "TE", "WR"]
                                    )
                                ],
                            ),
                            dmc.Group(
                                children=[
                                    i
                                    for i in (
                                        generate_position_buttons(i)
                                        for i in ["DB", "DL", "LB", "OL", "QB", "RB", "TE", "WR"]
                                    )
                                ],
                                position="flex-end",
                                style={
                                    "align-items": "flex-end",
                                    "justify-content": "flex-end",
                                    "display": "flex",
                                    "flex-wrap": "wrap",
                                },
                            ),
                        ]
                    ),
                    html.Br(),
                    dmc.Tabs(
                        [
                            dmc.Tab("2025 Players", value="2025", style={"font-family": "arial", "color": "#1e2f3f"}),
                            dmc.Tab("2024 Players", value="2024", style={"font-family": "arial", "color": "#1e2f3f"}),
                        ],
                        id="year-tabs",
                        value="2025",
                        color="#18639d",
                        variant="outline",
                        style={"display": "flex"},
                    ),
                    html.Div(id="tab-content"),
                    components.player_popup,
                ],
            ),
            html.Br(),
            components.footer,
        ]
    )
)


@app.callback(
    Output("tab-content", "children"),
    Input("year-tabs", "value"),
)
def render_tab_content(tab):
    if tab == "2024":
        return create_data_table(df_2024, "table-data", "table-filter", df_filter)
    else:
        return create_data_table(df_2025, "table-data", "table-filter", df_filter)


# Update the callbacks to handle both tables


@app.callback(
    Output("table-data", "data", allow_duplicate=True),
    [Input("search-input", "value"), Input("year-tabs", "value")],
    prevent_initial_call=True,
)
def update_table_search(search_value, active_tab):
    if search_value:
        if active_tab == "2024":
            filtered_data = df_2024[
                df_2024.apply(
                    lambda row: search_value.lower() in row["First Name"].lower()
                    or search_value.lower() in row["Last Name"].lower(),
                    axis=1,
                )
            ]
        else:
            filtered_data = df_2025[
                df_2025.apply(
                    lambda row: search_value.lower() in row["First Name"].lower()
                    or search_value.lower() in row["Last Name"].lower(),
                    axis=1,
                )
            ]
        return filtered_data.to_dict("records")
    else:
        return df_2024.to_dict("records") if active_tab == "2024" else df_2025.to_dict("records")


# Pagination callback


@app.callback(
    Output("table-data", "data", allow_duplicate=True),
    [Input("table-data", "page_current"), Input("table-data", "data")],
    prevent_initial_call=True,
)
def pagination(page_current, current_data):
    if page_current == 0:
        return current_data[page_current * 100 : (page_current + 1) * 100]
    else:
        return dash.no_update


# Filtering and sorting callback


@app.callback(
    Output("table-data", "data", allow_duplicate=True),
    [
        Input("table-filter", "data_timestamp"),
        Input("table-filter", "sort_by"),
        Input("table-filter", "data"),
        Input("table-data", "page_current"),
        Input("year-tabs", "value"),
    ],
    prevent_initial_call=True,
)
def update_table_dropdown_sort(timestamp, sort_by, filter_rows, page_current, active_tab):
    if timestamp is None or filter_rows is None:
        raise dash.exceptions.PreventUpdate

    data = df_2024.copy() if active_tab == "2024" else df_2025.copy()
    grades_to_numbers = {
        "A+": 0,
        "A": 1,
        "A-": 2,
        "B+": 3,
        "B": 4,
        "B-": 5,
        "C+": 6,
        "C": 7,
        "C-": 8,
        "D+": 9,
        "D": 10,
        "D-": 11,
        "F": 12,
    }
    numbers_to_grades = {
        0: "A+",
        1: "A",
        2: "A-",
        3: "B+",
        4: "B",
        5: "B-",
        6: "C+",
        7: "C",
        8: "C-",
        9: "D+",
        10: "D",
        11: "D-",
        12: "F",
    }

    # Apply filters
    for col, value in filter_rows[0].items():
        if value is not None and value != "":
            # Convert both the filter value and the data to strings for comparison
            data = data[data[col].astype(str) == str(value)]

    # Apply sorting
    if len(sort_by):
        replaced = data.replace(
            {
                "Flexibility Grade": grades_to_numbers,
                "Shin to Floor Grade": grades_to_numbers,
                "Thigh to Floor Grade": grades_to_numbers,
                "Back to Floor Grade": grades_to_numbers,
            }
        )
        dff = replaced.sort_values(
            [col["column_id"] for col in sort_by],
            ascending=[col["direction"] == "asc" for col in sort_by],
            inplace=False,
        )
        dff = dff.replace(
            {
                "Flexibility Grade": numbers_to_grades,
                "Shin to Floor Grade": numbers_to_grades,
                "Thigh to Floor Grade": numbers_to_grades,
                "Back to Floor Grade": numbers_to_grades,
            }
        )
    else:
        dff = data

    return dff.iloc[page_current * 100 : (page_current + 1) * 100].to_dict("records")


# Player popup callback


@app.callback(
    Output("player-popup", "opened"),
    Output("table-data", "style_data_conditional", allow_duplicate=True),
    Output("player-popup", "children"),
    [
        Input("table-data", "selected_cells"),
        Input("table-data", "active_cell"),
        Input("table-data", "page_current"),
        Input("year-tabs", "value"),
    ],
    [State("table-data", "data"), State("player-popup", "opened")],
    prevent_initial_call=True,
)
def display_player_popup(selected_cells, active_cell, page_current, active_tab, data, opened):
    ctx = dash.callback_context
    if not ctx.triggered:
        return opened, [], html.Div()

    style = [
        {
            "if": {"column_id": "First Name"},
            "font-weight": "bold",
        },
        {
            "if": {"column_id": "Last Name"},
            "font-weight": "bold",
        },
        {
            "if": {"row_index": "even"},
            "backgroundColor": "#18639d25",
        },
        {
            "if": {"state": "active"},
            "backgroundColor": "rgba(0, 116, 217, 0.3)",
            "border": "1px solid rgb(0, 116, 217)",
        },
        {
            "if": {"state": "selected"},
            "backgroundColor": "rgba(0, 116, 217, 0.3)",
            "border": "1px solid rgb(0, 116, 217)",
        },
    ]

    if active_cell:
        style.append(
            {
                "if": {"row_index": active_cell["row"]},
                "backgroundColor": "rgba(0, 116, 217, 0.3)",
                "border": "1px solid rgb(0, 116, 217)",
            }
        )
    if selected_cells and active_cell:
        selected_player = data[selected_cells[0]["row"]]
        return create_player_popup(selected_player, not opened, style, True)

    return opened, style, html.Div()


def create_player_popup(selected_player, opened_state, style, show_popup):
    first_name = selected_player["First Name"]
    last_name = selected_player["Last Name"]
    camp_num = selected_player["Camp #"]
    s3_bucket = selected_player["S3 Bucket"]
    overlay = selected_player["Overlay Video"]
    class_year = selected_player["Class"]
    school = selected_player["School"]
    state = selected_player["State"]
    pos = selected_player["Position"]
    flex_score = selected_player["Flexibility Score"]
    flex_grade = selected_player["Flexibility Grade"]
    back_grade = selected_player["Back to Floor Grade"]
    shin_grade = selected_player["Shin to Floor Grade"]
    thigh_grade = selected_player["Thigh to Floor Grade"]
    back_score = selected_player["Back to Floor Score"]
    shin_score = selected_player["Shin to Floor Score"]
    thigh_score = selected_player["Thigh to Floor Score"]
    video = f"https://{s3_bucket}.s3.amazonaws.com/{overlay}"

    player_header = html.Div(
        id="player-popup-header",
        children=[
            dmc.Group(
                [
                    dmc.Title(
                        f"{first_name} {last_name}",
                        td="underline",
                        style={
                            "color": "#ffffff",
                            "text-align": "center",
                            "width": "100%",
                            "margin": "5px",
                            "font-style": "italic",
                        },
                    ),
                    html.H2(
                        f"#{camp_num} | YR: {class_year} | POS: {pos} | SCHOOL: {school} | STATE: {state} ",
                        style={"color": "#ffffff", "text-align": "center", "width": "100%", "margin": "5px"},
                    ),
                ],
                align="center",
            ),
        ],
        style={
            "border-style": "solid",
            "border-color": "#18639d",
            "font-family": "arial",
            "font-color": "white",
            "background-color": "#011627",
            "display": "flex",
            "flex-direction": "row",
            "padding": "10px",
            "minWidth": "400px",
            "width": "400px",
            "maxWidth": "400px",
            "minHeight": "200px",
            "height": "200px",
            "maxHeight": "200px",
            "border-radius": "5px",
        },
    )

    div_styling = {
        "color": "#ffffff",
        "text-align": "center",
        "width": "150%",
        "height": "100%",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center",
        "margin": "0px",
    }
    score_styling = {
        "width": "150%",
        "height": "100%",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center",
        "margin": "0px",
    }

    player_scores_table = dmc.SimpleGrid(
        cols=3,
        spacing="5px",
        verticalSpacing="5px",
        children=[
            html.Div(children=[html.H2("Back to Floor:")], style=div_styling),
            html.Div(
                children=[components.set_grade(back_score, "score")],
                style=score_styling,
            ),
            html.Div(
                children=[components.set_grade(back_grade, "grade")],
                style=score_styling,
            ),
            html.Div(children=[html.H2("Shin to Floor:")], style=div_styling),
            html.Div(
                children=[components.set_grade(shin_score, "score")],
                style=score_styling,
            ),
            html.Div(
                children=[components.set_grade(shin_grade, "grade")],
                style=score_styling,
            ),
            html.Div(children=[html.H2("Thigh to Floor:")], style=div_styling),
            html.Div(
                children=[components.set_grade(thigh_score, "score")],
                style=score_styling,
            ),
            html.Div(
                children=[components.set_grade(thigh_grade, "grade")],
                style=score_styling,
            ),
        ],
        style={
            "border-radius": "5px",
            "font-family": "arial",
            "box-shadow": "rgba(0, 0, 0, 0.1) 0px 4px 12px",
            "align-items": "center",
        },
    )

    player_scores_div = html.Div(
        id="player-scores",
        children=[
            dmc.Group(
                [
                    html.H1("Flexibility Grade:", style={"text-align": "center", "color": "#ffffff"}),
                    components.set_grade(flex_grade, "grade"),
                ],
                position="center",
            ),
            html.Div(
                children=[player_scores_table],
            ),
        ],
        style={
            "padding": "10px",
            "font-family": "arial",
            "font-color": "white",
            "border-style": "solid",
            "border-color": "#18639d",
            "background-color": "#011627",
            "minWidth": "400px",
            "width": "400px",
            "maxWidth": "400px",
            "minHeight": "300px",
            "height": "300px",
            "maxHeight": "300px",
            "align-items": "center",
            "justify-content": "center",
            "border-radius": "5px",
        },
    )

    logo_div = html.Div(
        id="logo",
        children=[
            dmc.Stack(
                [
                    dmc.Anchor(
                        dmc.Image(src="assets/images/TS-Horizontal-RGB-Inverse.svg"),
                        href="https://telemetrysports.com/",
                        style={
                            "align-items": "center",
                            "justify-content": "center",
                            "minHeight": "80px",
                            "height": "80px",
                            "maxHeight": "80px",
                            "minWidth": "130px",
                            "width": "130px",
                            "maxWidth": "130px",
                        },
                    ),
                    dmc.Button(
                        dmc.Anchor(
                            dmc.Text("Contact Us", color="white"),
                            href="https://telemetrysports.com/contact",
                        ),
                        variant="outline",
                        radius="sm",
                        size="sm",
                        style={"margin-top": "10px", "border-color": "white"},
                    ),
                ],
                align="center",
            ),
        ],
        style={
            "minWidth": "400px",
            "width": "400px",
            "maxWidth": "400px",
            "minHeight": "160px",
            "height": "160px",
            "maxHeight": "160px",
            "align-items": "center",
            "justify-content": "center",
            "padding": "10px",
        },
    )

    player_popup = html.Div(
        id="player-popup-content",
        children=[
            dmc.Group(
                [
                    html.Video(
                        controls=True,
                        width="40%",
                        id="video_player",
                        src=video,
                        autoPlay=False,
                        style={
                            "margin-right": "8px",
                            "border-radius": "5px",
                            "align-items": "center",
                            "justify-content": "center",
                        },
                    ),
                    dmc.Stack(
                        [
                            player_header,
                            player_scores_div,
                            logo_div,
                        ]
                    ),
                ],
                position="center",
            ),
        ],
        style={
            "padding": "10px",
            "display": "flex",
            "flex-direction": "row",
            "background-color": "#011627",
        },
    )

    return opened_state, style, player_popup


# Export to Excel callbacks


@app.callback(
    Output("download-DB-xlsx", "data"),
    Input("button-export-DB", "n_clicks"),
    Input("year-tabs", "value"),
    prevent_initial_call=True,
)
def callback_DB(n, active_tab):
    if active_tab == "2024":
        return export_to_excel("DB", df_2024)
    else:
        return export_to_excel("DB", df_2025)


@app.callback(
    Output("download-DL-xlsx", "data"),
    Input("button-export-DL", "n_clicks"),
    Input("year-tabs", "value"),
    prevent_initial_call=True,
)
def callback_DL(n, active_tab):
    if active_tab == "2024":
        return export_to_excel("DL", df_2024)
    else:
        return export_to_excel("DL", df_2025)


@app.callback(
    Output("download-LB-xlsx", "data"),
    Input("button-export-LB", "n_clicks"),
    Input("year-tabs", "value"),
    prevent_initial_call=True,
)
def callback_LB(n, active_tab):
    if active_tab == "2024":
        return export_to_excel("LB", df_2024)
    else:
        return export_to_excel("LB", df_2025)


@app.callback(
    Output("download-OL-xlsx", "data"),
    Input("button-export-OL", "n_clicks"),
    Input("year-tabs", "value"),
    prevent_initial_call=True,
)
def callback_OL(n, active_tab):
    if active_tab == "2024":
        return export_to_excel("OL", df_2024)
    else:
        return export_to_excel("OL", df_2025)


@app.callback(
    Output("download-QB-xlsx", "data"),
    Input("button-export-QB", "n_clicks"),
    Input("year-tabs", "value"),
    prevent_initial_call=True,
)
def callback_QB(n, active_tab):
    if active_tab == "2024":
        return export_to_excel("QB", df_2024)
    else:
        return export_to_excel("QB", df_2025)


@app.callback(
    Output("download-RB-xlsx", "data"),
    Input("button-export-RB", "n_clicks"),
    Input("year-tabs", "value"),
    prevent_initial_call=True,
)
def callback_RB(n, active_tab):
    if active_tab == "2024":
        return export_to_excel("RB", df_2024)
    else:
        return export_to_excel("RB", df_2025)


@app.callback(
    Output("download-TE-xlsx", "data"),
    Input("button-export-TE", "n_clicks"),
    Input("year-tabs", "value"),
    prevent_initial_call=True,
)
def callback_TE(n, active_tab):
    if active_tab == "2024":
        return export_to_excel("TE", df_2024)
    else:
        return export_to_excel("TE", df_2025)


@app.callback(
    Output("download-WR-xlsx", "data"),
    Input("button-export-WR", "n_clicks"),
    Input("year-tabs", "value"),
    prevent_initial_call=True,
)
def callback_WR(n, active_tab):
    if active_tab == "2024":
        return export_to_excel("WR", df_2024)
    else:
        return export_to_excel("WR", df_2025)


def export_to_excel(pos, df_data):
    writer = pd.ExcelWriter(f"{pos}_sheet.xlsx", engine="xlsxwriter")
    filtered_df = df_data[df_data["Position"] == pos]
    filtered_df = filtered_df.drop(["S3 Bucket", "Overlay Video"], axis=1)
    filtered_df.to_excel(writer, sheet_name=f"{pos}_Sheet")
    writer.close()
    return dcc.send_file(f"{pos}_sheet.xlsx")


# Run the app
if __name__ == "__main__":
    app.run()  # hot reloading enabled
