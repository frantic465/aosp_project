#/usr/bin/python


import os
import os.path

base_dir = "../aosp"

include_paths = []
extra_include_paths = set()
headers = []
sources = []
extra_files = []

root_dirs = ['abi', 'frameworks', 'hardware', 'packages', 'system', 'bionic', 'libcore', 'libnativehelper']

for root_dir in root_dirs:
    for root, dirs, files in os.walk(os.path.join(base_dir, root_dir)):
        root = root.replace(base_dir, "", 1)
        for name in files:
            (bname, ext) = os.path.splitext(name)
            if ext == '.h':
                headers.append(os.path.join(root, name))
                if not '/include' in root:
                    extra_include_paths.add(root)
            elif ext == '.cpp' or ext == '.c' or ext == '.cc':
                sources.append(os.path.join(root, name))
            elif ext == '.mk':
                extra_files.append(os.path.join(root, name))

        for name in dirs:
            if name == 'include':
                include_paths.append(os.path.join(root, name))

print """
QT -= core gui
TARGET = android
TEMPLATE = app
"""

print "ROOT_DIR = " + base_dir

for include_path in include_paths:
    print "INCLUDEPATH += $${ROOT_DIR}" + include_path

for include_path in extra_include_paths:
    print "INCLUDEPATH += $${ROOT_DIR}" + include_path

for header in headers:
    print "SOURCES += $${ROOT_DIR}" + header

for extra_file in extra_files:
    print "SOURCES += $${ROOT_DIR}" + extra_file

for source in sources:
    print "SOURCES += $${ROOT_DIR}" + source