# Override the regular excepthook too -- it doesn't change anything either way
# because ipython doesn't use it, but we want to make sure Trio doesn't warn
# about it.
import sys

import _common  # isort: split


def custom_excepthook(*args):
    print("custom running!")
    return sys.__excepthook__(*args)


sys.excepthook = custom_excepthook

import IPython

ip = IPython.get_ipython()


# Set this to some random nonsense
class SomeError(Exception):
    pass


def custom_exc_hook(etype, value, tb, tb_offset=None):
    ip.showtraceback()


ip.set_custom_exc((SomeError,), custom_exc_hook)

from trio._core._multierror import MultiError  # Bypass deprecation warnings.

# The custom excepthook should run, because Trio was polite and didn't
# override it
raise MultiError([ValueError(), KeyError()])
