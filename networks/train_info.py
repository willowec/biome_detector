# Module which handles logging training results and hyperparameters used
from datetime import datetime
import json
from pathlib import Path

def write_info(hyperparameters: dict, train_accs: dict, test_accs: dict) -> str:
	"""
	Takes a dictionary of hyperparameters, a dict of the training accuracies, and a dict of the
	testing accuracies, and writes them to a json file

	returns written path
	"""

	# format a filename for the data
	now = str(datetime.now()).replace(' ', 'T').replace(':', '-').replace('.', '-')
	fname = Path('trainlog_' + now + '.json')
	
	# ensure folder exists
	folder = Path('logs')
	folder.mkdir(exist_ok=True)
	
	data = [
		{"hyperparameters": hyperparameters}, 
		{"train_accuracies": train_accs}, 
		{"test_accuracies": test_accs}
	]	

	# write the json
	with open(folder.joinpath(fname), 'w') as f:
		json.dump(data, f, indent=4)
	
	return str(folder.joinpath(fname))


if __name__ == "__main__":
	# write example file
	write_info({'a': 0.1, 'b': 2}, {'c': 11, 'd':4}, {1:2, 4:5})
	

