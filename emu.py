"""
Reads EMu data from csv into a DataFrame

Meant to import vernaculars, i.e.:
    >>> from emu import emu
"""


import pandas as pd
import os

emu_path = os.getenv('EMU_PATH')
emu = pd.read_csv(
    emu_path,
    keep_default_na=False,
    engine='pyarrow',
    on_bad_lines='skip'
)

