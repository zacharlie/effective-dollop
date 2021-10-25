"""Zoom attendance collection script

Simple script that gets historic meeting info and
generates a participant list info sheet from the zoom api

Requires a pro subscription to zoom"""

import os
import jwt  # pip install PyJWT
import requests  # pip install requests
import json
import pandas as pd  # pip install pandas

# pip install openpyxl  # used by pandas to write excel sheet
from time import time, sleep

# sign in to https://marketplace.zoom.us/ and create a new jwt app
API_KEY = "YOUR API KEY"
API_SECRET = "YOUR API SECRET"

USER_ID = "zoomuser@example.com"  # user account that hosted the meeting
MEETING_ID = 12345678910  # filter results to this meeting id

# Note that zoom apparently only allows you to go back 6 months
# using the API to retrieve the report/meeting info
FROM_DATE = "2021-10-01"
TO_DATE = "2021-10-31"
DIRID = "202110"  # store the individual meeting data in this directory
IDENTITY = "20211001_2021031"  # prefix the meeting data response

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{DIRID}")

if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

# generate jwt token
def generateToken():
    token = jwt.encode(
        # token payload with API Key and 1 hour expiration
        {"iss": API_KEY, "exp": time() + 5000},
        # Secret used to generate token signature
        API_SECRET,
        algorithm="HS256",
    )
    return token


# API auth header
headers = {
    "authorization": f"Bearer {generateToken()}",
    "content-type": "application/json",
}

# get historic meetings list for user

meetings_response = requests.get(
    f"https://api.zoom.us/v2/report/users/{USER_ID}/meetings?from={FROM_DATE}&to={TO_DATE}",
    headers=headers,
)

user_meetings = json.loads(meetings_response.text)

MEETING_JSON_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), f"{IDENTITY}_meetings.json"
)

with open(MEETING_JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(user_meetings, f, ensure_ascii=False, indent=2)

meeting_uuids = []

for meeting in user_meetings["meetings"]:
    if meeting["id"] == MEETING_ID:  # filter meeting list
        uuid = meeting["uuid"]
        uuid = requests.utils.quote(uuid)
        uuid = uuid.replace(
            "/", "%2F"
        )  # make absolutely sure we remove these stupid things
        meeting_uuids.append(uuid)

print(f"We're gonna get participants for these meetings OK?: {meeting_uuids}")

# uuids cause file name/ path errors
def fixPath(input_string):
    """remove invalid filename chars from uuid"""
    input_string = input_string.replace("/", "_")
    input_string = input_string.replace("\\", "_")
    input_string = input_string.replace("%", "_")
    input_string = input_string.replace("=", "_")
    input_string = input_string.replace("+", "_")
    input_string = input_string.replace("-", "_")
    return input_string


for uuid in meeting_uuids:

    print(f"Processing meeting {uuid}")

    idx = 0
    next_page = True
    next_page_token = ""

    while next_page:  # we need to loop through the paginated api responses
        response = requests.get(
            f"https://api.zoom.us/v2/report/meetings/{uuid}/participants?page_size=300&next_page_token={next_page_token}",
            headers=headers,
        )
        # You can also use the less informative past meetings API here:
        # response = requests.get(
        #     f'https://api.zoom.us/v2/past_meetings/{uuid}/participants?page_size=300&next_page_token={next_page_token}',
        #     headers=headers
        # )
        # Maybe it's useful where you don't have uuid or need a lighter tier API call with basic data
        # You couold probably also retrieve older meeting uuid info here, but I haven't tried
        data = json.loads(response.text)

        OUTPUT_JSON_FILE = os.path.join(f"{OUTDIR}", f"{fixPath(uuid)}_data_{idx}.json")

        with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        if "next_page_token" in data:
            if len(data["next_page_token"]) > 0:
                # https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits
                next_page_token = data["next_page_token"]
            else:
                next_page = False
        else:
            next_page = False
        print(f"Enumerated instance {idx}")
        idx += 1
        sleep(1)  # let's not anger the api gods

# take the json api response outputs and collate them into an excel workbook

extensions = ".json"

df = pd.DataFrame()

for path, dir, files in os.walk(OUTDIR):
    for name in files:
        if name.endswith(extensions):
            file = os.path.join(path, name)
            json_data = pd.read_json(file, typ="series")
            # the response can still "code": 3001
            # if there aren't >= 2 meeting participants
            if "code" in json_data:
                print(
                    f"Response Code: {json_data.code}, no further processing will occur."
                )
            else:
                try:
                    print("Processing dataframe")
                    dfx = pd.json_normalize(json_data.participants)
                    df = pd.concat([df, dfx])
                except Exception as e:
                    print(e)

# Save all the valid json info into an excel workbook
EXCELSIOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{DIRID}.xlsx")
df.to_excel(EXCELSIOR)

""" you can collate the excel outputs like with this afterwards

import os
import pandas as pd

extensions = (".xlsx", ".xls")

df = pd.DataFrame()

for path, dir, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
    for name in files:
        if name.endswith(extensions):
            print(f"Processing file: {name}")
            file = os.path.join(path, name)
            dfx = pd.read_excel(file)
            df = pd.concat([df, dfx])

EXCELSIOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"ALLDATA.xlsx")
df.to_excel(EXCELSIOR)
print("EXCELSIOR!")

"""
