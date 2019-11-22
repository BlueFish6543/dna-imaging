import cv2
import argparse
import sys
from processing.pca import Image


def main():
    # Load image
    parser = argparse.ArgumentParser(description=
                                     "This program uses OpenCV PCA to extract the coordinates of DNA bands.\n")
    parser.add_argument('src')
    args = parser.parse_args()
    src = cv2.imread(args.src)

    # Check if image is loaded succesfully
    if src is None:
        print("Problem loading image!")
        sys.exit(1)

    image = Image(src)
    image.draw_contours()
    image.show()
    centres = image.get_centres()

    cv2.waitKey()
    sys.exit(0)


if __name__ == "__main__":
    main()
