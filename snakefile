###############
# Snakemake execution templates:

# To run a default VP1 run(<600bp):
# snakemake  ev_a71/vp1/auspice/ev_a71_vp1.json --cores 1

# To run a default whole genome run ( <6400bp):
# snakemake ev_a71/whole_genome/auspice/ev_a71_whole_genome.json --cores 1

###############
segments = {'vp1','whole_genome','vp4vp1','2a3d'}

rule all:
    input:
        auspice_json = "ev_a71/{segments}/auspice/ev_a71_{segments}.json", segments = {"vp1","whole_genome",'vp4vp1','2a3d'}

vipr_fasta = "ev_a71/{segments}/data/vipr.fasta"
dropped_strains = "ev_a71/{segments}/config/dropped_strains.txt"
reference = "ev_a71/{segments}/config/reference_sequence.gb"
lat_longs = "ev_a71/{segments}/config/lat_longs.tsv"
auspice_config = "ev_a71/{segments}/config/auspice_config.json"
sequence_length = "{segments}"
colors = "ev_a71/{segments}/config/colors.tsv"
clades = "ev_a71/{segments}/config/clades_genome.tsv"


rule subsample_by_length:
    message:
        """
        Subsampling sequences by length (vp1 = 600-8000bp,
                                         whole genome = 6400-8000bp)
        """
    input:
        sequences = vipr_fasta
    output:
        sequences = "ev_a71/{segments}/results/{segments}_fasta.fasta"
    params:
        sequence_length = sequence_length
    shell:
        """
        python scripts/subsample_by_length.py \
            --input {input.sequences} \
            --output {output.sequences} \
            --sequence_length {params.sequence_length}
        """

rule parse:
    message:
        """
        Parsing sequences and metadata from viprbrc.fasta.
        """
    input:
        sequences = rules.subsample_by_length.output.sequences
    output:
        duplicate_sequences = "ev_a71/{segments}/results/duplicate_sequences.fasta",
        metadata = "ev_a71/{segments}/results/uncleaned_metadata.tsv"
    params:
        prettify_fields = "country"
    shell:
        """
        augur parse \
            --sequences {input.sequences} \
            --output-sequences {output.duplicate_sequences} \
            --output-metadata {output.metadata} \
            --fields accession name segment date host country abbreviation virus \
            --prettify-fields {params.prettify_fields} \
            --separator "|"
        """

rule remove_duplicates:
    message:
        """
        Removing duplicate sequences.
        """
    input:
        sequences = rules.parse.output.duplicate_sequences
    output:
        sequences = "ev_a71/{segments}/results/sequences.fasta"
    shell:
        """
        python scripts/remove_duplicate_sequences.py \
            --input {input.sequences} \
            --output {output.sequences}
        """

rule date_parse:
    message:
        """
        Cleaning dates in metadata.
        """
    input:
        metadata = rules.parse.output.metadata
    output:
        metadata = "ev_a71/{segments}/results/cleaned_metadata.tsv"
    shell:
        """
        python scripts/date_parse.py \
            --input {input.metadata} \
            --output {output.metadata}
        """

rule index_sequences:
    message:
        """
        Creating an index of sequence composition for filtering.
        """
    input:
        sequences = rules.remove_duplicates.output.sequences
    output:
        sequence_index = "ev_a71/{segments}/results/sequence_index.tsv"
    shell:
        """
        augur index \
            --sequences {input.sequences} \
            --output {output.sequence_index}
        """

rule filter:
    message:
        """
        Filtering to
          - {params.sequences_per_group} sequence(s) per {params.group_by!s}
          - from {params.min_date} onwards
          - excluding strains in {input.exclude}
        """
    input:
        sequences = rules.remove_duplicates.output.sequences,
        sequence_index = rules.index_sequences.output.sequence_index,
        metadata = rules.date_parse.output.metadata,
        exclude = dropped_strains
    output:
        sequences = "ev_a71/{segments}/results/filtered.fasta"
    params:
        group_by = "country",
        sequences_per_group = 2000,
        min_date = 1970 ##assign clade b2
    shell:
        """
        augur filter \
            --sequences {input.sequences} \
            --sequence-index {input.sequence_index} \
            --metadata {input.metadata} \
            --exclude {input.exclude} \
            --group-by {params.group_by} \
            --sequences-per-group {params.sequences_per_group} \
            --min-date {params.min_date} \
            --output {output.sequences} \
        """

rule reference_gb_to_fasta:
    message:
        """
        Converting reference sequence from genbank to fasta format
        """
    input:
        reference = reference
    output:
        reference = "ev_a71/{segments}/results/reference_sequence.fasta"
    shell:
        """
        python scripts/reference_genbank_to_fasta.py \
            --input {input.reference} \
            --output {output.reference}
        """

