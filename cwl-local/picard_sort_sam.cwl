cwlVersion: v1.0
baseCommand: [java, -jar]
class: CommandLineTool
requirements:
  InlineJavascriptRequirement: {}
inputs:
  path_to_picard:
    type: File
    inputBinding:
      position: 0
  picard_sort_sam:
    type: string
    inputBinding:
      position: 1
    default: SortSam
  input_file:
    type: File
    inputBinding:
      position: 2
      prefix: INPUT=
      separate: false
  output_file:
    type: string?
    inputBinding:
      prefix: OUTPUT=
      separate: false
      position: 3
      valueFrom: $(inputs.input_file.nameroot + "_sorted.sam")
  sort_order:
    type: string?
    inputBinding:
      position: 4
      separate: false
      prefix: SORT_ORDER=
    default: coordinate
outputs:
  sorted_sam:
    type: File
    outputBinding:
      glob: $(inputs.input_file.nameroot + "_sorted.sam")
