cwlVersion: v1.0
class: CommandLineTool
baseCommand: [java, -jar]

inputs:
  bvatools:
    type: [File, string]
    inputBinding:
      position: 1
  groupfixmate:
    type: string
    default: groupfixmate
    inputBinding: 
      position: 2
  level:
    type: int
    inputBinding:
      prefix: --level
      separate: true
      position: 3
  bam:
    type: File
    inputBinding:
      prefix: --bam
      separate: true
      position: 4
  output_filename:
    type: string
    inputBinding:
      prefix: --out
      separate: true
      position: 5

outputs:
  groupfixmate:
    type: File
    outputBinding:
      glob: $(inputs.output_filename)

