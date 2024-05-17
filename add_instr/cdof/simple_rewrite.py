import gtirb_rewriting.driver
from gtirb_rewriting import *


class NopPass(Pass):
    """
    Inserts a nop at the start of every function.
    """

    def begin_module(self, module, functions, context):
        context.register_insert(
            AllFunctionsScope(FunctionPosition.ENTRY, BlockPosition.ENTRY),
            Patch.from_function(self.nop_patch),
        )

    @patch_constraints()
    def nop_patch(self, context):
        return "nop"


if __name__ == "__main__":
    # Allow gtirb-rewriting to provide us a command line driver. See
    # docs/Drivers.md for details.
    gtirb_rewriting.driver.main(NopPass)