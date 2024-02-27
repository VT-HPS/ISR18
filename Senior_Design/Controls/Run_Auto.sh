#!/bin/bash

data=$(python3 Create_bullshit.py)

python3 Auto_Code_1.py --data "${data}"
