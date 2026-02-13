# LLVM-Demangle

Python bindings for the LLVM Demangle library, with vendored LLVM source.

Exposes Itanium, Microsoft, Rust, and D language demanglers, plus `ItaniumPartialDemangler` for querying individual symbol components. No system LLVM installation required.

## Install

Pick the LLVM version you need (11–21):

```bash
pip install llvm-demangle-fxti==18.0.0   # LLVM 18
pip install llvm-demangle-fxti==15.0.0   # LLVM 15
```

## Quick start

```python
import llvmdemangle

llvmdemangle.demangle("_Z3fooi")           # 'foo(int)'
llvmdemangle.demangle("?foo@@YAHH@Z")      # 'int __cdecl foo(int)'
```

CLI:

```bash
demangle _Z3fooi
# => foo(int)
```

## API reference

### `LLVM_VERSION`

Integer constant indicating the LLVM version the module was compiled with (e.g. `18`).

### `demangle(name) -> str`

Auto-detect mangling scheme and demangle. Returns the original string if unrecognized.

```python
llvmdemangle.demangle("_Z3fooi")       # 'foo(int)'
llvmdemangle.demangle("?foo@@YAHH@Z")  # 'int __cdecl foo(int)'
llvmdemangle.demangle("plain")         # 'plain'
```

### `itanium_demangle(name, *, parse_params=True) -> str | None`

Demangle an Itanium C++ ABI symbol. Returns `None` on failure.

`parse_params=False` omits function parameters (LLVM >= 18; ignored on older versions).

```python
llvmdemangle.itanium_demangle("_Z3fooi")                        # 'foo(int)'
llvmdemangle.itanium_demangle("_Z3fooi", parse_params=False)    # 'foo'  (LLVM 18+)
```

### `microsoft_demangle(name, *, flags=0) -> tuple[str, int] | None`

Demangle a Microsoft Visual C++ symbol. Returns `(demangled_name, n_read)` or `None`.

```python
llvmdemangle.microsoft_demangle("?foo@@YAHH@Z")
# ('int __cdecl foo(int)', 12)

llvmdemangle.microsoft_demangle("?foo@@YAHH@Z", flags=llvmdemangle.MSDF_NO_CALLING_CONVENTION)
# ('int foo(int)', 12)
```

Flag constants:

| Constant | Value | Description |
|---|---|---|
| `MSDF_NONE` | 0 | No flags |
| `MSDF_DUMP_BACKREFS` | 1 | Dump back-references |
| `MSDF_NO_ACCESS_SPECIFIER` | 2 | Omit access specifiers |
| `MSDF_NO_CALLING_CONVENTION` | 4 | Omit calling convention |
| `MSDF_NO_RETURN_TYPE` | 8 | Omit return type |
| `MSDF_NO_MEMBER_TYPE` | 16 | Omit member type |
| `MSDF_NO_VARIABLE_TYPE` | 32 | Omit variable type (LLVM >= 14) |

### `rust_demangle(name) -> str | None`

Demangle a Rust v0 symbol. Returns `None` on failure. Requires LLVM >= 13.

```python
llvmdemangle.rust_demangle("_RNvC8my_crate3foo")  # 'my_crate::foo'
```

### `dlang_demangle(name) -> str | None`

Demangle a D language symbol. Returns `None` on failure. Requires LLVM >= 14.

```python
llvmdemangle.dlang_demangle("_Dmain")  # 'D main'
```

### `non_microsoft_demangle(name, *, can_have_leading_dot=True, parse_params=True) -> str | None`

Demangle a non-Microsoft symbol (Itanium, Rust, or D). Returns `None` on failure. Requires LLVM >= 14. `parse_params` requires LLVM >= 18.

### `get_arm64ec_insertion_point(name) -> int | None`

Get the Arm64EC insertion point in a mangled name. Requires LLVM >= 19.

### `ItaniumPartialDemangler`

Parse Itanium C++ symbols into an AST and query individual components.

```python
d = llvmdemangle.ItaniumPartialDemangler()
if d.parse("_ZN3Foo3barIiEEvi"):
    d.full_name              # 'void Foo::bar<int>(int)'
    d.function_base_name     # 'bar'
    d.function_decl_context  # 'Foo'
    d.function_name          # 'Foo::bar<int>'
    d.function_parameters    # '(int)'
    d.function_return_type   # 'void'
    d.is_function            # True
    d.is_data                # False
    d.is_ctor_or_dtor        # False
    d.is_special_name        # False
    d.has_function_qualifiers  # False
```

All string properties return `None` if the symbol hasn't been parsed or the property doesn't apply. Boolean properties return `False` in that case.

### Version availability

| Feature | Minimum LLVM |
|---|---|
| `demangle`, `itanium_demangle`, `microsoft_demangle` | 11 |
| `ItaniumPartialDemangler` | 11 |
| `rust_demangle` | 13 |
| `dlang_demangle`, `non_microsoft_demangle` | 14 |
| `MSDF_NO_VARIABLE_TYPE` | 14 |
| `itanium_demangle(parse_params=)` | 18 |
| `non_microsoft_demangle(parse_params=)` | 18 |
| `get_arm64ec_insertion_point` | 19 |

Functions unavailable for the compiled LLVM version raise `NotImplementedError`.

## Build from source

```bash
# 1. Vendor LLVM Demangle source (downloads from GitHub releases)
python vendor_llvm.py --llvm-version 18

# 2. Build & install
LLVM_VERSION=18 pip install .
```

Supported LLVM versions: 11–21.

## License

- Wrapper code: [0BSD](LICENSE.txt)
- LLVM Demangle source: [Apache 2.0 with LLVM Exception](LLVM_LICENSE.txt)
