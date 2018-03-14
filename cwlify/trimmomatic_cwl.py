#!/usr/bin/env python

################################################################################
# Copyright (C) 2014, 2015 GenAP, McGill University and Genome Quebec Innovation Centre
#
# This file is part of MUGQIC Pipelines.
#
# MUGQIC Pipelines is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MUGQIC Pipelines is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with MUGQIC Pipelines.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

# Python Standard Modules
import logging
import os

# MUGQIC Modules
from core.config import *
from core.job import *

log = logging.getLogger(__name__)

# before trimmomatic_cwl is called


workflow = Workflow()

class MUGQICtoCWL:

	# ... picard
	def picard_sam_to_fastq():

	# when trimmomatic is called
	if 'picard_sam_to_fastq' in workflow.steps:
		input1 = 'picard_sam_to_fastq/fastq'
		input2 = 'picard_sam_to_fastq/fastq2'
	else if readset.fastq and readset.fastq2:
		input1 = 
		input2 =
	else:

	trimmomatic_cwl(input1, input2, ...)
	# and somehow that will chain them together because we know they interact in preset ways.

	def trimmomatic_cwl(
		input1,
		input2,
		paired_output1,
		unpaired_output1,
		paired_output2,
		unpaired_output2,
		single_output,
		quality_offset,
		adapter_file,
		trim_log,
		workflow
		):
		
		if input2:  # Paired end reads
			inputs = [input1, input2]
			outputs = [paired_output1, unpaired_output1, paired_output2, unpaired_output2]
		else:   # Single end reads
			inputs = [input1]
			outputs = [single_output]

		headcrop_length = config.param('trimmomatic', 'headcrop_length', required=False, type='posint')
		trimmomatic = CommandLineTool('trimmomatic')
		trimmomatic.add_input('fastq', input1)
		trimmomatic.add_input('trim_log', trim_log)
		if input2:
			trimmomatic.add_input('second_end_fastq', input2)
			trimmomatic.add_input('paired_output1', paired_output1)
			trimmomatic.add_input('paired_output2', paired_output2)
			trimmomatic.add_input('unpaired_output2', unpaired_output2)
			trimmomatic.add_input('unpaired_output1', unpaired_output1)
		if quality_offset == 64:
			trimmomatic.add_input('phred64', True)
		else:
			trimmomatic.add_input('phred33', True)

		workflow.add_step(trimmomatic)
		return
		# need to refactor eventually
		# but have this then add it to the workflow

# essentially I would have to map the function args to the input manually for each tool.
