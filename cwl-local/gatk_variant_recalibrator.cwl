cwlVersion: v1.0
class: CommandLineTool
baseCommand: [java, -jar]

inputs:
	path_to_gatk:
		type: [File, string]
    inputBinding:
      position: 1
  variantRecalibator:
    type: string
    default: VariantRecalibrator
    inputBinding:
      position: 2
      prefix: -T
      separate: true
	variant_inputs:
    type: [File, File[]]
    inputBinding:
      position: 3
      prefix: -input 
      separate: true
  reference:
    type: File
    inputBinding:
      position: 4
      prefix: -R 
      separate: true
	resources:
    type: string[]
    inputBinding:
      position: 5
      prefix: "-resource:"
      itemSeparator: "\n"

	recal_file
	tranches_file
	mode
	use_annotation
	aggregate
	rscript_file
	ignore_filter
	input_model
	output_model
	target_titv
	tranche
	ignore_all_filters
	allele_specific_annotations
	badLodCutoff
	dirichlet
	max_attempts
	max_gaussians
	max_iterations
	maxNegativeGaussians
	MaxNumTrainingData
	MQCapforLogitJitterTransform
	numKmeans
	priorCounts
	shrinkage
	stdThreshold
	trustAllPolymorphic