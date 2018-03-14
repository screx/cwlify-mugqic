cwlVersion: v1.0
class: CommandLineTool
baseCommand: [java, -jar]

inputs:
  path_to_gatk:
    type: [string, File]
    inputBinding: 
      position: 1
  indel_realigner:
    type: string
    inputBinding:
      position: 2
      prefix: -T
      separate: true
    default: IndelRealigner
  reference:
    type: [string, File]
    inputBinding:
      position: 3
      prefix: -R 
      separate: true
  input_bam:
    type: [string, File]
    inputBinding:
      position: 4
      prefix: -I
  known_indels:
    type: [string, File]
    inputBinding:
      position: 5
      prefix: -known 
      separate: true
  target_intervals:
    type: [string, File]
    inputBinding:
      position: 6
      prefix: -targetIntervals
      separate: true
  output_filename:
    type: string?
    default: $(inputs.input_bam + ".realigned.bam")

outputs:
  realigned_bam:
    type: File
    outputBinding:
      glob: *

