# Enterovirus A71 Nextstrain Analysis

This build performs a full Nextstrain analysis of Enterovirus A71. You can choose to run either a **>=600 bp VP1 run** or a **>=6400 bp whole genome run**.

This build could be extended in the future to do several additional things.
 1. The inclusion of additional metadata like patient age, granular spatial data or clinical outcomes.
 2. Automatic updates with the newest available sequences. See Emma Hodcroft' [Enterovirus D68 build](https://github.com/nextstrain/enterovirus_d68) for some efforts to implement this with a similar virus.

Data used for this build can be downloaded from [viprbrc.org](viprbrc.org). I've added instructions for how to download sequences manually at the end of this [README](#Sequences).

To learn more about Enterovirus A71, I recommend this very well written [review article by Solomon et al.](https://pubmed.ncbi.nlm.nih.gov/20961813/)

### Organization of repository:

This repo contains the following folders and files:

```
scripts
```
Custom python scripts which are being called from the `snakefile`.

```
snakefile
```
This file contains the entire computational pipeline. This file is using the **Snakemake workflow management system**, which allows elegant, reproducible biocomputational analyses. You can find snakemake's documentation [here](https://snakemake.readthedocs.io/en/stable/). If you want to change some part of the analysis, or call your own scripts, you need to edit this file.
```
vp1
```
Config files used for the **>=600 bp VP1 run**. In the folder `vp1/config` you can find config files (like coloring instructions and clade assignments) + a VP1 reference sequence containing VP1. Sequence data from ViPR should be saved as `vipr.fasta` in `vp1/data`.

```
whole_genome
```
Config files used for the **>=6400 bp whole genome run**. In the folder `whole_genome/config` you can find config files(like coloring instructions and clade assignments) + a whole genome reference sequence. Sequence data from ViPR should be saved as `vipr.fasta` in `whole_genome/data`

The reference sequence used for this build can be found [here](https://www.genome.jp/dbget-bin/www_bget?genbank-vrl:U22521). It was sequenced in **1970**, is called BrCr, its accession number is **U22521**.

# Quickstart

## Setup

### Nextstrain environment
To run this repository you need to install the Nextstrain environment. You can find detailed install instructions [here](https://docs.nextstrain.org/en/latest/guides/install/local-installation.html).

### Sequences

You need to download up-to-date sequences. This can be done via [viprbrc.org](viprbrc.org). On the landing page, pick **Enterovirus** (you should find this under the header "Featured Viruses").

Within the Enterovirus Taxonomy Browser, pick **Enterovirus A**. On the Genome Search page, click on "Search Criteria". There you can select Enterovirus A71 sequences. As of April 2021, there should be ~10'000 sequences. You do *NOT* need to specify sequence length, as subsampling by length is included in this build.

Sequences should be downloaded  in "Genome FASTA" format. Under **Format for FASTA file definition line** pick **Custom format**, adding *ALL* metadata fields. You can now download the sequences.

Save the resulting file as `vipr.fasta` in the folder `data`.

### Running build

Before running a build, you need to initialize nextstrain by executing
```
conda activate nextstrain
```

Following this you can create a **vp1 build** and a **whole genome build** simply by executing

```
snakemake --cores 1
```

If you only want one of those builds, you can either create a **vp1 build** by executing

```
snakemake ev_a71/vp1/auspice/ev_a71_vp1.json --cores 1
```

or you can create a **whole genome build** by executing
```
snakemake ev_a71/whole_genome/auspice/ev_a71_whole_genome.json --cores 1
```

### Visualizing build

If everything worked out, you can now visualize your build using auspice *(which is contained within nextstrain)*.

For the **vp1 build** do this via
```
auspice view --datasetDir ev_a71/vp1/auspice
```

For the **whole genome build** do this via
```
auspice view --datasetDir ev_a71/whole_genome/auspice
```

You might need to run the command `export PORT=4001` if you want to run two auspice visualizations at the same time.

## Feedback

If you have any questions or comments feel free to reach out via github, twitter (@Simon__Grimm) or via simon(dot)grimm(at)unibas(dot)ch.
