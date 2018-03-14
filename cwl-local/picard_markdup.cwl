cwlVersion: v1.0
class: CommandLineTool
baseCommand: [java, -jar]

inputs:
    picard:
      type: [File, string]
      inputBinding:
        position: 1
        valueFrom: $(picard + "/Markduplicates.jar")
    removeDuplicates:
      type: string
      inputBinding:
        position: 2
        separate: false
        prefix: REMOVE_DUPLICATES=
    validationStringency:
      type: string
      inputBinding:
        position: 3
        separate: false
        prefix: VALIDATION_STRINGENCY=
    createIndex:
      type: string
      inputBinding:
        position: 4
        separate: false
        prefix: CREATE_INDEX=
      default: true
    outputFilename:
      type: string
      inputBinding:
        position: 5
        prefix: OUTPUT=
        separate: false
    metricsFile:
      type: File
      inputBinding:
        position: 6
        prefix: METRICS_FILE=
        separate: False
    maxRecordsInRam:
      type: int
      inputBinding:
        position: 7
        prefix: MAX_RECORDS_IN_RAM=
        separate: false

outputs:
  markdup:
    type: File
    outputBinding:
      glob: $(inputs.outputFilename)


