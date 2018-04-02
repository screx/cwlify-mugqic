cwlVersion: v.1.0
class: CommandLineTool
baseCommand: [java, -jar]
requirements:
inputs:
  path_to_gatk:
    type: [File, string]
    inputBinding:
      position: 1
  callableLoci:
    type: string
    default: CallableLoci
    inputBinding:
      position: 2
      prefix: -T
      separate: true
  reference:
    type: File
    inputBinding:
      position: 3
      prefix: -R 
      separate: true
  input_bam:
    type: File
    inputBinding:
      position: 4
      prefix: -I
      separate: true
  summary_name:
    type: string
    inputBinding:
      position: 5
      prefix: -summary
      separate: true
  output_filename:
    type: string
    inputBinding:
      position: 6
      prefix: -o 
      separate: true
outputs:
  summary:
    type: File
    outputBinding:
  callable:
    type: File
    outputBinding:
