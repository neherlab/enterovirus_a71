"""
subsample_by_length.py subsamples from the initial sequence dataset, depending on the desired length (vp1 = 600-8000bp, whole genome = 6400-8000bp)

Arguments:
    --input: fasta file with sequences, from which this script will subsample
    --output: subsampled fasta file

subsample_by_length.py is called within `snakefile`.

"""


from Bio import SeqIO
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog = 'subsample_by_length',
        description="""
        Subsampling sequences by length (vp1 = 600-8000bp, whole genome = 6400-8000bp)
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument('-i', '--input',  metavar=' ', help="input sequences")
    parser.add_argument('-o', '--output', metavar=' ', help="output sequences")
    parser.add_argument('--sequence_length', metavar=' ', help="desired sequence length, (vp1 = 600-8000bp, whole genome/vp4vp1/2a3d = 6400-8000bp)")
    args = parser.parse_args()

    input_fasta = args.input
    output_fasta = args.output
    sequence_length = args.sequence_length

    whole_genome_sequences = []
    vp1_sequences = []

    for input_sequence in SeqIO.parse(input_fasta, 'fasta'):
        if len(input_sequence.seq) > 6000 and len(input_sequence.seq) < 8000:
            whole_genome_sequences.append(input_sequence)
            vp1_sequences.append(input_sequence)

        elif len(input_sequence.seq) > 600 and len(input_sequence.seq) < 8000:
            vp1_sequences.append(input_sequence)

    if sequence_length == 'vp1':
        SeqIO.write(vp1_sequences, output_fasta, "fasta")
    elif sequence_length == 'whole_genome' or \
         sequence_length == 'vp4vp1' or \
         sequence_length == '2a3d':
        SeqIO.write(whole_genome_sequences, output_fasta, "fasta")
