# Prepend find_dependency calls to TiffConfig.cmake so that CMath::CMath
# and ZLIB::ZLIB are available when TiffTargets.cmake is loaded.
file(READ "${TIFF_CONFIG}" _content)
string(FIND "${_content}" "find_dependency(CMath)" _pos)
if(_pos EQUAL -1)
    set(_deps "include(CMakeFindDependencyMacro)\nlist(APPEND CMAKE_MODULE_PATH \"\${CMAKE_CURRENT_LIST_DIR}\")\nfind_dependency(CMath)\nfind_dependency(ZLIB)\n\n")
    file(WRITE "${TIFF_CONFIG}" "${_deps}${_content}")
endif()
