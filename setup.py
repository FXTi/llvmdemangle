# setup.py

import os
import sys
import platform
from pathlib import Path
from setuptools import setup, find_packages, Extension

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# LLVM version from env (default: 15)
LLVM_MAJOR = int(os.environ.get("LLVM_VERSION", "15"))
PACKAGE_VERSION = os.environ.get("PACKAGE_VERSION", f"{LLVM_MAJOR}")

# Locate vendored source
vendor_dir = this_directory / "vendor" / f"llvm{LLVM_MAJOR}"
vendor_include = vendor_dir / "include"
vendor_lib = vendor_dir / "lib" / "Demangle"

if not vendor_dir.exists():
    print(
        f"Error: Vendored LLVM {LLVM_MAJOR} not found at {vendor_dir}\n"
        f"Run: python vendor_llvm.py --llvm-version {LLVM_MAJOR}",
        file=sys.stderr,
    )
    sys.exit(1)

# Collect vendored .cpp sources
llvm_sources = sorted(str(p) for p in vendor_lib.glob("*.cpp"))

# Platform-specific flags
extra_compile_args = []
extra_link_args = []

if platform.system() == "Windows":
    extra_compile_args = ["/std:c++17", "/EHsc"]
else:
    extra_compile_args = ["-std=c++17", "-fPIC"]
    if platform.system() == "Darwin":
        extra_compile_args.append("-stdlib=libc++")
        extra_link_args.append("-stdlib=libc++")

extensions = [
    Extension(
        "llvmdemangle.demangle",
        sources=["src/llvmdemangle/demangle.pyx"] + llvm_sources,
        language="c++",
        include_dirs=[str(vendor_include)],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
]

setup(
    name="llvm-demangle-fxti",
    version=PACKAGE_VERSION,
    description="Python wrapper around llvm::demangle, with vendored LLVM Demangle.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="0BSD AND Apache-2.0 WITH LLVM-exception",
    author="MNayer",
    author_email="marie.nayer@web.de",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/MNayer/llvmdemangle",
    keywords="demangling c++ cxx cpp llvm",
    install_requires=[
        "click",
    ],
    ext_modules=extensions,
    entry_points={
        "console_scripts": [
            "demangle = llvmdemangle.tools:demangle",
        ],
    },
    python_requires=">=3.8",
)
