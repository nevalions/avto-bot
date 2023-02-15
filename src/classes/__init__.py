import sys
import os
from pprint import pprint

sys.path.append(os.path.join(os.getcwd(), 'classes'))
pprint(sys.path)
from .users import User
from .cars import Car
# from helpers.checks import email_is_valid
