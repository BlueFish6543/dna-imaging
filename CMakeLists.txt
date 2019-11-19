cmake_minimum_required(VERSION 3.13)
project(dna_imaging)

set(CMAKE_CXX_STANDARD 14)

find_package(OpenCV REQUIRED)

set(SOURCE_FILES cpp/pca.cpp)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})

include_directories(${OpenCV_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})