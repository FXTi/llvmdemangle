"""Tests for microsoft_demangle(), non_microsoft_demangle(),
get_arm64ec_insertion_point(), MSDF_* constants, and LLVM_VERSION.

No direct LLVM C++ unit test counterpart for most of these — the C++ tests
for Microsoft demangling live in a separate large corpus. These tests verify
the Python API contract and flag behavior.
"""

import pytest
import llvmdemangle

V = llvmdemangle.LLVM_VERSION


class TestMicrosoftDemangle:
    """Tests for microsoft_demangle()."""

    def test_basic(self):
        result = llvmdemangle.microsoft_demangle("?foo@@YAHH@Z")
        assert result is not None
        name, n_read = result
        assert name == "int __cdecl foo(int)"
        assert n_read == 12

    def test_void_function(self):
        result = llvmdemangle.microsoft_demangle("?foo@@YAXH@Z")
        assert result is not None
        assert result[0] == "void __cdecl foo(int)"

    def test_invalid(self):
        assert llvmdemangle.microsoft_demangle("not_msvc") is None

    def test_invalid_itanium(self):
        assert llvmdemangle.microsoft_demangle("_Z3fooi") is None

    def test_flag_no_calling_convention(self):
        result = llvmdemangle.microsoft_demangle(
            "?foo@@YAHH@Z", flags=llvmdemangle.MSDF_NO_CALLING_CONVENTION)
        assert result is not None
        assert result[0] == "int foo(int)"

    def test_flag_no_return_type(self):
        result = llvmdemangle.microsoft_demangle(
            "?foo@@YAHH@Z", flags=llvmdemangle.MSDF_NO_RETURN_TYPE)
        assert result is not None
        assert "__cdecl" in result[0]
        assert not result[0].startswith("int")

    def test_flag_combined(self):
        flags = (llvmdemangle.MSDF_NO_CALLING_CONVENTION |
                 llvmdemangle.MSDF_NO_RETURN_TYPE)
        result = llvmdemangle.microsoft_demangle("?foo@@YAHH@Z", flags=flags)
        assert result is not None
        assert result[0] == "foo(int)"

    def test_n_read_matches_input_length(self):
        mangled = "?foo@@YAHH@Z"
        result = llvmdemangle.microsoft_demangle(mangled)
        assert result is not None
        assert result[1] == len(mangled)


class TestMSDFConstants:
    """Verify MSDF_* flag constants have correct values."""

    def test_msdf_none(self):
        assert llvmdemangle.MSDF_NONE == 0

    def test_msdf_dump_backrefs(self):
        assert llvmdemangle.MSDF_DUMP_BACKREFS == 1

    def test_msdf_no_access_specifier(self):
        assert llvmdemangle.MSDF_NO_ACCESS_SPECIFIER == 2

    def test_msdf_no_calling_convention(self):
        assert llvmdemangle.MSDF_NO_CALLING_CONVENTION == 4

    def test_msdf_no_return_type(self):
        assert llvmdemangle.MSDF_NO_RETURN_TYPE == 8

    def test_msdf_no_member_type(self):
        assert llvmdemangle.MSDF_NO_MEMBER_TYPE == 16

    def test_msdf_no_variable_type(self):
        assert llvmdemangle.MSDF_NO_VARIABLE_TYPE == 32


class TestNonMicrosoftDemangle:
    """Tests for non_microsoft_demangle()."""

    @pytest.mark.skipif(V < 14, reason="requires LLVM >= 14")
    def test_itanium(self):
        assert llvmdemangle.non_microsoft_demangle("_Z3fooi") == "foo(int)"

    @pytest.mark.skipif(V < 14, reason="requires LLVM >= 14")
    def test_rejects_microsoft(self):
        assert llvmdemangle.non_microsoft_demangle("?foo@@YAHH@Z") is None

    @pytest.mark.skipif(V < 14, reason="requires LLVM >= 14")
    def test_invalid(self):
        assert llvmdemangle.non_microsoft_demangle("not_mangled") is None

    @pytest.mark.skipif(V >= 14, reason="Only test on LLVM < 14")
    def test_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            llvmdemangle.non_microsoft_demangle("_Z3fooi")


class TestGetArm64ECInsertionPoint:
    """Tests for get_arm64ec_insertion_point()."""

    @pytest.mark.skipif(V < 19, reason="requires LLVM >= 19")
    def test_non_applicable(self):
        # Regular Itanium symbol — no insertion point
        result = llvmdemangle.get_arm64ec_insertion_point("_Z3fooi")
        assert result is None

    @pytest.mark.skipif(V >= 19, reason="Only test on LLVM < 19")
    def test_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            llvmdemangle.get_arm64ec_insertion_point("_Z3fooi")


class TestLLVMVersion:
    """Tests for the LLVM_VERSION constant."""

    def test_is_int(self):
        assert isinstance(llvmdemangle.LLVM_VERSION, int)

    def test_in_range(self):
        assert 11 <= llvmdemangle.LLVM_VERSION <= 99
