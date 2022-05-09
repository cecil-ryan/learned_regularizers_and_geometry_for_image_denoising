import tensorflow as tf
from tensorflow.keras.constraints import Constraint
from typing import Dict
import numpy as np
from matplotlib import pyplot as plt
import os


def getGPU():
    """
    Grabs GPU. Sometimes Tensorflow attempts to use CPU when this is not called on my machine.
    From: https://www.tensorflow.org/guide/gpu
    """

    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)


def save_image(img: np.ndarray,
               name: str,
               save_dir: str,
               absolute=False,
               colorbar=False):
    """

    Parameters
    ----------
    img : np image array
    name : name of image for saving
    save_dir : Dir to save image to
    change : Method of scaling image for saving
    """
    plt.clf()
    if absolute:
        img = np.abs(img)
    plt.imshow(img, cmap='gray')
    #plt.colorbar()
    plt.axis('off')
    if colorbar:
        plt.colorbar()
    plt.savefig(os.path.join(save_dir, name + '.png'),bbox_inches='tight')


def get_num_channels(config: Dict):
    """Get number of channels depending on configuration

    Parameters
    ----------
    config : (Dict) - Dictionary of model configuration
    """
    if config['grayscale']:
        num_channels = 1
    else:
        num_channels = 3
    return num_channels


class MinMax(Constraint):
    """Implements Keras constraint to enforce variable values to be in between (min, max)"""

    def __init__(self, min_value: float, max_value: float):
        """Initialize the constraint with min and max values

        Parameters
        ----------
        min_value: (float) - Minimum value of weights
        max_value: (float) - Maximum value of weights
        """
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, w):
        """Calls the constraint"""
        return tf.clip_by_value(w, self.min_value, self.max_value)

    def get_config(self):
        return {'min_value': self.min_value,
                'max_value': self.max_value}


def rmse(x, y):
    """Computes PSNR of x and y using numpy operations"""
    return np.sqrt(np.mean((x-y) ** 2))


def psnr(x, y, data_range=1.0):
    """Computes PSNR of x and y using numpy operations"""
    return 20*np.log10(range/np.sqrt(np.mean((x-y) ** 2)))


class L2DenoiseDataterm:
    """Implements L2DenoiseDataTerm for Variational Network.
    Code based on https://github.com/VLOGroup/tdv/blob/master/model.py"""

    @staticmethod
    def energy(x, z):
        """Compute the energy"""
        return 0.5 * (x - z) ** 2

    @staticmethod
    def prox(x, z, tau):
        """Compute proximal dataterm"""
        return (x + tau * z) / (1 + tau)

    @staticmethod
    def grad(x, z):
        """Compute grad of energy"""
        return x - z
