import sys
import code
import inspect
import keyword
import pprint
from contextlib import contextmanager

# ========================================================================
# Python Subprocess Manager
# ========================================================================


class PiiInterpreter(code.InteractiveConsole):
    def __init__(self):
        code.InteractiveConsole.__init__(self)

    def get_local(self, local_key):
        if local_key in self.locals.keys():
            return self.locals[local_key]
        else:
            return None

    def get_local_dir(self, local_key):
        local_dir = []
        # NEED TO HANDLE MODULES WITH MORE THAN ONE LEVEL, can use getattr(moduleobj, "module path")
        # to get the latest module object
        local_root = local_key.split(".")[0]
        local_dirname = ".".join(local_key.split(".")[1:])
        local_obj = self.get_local(local_root)
        if local_obj:
            if local_dirname:
                try:
                    obj_members = inspect.getmembers(self.recursive_getattr(local_obj,local_dirname))
                except AttributeError:
                    obj_members = []
            else:
                obj_members = inspect.getmembers(local_obj)
            local_dir = [k for k, v in obj_members]
        return local_dir

    def get_object_docstring(self, local_key):
        doc_string = ""
        local_root = local_key.split(".")[0]
        local_dirname = ".".join(local_key.split(".")[1:])
        local_obj = self.get_local(local_root)
        if local_obj:
            if local_dirname:
                try:
                    doc_string = self.recursive_getattr(local_obj,local_dirname).__doc__
                except AttributeError:
                    pass
            else:
                doc_string = local_obj.__doc__
                if not doc_string: doc_string = ""
        return doc_string

    def recursive_getattr(self, rootobj, modulepath):
        modules = modulepath.split(".")
        if len(modules) == 1:
            return getattr(rootobj,modules[0])
        else:
            new_root = getattr(rootobj, modules[0])
            new_path = ".".join(modules[1:])
            return self.recursive_getattr(new_root, new_path)

    def get_local_list(self):
        locals_list = list(self.locals.keys())
        keyword_list = keyword.kwlist
        final_list = locals_list + keyword_list
        final_list.sort()
        return final_list


# Function to enable pretty print output
def piidisplayhook(value):
    if value is not None:
        pprint.pprint(value)


@contextmanager
def redirect_stdout_and_stderr(new_out):
    # Replace stderr
    stderr_old = sys.stderr
    sys.stderr = new_out
    #  Now replace stdout
    stdout_old = sys.stdout
    sys.stdout = new_out
    # Replace sys.displayhook as well
    # for pprinting
    displayhook_old = sys.displayhook
    sys.displayhook = piidisplayhook
    # now execute any code
    try:
        yield new_out
    finally:
        # Finally reset stdout and err
        sys.stderr = stderr_old
        sys.stdout = stdout_old
        sys.displayhook = displayhook_old
