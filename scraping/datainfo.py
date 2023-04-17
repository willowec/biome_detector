import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path        
import glob, re
import argparse
from biomemap import names_from_ids


def get_biome_count(data_dir: Path):
    """
    For each biome directory in data_dir, counts the number of images.

    Returns:
    biomes - nx2 np array where the first column is biome id and the 
        second is the number of images for that biome
    """
    # get each of the biome folders
    biome_folders = np.asarray(glob.glob(str(data_dir.joinpath('*'))))
    
    # create an np array from biome_folders containing 
    #   the id's and their corresponding counts
    biomes = np.empty((len(biome_folders), 2), int)
    for i, p in enumerate(biome_folders):
        # match last set of ints in folder path to get biome id
        biomes[i, 0] = re.search(r'[0-9]+', p)[0] 
        # count n files in folder to get number of images for the biome id
        biomes[i, 1] = len(glob.glob(
            str(Path(biome_folders[i]).joinpath('*'))
            ))
    
    # sort by the second column so largest n images is first
    biomes = biomes[biomes[:, -1].argsort()]
    
    return biomes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data_directory', type=Path, 
        help="The root directory containing biome data folders")

    args = parser.parse_args()

    # get the data
    biomes = get_biome_count(args.data_directory)
    names = np.asarray(names_from_ids(biomes[:, 0]), str)

    # plot data
    plt.rc('font', size=8)
    fig, ax = plt.subplots()
    ax.barh(names, biomes[:, 1])
    plt.title("Number of images per biome in the dataset")
    plt.xlabel("Number of images")

    plt.show()