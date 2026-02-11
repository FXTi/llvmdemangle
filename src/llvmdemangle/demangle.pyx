# distutils: language = c++

from libcpp.string cimport string

cdef extern from "llvm/Demangle/Demangle.h" namespace "llvm":
    string demangle(const char*)

cpdef llvm_demangle(mangled_name):
    cdef string c_demangled_name = demangle(mangled_name.encode("ascii"))
    return c_demangled_name.decode("ascii")
