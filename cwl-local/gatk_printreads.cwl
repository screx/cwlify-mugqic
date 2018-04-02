class: CommandLineTool
cwlVersion: v1.0
baseCommand: [java, -jar]

inputs:
  path_to_gatk:
    type: [string,File]
    inputBinding:
      position: 1
	analysis_type:
		type: string
		default: PrintReads
		inputBinding:
			position: 2
			prefix: '--analysis_type'
      separate: true
  input_file:
    inputBinding:
      position: 3
      prefix: --input_file
      separate: true
    type: File
  reference_sequence:
    type: File
    inputBinding:
      prefix: --reference_sequence
      separate: true
      position: 4
  base_recal:
    type: int
    inputBinding:
      position: 5
      prefix: --BQSR
      separate: true
  output_filename:
    type: string
    inputBinding:
      position: 6
      prefix: --out
      separate: true

outputs:
  printed_reads:
    type: File
    outputBinding:
      glob: $(inputs.output_filename)