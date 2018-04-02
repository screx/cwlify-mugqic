cwlVersion: v1.0
class: CommandLineTool
baseCommand: [java, -jar]

inputs:
  path_to_picard:
    type: [File, string]
    inputBinding:
      position: 1
  sortSam:
    type: string
    default: SortSam
    inputBinding:
      position: 2
  sam:
    type: File
    inputBinding:
      prefix: I=
      separate: false
      position: 3
  output_filename:
    type: string
    inputBinding:
      position: 4
      prefix: O=
  sort_order:
    type: string
    inputBinding:
      position: 5
      prefix: SORT_ORDER= 
    default: coordinate
outputs:
  sorted:
    type: File
    outputBinding:
      glob: *