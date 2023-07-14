# -*- coding: utf-8 -*-
# Copyright (C) 2022 Mujin,Inc.
add_definitions("-Wall")
add_definitions("-DMUJINVISIONCONTROLLERCLIENT_DLL")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fvisibility=hidden")

include_directories(${MujinControllerCommon_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS} ${ZeroMQ_INCLUDE_DIR} ${LOG4CXX_INCLUDEDIR})
link_directories(${MujinControllerCommon_LIBRARY_DIRS} ${Boost_LIBRARY_DIRS} ${LOG4CXX_LIBDIR})

add_library(boost_assertion_failed STATIC boost_assertion_failed.cpp)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")

add_library(
    mujinvisioncontrollerclient
    SHARED
    visioncontrollerclient.cpp 
)   

set_target_properties(mujinvisioncontrollerclient PROPERTIES
  COMPILE_FLAGS "${MujinControllerCommon_CXX_FLAGS}"
  LINK_FLAGS "${MujinControllerCommon_LINK_FLAGS}"
  OUTPUT_NAME mujinvisioncontrollerclient${MUJINVISIONCONTROLLERCLIENT_LIBRARY_SUFFIX}
  SOVERSION 0 # always have it 0 since we're including the soversion as part of the library name
  VERSION ${MUJINVISIONCONTROLLERCLIENT_VERSION}
  CLEAN_DIRECT_OUTPUT 1
)
target_link_libraries(mujinvisioncontrollerclient
  PUBLIC ${LOG4CXX_LIBRARIES} ${ZeroMQ_LIBRARY} ${MujinControllerCommon_LIBRARIES} ${Boost_IOSTREAMS_LIBRARY}
  PRIVATE boost_assertion_failed
)
install(TARGETS mujinvisioncontrollerclient LIBRARY DESTINATION lib${LIB_SUFFIX})

install(DIRECTORY include/ DESTINATION include FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp")
