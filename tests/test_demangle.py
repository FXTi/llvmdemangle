"""Tests ported from LLVM 21.1.0 llvm/unittests/Demangle/DemangleTest.cpp

Tests the top-level demangle() function which auto-detects the mangling scheme.
"""

import pytest
import llvmdemangle

V = llvmdemangle.LLVM_VERSION


class TestDemangle:
    """Ported from TEST(Demangle, demangleTest)."""

    def test_underscore(self):
        assert llvmdemangle.demangle("_") == "_"

    def test_itanium_basic(self):
        assert llvmdemangle.demangle("_Z3fooi") == "foo(int)"

    def test_itanium_double_underscore(self):
        assert llvmdemangle.demangle("__Z3fooi") == "foo(int)"

    def test_itanium_block_invoke_triple_underscore(self):
        assert llvmdemangle.demangle("___Z3fooi_block_invoke") == \
            "invocation function for block in foo(int)"

    def test_itanium_block_invoke_quad_underscore(self):
        assert llvmdemangle.demangle("____Z3fooi_block_invoke") == \
            "invocation function for block in foo(int)"

    def test_microsoft(self):
        assert llvmdemangle.demangle("?foo@@YAXH@Z") == "void __cdecl foo(int)"

    def test_plain_name(self):
        assert llvmdemangle.demangle("foo") == "foo"

    @pytest.mark.skipif(V < 13, reason="rust_demangle requires LLVM >= 13")
    def test_rust(self):
        assert llvmdemangle.demangle("_RNvC3foo3bar") == "foo::bar"

    @pytest.mark.skipif(V < 15, reason="__R prefix for Rust requires LLVM >= 15")
    def test_rust_double_underscore(self):
        assert llvmdemangle.demangle("__RNvC3foo3bar") == "foo::bar"

    @pytest.mark.skipif(V < 14, reason="dlang_demangle requires LLVM >= 14")
    def test_dlang(self):
        assert llvmdemangle.demangle("_Dmain") == "D main"

    @pytest.mark.skipif(V < 13, reason="_ExtInt demangling requires LLVM >= 13")
    def test_vendor_extended_type_qualifier(self):
        """Regression test for https://bugs.llvm.org/show_bug.cgi?id=48009"""
        assert llvmdemangle.demangle("_Z3fooILi79EEbU7_ExtIntIXT_EEi") == \
            "bool foo<79>(int _ExtInt<79>)"


class TestLlvmDemangleCompat:
    """Test backward-compatible llvm_demangle() alias."""

    def test_alias(self):
        assert llvmdemangle.llvm_demangle("_Z3fooi") == "foo(int)"

    def test_alias_matches_demangle(self):
        name = "_ZN3Foo3barEid"
        assert llvmdemangle.llvm_demangle(name) == llvmdemangle.demangle(name)
