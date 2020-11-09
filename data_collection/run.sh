#!/bin/bash

current_dir=$PWD
cd /mnt/data_collection
python workflow/execute.py
cd $current_dir
