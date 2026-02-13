"""Shared fixtures for llvmdemangle tests."""

import pytest
import llvmdemangle


@pytest.fixture(params=llvmdemangle.SUPPORTED_VERSIONS)
def llvm(request):
    """Provide a backend module for each supported LLVM version."""
    return llvmdemangle.backend(request.param)
