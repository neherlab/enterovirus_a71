from Bio import SeqIO

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog = 'subsample_sequences',
                                     description='Subsampling sequences by vp1 length (600-8000bp) and whole genome length (6400-8000bp)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input',  metavar=' ', help="input sequences")
    parser.add_argument('-o', '--output', metavar=' ', help="output sequences")
    parser.add_argument('--sequence_length', metavar=' ', help="desired sequence length, (vp1 = 600-8000bp, whole genome = 6400-8000bp)")
    args = parser.parse_args()

    input_fasta = args.input
    sequences = args.output
    sequence_length = args.sequence_length
            
    whole_genome_sequences = []
    vp1_sequences = []                 

    for sequence in SeqIO.parse(input_fasta, 'fasta'):
        if len(sequence.seq) > 6000 and len(sequence.seq) < 8000:
            whole_genome_sequences.append(sequence)
            vp1_sequences.append(sequence)
            
        elif len(sequence.seq) > 600 and len(sequence.seq) < 8000:
            vp1_sequences.append(sequence)
            
    
    if sequence_length == 'vp1':
        SeqIO.write(vp1_sequences, sequences, "fasta")
    elif sequence_length == 'whole_genome':
        SeqIO.write(whole_genome_sequences, sequences, "fasta")
