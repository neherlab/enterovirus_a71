from Bio import SeqIO
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog = 'reference_genbank_to_fasta',
        description="""
        Converting reference sequence from genbank to fasta format
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument('-i', '--input',  metavar=' ', help="input genbank reference")
    parser.add_argument('-o', '--output', metavar=' ', help="output fasta reference") 
    args = parser.parse_args()

    genbank_reference = args.input
    fasta_reference = args.output

    SeqIO.convert(genbank_reference, "genbank", fasta_reference, "fasta")
