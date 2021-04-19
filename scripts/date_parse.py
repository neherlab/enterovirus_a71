import pandas as pd
import numpy as np

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog = 'date_parse',
                                     description='Clean dates of metadata',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input',  metavar=' ', help="input meta file")
    parser.add_argument('-o', '--output', metavar=' ', help="output meta file") 
    args = parser.parse_args()

    input_csv_meta = args.input
    output_csv_meta = args.output

    meta = pd.read_csv(input_csv_meta, sep='\t', index_col=False)

    #clean dates to make them compatible with augur
    newDate = []
    for d in meta["date"]:
        if pd.isna(d):
            d = "20XX-XX-XX"
            augur_date = d 
        elif d.count("_") == 2:
            augur_date = d.replace("_", "-")
        elif d.count("_") == 1: 
            dash_date = d.replace("_", "-")
            augur_date = dash_date + "-XX"
        elif d.count("-") == 1:
            augur_date = d + "-XX"
        elif len(d) == 4:
            augur_date = d + "-XX-XX"
        else:
            augur_date = d
        newDate.append(augur_date)
    meta['date'] = newDate
    meta.to_csv(output_csv_meta, sep='\t', index=False)