import pandas as pd


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog = 'country_name_parse',
                                     description='Clean country names',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input',  metavar=' ', help="input meta file")
    parser.add_argument('-o', '--output', metavar=' ', help="output meta file") 
    args = parser.parse_args()

    input_csv_meta = args.input
    output_csv_meta = args.output

    meta = pd.read_csv(input_csv_meta, sep='\t', index_col=False)

    #clean country names to make them compatible with auspice

    Meta_without_NaN = meta["country"].fillna(value = "?")

    newCountry = []
    for d in Meta_without_NaN:
        if "_" in d: 
            auspice_country = d.replace("_", " ")
        else:
            auspice_country = d
        newCountry.append(auspice_country)
        
    meta['country'] = newCountry
    
    meta.to_csv(output_csv_meta, sep='\t', index=False)
