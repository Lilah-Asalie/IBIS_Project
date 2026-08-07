import pandas as pd
import numpy as np
import xarray as xr
import gsw
from xgcm import Grid
import numba
import scipy.special as sc
from scipy import integrate
from scipy.stats import linregress
from tqdm import tqdm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import warnings
import os
import glob
import imageio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mpl_dates
from scipy.stats import t as t_dist


#convert longitude to 0 - 360
def lon_convert(data):
    data.coords['lon'] = (((360 + (data.lon % 360)) % 360))
    data_new_lon = data.sortby(data.lon)
    return data_new_lon

### PLOTTING FUNCTIONS -----------------------------------


#create gif
def create_gif(filepath,savepath):

    image_dir = filepath

    # Get a list of all PNG files in the directory
    images = [img for img in os.listdir(image_dir) if img.endswith(".png")]
    #images.sort()  # Sort the images if needed

    def sort_files_by_date(directory):
        """Sorts files in a directory by their modification date.

        Args:
            directory: The path to the directory.

        Returns:
            A list of file paths sorted by modification date (oldest to newest).
        """
        files = glob.glob(os.path.join(image_dir, '*'))
        files = [f for f in files if os.path.isfile(f)]
        files.sort(key=os.path.getmtime)
        return files

    sorted_files = sort_files_by_date(image_dir)

    # for file_path in sorted_files:
        # print(file_path)
    # Create a figure and axis for the animation
    fig, ax = plt.subplots()

    # Function to update the figure for each frame
    def update(frame):
        img_path = os.path.join(image_dir, images[frame])
        img = plt.imread(img_path)
        ax.imshow(img)
        ax.axis('off')  # Hide axes
    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=len(images), repeat=True)

    # Save the animation as a GIF or display it
    ani.save(savepath, writer='imagemagick', fps=2,dpi = 400)  # Save as GIF