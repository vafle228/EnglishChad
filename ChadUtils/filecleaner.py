import os
from ChadUtils.constants import TEMP_ROOT


def deleteFile(file, file_name):
    file.close()
    os.remove(TEMP_ROOT.format(file_name))