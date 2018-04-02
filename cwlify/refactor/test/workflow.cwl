class: Workflow
cwlVersion: v1.0
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  ShellCommandRequirement: {}
  StepInputExpressionRequirement: {}
inputs:
  sam2fq_fastq:
    type: string
  sam2fq_input:
    type: File
  sam2fq_second_end_fastq:
    type: string
  shared_picard:
    type: File
  shared_trimmomatic:
    type: File
  trimmomatic_illumina_clip:
    type: string
  trimmomatic_min_len:
    type: int
  trimmomatic_paired_end:
    type: boolean
  trimmomatic_sliding_window:
    type: string
  trimmomatic_trailing:
    type: int
outputs:
  trim_forward_paired:
    outputSource: trimmomatic/forward_paired
    type: File
  trim_reverse_paired:
    outputSource: trimmomatic/reverse_paired
    type: File
steps:
  sam2fq:
    in:
      fastq: sam2fq_fastq
      input: sam2fq_input
      path_to_picard: shared_picard
      second_end_fastq: sam2fq_second_end_fastq
    out:
    - output_fastq
    - output_fastq2
    run: cwl/picard_sam_to_fastq.cwl
  trimmomatic:
    in:
      illumina_clip: trimmomatic_illumina_clip
      input_forward: sam2fq/output_fastq
      input_reverse: sam2fq/output_fastq2
      min_len: trimmomatic_min_len
      paired_end: trimmomatic_paired_end
      path_to_trimmomatic: shared_trimmomatic
      sliding_window: trimmomatic_sliding_window
      trailing: trimmomatic_trailing
    out:
    - forward_paired
    - reverse_paired
    - forward_unpaired
    - reverse_unpaired
    run: cwl/trimmomatic.cwl
