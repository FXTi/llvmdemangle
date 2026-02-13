from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("llvm-demangle-fxti")
except PackageNotFoundError:
    __version__ = "0.0.0"

from llvmdemangle.demangle import (
    LLVM_VERSION,
    # Functions
    demangle,
    llvm_demangle,
    itanium_demangle,
    microsoft_demangle,
    rust_demangle,
    dlang_demangle,
    non_microsoft_demangle,
    get_arm64ec_insertion_point,
    # Flag constants
    MSDF_NONE,
    MSDF_DUMP_BACKREFS,
    MSDF_NO_ACCESS_SPECIFIER,
    MSDF_NO_CALLING_CONVENTION,
    MSDF_NO_RETURN_TYPE,
    MSDF_NO_MEMBER_TYPE,
    MSDF_NO_VARIABLE_TYPE,
    # Class
    ItaniumPartialDemangler,
)

__all__ = [
    "LLVM_VERSION",
    "demangle",
    "llvm_demangle",
    "itanium_demangle",
    "microsoft_demangle",
    "rust_demangle",
    "dlang_demangle",
    "non_microsoft_demangle",
    "get_arm64ec_insertion_point",
    "MSDF_NONE",
    "MSDF_DUMP_BACKREFS",
    "MSDF_NO_ACCESS_SPECIFIER",
    "MSDF_NO_CALLING_CONVENTION",
    "MSDF_NO_RETURN_TYPE",
    "MSDF_NO_MEMBER_TYPE",
    "MSDF_NO_VARIABLE_TYPE",
    "ItaniumPartialDemangler",
]
