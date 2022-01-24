"""
remove_duplicate_sequences.py removes duplicate sequences by spotting duplicate ids. An id looks like this: "049/LY/CHN/AM/10/EV71".

Arguments:
    --input: fasta file with sequences, from which duplicates will be removed
    --output: fasta file without duplicate sequences

remove_duplicate_sequences.py is called within `snakefile`.

"""


import pandas as pd
from Bio import SeqIO
import numpy as np

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        prog = 'remove_duplicate_sequences',
        description="""
        Remove duplicate sequences.
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument('-i', '--input',  metavar=' ', help="input sequences")
    parser.add_argument('-o', '--output', metavar=' ', help="output sequences")
    args = parser.parse_args()

    input_sequences = args.input
    output_sequences = args.output

    input_sequences_list = list(SeqIO.parse(input_sequences,
                                "fasta"))
    input_ids = []
    for inputSequence in input_sequences_list:
        input_ids.append(inputSequence.id)

    duplicates_bool = pd.Series(input_ids).duplicated(keep='first')

    unique_sequences = list(pd.Series(input_sequences_list)[~duplicates_bool])

    SeqIO.write(unique_sequences, output_sequences, "fasta")