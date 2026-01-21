## Introduction

The main purpose of this exercise is to reproduce the apo-GIST analysis of gist-tutorial: https://github.com/liedllab/gist-tutorial

## Material
available at: https://researchdata.uibk.ac.at//records/4mbrd-67m83

- streptavidin_gist.dat
- streptavidin.nc
- streptavidin.parm7
- streptavidin.rst

## Step 1. extract first and last frame from trajectory
```
python extract_frame.py
```
## Step 2. export free energy grid file
```
python export_dg.py
```
