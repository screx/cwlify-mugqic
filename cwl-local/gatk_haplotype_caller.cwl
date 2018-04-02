cwlVersion: v1.0
class: CommandLineVersion
baseCommand: [java, -jar]
requirements:
inputs:
  path_to_gatk:
    type: [File, string]
    inputBinding:
      position: 1
  haplotypeCaller:
    type: string
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
  inputBam:
    type: [File, File[]]
    inputBinding:
      itemSeparator: " "
      position: 4
      separate: true
      prefix: -I
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
