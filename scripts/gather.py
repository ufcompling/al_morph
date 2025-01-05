# e.g., python3 scripts/gather.py al_trainselect/ surSeg

import io, os, sys

datadir = sys.argv[1]

arch = 'transformer_tiny'

lgs = ['bdg'] #['btz', 'cho', 'lez', 'ntu', 'tau', 'bdg']
sizes = ['500'] #, '1000', '1500', '2000', '2500', '3000']

iteration_size = [25]#, 50, 100, 200]

header = ['Language', 'Task', 'Size', 'Select_interval', 'Select_size', 'Model', 'Metric', 'Value']

task = sys.argv[2]

outfile = open(task + '_results.txt', 'w')
outfile.write(' '.join(tok for tok in header) + '\n')

for size in sizes:
	for select_interval in iteration_size:
		select_interval = str(select_interval)
		for lg in lgs:

			## Get all selection sizes
			select_sizes = []
			for select_dir in os.listdir(datadir + lg + '_' + task + size + '/' + select_interval + '/'):
				select_size = select_dir[6 : ]
				select_sizes.append(int(select_size))
			select_sizes.sort()

			## Getting evaluation results
			for i in range(len(select_sizes)):
				select = str(select_sizes[i])
				print(select)
				evaluation_file = datadir + lg + '_' + task + size + '/' + select_interval + '/select' + str(select) + '/' + arch + '/eval.txt'
				print(evaluation_file)
				if os.path.exists(evaluation_file):
					print(evaluation_file)
					precision = ''
					recall = ''
					f1 = ''
					with open(evaluation_file) as f:
						for line in f:
							toks = line.strip().split()
							if line.startswith('Precision'):
								precision = toks[1]
							if line.startswith('Recall'):
								recall = toks[1]
							if line.startswith('F1'):
								f1 = toks[1]
					info = [lg, task, size, select_interval, select, arch, 'precision', precision]
					outfile.write(' '.join(str(tok) for tok in info) + '\n')
					info = [lg, task, size, select_interval, select, arch, 'recall', recall]
					outfile.write(' '.join(str(tok) for tok in info) + '\n')
					info = [lg, task, size, select_interval, select, arch, 'f1', f1]
					outfile.write(' '.join(str(tok) for tok in info) + '\n')

				else:
					print(lg, task, select_interval, select)

