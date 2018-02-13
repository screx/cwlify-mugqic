cwlVersion: v1.0
class: CommandLineTool
baseCommand: java
arguments: [-jar]

inputs:
  path_to_picard:
    type: File
    inputBinding:
      position: 1
  sam_to_fastq:
    type: string
    inputBinding:
      position: 5
    default: "SamToFastq"
  input:
    type: File
    inputBinding:
      position: 9
      prefix: INPUT=
      separate: false
  validation_stringency:
    type: boolean?
    inputBinding:
      position: 10
      prefix: VALIDATION_STRINGENCY=LENIENT
    default: true
  fastq:
    type: string
    inputBinding:
      position: 11
      prefix: FASTQ=
      separate: false
  second_end_fastq:
    type: string?
    inputBinding:
      position: 12
      prefix: SECOND_END_FASTQ=
      separate: false
  output_per_rg:
    type: boolean?
    inputBinding:
      position: 13
      prefix: OUTPUT_PER_RG=true
  rg_tag:
    type: string?
    inputBinding:
      position: 14
      prefix: INPUT
      separate: false
  output_dir:
    type: string?
    inputBinding:
      position: 15
  re_reverse:
    type: string?
    inputBinding:
      position: 16
      prefix: RE_REVERSE=
  interleave:
    type: string?
    inputBinding:
      position: 17
      prefix: INTERLEAVE=

outputs:
  fastq:
    type: File
    outputBinding:
      glob: $(inputs.FASTQ)
  fastq2:
    type: File?
    outputBinding:
      glob: $(inputs.SECOND_END_FASTQ)

