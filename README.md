# Darkdetect

This package allows to detect if the user is using Dark Mode ([macOS 10.14+](https://support.apple.com/en-us/HT208976) or [Windows 10 1607+](https://au.pcmag.com/netflix/63426/how-to-enable-dark-mode-in-windows-10)). The main application of this package is to detect the Dark mode from your GUI Python application (Tkinter/wx/pyqt/qt for python (pyside)/...) and apply the needed adjustments to your interface. Darkdetect is particularly useful if your GUI library **does not** provide a public API for this detection (I am looking at you, Qt). In addition, this package does not depend on other modules or packages that are not already included in standard Python distributions.


## Usage

```
import darkdetect

>>> darkdetect.theme()
'Dark'

>>> darkdetect.isDark()
True

>>> darkdetect.isLight()
False
```
It's that easy.

## Install

The preferred channel is PyPI:
```
pip install darkdetect
```

Alternatively, you are free to vendor directly a copy of Darkdetect in your app. Further information on vendoring can be found [here](https://medium.com/underdog-io-engineering/vendoring-python-dependencies-with-pip-b9eb6078b9c0).

## Notes

- This software is licensed under the terms of the 3-clause BSD License.
- This package can be installed on any operative system, but it will always return `None` unless executed on a version of macOS or Windows that supports Dark Mode e.g. the oldest version of macOS is 10.14 Mojave and the oldest version of Windows 10 is the Anniversary Update (1607). This package is designed to work also with older versions of macOS and Windows and in those cases it will also return `None`. Detection of the dark menu bar and dock option (available from 10.10) is not supported.
- [Details](https://stackoverflow.com/questions/25207077/how-to-detect-if-os-x-is-in-dark-mode) on the detection method used.
