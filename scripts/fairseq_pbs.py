# e.g., python3 scripts/fairseq_pbs.py surSeg 25

import io, os, sys

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

task = sys.argv[1]
select_interval = sys.argv[2]

if not os.path.exists('pbs_new/'):
	os.system('mkdir pbs_new/')

lgs = ['btz', 'cho', 'lez', 'ntu', 'tau', 'bdg']
#sizes = ['50', '100', '500', '1000', '1500', '2000']
sizes = ['500', '1000', '1500', '2000']

overall_max_size = 2500 # Assuming a fixed bugget for doing mannual annotations for 2500 words in total

for lg in lgs:
	for size in sizes:
		select_file = '/blue/liu.ying/al_morphseg/al_trainselect/select.' + lg + '_' + task + size + '.input'

		iterations = int(overall_max_size / int(select_interval))
		for i in range(iterations):
			select = str(i * int(select_interval))
			if int(size) + int(select) <= overall_max_size: ## assuming a fixed budge for mannual annotations of 2500 words
				for arch in ['transformer']: #, 'transformer_tiny', 'lstm']:

					with open('pbs_new/' + lg + '_' + task + size + '_' + select_interval + '_select' + select + '_' + arch +'.pbs', 'w') as f:
						first_string = '''#!/bin/bash\n#SBATCH --job-name=''' + lg + '_' + task + size + '_' + select_interval + '_select' + select + '_' + arch + '    # Job name'

						f.write(first_string + '\n')
						f.write(second_string + '\n')

						f.write('python scripts/fairseq_wu.py /blue/liu.ying/al_morphseg/al_trainselect/ ' + lg + ' ' + size + ' ' + select_interval + ' ' + select + ' ' + arch + ' ' + task + '\n')
						f.write('\n')

						f.write('module unload fairseq' + '\n')
						f.write('module load python3' + '\n')
						f.write('\n')
						f.write('python scripts/eval.py /blue/liu.ying/al_morphseg/al_trainselect/ ' + lg + ' ' + size + ' ' + select_interval + ' ' + select + ' ' + arch + ' ' + task + '\n')
						f.write('\n')
			
						f.write('date' + '\n')
						f.write('\n')

		# Only need to run one of these pbs files since the total amount of data available is the same
		select = 'all'
		for arch in ['transformer']: #, 'transformer_tiny', 'lstm']:

			with open('pbs_new/' + lg + '_' + task + size + '_' + select_interval + '_select' + select + '_' + arch +'.pbs', 'w') as f:
				first_string = '''#!/bin/bash\n#SBATCH --job-name=''' + lg + '_' + task + size + '_' + select_interval + '_select' + select + '_' + arch + '    # Job name'

				f.write(first_string + '\n')
				f.write(second_string + '\n')

				f.write('python scripts/fairseq_wu.py /blue/liu.ying/al_morphseg/al_trainselect/ ' + lg + ' ' + size + ' ' + select_interval + ' ' + select + ' ' + arch + ' ' + task + '\n')
				f.write('\n')

				f.write('module unload fairseq' + '\n')
				f.write('module load python3' + '\n')
				f.write('\n')
				f.write('python scripts/eval.py /blue/liu.ying/al_morphseg/al_trainselect/ ' + lg + ' ' + size + ' ' + select_interval + ' ' + select + ' ' + arch + ' ' + task + '\n')
				f.write('\n')
			
				f.write('date' + '\n')
				f.write('\n')

#for task in ['surSeg', 'surSegGls', 'gls']:
	
#	iterations = int(overall_max_size / 25)
#	for i in range(iterations):
#		select = str(i * 25)
#		for lg in lgs:
#			together_file = open('pbs_new/' + lg + '_' + task + '_select' + select + '.sh', 'w') # doing sbatch all together
#			c = 0
#			for size in sizes:
#				for arch in ['transformer']:
#					if lg + '_' + task + size + '_select' + select + '_' + arch +'.pbs' in os.listdir('pbs_new/'):
#						together_file.write('sbatch pbs_new/' + lg + '_' + task + size + '_select' + select + '_' + arch +'.pbs' + '\n')
#						c += 1
#			if c == 0:
#				os.system('rm ' + 'pbs_new/' + lg + '_' + task + '_select' + select + '.sh')


## For each start size, combine pbs files for all languages for a given select interval and select size
iterations = int(overall_max_size / int(select_interval))
for i in range(iterations):
	select = str(i * int(select_interval))
	for size in sizes:
		together_file = open('pbs_new/' + task + size + '_' + select_interval + '_select' + select + '.sh', 'w') # doing sbatch all together
		c = 0
		for lg in lgs:			
			for arch in ['transformer']:
				if lg + '_' + task + size + '_' + select_interval + '_select' + select + '_' + arch +'.pbs' in os.listdir('pbs_new/'):
					evaluation_file = '/blue/liu.ying/al_morphseg/al_trainselect/' + lg + '_' + task + size + '/' + select_interval + '/select' + str(select) + '/' + arch + '/eval.txt'
					if os.path.exists(evaluation_file) and os.stat(evaluation_file).st_size != 0:
						pass
					else:
						together_file.write('sbatch pbs_new/' + lg + '_' + task + size + '_' + select_interval + '_select' + select + '_' + arch +'.pbs' + '\n')
						c += 1
		if c == 0:
			os.system('rm ' + 'pbs_new/' + task + size + '_' + select_interval + '_select' + select + '.sh')

'''
#SBATCH --account=smoeller
#SBATCH --qos=smoeller

sbatch job --account=smoeller --qos smoeller
'''

'''					
for size in sizes:
	for lg in ['btz']:
		for task in ['surSeg']: #, 'surSegGls', 'gls']:
			select = 25
			while select < 200:
				try:
					os.system('bash pbs_new/' + lg + '_' + task + '_select' + str(select) + '.sh')
					print('pbs_new/' + lg + '_' + task + '_select' + str(select))
					print('pbs_new/' + lg + '_' + task + '_select' + str(select) + '.sh')
					select += 25
				except:
					pass
'''

'''
i=925
while i <= 1500:
	os.system('bash pbs_new/btz_surSeg_select' + str(i) + '.sh')
	i += 25
'''

'''
import io, os
size = '1500'#, '100', '500', '1500']
max_select_size = 1000
i=525
while i <= max_select_size:
	os.system('sbatch pbs_new/btz_surSeg' + size + '_select' + str(i) + '_transformer.pbs')
	print('pbs_new/btz_surSeg' + size + '_select' + str(i) + '_transformer.pbs')
	i += 25
'''