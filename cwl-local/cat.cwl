cwlVersion: v1.0
class: CommandLineTool
baseCommand: cat

inputs:
  inp_files:
    type: File[]
    inputBinding:
      position: 1
stdout: cat_out.txt

outputs:
  cat_out:
    type: stdout
