#!/bin/bash
tree -I *.pyc -I __A_GIS__ -I __init__.py -I __pycache__ -f -I tests $*

