import pandas as pd
import numpy as np
from Bio import SeqIO

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog = 'remove_dupl',
                                     description='Remove duplicate sequences',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input',  metavar=' ', help="input sequences")
    parser.add_argument('-o', '--output', metavar=' ', help="output sequences") 
    args = parser.parse_args()

    input_sequences = args.input
    output_sequences = args.output

    duplicate_sequences = list(SeqIO.parse(input_sequences,
                           "fasta"))
    duplicate_ids = []
    for sequence in duplicate_sequences:
        duplicate_ids.append(sequence.id)

    duplicates_bool = pd.Series(duplicate_ids).duplicated(keep='first')

    sequences_unique = list(pd.Series(duplicate_sequences)[~duplicates_bool])

    SeqIO.write(sequences_unique, output_sequences, "fasta")