rule align:
    message:
        """
        Aligning sequences to {input.reference} using Nextalign
        """
    input:
        sequences = rules.filter.output.sequences,
        reference = rules.reference_gb_to_fasta.output.reference
    output:
        alignment = "ev_a71/{segments}/results/aligned.fasta",
        insertions = "ev_a71/{segments}/results/insertions.csv"

    params:
        nuc_mismatch_all = 10,
        nuc_seed_length = 30
    shell:
        """
        nextalign \
            --sequences {input.sequences} \
            --reference {input.reference} \
            --nuc-mismatches-allowed {params.nuc_mismatch_all} \
            --nuc-seed-length {params.nuc_seed_length} \
            --output-fasta {output.alignment} \
            --output-insertions {output.insertions} \
        """

rule tree:
    message: "Building tree"
    input:
        alignment = rules.align.output.alignment
    output:
        tree = "ev_a71/{segments}/results/tree_raw.nwk"
    shell:
        """
        augur tree \
            --alignment {input.alignment} \
            --output {output.tree}
        """

rule refine:
    message:
        """
        Refining tree
          - estimate timetree
          - use {params.coalescent} coalescent timescale
          - estimate {params.date_inference} node dates
          - filter tips more than {params.clock_filter_iqd} IQDs from clock expectation
        """
    input:
        tree = rules.tree.output.tree,
        alignment = rules.align.output.alignment,
        metadata = rules.date_parse.output.metadata
    output:
        tree = "ev_a71/{segments}/results/tree.nwk",
        node_data = "ev_a71/{segments}/results/branch_lengths.json"
    params:
        coalescent = "opt",
        date_inference = "marginal",
        clock_filter_iqd = 3,
        clock_rate = 0.004,
        clock_std_dev = 0.0015
    shell:
        """
        augur refine \
            --tree {input.tree} \
            --alignment {input.alignment} \
            --metadata {input.metadata} \
            --output-tree {output.tree} \
            --output-node-data {output.node_data} \
            --timetree \
            --coalescent {params.coalescent} \
            --date-confidence \
            --clock-rate {params.clock_rate} \
            --clock-std-dev {params.clock_std_dev} \
            --date-inference {params.date_inference} \
            --clock-filter-iqd {params.clock_filter_iqd}
        """

rule ancestral:
    message: "Reconstructing ancestral sequences and mutations"
    input:
        tree = rules.refine.output.tree,
        alignment = rules.align.output.alignment
    output:
        node_data = "ev_a71/{segments}/results/nt_muts.json"
    params:
        inference = "joint"
    shell:
        """
        augur ancestral \
            --tree {input.tree} \
            --alignment {input.alignment} \
            --output-node-data {output.node_data} \
            --inference {params.inference}
        """

rule translate:
    message: "Translating amino acid sequences"
    input:
        tree = rules.refine.output.tree,
        node_data = rules.ancestral.output.node_data,
        reference = reference
    output:
        node_data = "ev_a71/{segments}/results/aa_muts.json"
    shell:
        """
        augur translate \
            --tree {input.tree} \
            --ancestral-sequences {input.node_data} \
            --reference-sequence {input.reference} \
            --output-node-data {output.node_data} \
        """

rule clades:
    message: "Assigning clades according to nucleotide mutations"
    input:
        tree=rules.refine.output.tree,
        aa_muts = rules.translate.output.node_data,
        nuc_muts = rules.ancestral.output.node_data,
        clades = clades
    output:
        clade_data = "ev_a71/{segments}/results/clades.json"
    shell:
        """
        augur clades --tree {input.tree} \
            --mutations {input.nuc_muts} {input.aa_muts} \
            --clades {input.clades} \
            --output-node-data {output.clade_data}
        """

rule traits:
    message: "Inferring ancestral traits for {params.columns!s}"
    input:
        tree = rules.refine.output.tree,
        metadata = rules.date_parse.output.metadata
    output:
        node_data = "ev_a71/{segments}/results/traits.json",
    params:
        columns = "country"
    shell:
        """
        augur traits \
            --tree {input.tree} \
            --metadata {input.metadata} \
            --output-node-data {output.node_data} \
            --columns {params.columns} \
            --confidence
        """



rule export:
    message: "Exporting data files for for auspice"
    input:
        tree = rules.refine.output.tree,
        metadata = rules.date_parse.output.metadata,
        branch_lengths = rules.refine.output.node_data,
        traits = rules.traits.output.node_data,
        nt_muts = rules.ancestral.output.node_data,
        aa_muts = rules.translate.output.node_data,
        clades = rules.clades.output.clade_data,
        colors = colors,
        lat_longs = lat_longs,
        auspice_config = auspice_config
    output:
        auspice_json = rules.all.input.auspice_json,
    shell:
        """
        augur export v2 \
            --tree {input.tree} \
            --metadata {input.metadata} \
            --node-data {input.branch_lengths} {input.traits} {input.nt_muts} {input.aa_muts} {input.clades} \
            --colors {input.colors} \
            --lat-longs {input.lat_longs} \
            --auspice-config {input.auspice_config} \
            --output {output.auspice_json}
        """

rule clean:
    message: "Removing directories: {params}"
    params:
        "results ",
