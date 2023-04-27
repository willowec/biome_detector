# Module which handles logging training results and hyperparameters used
from datetime import datetime
import json
from pathlib import Path
import torch
import matplotlib.pylab as plt
import numpy as np


def write_info(hyperparameters: dict, train_accs: dict, test_accs: dict, class_sizes: dict) -> str:
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
		{"test_accuracies": test_accs},
		{"imgs_per_class": class_sizes}
	]	

	# write the json
	with open(folder.joinpath(fname), 'w') as f:
		json.dump(data, f, indent=4)
	
	return str(folder.joinpath(fname))


def get_class_sizes(all_data) -> dict:
	"""
	Returns a dictionary containing the number of images per class in all_data
	where all_data is a 2d list of class images
	"""
	sizes_d = {}
	
	sizes = [len(all_data[i]) for i in range(len(all_data))] #data sizes
	for i in range(len(sizes)):
		sizes_d[i] = sizes[i]
	
	return sizes_d


def plot_accuracies(acc_dict: dict, sizes_dict: dict, title: str, save_path=None):
	"""
	Plots a dictionary of accuracies by class and fits a line to them
	
	if save_path is specified, saves the figure to that path. Otherwise, displays the plot
	"""
	fit_order = 2

	d = sorted(acc_dict.items(), key=lambda x: x[1]) # sort the accuracies by accuracy
	x, y = zip(*d)

	datalen = len(acc_dict.values())
	sizes = list(sizes_dict.values())
	#sizes = [len(all_data.data[i]) for i in range(datalen)] #data sizes
	accs = list(acc_dict.values()) #accuracies
	d = list(zip(sizes, accs))

	sorted_acc_by_size = [sorted(d)[i][1] for i in range(datalen)]

	fig, ax = plt.subplots()
	ax.scatter(sorted(sizes), sorted_acc_by_size)
	plt.title(title + " fit order = {}".format(fit_order))
	plt.ylabel("Accuracy")
	plt.xlabel("Class Size")

	# fitline
	poly = np.polyfit(sorted(sizes), sorted_acc_by_size, fit_order)
	f = np.poly1d(poly)
	fit_x = np.linspace(-10, sorted(sizes)[-1])

	plt.plot(fit_x, f(fit_x) ,"r--")

	if not save_path:
		plt.show()
	else:
		plt.savefig(save_path)	

	
def per_class_accuracies(predictions, labels):
	"""
	Calculates the accuracy for each class
	""" 
	# sort both arrays by the true labels
	labels, inds = torch.sort(labels)
	predictions = predictions[inds]
    
	# populate "accuracies" dict with true predictions, n predictions
	accuracies = {}
	accuracy = 0 # also calculate total accuracy
	for i, l in enumerate(labels):
		l = int(l)
		if not l in accuracies.keys():
			accuracies[l] = [0, 0]
		grade = int(l == int(predictions[i])) # 1 if correct, 0 if incorrect
		accuracy += grade
		accuracies[l] = [accuracies[l][0] + grade, accuracies[l][1] + 1]
        
	# calculate accuracies for each class
	for l, vals in accuracies.items():
		accuracies[l] = vals[0] / vals[1]
	accuracy /= len(labels)
        
	return accuracies, accuracy


def load_info(logfile):
	"""
	Loads a training log json file and renders information from it
	"""
	with open(logfile, 'r') as f:
		data = json.load(f)
		hyper = data[0]['hyperparameters']
		train_accs = data[1]['train_accuracies']
		test_accs = data[2]['test_accuracies']
		img_per_cls = data[3]['imgs_per_class']

		# calculate average accuracies
		avg_acc_train =0
		avg_acc_test = 0
		for key in train_accs.keys():
			avg_acc_train += train_accs[key]
			avg_acc_test += test_accs[key]

		avg_acc_train /= len(list(train_accs.keys()))
		avg_acc_test  /= len(list(train_accs.keys()))

		print(f"Average class training accuracy: {avg_acc_train:>3f}\nAverage class testing accuracy: {avg_acc_test:>3f}")

		# plot the per class accuracies
		plot_accuracies(train_accs, img_per_cls, "Per class training accuracies")
		plot_accuracies(test_accs, img_per_cls, "Per class testing accuracies")

	
if __name__ == "__main__":
	# write example file
	write_info({'a': 0.1, 'b': 2}, {'c': 11, 'd':4}, {1:2, 4:5})
		

