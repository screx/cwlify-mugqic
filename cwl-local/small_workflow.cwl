cwlVersion: v1.0
class: Workflow

inputs:
  path_to_picard:
    type: File
  path_to_trimmomatic:
    type: File
  sam_files:
    type: File
  reference_genome:
    type: File
    secondaryFiles:
      - ^.fa.ann
      - ^.fa.amb
      - ^.fa.bwt
      - ^.fa.pac
      - ^.fa.sa
  bwa_mem_thread:
    type: int 
  bwa_mem_mark_shorter:
    type: boolean
  bwa_mem_hard_clipping:
    type: boolean
  bwa_paired_end_mode:
    type: boolean
  trimmomatic_min_len: int
  trimmomatic_sliding_window: string
  trimmomatic_trailing: int
  sort_sam_sort_order: string

requirements:
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
  MultipleInputFeatureRequirement: {}
  StepInputExpressionRequirement: {}

steps:
  samtofastq:
    requirements:
      InlineJavascriptRequirement: {}
    run: picard_sam_to_fastq.cwl
    in:
      path_to_picard: path_to_picard
      INPUT: sam_files
      FASTQ: 
        default: 1.fastq
      SECOND_END_FASTQ:  
        default: 2.fastq
    out: [fastq, fastq2]
  trimmomatic:
    requirements:
      InlineJavascriptRequirement: {}
    run: trimmomatic.cwl
    in:
      path_to_trimmomatic: path_to_trimmomatic
      paired_end:
        default: true
      phred33:
        default: true
      input_forward: samtofastq/fastq
      input_reverse: samtofastq/fastq2
      trailing: trimmomatic_trailing
      sliding_window: trimmomatic_sliding_window
      min_len: trimmomatic_min_len
    out: [forward_paired, reverse_paired, forward_unpaired, reverse_unpaired, trim_log]
  bwa_mem:
    requirements:
      ScatterFeatureRequirement: {}
      InlineJavascriptRequirement: {}

    run: bwa_mem.cwl
    in:
      reference: reference_genome
      reads: [trimmomatic/forward_paired, trimmomatic/reverse_paired]
      threads: bwa_mem_thread
      mark_shorter: bwa_mem_mark_shorter
      hard_clipping: bwa_mem_hard_clipping
      paired_end_mode: bwa_paired_end_mode
    scatter: reads
    out: [aligned_sam]
  picard_sort_sam:
    requirements: 
      ScatterFeatureRequirement: {}
    run: picard_sort_sam.cwl
    in:
      path_to_picard: path_to_picard
      input_file: [bwa_mem/aligned_sam]
      sort_order: sort_sam_sort_order
    out: [sorted_sam]
    scatter: input_file
outputs:
  aligned_sams:
    type: File[]
    outputSource: picard_sort_sam/sorted_sam
