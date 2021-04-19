from Bio import Phylo
from Bio import SeqIO
import pandas as pd

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog = 'subsample_tree',
                                     description='Subsampling sequences from tree.\
                                                  Subsample comprises children of\
                                                  common ancestor, determined from terminal leafs given.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_tree',  metavar=' ', help="input tree file")
    parser.add_argument('--tree_format',  metavar=' ', help="tree format (e.g. .nwk)")
    parser.add_argument('--input_fasta',  metavar=' ', help="fasta being subsampled")
    parser.add_argument('--input_metadata',  metavar=' ', help="metadata being subsampled")
    parser.add_argument('--terminal_1',  metavar=' ', help="first terminal leaf name")
    parser.add_argument('--terminal_2',  metavar=' ', help="second terminal leaf name")
    parser.add_argument('--output_sequences', metavar=' ', help="subsampled sequences")
    parser.add_argument('--output_metadata', metavar=' ', help="subsampled metadata")
    args = parser.parse_args()
   
    tree = args.input_tree
    tree_format = args.tree_format
    input_fasta = args.input_fasta
    input_metadata = args.input_metadata
    terminal_1 = args.terminal_1 
    terminal_2 = args.terminal_2
    output_sequences = args.output_sequences
    output_metadata = args.output_metadata


    args = parser.parse_args()
    import pandas as pd

    trees = Phylo.read(tree, tree_format)
    cma = trees.common_ancestor(terminal_1, terminal_2)
    cma_names = [] 
    for n in cma.get_terminals():
        cma_names.append(n.name)

    def match(sequence_name):
        return sequence_name in cma_names
           
    input_sequence_ids = pd.Series(map(lambda x: x.id, SeqIO.parse(input_fasta,"fasta")))
    mask_fasta = input_sequence_ids.map(match)
    cma_records = list(pd.Series(SeqIO.parse(input_fasta, "fasta"))
                       [mask_fasta])

    input_metadata_df = pd.read_csv(input_metadata, sep = "\t")
    mask_metadata = input_metadata_df.strain.map(match)
    output_metadata_df = input_metadata_df[mask_metadata]


    output_metadata_df.to_csv (output_metadata, sep='\t',index=False)
    SeqIO.write(cma_records, output_sequences, "fasta")

