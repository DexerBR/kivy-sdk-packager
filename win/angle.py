from __future__ import absolute_import, print_function
from .common import *

__version__ = '0.5.0'


def get_angle(cache, build_path, arch, package, output, download_only=False):
    data = []
    base_dir = join(build_path, 'Release_{}'.format(arch))
    
    # Original behavior: DLLs
    for dll in ('libEGL.dll', 'libGLESv2.dll', 'd3dcompiler_47.dll'):
        data.append((join(base_dir, dll), join('bin', dll),
                     join('share', package, 'bin'), False))
    
    # Added: static libraries
    static_dir = join(base_dir, 'bin', 'static')
    for lib in ('libEGL.lib', 'libGLESv2.lib'):
        data.append((join(static_dir, lib), join('bin', 'static', lib),
                     join('share', package, 'bin', 'static'), False))
    
    # Added: header files for static linking
    include_dir = join(build_path, 'include')
    if exists(include_dir):
        for root, dirs, files in walk(include_dir):
            for file in files:
                if file.endswith('.h'):
                    src_path = join(root, file)
                    rel_path = relpath(src_path, include_dir)
                    data.append((src_path, join('include', rel_path),
                               join('share', package, 'include'), False))

    make_package(
        join(build_path, 'project'), package, data, __version__, output, 'MIT')


if __name__ == '__main__':
    parse_args(get_angle)
