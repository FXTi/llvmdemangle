# LLVM-Demangle

Python wrapper around `llvm::demangle`, with vendored LLVM Demangle source.

No system LLVM installation required. Pre-built wheels available for Linux, macOS, and Windows.

## Install

Pick the LLVM version you need (15–20):

```bash
pip install llvm-demangle-fxti==18.0.0   # LLVM 18
pip install llvm-demangle-fxti==15.0.0   # LLVM 15
```

## Usage

```python
from llvmdemangle.demangle import llvm_demangle
llvm_demangle("_Z5isinfUa9enable_ifILb1EEd")
# => 'isinf(double) [enable_if:true]'
```

CLI:

```bash
demangle _Z5isinfUa9enable_ifILb1EEd
# => isinf(double) [enable_if:true]
```

## Build from source

```bash
# 1. Vendor LLVM Demangle source (downloads from GitHub releases)
python vendor_llvm.py --llvm-version 18

# 2. Build & install
LLVM_VERSION=18 pip install .
```

Supported LLVM versions: 15, 16, 17, 18, 19, 20.

## License

- Wrapper code: [0BSD](LICENSE.txt)
- LLVM Demangle source: [Apache 2.0 with LLVM Exception](LLVM_LICENSE.txt)
