import cv2
import argparse
import sys
import copy
from processing import Image
import numpy as np
import matplotlib.pyplot as plt

NUM_COLUMNS = 5
LADDER_THRESHOLD = 5
SAMPLE_THRESHOLD = 3


def plot_calibration_data(calibration_data):
    # Fit to log(y) = a + b x
    p = np.poly1d(np.polyfit(calibration_data[:, 0], np.log(calibration_data[:, 1]), 1))
    fitted = np.exp(p(calibration_data[:, 0]))
    plt.clf()
    plt.scatter(calibration_data[:, 0], calibration_data[:, 1])
    plt.semilogy(calibration_data[:, 0], fitted)
    plt.xlabel("$y$ coordinate")
    plt.ylabel("Value")
    plt.grid()
    return p


def sort_into_bins(centres, num_columns):
    centres = centres[np.argsort(centres[:, 0])]  # sort in ascending x coordinates
    hist, bins, patches = plt.hist(centres[:, 0], bins=num_columns)
    coords = []
    idx = 0
    for i in range(len(hist)):
        coords.append(centres[idx:idx + int(hist[i]), 1])
        idx += int(hist[i])
    return coords, bins
    

def process_image(src, threshold, num_columns):
    image = Image(src, threshold)
    image.draw_contours()
    
    centres = image.get_centres()
    coords, bins = sort_into_bins(centres, num_columns)
    arr = np.asarray(image.img, dtype=np.int64)
    
    return arr, coords, bins


def find_contours(src, sample_threshold, ladder_threshold, num_columns):
    src = cv2.imread(src)
    assert src is not None

    arr1, coords1, bins = process_image(copy.copy(src), SAMPLE_THRESHOLD, num_columns)
    arr1[:, :int(bins[1]), :] = 0
    arr2, coords2, _ = process_image(copy.copy(src), LADDER_THRESHOLD, num_columns)
    arr2[:, int(bins[1]):, :] = 0
    image = np.asarray(arr1 + arr2, dtype=np.uint8)

    coords = coords1
    coords[0] = coords2[0]

    return image, coords


def calibrate_data(coords, calibration_vals, show_plot=False):
    if len(calibration_vals) < 4:
        # Too little data points
        return

    calibration_vals = np.asarray(calibration_vals)
    calibration_data = np.column_stack((np.sort(coords[0]), calibration_vals))
    p = plot_calibration_data(calibration_data)
    results = []

    for i in range(1, len(coords)):
        values = np.exp(p(coords[i]))
        for val in values:
            results.append([i, int(round(val))])
        plt.scatter(coords[i], values, label="Column {}".format(i))

    if show_plot:
        plt.legend()
        plt.show()

    return results
