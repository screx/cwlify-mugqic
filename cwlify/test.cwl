class: Workflow
cwlVersion: v1.0
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  ShellCommandRequirement: {}
  StepInputExpressionRequirement: {}
inputs:
  trimmomatic_paired_end:
    type: boolean
  trimmomatic_path:
    type: File
outputs:
  trim_forward_paired:
    output_source: trimmomatic/forward_paired
  trim_reverse_paired:
    output_source: trimmomatic/reverse_paired
steps:
  trimmomatic:
    in:
      paired_end: trimmomatic_paired_end
      path_to_picard: trimmomatic_path
    out:
    - forward_paired
    - reverse_paired
    - forward_unpaired
    - reverse_unpaired
    run: trimmomatic.cwl
