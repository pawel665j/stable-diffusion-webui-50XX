import requests
import os
import numpy as np
from PIL import ImageDraw
from modules import paths_internal
from packaging.version import parse as parse_version

GREEN = "#0F0"
BLUE = "#00F"
RED = "#F00"


def crop_image(im, settings):
    """ Intelligently crop an image to the subject matter """
