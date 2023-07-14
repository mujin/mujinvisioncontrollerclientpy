# -*- coding: utf-8 -*-
# Copyright (C) 2022 Mujin,Inc.
cmake_minimum_required(VERSION 2.8)

project(mujinvisioncontrollerclient)
set( CMAKE_ALLOW_LOOSE_LOOP_CONSTRUCTS TRUE )

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake")

# Define here the needed parameters
# make sure to change the version in docs/Makefile
set (MUJINVISIONCONTROLLERCLIENT_VERSION_MAJOR 0)
set (MUJINVISIONCONTROLLERCLIENT_VERSION_MINOR 1)
set (MUJINVISIONCONTROLLERCLIENT_VERSION_PATCH 0)
set (MUJINVISIONCONTROLLERCLIENT_VERSION ${MUJINVISIONCONTROLLERCLIENT_VERSION_MAJOR}.${MUJINVISIONCONTROLLERCLIENT_VERSION_MINOR}.${MUJINVISIONCONTROLLERCLIENT_VERSION_PATCH})
set (MUJINVISIONCONTROLLERCLIENT_SOVERSION ${MUJINVISIONCONTROLLERCLIENT_VERSION_MAJOR}.${MUJINVISIONCONTROLLERCLIENT_VERSION_MINOR})
message(STATUS "Compiling MUJIN VisionController Client Library Version ${MUJINVISIONCONTROLLERCLIENT_VERSION}, soversion=${MUJINVISIONCONTROLLERCLIENT_SOVERSION}")
set (MUJINVISIONCONTROLLERCLIENT_CMAKE_INSTALL_DIR "mujinvisioncontrollerclient-${MUJINVISIONCONTROLLERCLIENT_VERSION_MAJOR}.${MUJINVISIONCONTROLLERCLIENT_VERSION_MINOR}")

message(STATUS "Using cmake version ${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}.${CMAKE_PATCH_VERSION}" )
# http://www.cmake.org/cmake/help/cmake-2.6.html#policy:CMP0002
cmake_policy(SET CMP0002 NEW)
# http://www.cmake.org/cmake/help/cmake-2.6.html#policy:CMP0003
cmake_policy(SET CMP0003 NEW)

# Use, i.e. don't skip the full RPATH for the build tree
set(CMAKE_SKIP_BUILD_RPATH  FALSE)

# When building, don't use the install RPATH already
# (but later on when installing)
set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)

set(LIB_SUFFIX CACHE STRING "suffix for the library directory need for x86-64 systems that use lib64 ")

# The RPATH to be used when installing
set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib${LIB_SUFFIX}")

# Add the automatically determined parts of the RPATH
# which point to directories outside the build tree to the install RPATH
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

set(
  MUJINVISIONCONTROLLERCLIENT_LIBRARY_SUFFIX
  "${MUJINVISIONCONTROLLERCLIENT_SOVERSION}" CACHE STRING "Suffix to append to library names"
)

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}/src/include
  ${CMAKE_CURRENT_BINARY_DIR}/include
) # have to do this before every other include!

configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/config.h.in
  ${CMAKE_CURRENT_BINARY_DIR}/include/mujinvisioncontrollerclient/config.h
  IMMEDIATE @ONLY
)
  
install(
  FILES
  ${CMAKE_CURRENT_BINARY_DIR}/include/mujinvisioncontrollerclient/config.h
  DESTINATION
  include/mujinvisioncontrollerclient
)

# dependencies
find_package(PkgConfig)
pkg_check_modules(LOG4CXX REQUIRED liblog4cxx)
find_package(ZeroMQ 4.3.2 REQUIRED)

if(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX OR COMPILER_IS_CLANG )
  add_definitions(-fPIC) # this is a very important switch and some libraries seem now to have it....
  add_definitions(-Wall -Werror -Werror=shadow)
  
  set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")
  set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "-g3 -O3 -DNDEBUG")
  set(CMAKE_CXX_FLAGS_DEBUG "-g3 -D_DEBUG")
endif()
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DMUJINVISIONCONTROLLERCLIENT_DLL")

find_package(MujinControllerCommon 0.56 REQUIRED)
find_package(RapidJSON REQUIRED)

find_package(Boost COMPONENTS iostreams chrono)# date_time filesystem program_options system
add_definitions("-DBOOST_ENABLE_ASSERT_HANDLER") # turns segfault into exception
add_definitions("-DRAPIDJSON_ASSERT=BOOST_ASSERT") # use boost assert for rapidjson, turns assert segfault into exception

# install cmake config files
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/mujinvisioncontrollerclient-config.cmake.in" "${CMAKE_CURRENT_BINARY_DIR}/mujinvisioncontrollerclient-config.cmake" IMMEDIATE @ONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/mujinvisioncontrollerclient-config-version.cmake.in" "${CMAKE_CURRENT_BINARY_DIR}/mujinvisioncontrollerclient-config-version.cmake" IMMEDIATE @ONLY)

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/mujinvisioncontrollerclient-config.cmake" "${CMAKE_CURRENT_BINARY_DIR}/mujinvisioncontrollerclient-config-version.cmake" DESTINATION "lib${LIB_SUFFIX}/cmake/${MUJINVISIONCONTROLLERCLIENT_CMAKE_INSTALL_DIR}")

add_subdirectory(src)

# add make uninstall capability
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/cmake_uninstall.cmake.in" "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake" IMMEDIATE @ONLY)
add_custom_target(uninstall "${CMAKE_COMMAND}" -P "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake")
