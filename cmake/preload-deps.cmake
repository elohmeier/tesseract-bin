# Preload dependency targets so that statically-linked library configs
# (libtiff, leptonica) can resolve their transitive dependencies.
# Passed to downstream builds via CMAKE_PROJECT_INCLUDE.

# FindCMath.cmake is installed alongside TiffConfig.cmake
get_filename_component(_staging "${CMAKE_PREFIX_PATH}" ABSOLUTE)
list(APPEND CMAKE_MODULE_PATH "${_staging}/lib/cmake/tiff")

find_package(ZLIB QUIET)
find_package(CMath QUIET)
find_package(PNG QUIET)
find_package(TIFF QUIET)
