import pandas as pd
import numpy as np
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog = 'date_parse',
        description="""
        Clean dates of metadata
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input',  metavar=' ', help="input metadata")
    parser.add_argument('-o', '--output', metavar=' ', help="output metadata")
    args = parser.parse_args()

    input_csv_meta = args.input
    output_csv_meta = args.output

    meta = pd.read_csv(input_csv_meta, keep_default_na=True, sep='\t', index_col=False)

    newDates = []

    for oldDate in meta["date"]:
        if pd.isna(oldDate):
            oldDate = "20XX-XX-XX"
            augur_date = oldDate
        elif oldDate.count("_") == 2:
            augur_date = oldDate.replace("_", "-")
        elif oldDate.count("_") == 1:
            dash_date = oldDate.replace("_", "-")
            augur_date = dash_date + "-XX"
        elif oldDate.count("-") == 1:
            augur_date = oldDate + "-XX"
        elif len(oldDate) == 4:
            augur_date = oldDate + "-XX-XX"
        else:
            augur_date = oldDate
        newDates.append(augur_date)

    meta['date'] = newDates

    meta.to_csv(output_csv_meta, sep='\t', index=False)