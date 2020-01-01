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


def calibrate(coords):
    calibration_data = []
    for coord in np.sort(coords[0]):
        while True:
            val = input("Enter value for reference point at y coordinate {}:\n".format(coord))
            try:
                val = int(val)
                break
            except ValueError:
                print("Invalid input. Try again.")
        calibration_data.append([coord, val])
    calibration_data = np.array(calibration_data)
    return calibration_data


def sort_into_bins(centres):
    centres = centres[np.argsort(centres[:, 0])]  # sort in ascending x coordinates
    hist, bins, patches = plt.hist(centres[:, 0], bins=NUM_COLUMNS)
    coords = []
    idx = 0
    for i in range(len(hist)):
        coords.append(centres[idx:idx + int(hist[i]), 1])
        idx += int(hist[i])
    # print(coords)
    return coords, bins


def main():
    # Load image
    parser = argparse.ArgumentParser(description=
                                     "This program uses OpenCV to extract the coordinates of DNA bands.\n")
    parser.add_argument('src')
    args = parser.parse_args()
    src = cv2.imread(args.src)

    # Check if image is loaded successfully
    if src is None:
        print("Problem loading image!")
        sys.exit(1)

    image1 = Image(copy.copy(src), SAMPLE_THRESHOLD)
    image1.draw_contours()

    centres = image1.get_centres()
    coords, bins = sort_into_bins(centres)
    part1 = np.asarray(image1.img, dtype=np.int64)
    part1[:, :int(bins[1]), :] = 0
    
    image2 = Image(copy.copy(src), LADDER_THRESHOLD)
    image2.draw_contours()
    part2 = np.asarray(image2.img, dtype=np.int64)
    part2[:, int(bins[1]):, :] = 0
    
    image = np.asarray(part1 + part2, dtype=np.uint8)
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.imshow("output", image)
    cv2.waitKey()
    
    return

    if len(coords[0]) < 4:
        print("Insufficient data points to generate calibration line.")

    else:
        calibration_data = calibrate(coords)
        p = plot_calibration_data(calibration_data)
        for i in range(1, len(coords)):
            values = np.exp(p(coords[i]))
            plt.scatter(coords[i], values, label="Column {}".format(i))
        plt.legend()
        plt.show()

    cv2.waitKey()
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
