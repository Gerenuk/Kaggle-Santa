import logging
import os

from filegetter import FileGetter


join = os.path.join
project_dir = os.path.abspath(join(__file__, "../.."))

data_dir = join(project_dir, "no-vc/data")

data = FileGetter(data_dir)
results = FileGetter(project_dir, "results")
temp = FileGetter(project_dir, "temp")

logging.basicConfig()
