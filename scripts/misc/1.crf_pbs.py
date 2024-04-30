import io, os

second_string = '''#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=liu.ying@ufl.edu     # Where to send mail	
#SBATCH --ntasks=1                    # Run on a single CPU
#SBATCH --cpus-per-task=1                    
#SBATCH --mem=8gb                     # Job memory request
#SBATCH --time=48:00:00               # Time limit hrs:min:sec
#SBATCH --output=serial_test_%j.log   # Standard output and error log

pwd; hostname; date

module load conda
mamba activate data_partition
module load python

cd /blue/bonniejdorr/zoeyliu/morphseg_split

'''

if not os.path.exists('pbs/'):
	os.system('mkdir pbs/')

lgs = ['tepehua', 'seneca', 'english', 'finnish', 'german', 'indonesian', 'turkish', 'zulu'] #'mayo', 'mexicanero', 'nahuatl', 'wixarika', 'shp', 'tar', 'popoluca', 'tepehua', 'seneca', 'hupa', 'english', 'finnish', 'german', 'indonesian', 'turkish', 'zulu']

for method in ['random', 'adversarial']:
	for lg in lgs:
		for test_proportion in ['0.1', '0.2', '0.3', '0.4', '0.5']: #, '0.6', '0.7', '0.8']:
			with open('pbs/' + lg + '_' + method + '_crf_' + test_proportion + '.pbs', 'w') as f:
				first_string = '''#!/bin/bash\n#SBATCH --job-name=''' + lg + '_crf_' + test_proportion + '    # Job name'

				f.write(first_string + '\n')
				f.write(second_string + '\n')

#				f.write('python3 scripts/data_split.py --lg ' + lg + ' --test ' + test_proportion + ' --method ' + method + '\n')
				f.write('\n')
				f.write('python3 scripts/crf.py --lg ' + lg + ' --test ' +  test_proportion + '\n')
				f.write('\n')
#				f.write('python3 scripts/openNMT_cmds.py --lg ' + lg + ' --test ' +  test_proportion + '\n')
#				f.write('\n')
			
				f.write('date' + '\n')
				f.write('\n')


lg_maps = {'mayo': 'Yorem Nokki', 'mexicanero': 'Mexicanero', 'nahuatl': 'Nahuatl', 'wixarika': 'Wixarika', 'shp': 'Shipibo-Konibo', 'tar': 'Raramuri', 'hupa': 'Hupa'}
