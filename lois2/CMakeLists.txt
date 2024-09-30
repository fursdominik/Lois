cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(untitled LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

file(
  GLOB_RECURSE
  SOURCES
  CONFIGURE_DEPENDS
  "src/*.cpp"
  "src/*.hpp")

add_executable(${PROJECT_NAME} ${SOURCES})

target_include_directories(${PROJECT_NAME} PRIVATE src)

add_definitions("-DINPUT_FILE_PATH=\"${CMAKE_SOURCE_DIR}/resources/input.txt\"")
add_definitions("-DOUTPUT_FILE_PATH=\"${CMAKE_SOURCE_DIR}/resources/output.txt\"")
