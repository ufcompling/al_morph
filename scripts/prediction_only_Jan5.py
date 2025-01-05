#!/usr/bin/env python
# coding: utf-8

import subprocess
import os
import sys, statistics
from datetime import datetime  

def main(datadir, lang, size, select_interval, select, arch, task):

	subprocess.run(['mkdir', '-p', datadir + lang + '_' + task + size])
	subprocess.run(['mkdir', '-p', datadir + lang + '_' + task + size + '/' + select_interval])
	subprocess.run(['mkdir', '-p', datadir + lang + '_' + task + size + '/' + select_interval + '/select' + select])
	subprocess.run(['mkdir', '-p', datadir + lang + '_' + task + size + '/' + select_interval + '/select' + select + '/' + arch])

	sub_datadir = datadir + lang + '_' + task + size + '/' + select_interval + '/select' + select + '/'
	previous_datadir = ''
	if select not in ['0', 'all']:
		previous_datadir = datadir + lang + '_' + task + size + '/' + select_interval + '/select' + str(int(select) - int(select_interval)) + '/'

	if select == '0':
		os.system('cp ' + 'al_trainselect/train.' + lang + '_' + task + size + '.input ' + sub_datadir)
		os.system('cp ' + 'al_trainselect/train.' + lang + '_' + task + size + '.output ' + sub_datadir)
		os.system('cp ' + 'al_trainselect/select.' + lang + '_' + task + size + '.input ' + sub_datadir)
		os.system('cp ' + 'al_trainselect/select.' + lang + '_' + task + size + '.output ' + sub_datadir)

	elif select == 'all':
		os.system('cat ' + 'al_trainselect/train.' + lang + '_' + task + size + '.input ' + 'al_trainselect/select.' + lang + '_' + task + size + '.input >' + sub_datadir + 'train.' + lang + '_' + task + size + '.input')
		os.system('cat ' + 'al_trainselect/train.' + lang + '_' + task + size + '.output ' + 'al_trainselect/select.' + lang + '_' + task + size + '.output >' + sub_datadir + 'train.' + lang + '_' + task + size + '.output')

	else:
		os.system('cat ' + previous_datadir + 'train.' + lang + '_' + task + size + '.input ' + previous_datadir + '/increment.input >' + sub_datadir + 'train.' + lang + '_' + task + size + '.input')
		os.system('cat ' + previous_datadir + 'train.' + lang + '_' + task + size + '.output ' + previous_datadir + '/increment.output >' + sub_datadir + 'train.' + lang + '_' + task + size + '.output')
		os.system('cp ' + previous_datadir + 'residual.input ' + sub_datadir + 'select.' + lang + '_' + task + size + '.input')
		os.system('cp ' + previous_datadir + 'residual.output ' + sub_datadir + 'select.' + lang + '_' + task + size + '.output')

	SRC = lang + '_' + task + size + '.input'
	TGT = lang + '_' + task + size + '.output'
	TESTIN = datadir + 'test.' + lang + '_' + task + '.input'
	TO_PREDICT = sub_datadir + 'select.'+ lang + '_' + task + size + '.input'

	### Collecting the pool of words to select from
	select_input = []
	select_output = []
	select_combo = []
	if select != 'all':
		with open(sub_datadir + 'select.'+ lang + '_' + task + size + '.input') as f:
			for line in f:
				toks = line.strip()
				select_input.append(toks)

	
		with open(sub_datadir + 'select.'+ lang + '_' + task + size + '.output') as f:
			for line in f:
				toks = line.strip()
				select_output.append(toks)

		select_combo = [select_input[i] + '_' + select_output[i] for i in range(len(select_input))]

	confidence_dict = {}

	for seed in ['1', '2']:
		PREDDIR = datadir + lang + '_' + task + size + '/' + select_interval + '/select' + select + '/' + arch + '/' + seed + '/preds/' ## seed
		FROMDIR = datadir + lang + '_' + task + size + '/' + select_interval + '/select' + select + '/' + arch + '/' + seed + '/data-bin/'
		SAVEDIR = datadir + lang + '_' + task + size + '/' + select_interval + '/select' + select + '/' + arch + '/' + seed + '/checkpoints/'
	#    SCOREDIR = datadir + experiment + '/' + task + '/' + arch + '/' + seed + '/scores/'
	
		MODELPATH = SAVEDIR + 'checkpoint_best.pt'   
	
		GUESSPATH = PREDDIR + lang + '_' + task + size + '.testpredict'
		U_CONFIDENCE = ''
		U_PREDICTIONS = ''
		if select != 'all':
			U_CONFIDENCE = PREDDIR + lang + '_' + task + size + '.confidence'
			U_PREDICTIONS = PREDDIR + lang + '_' + task + size + '.predict'
		else:
			pass

		if select != 'all':

			## Extracting confidence scores
			confidence_scores = []
			with open(U_CONFIDENCE) as f:
				for line in f:
					toks = line.strip().split('\t')
					confidence_scores.append(toks[1])
			
			## Do not merge duplicates
			for i in range(len(select_output)):
				pair = select_input[i] + '_' + select_output[i] + '\t' + str(i)
				confidence_score = confidence_scores[i]
				if seed == '1':
					confidence_dict[pair] = [float(confidence_score)]
				else:
					confidence_dict[pair].append(float(confidence_score))

		else:
			pass

		### Cleaning space
	#	subprocess.run(['rm', '-rf', FROMDIR])

	### Selecting words

	if select != 'all':
		for k, v in confidence_dict.items():
			confidence_dict[k] = statistics.mean(v)
	
		sorted_confidence_dict = sorted(confidence_dict.items(), key = lambda item: item[1])
		increment_words = sorted_confidence_dict[ : int(select_interval)]
	#	for combo in increment_words:
	#		print(combo[0], confidence_dict[combo[0]])
	#	print('')
	#	print('')
	#	for combo in sorted_confidence_dict[int(select_interval) + 1 : int(select_interval) + 5]:
	#		print(combo[0], confidence_dict[combo[0]])

		increment_input = open(sub_datadir + 'increment.input', 'w')
		increment_output = open(sub_datadir + 'increment.output', 'w')
		increment_pairs = []
		for combo in increment_words:
			pair = combo[0]
			print(pair)
			increment_pairs.append(pair)
			pair = pair.split('\t')[0].split('_')
			print(pair)
			print('\n')
			w_input = pair[0]
			w_output = pair[1]
			increment_input.write(w_input + '\n')
			increment_output.write(w_output + '\n')

		print('')
		print('Start writing residual output' + '\n')
		residual_input = open(sub_datadir + 'residual.input', 'w')
		residual_output = open(sub_datadir + 'residual.output', 'w')
		print('Increment pairs length: ', len(increment_pairs))
		print('Select combo length: ', len(select_combo))
		for tok in sorted_confidence_dict:
			pair = tok[0]
	#	for pair in select_combo:
			if pair not in increment_pairs:
				pair = pair.split('\t')[0].split('_')
				w_input = pair[0]
				w_output = pair[1]
				residual_input.write(w_input + '\n')
				residual_output.write(w_output + '\n')


if __name__== '__main__':

	evaluation_file = sys.argv[1] + sys.argv[2] + '_' +  sys.argv[7] + sys.argv[3] + '/' + sys.argv[4] + '/select' + sys.argv[5] + '/' + sys.argv[6] + '/eval.txt'
#	if os.path.exists(evaluation_file) and os.stat(evaluation_file).st_size != 0:
#		pass
#	else:
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
	print('\n########### FINISHED ', sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], ' ###########\n')
