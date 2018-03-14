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
  level:
    type: int
    inputBinding:
      prefix: --level
      separate: true
      position: 2
  bam:
    type: File
    inputBinding:
      prefix: --bam
      separate: true
      position: 3
  output_filename:
    type: string
    inputBinding:
      prefix: --out
      separate: true
      position: 4

outputs:
  groupfixmate:
    type: File
    outputBinding:
      glob: $(inputs.output_filename)

