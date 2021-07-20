import pandas as pd
from sodapy import Socrata
from main import db

def find_squirrel(hectare):
    with Socrata("data.cityofnewyork.us", None) as client:
        results = client.get("vfnx-vebw", hectare=hectare)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    for idx, row in results_df.iterrows():
        activity = []
        if row["running"]:
            activity.append('running')
        if row["chasing"]:
            activity.append('chasing')
        if row["climbing"]:
            activity.append('climbing')
        if row["eating"]:
            activity.append('eating')
        if row["foraging"]:
            activity.append('foraging')
        if row["kuks"]:
            activity.append('kuks')
        if row["quaas"]:
            activity.append('quaas')
        if row["moans"]:
            activity.append('moans')
        if row["tail_flags"]:
            activity.append('tail flags')
        if row["tail_twitches"]:
            activity.append('tail twitches')
        if row["approaches"]:
            activity.append('approaches')
        if row["indifferent"]:
            activity.append('indifferent')
        if row["runs_from"]:
            activity.append('runs from')
        
        print("ID: {}\tHectare: {}\tColor: {}\tAge: {}\tLocation: {}\tActivities: {}"
              .format(row['unique_squirrel_id'],
                      row['hectare'],
                      row['primary_fur_color'],
                      row["age"],
                      row["location"],
                      ' '.join([str(elem) for elem in activity])))

if __name__ == "__main__":
    find_squirrel('22F')