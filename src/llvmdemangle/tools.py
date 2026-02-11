import click
from llvmdemangle.demangle import llvm_demangle

@click.command()
@click.argument("mangled_name", nargs=1)
def demangle(mangled_name):
    print(llvm_demangle(mangled_name))
