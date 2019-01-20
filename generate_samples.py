import os
import pdb
import pickle
import argparse

import warnings

warnings.filterwarnings("ignore")

# Numpy & Scipy imports
import numpy as np
import scipy
import scipy.misc

# Torch imports
import torch
import torch.nn as nn
import torch.optim as optim

# Local imports
import utils
from data_loader import get_emoji_loader
from models import DCGenerator, DCDiscriminator


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def sample_noise(dim):
    """
    Generate a PyTorch Variable of uniform random noise.
    Input:
    - batch_size: Integer giving the batch size of noise to generate.
    - dim: Integer giving the dimension of noise to generate.
    Output:
    - A PyTorch Variable of shape (batch_size, dim, 1, 1) containing uniform
      random noise in the range (-1, 1).
    """
    return utils.to_var(torch.rand(16, dim) * 2 - 1).unsqueeze(2).unsqueeze(3)

def create_image_grid(array, ncols=None):
    """
        Makes 4x4 grid of sample images for testing during training
    """
    print(array.dtype)
    num_images, channels, cell_h, cell_w = array.shape

    if not ncols:
        ncols = int(np.sqrt(num_images))
    nrows = int(np.math.floor(num_images / float(ncols)))
    result = np.zeros((cell_h * nrows, cell_w * ncols, channels), dtype=np.float32)
    for i in range(0, nrows):
        for j in range(0, ncols):
            result[i * cell_h:(i + 1) * cell_h, j * cell_w:(j + 1) * cell_w, :] = array[i * ncols + j].transpose(1, 2,
                                                                                                                 0)

    if channels == 1:
        result = result.squeeze()
    return result

def generate():
	"""
		Generates 50 images and saves to samples file
	"""
	G = load_obj('Trained Model_2000')
	opts = load_obj('Model Opts_2000')

	# Generate noise
	sample_noisee = sample_noise(opts.noise_size)
	sample_images = G(sample_noisee)

	generated_images = utils.to_data(sample_images)

	grid = create_image_grid(generated_images)

	print(np.shape(grid))
	#for i, ggr in enumerate(generated_images):
	path = os.path.join("./samples_generated", 'sample-{:06d}.png'.format(i))

	scipy.misc.imsave(path, ggr)

if __name__ == '__main__':
	generate()