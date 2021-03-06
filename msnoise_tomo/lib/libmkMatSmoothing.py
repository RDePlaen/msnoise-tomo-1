import os
from future.utils import native_str
import ctypes
import numpy as np
from obspy.core.util.libnames import cleanse_pymodule_filename, _get_lib_name
import platform
lib = "mkMatSmoothing"

libname = _get_lib_name(lib, add_extension_suffix=True)
libname = os.path.join(os.path.dirname(__file__), libname)
print("Smoothing lib name:", libname)

libsmooth = ctypes.CDLL(str(libname))

LP_c_char = ctypes.POINTER(ctypes.c_char)
LP_LP_c_char = ctypes.POINTER(LP_c_char)

libsmooth.main.argtypes = [ctypes.c_int, # argc
                           LP_LP_c_char] # argv]
libsmooth.main.restype = ctypes.c_int


def smooth(lcorr, gridfile):

    args = ["placeholder",
            lcorr,
            gridfile]
    argc = len(args)
    argv = (LP_c_char * (argc + 1))()
    for i, arg in enumerate(args):
        enc_arg = arg.encode('utf-8')
        argv[i] = ctypes.create_string_buffer(enc_arg)

    return libsmooth.main(argc, argv)