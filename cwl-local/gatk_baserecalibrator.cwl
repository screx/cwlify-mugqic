class: CommandLineTool
cwlVersion: v1.0
baseCommand: [java, -jar]

inputs:
  path_to_gatk:
    type: [string, File]
    inputBinding:
      position: 1
  analysis_type:
    default: BaseRecalibrator
    inputBinding:
      prefix: --analysis_type
      position: 2
      separate: true
    type: string
  input_file:
    type: File
    inputBinding:
      position: 3
      prefix: --input_file
      separate: true
  reference_sequence:
    type: File
    inputBinding:
      position: 4
      prefix: --reference_sequence
      separate: true
  intervals:
    type: string?
    inputBinding:
      position: 5
      prefix: --intervals
      separate: true
  known_snp_sites:
    type: string
    inputBinding:
      position: 6
      prefix: --knownSites
      separate: true
  known_indel_sites:
    type: string
    inputBinding:
      position: 7
      prefix: --knownSites
      separate: true
  output_filename:
    type: string
    inputBinding:
      position: 8
      prefix: --out
      separate: true
outputs:
  recalibrated:
    type: File
    outputBinding:
      glob: $(inputs.output_filename)