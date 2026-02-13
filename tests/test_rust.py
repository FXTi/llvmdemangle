"""Tests ported from LLVM 21.1.0 llvm/unittests/Demangle/RustDemangleTest.cpp

Tests the rust_demangle() function.
"""

import pytest
import llvmdemangle

V = llvmdemangle.LLVM_VERSION

pytestmark = pytest.mark.skipif(V < 13, reason="rust_demangle requires LLVM >= 13")


class TestRustDemangle:
    """Ported from TEST(RustDemangle, Success) and TEST(RustDemangle, Invalid)."""

    def test_success(self):
        assert llvmdemangle.rust_demangle("_RNvC1a4main") == "a::main"

    def test_invalid_prefix(self):
        assert llvmdemangle.rust_demangle("_ABCDEF") is None

    def test_correct_prefix_but_invalid(self):
        assert llvmdemangle.rust_demangle("_RRR") is None

    def test_crate_function(self):
        assert llvmdemangle.rust_demangle("_RNvC8my_crate3foo") == "my_crate::foo"

    def test_not_rust(self):
        assert llvmdemangle.rust_demangle("_Z3fooi") is None

    def test_plain_string(self):
        assert llvmdemangle.rust_demangle("not_rust") is None


class TestRustDemangleVersionGuard:
    """Verify NotImplementedError on old LLVM versions."""

    @pytest.mark.skipif(V >= 13, reason="Only test on LLVM < 13")
    def test_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            llvmdemangle.rust_demangle("_RNvC1a4main")
