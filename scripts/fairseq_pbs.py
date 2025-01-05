# e.g., python3 scripts/fairseq_pbs.py surSeg 25

import io, os, sys

second_string = '''#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=liu.ying@ufl.edu     # Where to send mail	
#SBATCH --ntasks=1                    # Run on a single CPU
#SBATCH --cpus-per-task=1                    
#SBATCH --mem=8gb                     # Job memory request
#SBATCH --time=120:00:00               # Time limit hrs:min:sec
#SBATCH --output=serial_test_%j.log   # Standard output and error log
#SBATCH --partition=gpu
#SBATCH --gpus=a100:1

pwd; hostname; date

module load conda
mamba activate fairseq-env

cd /blue/liu.ying/al_morph/

'''

task = sys.argv[1]

if not os.path.exists('pbs/'):
	os.system('mkdir pbs/')

lgs = ['bdg'] #['btz', 'cho', 'lez', 'ntu', 'tau', 'bdg']
sizes = ['500'] #, '1000', '1500', '2000', '2500', '3000']

iteration_sizes = [25] #, 50, 100, 200] # 250, 500]

initial_max_size = 5000

for lg in lgs:
	overall_max_size = 0
	train_reference = 'al_trainselect/train.' + lg + '_' + task + '50.input'
	select_reference = 'al_trainselect/select.' + lg + '_' + task + '50.input'
	 
	### Setting overall max size to be the full dataset (train + select)
	with open(train_reference) as train_reference_f:
		for line in train_reference_f:
			overall_max_size += 1
	with open(select_reference) as select_reference_f:
		for line in select_reference_f:
			overall_max_size += 1

	print(lg, overall_max_size)

	for size in sizes:
		for select_interval in iteration_sizes:
			select_interval = str(select_interval)
			for arch in ['transformer_tiny']:			
				with open('pbs/' + lg + '_' + task + size + '_' + select_interval + '.pbs', 'w') as f:
					first_string = '''#!/bin/bash\n#SBATCH --job-name=''' + lg + '_' + task + size + '_' + select_interval + '    # Job name'
					f.write(first_string + '\n')
					f.write(second_string + '\n')

					### Generating pbs files before reaching initial_max_size
					initial_iterations = (initial_max_size - int(size)) / int(select_interval) + 1
					select_list = []
					for i in range(int(initial_iterations)):
						select = i * int(select_interval)
						select_list.append(select)
						if int(size) + select <= initial_max_size:
							select = str(select)
							print(select)
							f.write('python scripts/fairseq_wu.py /blue/liu.ying/al_morph/al_trainselect/ ' + lg + ' ' + size + ' ' + select_interval + ' ' + select + ' ' + arch + ' ' + task + '\n')
							f.write('\n')

							f.write('module load python3' + '\n')
							f.write('\n')
							f.write('python scripts/eval.py /blue/liu.ying/al_morph/al_trainselect/ ' + lg + ' ' + size + ' ' + select_interval + ' ' + select + ' ' + arch + ' ' + task + '\n')
							f.write('\n')
							f.write('module load conda' + '\n')
							f.write('mamba activate fairseq-env' + '\n')
							f.write('\n')
						else:
							pass
				#	print(select_list)
					initial_max_select = max(select_list)
					print(initial_max_select)
					max_iterations = (overall_max_size - initial_max_select) / 200 + 1# After reaching 5000 words, increase at a constant step of 200 words
				#	print(size, select_interval, initial_max_select)
					for i in range(int(max_iterations)):
						select = initial_max_select + i * 200
						if int(size) + select <= overall_max_size:
							select = str(select)
				#			print(select)
							f.write('python scripts/fairseq_wu.py /blue/liu.ying/al_morph/al_trainselect/ ' + lg + ' ' + size + ' ' + select_interval + ' ' + select + ' ' + arch + ' ' + task + '\n')
							f.write('\n')

							f.write('module load python3' + '\n')
							f.write('\n')
							f.write('python scripts/eval.py /blue/liu.ying/al_morph/al_trainselect/ ' + lg + ' ' + size + ' ' + select_interval + ' ' + select + ' ' + arch + ' ' + task + '\n')
							f.write('\n')
							f.write('module load conda' + '\n')
							f.write('mamba activate fairseq-env' + '\n')
							f.write('\n')

					f.write('date' + '\n')
					f.write('\n')

					print('\n')
