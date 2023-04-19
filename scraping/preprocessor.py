# Script which preprocesses the imagery data to 
# reduce workload for the neural network during training
# if run on ACG, need to load conda first

from PIL import Image
from pathlib import Path
from glob import glob
import argparse
import shutil, os

def get_class_dirs(data_dir: Path, min_len: int):
	"""
	Returns list of class directories to operate on
	"""
	dirs = glob(f"{data_dir}/*")
	for d in dirs:
		n = len(glob(f"{d}/*"))
		if n < min_len:
			dirs.remove(d)
	return dirs


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('data_dir', type=Path,
		help="The root directory containing the unprocessed biome data folders")
	parser.add_argument('output_dir', type=Path,
		help="The root directory for the processed images to be stored in. If it already exists, the directory will be overwritten.")
	parser.add_argument('min_class_len', type=int,
		help="The minimum number of images a class must have to be processed")
	parser.add_argument('im_w', type=int,
		help="Width to resize images to")
	parser.add_argument('im_h', type=int,
		help="Height to resize images to")

	args = parser.parse_args()
	assert args.data_dir.exists()

	# overwrite old output
	if args.output_dir.exists():
		if str((input(f"Are you sure you want to overwrite {args.output_dir}? y/n"))) == 'y':
			print('Overwriting preprocessed data')
			for d in glob(f"{args.output_dir}/*"):
				shutil.rmtree(d)
		else:
			quit() # cancel operation (do not overwrite old preprocessed_data)
	else:
		os.mkdir(args.output_dir)

	# gather all valid classes 
	dirs = get_class_dirs(args.data_dir, args.min_class_len)

	# resize the images	
	for d in dirs:
		# make the new directory
		new_dir = args.output_dir.joinpath(Path(d).parts[-1])
		if not new_dir.exists():
			os.mkdir(str(new_dir))

		print("Populating", str(new_dir))
		# resize and write all images into the new directory
		for imname in glob(f"{d}/*"):
			im = Image.open(imname)
			im = im.resize((args.im_w, args.im_h))
			im.save(new_dir.joinpath(Path(imname).name))

	print("Resizing complete")
		
