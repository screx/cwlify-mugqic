cwlVersion: v1.0
baseCommand: echo
class: CommandLineTool

inputs:
  message:
    type: string
    inputBinding:
      position: 1
outputs:
  echo_out:
    type: stdout
stdout: strings.txt

