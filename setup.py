import os
import sysconfig as dsc
from sysconfig import get_config_vars as default_get_config_vars

import Cython.Compiler.Options
from Cython.Build import cythonize

# we'd better have Cython installed, or it's a no-go
from Cython.Distutils import build_ext
from setuptools import Extension, Distribution
from setuptools import setup
from setuptools.command.bdist_wheel import bdist_wheel as _bdist_wheel
from setuptools_scm.version import get_local_dirty_tag

Cython.Compiler.Options.docstrings = False


# manipulate get_config_vars:
# 1. step: wrap functionality and filter


def remove_debug(x):
    if type(x) is str:
        # x.replace(" -g ") would be probably enough...
        # but we want to make sure we make it right for every input
        if x == "-g":
            return ""
        if x.startswith("-g "):
            return remove_debug(x[len("-g ") :])
        if x.endswith(" -g"):
            return remove_debug(x[: -len(" -g")])
        return x.replace(" -g ", " ")
    return x


def my_get_config_vars(*args):
    result = default_get_config_vars(*args)
    # sometimes result is a list and sometimes a dict:
    if type(result) is list:
        return [remove_debug(x) for x in result]
    elif type(result) is dict:
        return {k: remove_debug(x) for k, x in result.items()}
    else:
        raise Exception("cannot handle type" + type(result))


# 2.step: replace

dsc.get_config_vars = my_get_config_vars

# change this as needed
libdvIncludeDir = "/usr/include/libdv"


# scan the 'dvedit' directory for extension files, converting
# them to extension names in dotted notation
def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if (
            os.path.isfile(path)
            and path.endswith(".py")
            and not path.endswith("__init__.py")
        ):
            files.append(path.replace(os.path.sep, ".")[:-3])
        elif os.path.isdir(path):
            scandir(path, files)
    return files


# generate an Extension object from its dotted name
def make_extension(ext_name):
    ext_path = ext_name.replace(".", os.path.sep) + ".py"
    return Extension(
        ext_name,
        [ext_path],
        include_dirs=["."],  # adding the '.' to include_dirs is CRUCIAL!!
        extra_compile_args=["-O3", "-Wall"],
    )


# get the list of extensions
extNames = scandir("ai_search")

# and build up the set of Extension objects
extensions = [make_extension(name) for name in extNames]


class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""

    def has_ext_modules(self):
        return True


def clean_scheme(version):
    return get_local_dirty_tag(version) if version.dirty else "+clean"


print(os.getenv("CI", "false"))
print(type(os.getenv("CI")))

# finally, we can pass all this to distutils
setup(
    name="ai-search",
    # packages=find_packages(where='ai_search'),
    ext_modules=cythonize(extensions, gdb_debug=False),
    cmdclass={"build_ext": build_ext, "bdist_wheel": bdist_wheel},
    distclass=BinaryDistribution,
    use_scm_version={
        "version_scheme": "only-version"
        if os.getenv("CI", "false") == "true"
        else "guess-next-dev",
        "local_scheme": "no-local-version"
        if os.getenv("CI", "false") == "true"
        else "node-and-date",
    },
)
