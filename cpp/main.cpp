#include "opencv2/core.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgcodecs.hpp"
#include <iostream>

static const int NUM_COLOURS = 8;
static const int THRESHOLD = 3; // between 1 and NUM_COLOURS inclusive, lower is more selective

// Function declarations
void drawAxis(cv::Mat&, cv::Point, cv::Point, const cv::Scalar &, float);
double getOrientation(const std::vector<cv::Point> &, cv::Mat &);
cv::Mat colorQuantize(const cv::Mat &src, cv::Mat &dst);
void showContours(cv::Mat &src);

void drawAxis(cv::Mat &img, cv::Point p, cv::Point q, const cv::Scalar &colour, const float scale = 0.2) {
    double angle = atan2((double) p.y - q.y, (double) p.x - q.x); // angle in radians
    double hypotenuse = sqrt((double) (p.y - q.y) * (p.y - q.y) + (p.x - q.x) * (p.x - q.x));

    // Lengthen the arrow by a factor of scale
    q.x = (int) (p.x - scale * hypotenuse * cos(angle));
    q.y = (int) (p.y - scale * hypotenuse * sin(angle));
    cv::line(img, p, q, colour, 1, cv::LINE_AA);

    // Create the arrow hooks
    p.x = (int) (q.x + 9 * cos(angle + CV_PI / 4));
    p.y = (int) (q.y + 9 * sin(angle + CV_PI / 4));
    cv::line(img, p, q, colour, 1, cv::LINE_AA);

    p.x = (int) (q.x + 9 * cos(angle - CV_PI / 4));
    p.y = (int) (q.y + 9 * sin(angle - CV_PI / 4));
    cv::line(img, p, q, colour, 1, cv::LINE_AA);
}

double getOrientation(const std::vector<cv::Point> &pts, cv::Mat &img) {
    // Construct a buffer used by the PCA analysis
    int sz = static_cast<int>(pts.size());
    cv::Mat data_pts = cv::Mat(sz, 2, CV_64F);
    for (int i = 0; i < data_pts.rows; i++) {
        data_pts.at<double>(i, 0) = pts[i].x;
        data_pts.at<double>(i, 1) = pts[i].y;
    }

    // Perform PCA analysis
    cv::PCA pca_analysis(data_pts, cv::Mat(), cv::PCA::DATA_AS_ROW);

    // Store the centre of the object
    cv::Point cntr = cv::Point(static_cast<int>(pca_analysis.mean.at<double>(0, 0)),
                               static_cast<int>(pca_analysis.mean.at<double>(0, 1)));

    // Store the eigenvalues and eigenvectors
    std::vector<cv::Point2d> eigen_vecs(2);
    std::vector<double> eigen_vals(2);
    for (int i = 0; i < 2; i++) {
        eigen_vecs[i] = cv::Point2d(pca_analysis.eigenvectors.at<double>(i, 0),
                                    pca_analysis.eigenvectors.at<double>(i, 1));
        eigen_vals[i] = pca_analysis.eigenvalues.at<double>(i);
    }

    // Draw the principal components
    cv::circle(img, cntr, 3, cv::Scalar(255, 0, 255), 2);
    cv::Point p1 = cntr + 0.02 * cv::Point(static_cast<int>(eigen_vecs[0].x * eigen_vals[0]),
                                           static_cast<int>(eigen_vecs[0].y * eigen_vals[0]));
    cv::Point p2 = cntr - 0.02 * cv::Point(static_cast<int>(eigen_vecs[1].x * eigen_vals[1]),
                                           static_cast<int>(eigen_vecs[1].y * eigen_vals[1]));
    drawAxis(img, cntr, p1, cv::Scalar(0, 255, 0), 2);
    drawAxis(img, cntr, p2, cv::Scalar(255, 255, 0), 10);

    double angle = atan2(eigen_vecs[0].y, eigen_vecs[0].x); // orientation in radians
    return angle;
}

// https://answers.opencv.org/question/182006/opencv-c-k-means-color-clustering/
cv::Mat colorQuantize(const cv::Mat &src, cv::Mat &dst) {
    cv::Mat data;
    src.convertTo(data, CV_32F);
    data = data.reshape(1, static_cast<int>(data.total()));

    cv::TermCriteria criteria(cv::TermCriteria::EPS + cv::TermCriteria::MAX_ITER, 10, 1.0);
    cv::Mat labels, centres;
    cv::kmeans(data, NUM_COLOURS, labels, criteria, 10, cv::KMEANS_RANDOM_CENTERS, centres);

    centres = centres.reshape(3, centres.rows);
    data = data.reshape(3, data.rows);
    cv::Mat intensities;
    cv::cvtColor(centres, intensities, cv::COLOR_BGR2GRAY);
    cv::sort(intensities, intensities, cv::SORT_EVERY_COLUMN + cv::SORT_ASCENDING);

    auto *p = data.ptr<cv::Vec3f>();
    for (size_t i = 0; i < data.rows; i++) {
        int centreId = labels.at<int>(static_cast<int>(i));
        p[i] = centres.at<cv::Vec3f>(centreId);
    }

    dst = data.reshape(3, src.rows);
    dst.convertTo(dst, CV_8U);

    return intensities;
}

void showContours(cv::Mat &src) {
    cv::Mat quantized, intensities;
    intensities = colorQuantize(src, quantized);
    int thresh = static_cast<int>(intensities.at<float>(NUM_COLOURS - THRESHOLD)) - 2;

    // Convert image to grayscale
    cv::Mat gray;
    cv::cvtColor(quantized, gray, cv::COLOR_BGR2GRAY);

    // Convert image to binary
    cv::Mat bw;
    threshold(gray, bw, thresh, 255, cv::THRESH_BINARY);

    // Find all the contours in the threshold range
    std::__1::vector<std::__1::vector<cv::Point>> contours;
    findContours(bw, contours, cv::RETR_LIST, cv::CHAIN_APPROX_NONE);

    for (size_t i = 0; i < contours.size(); i++) {
        // Calculate the area of each contour
        double area = contourArea(contours[i]);
        // Ignore contours that are too small or too large
        if (area < 1e2 || area > 1e5) continue;

        // Draw each contour only for visualisation purposes
        drawContours(src, contours, static_cast<int>(i), cv::Scalar(0, 0, 255), 2);
        // Find the orientation of each shape
        getOrientation(contours[i], src);
    }

    cv::imshow("output", src);
}

int main(int argc, char** argv) {
    // Load image
    cv::CommandLineParser parser(argc, argv, "{@input | | input image}");
    parser.about("This program uses OpenCV to extract the coordinates of DNA bands.\n");
    parser.printMessage();

    cv::Mat src = cv::imread(cv::samples::findFile(parser.get<cv::String>("@input")));

    // Check if image is loaded successfully
    if (src.empty()) {
        std::cout << "Problem loading image!" << std::endl;
        return EXIT_FAILURE;
    }

    showContours(src);

    cv::waitKey();
    return EXIT_SUCCESS;
}
