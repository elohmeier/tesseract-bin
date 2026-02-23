# CHANGELOG

<!-- version list -->

## v1.1.0 (2026-02-23)

### Bug Fixes

- Force CMAKE_INSTALL_LIBDIR=lib for consistent lib paths on x86_64 Linux
  ([`6173b6d`](https://github.com/elohmeier/tesseract-bin/commit/6173b6d56ebe9d0773ce975e3d704b0203bed64c))

### Chores

- Fix sdist config
  ([`4a7d1bf`](https://github.com/elohmeier/tesseract-bin/commit/4a7d1bf80788cdabb850760008caad7f430296d6))

### Features

- Add libjpeg-turbo support for JPEG and full TIFF I/O
  ([`ec58395`](https://github.com/elohmeier/tesseract-bin/commit/ec58395814b5c3722f34ff9d8d7a4ec0951ca02a))

- Add libtiff support and fix sdist includes
  ([`abf0c43`](https://github.com/elohmeier/tesseract-bin/commit/abf0c433f66eb9d11e6e02118a6d6656ccafab89))

- Bundle eng + deu tessdata and add OCR pytest
  ([`36699a8`](https://github.com/elohmeier/tesseract-bin/commit/36699a8e574a74cbf410e9e3e133d22757bf2a15))


## v1.0.1 (2026-02-23)

### Bug Fixes

- Build wheels for cp314 in addition to cp313
  ([`b1ebd22`](https://github.com/elohmeier/tesseract-bin/commit/b1ebd22d9e29113a8d1b60c3d5114cbe3b9a0ab0))


## v1.0.0 (2026-02-23)

- Initial Release
