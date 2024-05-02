import io, os

second_string = '''#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=liu.ying@ufl.edu     # Where to send mail	
#SBATCH --ntasks=1                    # Run on a single CPU
#SBATCH --cpus-per-task=1                    
#SBATCH --mem=8gb                     # Job memory request
#SBATCH --time=48:00:00               # Time limit hrs:min:sec
#SBATCH --output=serial_test_%j.log   # Standard output and error log
#SBATCH --partition=gpu
#SBATCH --gpus=a100:1

pwd; hostname; date

module load conda
mamba activate al
module load fairseq

cd /blue/liu.ying/al_morphseg/

'''

if not os.path.exists('pbs/'):
	os.system('mkdir pbs/')

#lgs = ['btz', 'cho', 'lez', 'ntu', 'tau']
lgs = ['bdg']
sizes = ['50', '100', '500', '1000', '1500', '2000']

overall_max_size = 0

for task in ['surSeg', 'surSegGls', 'gls']:
	for lg in lgs:
		for size in sizes:
			select_file = '/blue/liu.ying/al_morphseg/al_trainselect/select.' + lg + '_' + task + size + '.input'
			max_size = 0
			with open(select_file) as f:
				for line in f:
					max_size += 1

			if max_size > overall_max_size:
				overall_max_size = max_size

			iterations = int(max_size / 25)
			for i in range(iterations):
				select = str(i * 25)
				for arch in ['transformer']: #, 'transformer_tiny', 'lstm']:

					with open('pbs/' + lg + '_' + task + size + '_select' + select + '_' + arch +'.pbs', 'w') as f:
						first_string = '''#!/bin/bash\n#SBATCH --job-name=''' + lg + '_' + task + size + '_select' + select + '_' + arch + '    # Job name'

						f.write(first_string + '\n')
						f.write(second_string + '\n')

						f.write('python scripts/fairseq_wu.py /blue/liu.ying/al_morphseg/al_trainselect/ ' + lg + ' ' + size + ' ' + select + ' ' + arch + ' ' + task + '\n')
						f.write('\n')

						f.write('module unload fairseq' + '\n')
						f.write('module load python3' + '\n')
						f.write('\n')
						f.write('python scripts/eval.py /blue/liu.ying/al_morphseg/al_trainselect/ ' + lg + ' ' + size + ' ' + select + ' ' + arch + ' ' + task + '\n')
						f.write('\n')
			
						f.write('date' + '\n')
						f.write('\n')

			select = 'all'
			for arch in ['transformer']: #, 'transformer_tiny', 'lstm']:

				with open('pbs/' + lg + '_' + task + size + '_select' + select + '_' + arch +'.pbs', 'w') as f:
					first_string = '''#!/bin/bash\n#SBATCH --job-name=''' + lg + '_' + task + size + '_select' + select + '_' + arch + '    # Job name'

					f.write(first_string + '\n')
					f.write(second_string + '\n')

					f.write('python scripts/fairseq_wu.py /blue/liu.ying/al_morphseg/al_trainselect/ ' + lg + ' ' + size + ' ' + select + ' ' + arch + ' ' + task + '\n')
					f.write('\n')

					f.write('module unload fairseq' + '\n')
					f.write('module load python3' + '\n')
					f.write('\n')
					f.write('python scripts/eval.py /blue/liu.ying/al_morphseg/al_trainselect/ ' + lg + ' ' + size + ' ' + select + ' ' + arch + ' ' + task + '\n')
					f.write('\n')
			
					f.write('date' + '\n')
					f.write('\n')

for task in ['surSeg', 'surSegGls', 'gls']:
	
	iterations = int(overall_max_size / 25)
	for i in range(iterations):
		select = str(i * 25)
		for lg in lgs:
			together_file = open('pbs/' + lg + '_' + task + '_select' + select + '.sh', 'w') # doing sbatch all together
			for size in sizes:
				for arch in ['transformer']:
					if lg + '_' + task + size + '_select' + select + '_' + arch +'.pbs' in os.listdir('pbs/'):
						together_file.write('sbatch pbs/' + lg + '_' + task + size + '_select' + select + '_' + arch +'.pbs' + '\n')
'''
for size in sizes:
	for lg in ['btz']:
		for task in ['surSeg']: #, 'surSegGls', 'gls']:
			select = 25
			while select < 200:
				try:
					os.system('bash pbs/' + lg + '_' + task + '_select' + str(select) + '.sh')
					print('pbs/' + lg + '_' + task + '_select' + str(select))
					print('pbs/' + lg + '_' + task + '_select' + str(select) + '.sh')
					select += 25
				except:
					pass
'''

'''
i=0
while i <= 500:
	os.system('bash pbs/bdg_surSeg_select' + str(i) + '.sh')
	i += 25
'''
