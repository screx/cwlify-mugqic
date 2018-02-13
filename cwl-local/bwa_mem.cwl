cwlVersion: v1.0
class: CommandLineTool
baseCommand: bwa
requirements: 
  InlineJavascriptRequirement: {}

inputs:
  bwa_type:
    type: string
    default: mem
    inputBinding:
      position: 0
  threads:
    type: int?
    label: number of threads
    inputBinding:
      prefix: -t 
      separate: true
      position: 2
  min_seed_length:
    type: int?
    label: Minimum seed length.
    inputBinding:
      prefix: -k 
      separate: true
      position: 3
  min_band_width:
    type: int?
    label: Band Width
    inputBinding:
      prefix: -w 
      separate: true
      position: 4
  off_diagonal_x_dropoff:
    type: int?
    label: off-diagonal x-dropoff(z-dropoff)
    inputBinding:
      prefix: -d 
      separate: true
      position: 5
  trigger_reseeding_value:
    type: float?
    label: Trigger re-seeding for a MEM longer than minSeedLen*FLOAT
    inputBinding:
      prefix: -r 
      separate: true
      position: 6
  discard_occurence_threshold:
    type: int?
    label: Discard a MEM if it has more than INT occurence in the genome.
    inputBinding:
      prefix: -c
      separate: true
      position: 7
  paired_end_mode:
    type: boolean?
    label: In the paired-end mode, perform SW to rescue missing hits
    inputBinding:
      prefix: -p
      separate: true
      position: 1
  match_score:
    type: int?
    label: Matching Score
    inputBinding:
      prefix: -A
      separate: true
      position: 8
  mismatch_penalty:
    type: int?
    label: mismatch penalty
    inputBinding:
      prefix: -B
      separate: true
      position: 9
  gap_open_penalty:
    type: int?
    label: gap open penalty
    inputBinding:
      prefix: -O
      separate: true
      position: 10
  gap_extension_penalty:
    type: int?
    label: gap extension penalty
    inputBinding:
      prefix: -E
      separate: true
      position: 11
  clipping_penalty:
    type: int?
    label: clipping penalty
    inputBinding:
      prefix: -L
      separate: true
      position: 12
  unpaired_penalty:
    type: int?
    label: upaired read pair penalty
    inputBinding:
      prefix: -U
      separate: true
      position: 13
  read_group_header_line:
    type: string?
    label: Complete read group header line
    inputBinding:
      prefix: -R
      separate: true
      position: 14
  score_threshold:
    type: int?
    label: will not output alignment with scores lower than score_threshold
    inputBinding:
      prefix: -T
      separate: true
      position: 15
  output_all:
    type: boolean?
    label: Output all found alignments 
    inputBinding:
      prefix: -a
      separate: true
      position: 1
  append_comments:
    type: boolean?
    label: append FASTA/Q comment to SAM output
    inputBinding:
      prefix: -c
      separate: true
      position: 1
  hard_clipping:
    type: boolean?
    label: Use hard clipping ’H’ in the SAM output
    inputBinding:
      prefix: -H
      separate: true
      position: 1
  mark_shorter:
    type: boolean?
    label: 
    inputBinding:
      prefix: -M
      separate: true
      position: 1
  verbose_level:
    type: int?
    label:  Control the verbose level of the output
    inputBinding:
      prefix: -v
      separate: true
      position: 16
  reference:
    type: File
    inputBinding:
      position: 17
    secondaryFiles:
      - .ann
      - .amb
      - .bwt
      - .pac
      - .sa
  reads:
    type: File
    inputBinding:
      position: 18
      
outputs:
  aligned_sam:
    type: stdout


stdout: $(inputs.reads.nameroot + "_aligned.sam")

