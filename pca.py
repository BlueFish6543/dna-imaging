import numpy as np
import cv2
import argparse
import sys
import copy


def draw_axis(img, p, q, colour, scale=0.2):
    angle = np.arctan2(p[1] - q[1], p[0] - q[0])
    hypotenuse = np.sqrt((p[1] - q[1]) ** 2 + (p[0] - q[0]) ** 2)
    q = np.zeros_like(q, dtype=np.int64)

    # Lengthen the arrow by a factor of scale
    q[0] = int(p[0] - scale * hypotenuse * np.cos(angle))
    q[1] = int(p[1] - scale * hypotenuse * np.sin(angle))
    cv2.line(img, (p[0], p[1]), (q[0], q[1]), colour, 1, cv2.LINE_AA)

    # Create the arrow hooks
    p[0] = int(q[0] + 9 * np.cos(angle + np.pi / 4))
    p[1] = int(q[1] + 9 * np.sin(angle + np.pi / 4))
    cv2.line(img, (p[0], p[1]), (q[0], q[1]), colour, 1, cv2.LINE_AA)

    p[0] = int(q[0] + 9 * np.cos(angle - np.pi / 4))
    p[1] = int(q[1] + 9 * np.sin(angle - np.pi / 4))
    cv2.line(img, (p[0], p[1]), (q[0], q[1]), colour, 1, cv2.LINE_AA)


def get_orientation(pts, img):
    # Construct a buffer used by the PCA analysis
    data_pts = np.squeeze(np.array(pts, dtype=np.float64))

    # Perform PCA analysis
    # https://stackoverflow.com/questions/22612828/python-opencv-pcacompute-eigenvalue
    covar, mean = cv2.calcCovarMatrix(data_pts, np.mean(data_pts, axis=0),
                                      cv2.COVAR_SCALE | cv2.COVAR_ROWS | cv2.COVAR_SCRAMBLED)
    eigenvalues, eigenvectors = cv2.eigen(covar)[1:]
    eigenvectors = cv2.gemm(eigenvectors, data_pts - mean, 1, None, 0)
    eigenvectors = np.apply_along_axis(lambda n: cv2.normalize(n, dst=None).flat, 1, eigenvectors)

    # Store the centre of the object
    cntr = np.array([int(mean[0, 0]), int(mean[0, 1])])

    # Draw the principal components
    cv2.circle(img, (cntr[0], cntr[1]), 3, (255, 0, 255), 2)
    p1 = cntr + 0.02 * eigenvectors[0] * eigenvalues[0]
    p2 = cntr - 0.02 * eigenvectors[1] * eigenvalues[1]
    draw_axis(img, copy.copy(cntr), p1, (0, 255, 0), 2)
    draw_axis(img, copy.copy(cntr), p2, (255, 255, 0), 10)

    return np.arctan2(eigenvectors[0, 1], eigenvectors[0, 0])  # orientation in radians


def main():
    # Load image
    parser = argparse.ArgumentParser(description=
                                     "This program demonstrates how to use OpenCV PCA to extract "
                                     "the orientation of an object.\n")
    parser.add_argument('src')
    args = parser.parse_args()
    src = cv2.imread(args.src)

    # Check if image is loaded succesfully
    if src is None:
        print("Problem loading image!")
        sys.exit(1)

    cv2.imshow("src", src)

    # Convert image to grayscale
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # Convert image to binary
    retval, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Find all the contours in the threshold range
    contours, hierarchy = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for i in range(len(contours)):
        # Calculate the area in each contour
        area = cv2.contourArea(contours[i])
        # Ignore contours that are too small or too large
        if (area < 1e2) or (area > 1e5):
            continue

        # Draw each contour only for visualisation purposes
        cv2.drawContours(src, contours, i, (0, 0, 255), 2)
        # Find the orientation of each shape
        get_orientation(contours[i], src)

    cv2.imshow("output", src)

    cv2.waitKey()
    sys.exit(0)


if __name__ == "__main__":
    main()
