cwlVersion: v1.0
class: CommandLineTool
baseCommand: [java, -jar]
requirements:
  - class: InlineJavascriptRequirement
inputs:
  path_to_trimmomatic:
    type: File
    inputBinding: 
      position: 1
  paired_end:
    type: boolean?
    inputBinding:
      prefix: PE
      position: 10
  single_end:
    type: boolean?
    inputBinding:
      prefix: SE
      position: 10
# phred33 vs phred64 use a record?
  phred33:
    type: boolean?
    inputBinding:
      prefix: -phred33
      position: 15
  phred64:
    type: boolean?
    inputBinding:
      prefix: -phred64
      position: 16
  input_forward:
    type: File
    inputBinding:
      position: 17    
  input_reverse:
    type: File
    inputBinding:
      position: 18    
  output_forward_paired:
    type: string?
    inputBinding:
      position: 19
      valueFrom: $(inputs.input_forward.nameroot + "_f_pair.fastq")     
  output_forward_unpaired:
    type: string?
    inputBinding:
      position: 20
      valueFrom: $(inputs.input_forward.nameroot + "_f_unpair.fastq")      
  output_reverse_paired:
    type: string?
    inputBinding:
      position: 21
      valueFrom: $(inputs.input_reverse.nameroot + "_r_pair.fastq")      
  output_reverse_unpaired:
    type: string?
    inputBinding:
      position: 22
      valueFrom: $(inputs.input_reverse.nameroot + "_r_unpair.fastq")     
  illumina_clip:
    type: string?
    inputBinding:
      prefix: 'ILLUMINACLIP:'
      separate: false 
      position: 23
  trailing:
    type: int
    inputBinding:
      prefix: 'TRAILING:'
      position: 24
      separate: false 
  sliding_window:
    type: string
    inputBinding:
      prefix: 'SLIDINGWINDOW:'
      position: 25
      separate: false
  min_len:
    type: int
    inputBinding:
      prefix: 'MINLEN:'
      position: 26
      separate: false      
outputs:
  forward_paired:
    type: File
    outputBinding:
      glob: $(inputs.input_forward.nameroot + "_f_pair.fastq")
  reverse_paired:
    type: File
    outputBinding:
      glob: $(inputs.input_reverse.nameroot + "_r_pair.fastq")
  forward_unpaired:
    type: File
    outputBinding:
      glob: $(inputs.input_forward.nameroot + "_f_unpair.fastq")
  reverse_unpaired:
    type: File
    outputBinding:
      glob: $(inputs.input_reverse.nameroot + "_r_unpair.fastq")
  trim_log:
    type: stderr
      
stderr: trim_log.txt
