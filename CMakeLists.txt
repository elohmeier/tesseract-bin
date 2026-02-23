cmake_minimum_required(VERSION 3.18)
project(tesseract-bin LANGUAGES C CXX)

include(ExternalProject)

set(STAGING_PREFIX "${CMAKE_BINARY_DIR}/staging" CACHE PATH "Staging install prefix")
set(COMMON_CMAKE_ARGS
    -DCMAKE_PREFIX_PATH=${STAGING_PREFIX}
    -DCMAKE_FIND_ROOT_PATH=${STAGING_PREFIX}
    -DCMAKE_INSTALL_PREFIX=${STAGING_PREFIX}
    -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
    -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
    -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
    -DCMAKE_OSX_ARCHITECTURES=${CMAKE_OSX_ARCHITECTURES}
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON
)

# --- zlib ---
# Build both shared and static so the ZLIB::ZLIB target is available for
# libpng's find_package(ZLIB), then remove the shared library so downstream
# consumers link the static archive instead.
ExternalProject_Add(ep_zlib
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/extern/zlib"
    CMAKE_ARGS
        ${COMMON_CMAKE_ARGS}
        -DZLIB_BUILD_SHARED=ON
        -DZLIB_BUILD_STATIC=ON
        -DZLIB_BUILD_TESTING=OFF
    INSTALL_DIR "${STAGING_PREFIX}"
)

# Remove shared zlib after install so the linker picks the static archive
ExternalProject_Add_Step(ep_zlib remove_shared
    COMMAND ${CMAKE_COMMAND} -E rm -f
        "${STAGING_PREFIX}/lib/libz.dylib"
        "${STAGING_PREFIX}/lib/libz.1.dylib"
        "${STAGING_PREFIX}/lib/libz.1.3.2.dylib"
        "${STAGING_PREFIX}/lib/libz.so"
        "${STAGING_PREFIX}/lib/libz.so.1"
        "${STAGING_PREFIX}/lib/libz.so.1.3.2"
    DEPENDEES install
    COMMENT "Removing shared zlib libraries to force static linking"
)

# --- libpng ---
ExternalProject_Add(ep_libpng
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/extern/libpng"
    CMAKE_ARGS
        ${COMMON_CMAKE_ARGS}
        -DPNG_SHARED=OFF
        -DPNG_STATIC=ON
        -DPNG_FRAMEWORK=OFF
        -DPNG_TESTS=OFF
        -DPNG_TOOLS=OFF
    INSTALL_DIR "${STAGING_PREFIX}"
    DEPENDS ep_zlib
)

# --- leptonica ---
ExternalProject_Add(ep_leptonica
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/extern/leptonica"
    CMAKE_ARGS
        ${COMMON_CMAKE_ARGS}
        -DBUILD_SHARED_LIBS=OFF
        -DBUILD_PROG=OFF
        -DENABLE_JPEG=OFF
        -DENABLE_GIF=OFF
        -DENABLE_TIFF=OFF
        -DENABLE_WEBP=OFF
        -DENABLE_OPENJPEG=OFF
        -DENABLE_ZLIB=ON
        -DENABLE_PNG=ON
    INSTALL_DIR "${STAGING_PREFIX}"
    DEPENDS ep_libpng
)

# --- tesseract ---
ExternalProject_Add(ep_tesseract
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/extern/tesseract"
    CMAKE_ARGS
        ${COMMON_CMAKE_ARGS}
        -DBUILD_SHARED_LIBS=OFF
        -DBUILD_TRAINING_TOOLS=OFF
        -DBUILD_TESTS=OFF
        -DDISABLE_TIFF=ON
        -DDISABLE_ARCHIVE=ON
        -DDISABLE_CURL=ON
        -DGRAPHICS_DISABLED=ON
        -DOPENMP_BUILD=OFF
    INSTALL_DIR "${STAGING_PREFIX}"
    DEPENDS ep_leptonica
)

# --- Install tesseract binary into the wheel ---
install(PROGRAMS "${STAGING_PREFIX}/bin/tesseract" DESTINATION bin)

# --- Install tessdata configs ---
install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/extern/tesseract/tessdata/configs"
    DESTINATION share/tessdata
    PATTERN "Makefile*" EXCLUDE
)
install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/extern/tesseract/tessdata/tessconfigs"
    DESTINATION share/tessdata
    PATTERN "Makefile*" EXCLUDE
)
install(FILES
    "${CMAKE_CURRENT_SOURCE_DIR}/extern/tesseract/tessdata/pdf.ttf"
    DESTINATION share/tessdata
)
