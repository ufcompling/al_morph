import io, os, sys

datadir = sys.argv[1]

arch = 'transformer'

lgs = ['btz', 'cho', 'lez', 'ntu', 'tau']
sizes = ['50', '100', '500', '1000', '1500', '2000']

header = ['Language', 'Task', 'Size', 'Select_size', 'Model', 'Metric', 'Value']

for task in ['surSeg']:#, 'surSegGls', 'gls']:
	outfile = open(task + '_results.txt', 'w')
	outfile.write(' '.join(tok for tok in header) + '\n')
	for lg in lgs:
		for size in sizes:
			select = 0
			while select < 1000:
				evaluation_file = datadir + lg + '_' + task + size + '/select' + str(select) + '/' + arch + '/eval.txt'
				if os.path.exists(evaluation_file):
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

					info = [lg, task, size, select, arch, 'precision', precision]
					outfile.write(' '.join(str(tok) for tok in info) + '\n')
					info = [lg, task, size, select, arch, 'recall', recall]
					outfile.write(' '.join(str(tok) for tok in info) + '\n')
					info = [lg, task, size, select, arch, 'f1', f1]
					outfile.write(' '.join(str(tok) for tok in info) + '\n')

				else:
					print(lg, task, size, select)

				select += 25

			select = 'all'
			evaluation_file = datadir + lg + '_' + task + size + '/select' + str(select) + '/' + arch + '/eval.txt'
			if os.path.exists(evaluation_file):
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

				info = [lg, task, size, select, arch, 'precision', precision]
				outfile.write(' '.join(str(tok) for tok in info) + '\n')
				info = [lg, task, size, select, arch, 'recall', recall]
				outfile.write(' '.join(str(tok) for tok in info) + '\n')
				info = [lg, task, size, select, arch, 'f1', f1]
				outfile.write(' '.join(str(tok) for tok in info) + '\n')

			else:
				print(lg, task, size, select)
				