import datetime
import dateutil
import json
import logging
import pandas as pd
import requests

# Set logging parameters
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)


def getData():
    # Assign variables
    file = open("credentials.json")
    creds = json.load(file)

    # Pull credentials from the JSON file
    credentials = creds["credentials"]["Username"], creds["credentials"]["Password"]

    # Save the file to OneDrive for Sharepoint Power Automation
    zendesk = "https://stpiusxhighschool.zendesk.com"
    path = "/Users/jon/OneDrive - St. Pius X High School/ZenDesk Reports"

    # Set the new month to pull data from
    today = datetime.datetime.now()

    # These lines use datetime to fix the month/year automatically
    monthFix = dateutil.relativedelta.relativedelta(months=1)
    new_month = str(today - monthFix)

    filename = months[new_month[5:7]] + " " + str(new_month[0:4])
    fixed_month_url = new_month[0:4] + "-" + new_month[5:7] + "-" + "01"

    # Get URL for tickets
    url = f"{zendesk}/api/v2/search.json?query=type:ticket created>{fixed_month_url}"
    response = requests.get(url, auth=(credentials))
    logging.info(response)

    # Make Dataframe
    data = response.json()
    df = pd.DataFrame(data["results"])

    # Reformat from DateTime to Date and rename 2 columns
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.date
    df["updated_at"] = pd.to_datetime(df["updated_at"]).dt.date
    df.rename(
        columns={"created_at": "Created On", "updated_at": "Updated On"}, inplace=True
    )

    # Choose only the necessary columns
    selection = df[
        ["id", "Created On", "Updated On", "status", "recipient"]
    ].sort_values("Created On")

    # Save to the assigned path and filename
    selection.to_csv(f"{path}/{filename}.csv", index=False)


# Month Dictionary for auto name conversion
months = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}

# Run the function
getData()
