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

# --- libtiff ---
ExternalProject_Add(ep_libtiff
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/extern/libtiff"
    CMAKE_ARGS
        ${COMMON_CMAKE_ARGS}
        -DBUILD_SHARED_LIBS=OFF
        -Dtiff-tools=OFF
        -Dtiff-tests=OFF
        -Dtiff-contrib=OFF
        -Dtiff-docs=OFF
        -Dtiff-deprecated=OFF
        -Dtiff-install=ON
        -Djbig=OFF
        -Dlerc=OFF
        -Dlzma=OFF
        -Dwebp=OFF
        -Dzstd=OFF
        -Djpeg=OFF
        -Dcxx=OFF
        -Dlibdeflate=OFF
    INSTALL_DIR "${STAGING_PREFIX}"
    DEPENDS ep_zlib
)

# libtiff v4.7.0 static builds export CMath::CMath and ZLIB::ZLIB as link
# dependencies in TiffTargets.cmake but TiffConfig.cmake has a TODO to call
# find_dependency() for them. Copy FindCMath.cmake into the installed tiff
# cmake dir and patch TiffConfig.cmake to import it before loading targets.
ExternalProject_Add_Step(ep_libtiff fix_cmake_config
    COMMAND ${CMAKE_COMMAND} -E copy
        "${CMAKE_CURRENT_SOURCE_DIR}/extern/libtiff/cmake/FindCMath.cmake"
        "${STAGING_PREFIX}/lib/cmake/tiff/FindCMath.cmake"
    COMMAND ${CMAKE_COMMAND}
        -DTIFF_CONFIG=${STAGING_PREFIX}/lib/cmake/tiff/TiffConfig.cmake
        -P "${CMAKE_CURRENT_SOURCE_DIR}/cmake/patch-tiff-config.cmake"
    DEPENDEES install
    COMMENT "Patching TiffConfig.cmake to resolve CMath::CMath for static linking"
)

# Preload script ensures transitive dependency targets (ZLIB::ZLIB,
# CMath::CMath, etc.) are available when consuming statically-linked
# libtiff and leptonica configs that omit find_dependency() calls.
set(PRELOAD_DEPS "${CMAKE_CURRENT_SOURCE_DIR}/cmake/preload-deps.cmake")

# --- leptonica ---
ExternalProject_Add(ep_leptonica
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/extern/leptonica"
    CMAKE_ARGS
        ${COMMON_CMAKE_ARGS}
        -DCMAKE_PROJECT_INCLUDE=${PRELOAD_DEPS}
        -DBUILD_SHARED_LIBS=OFF
        -DBUILD_PROG=OFF
        -DENABLE_JPEG=OFF
        -DENABLE_GIF=OFF
        -DENABLE_TIFF=ON
        -DENABLE_WEBP=OFF
        -DENABLE_OPENJPEG=OFF
        -DENABLE_ZLIB=ON
        -DENABLE_PNG=ON
    INSTALL_DIR "${STAGING_PREFIX}"
    DEPENDS ep_libpng ep_libtiff
)

# --- tesseract ---
ExternalProject_Add(ep_tesseract
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/extern/tesseract"
    CMAKE_ARGS
        ${COMMON_CMAKE_ARGS}
        -DCMAKE_PROJECT_INCLUDE=${PRELOAD_DEPS}
        -DBUILD_SHARED_LIBS=OFF
        -DBUILD_TRAINING_TOOLS=OFF
        -DBUILD_TESTS=OFF
        -DDISABLE_TIFF=OFF
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
