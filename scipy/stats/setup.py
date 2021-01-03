from os.path import join
from platform import system


def pre_build_hook(build_ext, ext):
    from scipy._build_utils.compiler_helper import get_cxx_std_flag
    std_flag = get_cxx_std_flag(build_ext._cxx_compiler)
    if std_flag is not None:
        ext.extra_compile_args.append(std_flag)


def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    import numpy as np
    config = Configuration('stats', parent_package, top_path)

    config.add_data_dir('tests')

    statlib_src = [join('statlib', '*.f')]
    config.add_library('statlib', sources=statlib_src)

    # add statlib module
    config.add_extension('statlib',
        sources=['statlib.pyf'],
        f2py_options=['--no-wrap-functions'],
        libraries=['statlib'],
        depends=statlib_src
    )

    # add _stats module
    config.add_extension('_stats',
        sources=['_stats.c'],
    )

    # add mvn module
    config.add_extension('mvn',
        sources=['mvn.pyf','mvndst.f'],
    )

    # add BiasedUrn module
    config.add_data_files(['random.pxd', 'biasedurn.pxd'])
    npy_major_version = int(np.__version__.split('.')[1])
    if npy_major_version >= 18:
        inc_dirs = [np.get_include()]
    else:
        from scipy._build_utils.npy_1_18_compat import get_include
        inc_dirs = [get_include()]
    ext = config.add_extension(
        'biasedurn',
        sources=[
            'biasedurn.cxx',
            'biasedurn/impls.cpp',
            'biasedurn/fnchyppr.cpp',
            'biasedurn/wnchyppr.cpp',
            'biasedurn/stoc1.cpp',
            'biasedurn/stoc3.cpp'],
        include_dirs=inc_dirs,
        define_macros=[('R_BUILD', None)],
        language='c++',
        extra_compile_args=['-Wno-narrowing'] if system() == 'Darwin' else [],
    )
    ext._pre_build_hook = pre_build_hook

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
