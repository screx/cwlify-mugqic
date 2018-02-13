cwlVersion: v1.0
class: CommandLineTool
baseCommand: [java, -jar]
inputs:
  path_to_picard:
    type: File
    inputBinding:
      position: 0
  picard_command:
    type: string
    default: MergeSamFiles
    inputBinding:
      position: 1
  sam_files:
    type: 
      type: array
      items: File
      inputBinding:
        prefix: INPUT=
        separate: false
    inputBinding:
      position: 3
  validation_stringency:
    type: string?
    inputBinding:
      prefix: VALIDATION_STRINGENCY=
      separate: false
      position: 2
    default: LENIENT
  output_filename:
    type: string
    inputBinding:
      prefix: OUTPUT=
      separate: false
      position: 5
  sort_order:
    type: string?
    inputBinding:
      prefix: SORT_ORDER=
      position: 6
    default: coordinate
  assume_sorted:
    type: boolean?
    inputBinding:
      prefix: ASSUME_SORTED=
      position: 7
    default: false
outputs:
  merged_file:
    type: File
    outputBinding:
      glob: $(inputs.output_filename)
