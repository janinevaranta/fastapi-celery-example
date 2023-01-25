import os
from pathlib import Path
from typing import Union

def cleanup(filenames: list[Union[str, Path]]) -> None:
  """Cleanup for files that are saved only temporarely."""
  for file in filenames:
    os.remove(file)