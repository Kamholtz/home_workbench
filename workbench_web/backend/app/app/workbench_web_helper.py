import os
from typing import Optional

from pyvisa.errors import VisaIOError

from home_workbench.spd3303c import SPD3303C


class WorkbenchWebHelper:
    @staticmethod
    def get_full_path_from_cwd(path):
        root = os.path.dirname(os.path.realpath(__file__))
        return f"{root}\\{path}"

    @staticmethod
    def get_path_relative_to_this_module(path):
        return f"workbench_web/{path}"

    @staticmethod
    def get_power_supply() -> Optional[SPD3303C]:
        ps = None
        try:
            ps = SPD3303C()
        except VisaIOError:
            ps = None

        return ps
