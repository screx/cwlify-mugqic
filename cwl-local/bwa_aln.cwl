cwlVersion: v1.0
class: CommandLineTool
baseCommand: bwa mem

inputs:
  max_edit_distance:
    type: int? 
    inputBinding:
      prefix: -n
      separate: true
      position:
  max_gap_open:
    type: int?
    inputBinding:
      prefix: -o
      position:
  max_gap_extension:
    type: int?
    inputBinding:
      prefix: -e
      separate: true
      position:
  long_deletion_threshold:
    type: int?
    inputBinding:
      prefix: -d
      separate: true
      position:
  indel_threshold:
    type: int?
    inputBinding:
      prefix: -i
      separate: true
      position:
  seed_distance:
    type: int?
    inputBinding:
      prefix: -l
      separate: true
      position:
  max_seed_edit_distance:
    type: int?
    inputBinding:
      prefix: -d
      separate: true
      position:
  threads:
    type: int?
    inputBinding:
      prefix: -t
      separate: true
      position:
  mismatch_penalty:
    type: int?
    inputBinding:
      prefix: -M
      separate: true
      position:
  gap_open_penalty:
    type: int?
    inputBinding:
      prefix: -O
      separate: true
      position:
  gap_extension_penalty:
    type: int?
    inputBinding:
      prefix: -E
      separate: true
      position:
  suboptimal_alignment_threshold:
    type: int?
    inputBinding:
      prefix: -R
      separate: true
      position:             
  reverse_query:
    type: int?
    inputBinding:
      prefix: -c
      separate: true
      position:
  disable_iterative_search:
    type: boolean?
    inputBinding:
      prefix: -N
      position:
  read_trimming_length:
    type: int?
    inputBinding:
      prefix: -q
      separate: true
      position:                    
  illumina_1.3:
    type: boolean?
    inputBinding:
      prefix: -I
      position:
  barcode_length:
    type: int?
    inputBinding:
      prefix: -B
      separate: true
      position:
  bam_input:
    type: -b
    inputBinding:
      prefix: -I
      position:          