[TOC]


DNA-Seq Pipeline
================

The standard MUGQIC DNA-Seq pipeline uses BWA to align reads to the reference genome. Treatment
and filtering of mapped reads approaches as INDEL realignment, mark duplicate reads, recalibration
and sort are executed using Picard and GATK. Samtools MPILEUP and bcftools are used to produce
the standard SNP and indels variants file (VCF). Additional SVN annotations mostly applicable
to human samples include mappability flags, dbSNP annotation and extra information about SVN
by using published databases.  The SNPeff tool is used to annotate variants using an integrated database
of functional predictions from multiple algorithms (SIFT, Polyphen2, LRT and MutationTaster, PhyloP and GERP++, etc.)
and to calculate the effects they produce on known genes. A list of effects and annotations
that SnpEff calculate can be found [here](http://snpeff.sourceforge.net/faq.html#What_effects_are_predicted?).

A summary html report is automatically generated by the pipeline. This report contains description
of the sequencing experiment as well as a detailed presentation of the pipeline steps and results.
Various Quality Control (QC) summary statistics are included in the report and additional QC analysis
is accessible for download directly through the report. The report includes also the main references
of the software and methods used during the analysis, together with the full list of parameters
that have been passed to the pipeline main script.

An example of the DNA-Seq report for an analysis on public data  is available for illustration purpose only:
[DNA-Seq report](http://gqinnovationcenter.com/services/bioinformatics/tools/dnaReport/index.html).

[Here](https://bitbucket.org/mugqic/mugqic_pipelines/downloads/MUGQIC_Bioinfo_DNA-Seq.pptx)
is more information about DNA-Seq pipeline that you may find interesting.


Usage
-----
```
#!text

usage: dnaseq.py [-h] [--help] [-c CONFIG [CONFIG ...]] [-s STEPS]
                 [-o OUTPUT_DIR] [-j {pbs,batch,daemon}] [-f] [--json]
                 [--report] [--clean] [-l {debug,info,warning,error,critical}]
                 [-t {mugqic,mpileup}] [-r READSETS] [-v]

Version: 3.0.1-beta

For more documentation, visit our website: https://bitbucket.org/mugqic/mugqic_pipelines/

optional arguments:
  -h                    show this help message and exit
  --help                show detailed description of pipeline and steps
  -c CONFIG [CONFIG ...], --config CONFIG [CONFIG ...]
                        config INI-style list of files; config parameters are
                        overwritten based on files order
  -s STEPS, --steps STEPS
                        step range e.g. '1-5', '3,6,7', '2,4-8'
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        output directory (default: current)
  -j {pbs,batch,daemon}, --job-scheduler {pbs,batch,daemon}
                        job scheduler type (default: pbs)
  -f, --force           force creation of jobs even if up to date (default:
                        false)
  --json                create a JSON file per analysed sample to track the
                        analysis status (default: false)
  --report              create 'pandoc' command to merge all job markdown
                        report files in the given step range into HTML, if
                        they exist; if --report is set, --job-scheduler,
                        --force, --clean options and job up-to-date status are
                        ignored (default: false)
  --clean               create 'rm' commands for all job removable files in
                        the given step range, if they exist; if --clean is
                        set, --job-scheduler, --force options and job up-to-
                        date status are ignored (default: false)
  -l {debug,info,warning,error,critical}, --log {debug,info,warning,error,critical}
                        log level (default: info)
  -t {mugqic,mpileup}, --type {mugqic,mpileup}
                        DNAseq analysis type
  -r READSETS, --readsets READSETS
                        readset file
  -v, --version         show the version information and exit

Steps:
------

----
mugqic:
1- picard_sam_to_fastq
2- trimmomatic
3- merge_trimmomatic_stats
4- bwa_mem_picard_sort_sam
5- picard_merge_sam_files
6- gatk_indel_realigner
7- merge_realigned
8- fix_mate_by_coordinate
9- picard_mark_duplicates
10- recalibration
11- verify_bam_id
12- metrics
13- picard_calculate_hs_metrics
14- gatk_callable_loci
15- extract_common_snp_freq
16- baf_plot
17- gatk_haplotype_caller
18- merge_and_call_individual_gvcf
19- combine_gvcf
20- merge_and_call_combined_gvcf
21- variant_recalibrator
22- dna_sample_metrics
23- haplotype_caller_filter_nstretches
24- haplotype_caller_flag_mappability
25- haplotype_caller_snp_id_annotation
26- haplotype_caller_snp_effect
27- haplotype_caller_dbnsfp_annotation
28- haplotype_caller_metrics_vcf_stats
29- haplotype_caller_metrics_snv_graph_metrics
----
mpileup:
1- picard_sam_to_fastq
2- trimmomatic
3- merge_trimmomatic_stats
4- bwa_mem_picard_sort_sam
5- picard_merge_sam_files
6- gatk_indel_realigner
7- merge_realigned
8- fix_mate_by_coordinate
9- picard_mark_duplicates
10- recalibration
11- metrics
12- picard_calculate_hs_metrics
13- gatk_callable_loci
14- extract_common_snp_freq
15- baf_plot
16- gatk_haplotype_caller
17- merge_and_call_individual_gvcf
18- combine_gvcf
19- merge_and_call_combined_gvcf
20- variant_recalibrator
21- dna_sample_metrics
22- rawmpileup
23- rawmpileup_cat
24- snp_and_indel_bcf
25- merge_filter_bcf
26- mpileup_filter_nstretches
27- mpileup_flag_mappability
28- mpileup_snp_id_annotation
29- mpileup_snp_effect
30- mpileup_dbnsfp_annotation
31- mpileup_metrics_vcf_stats
32- mpileup_metrics_snv_graph_metrics
33- verify_bam_id

```
1- picard_sam_to_fastq
----------------------
Convert SAM/BAM files from the input readset file into FASTQ format
if FASTQ files are not already specified in the readset file. Do nothing otherwise.

2- trimmomatic
--------------
Raw reads quality trimming and removing of Illumina adapters is performed using [Trimmomatic](http://www.usadellab.org/cms/index.php?page=trimmomatic).
If an adapter FASTA file is specified in the config file (section 'trimmomatic', param 'adapter_fasta'),
it is used first. Else, 'Adapter1' and 'Adapter2' columns from the readset file are used to create
an adapter FASTA file, given then to Trimmomatic. For PAIRED_END readsets, readset adapters are
reversed-complemented and swapped, to match Trimmomatic Palindrome strategy. For SINGLE_END readsets,
only Adapter1 is used and left unchanged.

This step takes as input files:

1. FASTQ files from the readset file if available
2. Else, FASTQ output files from previous picard_sam_to_fastq conversion of BAM files

3- merge_trimmomatic_stats
--------------------------
The trim statistics per readset are merged at this step.

4- bwa_mem_picard_sort_sam
--------------------------
The filtered reads are aligned to a reference genome. The alignment is done per sequencing readset.
The alignment software used is [BWA](http://bio-bwa.sourceforge.net/) with algorithm: bwa mem.
BWA output BAM files are then sorted by coordinate using [Picard](http://broadinstitute.github.io/picard/).

This step takes as input files:

1. Trimmed FASTQ files if available
2. Else, FASTQ files from the readset file if available
3. Else, FASTQ output files from previous picard_sam_to_fastq conversion of BAM files

5- picard_merge_sam_files
-------------------------
BAM readset files are merged into one file per sample. Merge is done using [Picard](http://broadinstitute.github.io/picard/).

This step takes as input files:

1. Aligned and sorted BAM output files from previous bwa_mem_picard_sort_sam step if available
2. Else, BAM files from the readset file

6- gatk_indel_realigner
-----------------------
Insertion and deletion realignment is performed on regions where multiple base mismatches
are preferred over indels by the aligner since it can appear to be less costly by the algorithm.
Such regions will introduce false positive variant calls which may be filtered out by realigning
those regions properly. Realignment is done using [GATK](https://www.broadinstitute.org/gatk/).
The reference genome is divided by a number regions given by the `nb_jobs` parameter.

7- merge_realigned
------------------
BAM files of regions of realigned reads are merged per sample using [Picard](http://broadinstitute.github.io/picard/).

8- fix_mate_by_coordinate
-------------------------
Fix the read mates. Once local regions are realigned, the read mate coordinates of the aligned reads
need to be recalculated since the reads are realigned at positions that differ from their original alignment.
Fixing the read mate positions is done using [BVATools](https://bitbucket.org/mugqic/bvatools).

9- picard_mark_duplicates
-------------------------
Mark duplicates. Aligned reads per sample are duplicates if they have the same 5' alignment positions
(for both mates in the case of paired-end reads). All but the best pair (based on alignment score)
will be marked as a duplicate in the BAM file. Marking duplicates is done using [Picard](http://broadinstitute.github.io/picard/).

10- recalibration
-----------------
Recalibrate base quality scores of sequencing-by-synthesis reads in an aligned BAM file. After recalibration,
the quality scores in the QUAL field in each read in the output BAM are more accurate in that
the reported quality score is closer to its actual probability of mismatching the reference genome.
Moreover, the recalibration tool attempts to correct for variation in quality with machine cycle
and sequence context, and by doing so, provides not only more accurate quality scores but also
more widely dispersed ones.

11- verify_bam_id
-----------------
verifyBamID is a software that verifies whether the reads in particular file match previously known
genotypes for an individual (or group of individuals), and checks whether the reads are contaminated
as a mixture of two samples. verifyBamID can detect sample contamination and swaps when external
genotypes are available. When external genotypes are not available, verifyBamID still robustly
detects sample swaps.

12- metrics
-----------
Compute metrics and generate coverage tracks per sample. Multiple metrics are computed at this stage:
Number of raw reads, Number of filtered reads, Number of aligned reads, Number of duplicate reads,
Median, mean and standard deviation of insert sizes of reads after alignment, percentage of bases
covered at X reads (%_bases_above_50 means the % of exons bases which have at least 50 reads)
whole genome or targeted percentage of bases covered at X reads (%_bases_above_50 means the % of exons
bases which have at least 50 reads). A TDF (.tdf) coverage track is also generated at this step
for easy visualization of coverage in the IGV browser.

13- picard_calculate_hs_metrics
-------------------------------
Compute on target percent of hybridisation based capture.

14- gatk_callable_loci
----------------------
Computes the callable region or the genome as a bed track.

15- extract_common_snp_freq
---------------------------
Extracts allele frequencies of possible variants accross the genome.

16- baf_plot
------------
Plots DepthRatio and B allele frequency of previously extracted alleles.

17- gatk_haplotype_caller
-------------------------
GATK haplotype caller for snps and small indels.

18- merge_and_call_individual_gvcf
----------------------------------
Merges the gvcfs of haplotype caller and also generates a per sample vcf containing genotypes.

19- combine_gvcf
----------------
Combine the per sample gvcfs of haplotype caller into one main file for all sample.

20- merge_and_call_combined_gvcf
--------------------------------
Merges the combined gvcfs and also generates a general vcf containing genotypes.

21- variant_recalibrator
------------------------
GATK VariantRecalibrator.
The purpose of the variant recalibrator is to assign a well-calibrated probability to each variant call in a call set.
You can then create highly accurate call sets by filtering based on this single estimate for the accuracy of each call.
The approach taken by variant quality score recalibration is to develop a continuous, covarying estimate of the relationship
between SNP call annotations (QD, MQ, HaplotypeScore, and ReadPosRankSum, for example) and the probability that a SNP
is a true genetic variant versus a sequencing or data processing artifact. This model is determined adaptively based
on "true sites" provided as input, typically HapMap 3 sites and those sites found to be polymorphic on the Omni 2.5M SNP
chip array. This adaptive error model can then be applied to both known and novel variation discovered in the call set
of interest to evaluate the probability that each call is real. The score that gets added to the INFO field of each variant
is called the VQSLOD. It is the log odds ratio of being a true variant versus being false under the trained Gaussian mixture model.
Using the tranche file generated by the previous step the ApplyRecalibration walker looks at each variant's VQSLOD value
and decides which tranche it falls in. Variants in tranches that fall below the specified truth sensitivity filter level
have their filter field annotated with its tranche level. This will result in a call set that simultaneously is filtered
to the desired level but also has the information necessary to pull out more variants for a higher sensitivity but a
slightly lower quality level.

22- dna_sample_metrics
----------------------
Merge metrics. Read metrics per sample are merged at this step.

23- haplotype_caller_filter_nstretches
--------------------------------------
See general filter_nstretches description !  Applied to haplotype caller vcf

24- haplotype_caller_flag_mappability
-------------------------------------
See general flag_mappability !  Applied to haplotype caller vcf

25- haplotype_caller_snp_id_annotation
--------------------------------------
See general snp_id_annotation !  Applied to haplotype caller vcf

26- haplotype_caller_snp_effect
-------------------------------
See general snp_effect !  Applied to haplotype caller vcf

27- haplotype_caller_dbnsfp_annotation
--------------------------------------
See general dbnsfp_annotation !  Applied to haplotype caller vcf

28- haplotype_caller_metrics_vcf_stats
--------------------------------------
See general metrics_vcf_stats !  Applied to haplotype caller vcf

29- haplotype_caller_metrics_snv_graph_metrics
----------------------------------------------
See general metrics_vcf_stats !  Applied to haplotype caller vcf

