"""
Setuptools script for the installation of SymForce.
"""
import os
from pathlib import Path
import subprocess
import sys

from setuptools import Extension
from setuptools import find_packages
from setuptools import setup
from setuptools.command.build_ext import build_ext

SOURCE_DIR = Path(__file__).resolve().parent


class CMakeExtension(Extension):
    """
    CMake extension type.
    """

    def __init__(self, name: str):
        Extension.__init__(self, name, sources=[])


class CMakeBuild(build_ext):
    """
    Custom extension builder that runs CMake.
    """

    def run(self) -> None:
        # Test for CMake
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: "
                + ", ".join(e.name for e in self.extensions)
            )

        build_directory = os.path.abspath(self.build_temp)

        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + build_directory,
            "-DPYTHON_EXECUTABLE=" + sys.executable,
        ]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        # NOTE(hayk): Not building tests here to save time. Is that okay, and do we want to build
        # C++ examples? Also could be a waste.
        cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg, "-DSYMFORCE_BUILD_TESTS=OFF"]

        # Assuming Makefiles
        build_args += ["--", "-j7"]

        self.build_args = build_args

        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get("CXXFLAGS", ""), self.distribution.get_version()
        )
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # CMakeLists.txt is in the same directory as this setup.py file
        cmake_list_dir = os.path.abspath(os.path.dirname(__file__))
        print("-" * 10, "Running CMake prepare", "-" * 40)
        subprocess.check_call(["cmake", cmake_list_dir] + cmake_args, cwd=self.build_temp, env=env)

        print("-" * 10, "Building extensions", "-" * 40)
        cmake_cmd = ["cmake", "--build", "."] + self.build_args
        subprocess.check_call(cmake_cmd, cwd=self.build_temp)

        # Move from build temp to final position
        for ext in self.extensions:
            self.move_output(ext)

    def move_output(self, ext: CMakeExtension) -> None:
        build_temp = Path(self.build_temp).resolve()
        dest_path = Path(self.get_ext_fullpath(ext.name)).resolve()
        source_path = build_temp / self.get_ext_filename(ext.name)
        dest_directory = dest_path.parents[0]
        dest_directory.mkdir(parents=True, exist_ok=True)
        self.copy_file(source_path, dest_path)


setup(
    name="symforce",
    version="0.3.1",
    author="Skydio, Inc",
    author_email="hayk@skydio.com",
    description="A fast symbolic computation and code generation library for robotics",
    keywords="python cpp robotics optimization code-generation symbolic-computation",
    license="BSD-3",
    license_file="LICENSE",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/symforce-org/symforce",
    project_urls={
        "Bug Tracker": "https://github.com/symforce-org/symforce/issues",
        "Source": "https://github.com/symforce-org/symforce",
    },
    # For a list of valid classifiers see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    # -------------------------------------------------------------------------
    # Build info
    # -------------------------------------------------------------------------
    # Minimum Python version
    python_requires=">=3.8",
    # Find all packages in the
    packages=find_packages(),
    # Override the extension builder with our cmake class
    cmdclass=dict(build_ext=CMakeBuild),
    # Build C++ extension module
    ext_modules=[CMakeExtension("pybind.cc_sym",),],
    # Barebones packages needed to run symforce
    install_requires=[
        "black",
        "clang-format",
        "graphviz",
        "jinja2",
        f"lcmtypes @ file://localhost/{SOURCE_DIR}/lcmtypes/gen/python2.7",
        "numpy",
        "sympy",
        f"skymarshal @ file://localhost/{SOURCE_DIR}/third_party/skymarshal",
        f"sym @ file://localhost/{SOURCE_DIR}/gen/python",
    ],
    # Manifest is needed at runtime
    data_files=[("build", ["build/manifest.json",])],
    # Not okay to zip
    zip_safe=False,
)
