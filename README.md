# gisttools
Post-processing of data generated by the GIST (Grid Inhomogeneous Solvation Theory) action in cpptraj

Grid Inhomogeneous Solvation Theory (GIST) is a method first devised by Gilson and coworkers, that calculates thermodynamic properties of hydration on a 3-dimensional grid, based on a Molecular Dynamics (MD) simulation of a restrained solute molecule in explicit solvent. GIST is implemented in the cpptraj program (AmberTools). The output of GIST is a table of thermodynamic quantities (e.g. enthalpic and entropic contributions to hydration) for each grid voxel.

This Python module is a collection of tools that are intended for easy handling and further post-processing of GIST output files. The core functionality has been repeatedly used in scientific work at the university of Innsbruck. However, the module is still quickly evolving and the user interface can (and will) change without warning! Also, notice that more specialized use cases might not have been tested.

## Overview of functionality
* Load GIST output files in table format (using pandas) or .dx format (using gridDataFormats)
* Automatically subtract reference values for the solvent-solvent interaction enrgy and compute derived quantities such as the free energy.
* Project free energy contributions to atoms in a .pdb file. Two different methods (mean: compute the average in a sphere around each atom; nearest: assign every voxel within a certain distance of the solute to exactly one atom) are supported. Furthermore, a weighting of the voxel contributions based on the distance to an atom can be used.
* Integrate free energy contributions within a certain distance of the solute.
* Compute "rdfs", i.e., summations of the free energy contributions binned by the distance to the nearest atom. The resulting rdfs are reported per atom.
* The grid functionality can be used independently of the GIST post-processing. This can be quite handy. For instance, one can combine the grid functionality with a marching cubes algorithm (e.g., from skimage) to compute triangulated SASAs (solvent accessible surface areas).

## Installation
This module depends on the following packages:
* mdtraj
* numpy
* scipy
* pandas
* numba

Optional dependencies (only for some functionality):
* nglview (for previewing datasets)
* gridDataFormats (for loading .dx files)

You should be able to install gisttools in a local environment using `pip install .`. gisttools has been tested mainly on Pyton 3.7, but all versions >= 3.6 *should* work, so If you experience errors with any of those versions, feel free to contact me.
<h2>Mean energy per water and number density for various water models<sup>1</sup></h2>
<img src="https://github.com/gkxiao/gisttools/blob/master/mean-energy-per-water.png"  alt="Mean energy per water">
<p>(1) Ramsey, S.; Nguyen, C.; Salomon-Ferrer, R.; Walker, R. C.; Gilson, M. K.; Kurtzman, T. Solvation Thermodynamic Mapping of Molecular Surfaces in AmberTools: GIST. J. Comput. Chem. 2016, 37 (21), 2029–2037. https://doi.org/10.1002/jcc.24417.</p>
<h2>Examples</h2>
<h3>Export g_O as a dx file</h3>
<pre line="1" lang="python">
#!/usr/bin/env python3
import gisttools.gist as gist
from io import StringIO
from textwrap import dedent
import numpy as np
from numpy.testing import assert_array_equal, assert_allclose
import pandas as pd
import pytest

example1 = gist.load_gist_file('example/benzene/out.dat', eww_ref=-9.533)
example1.save_dx('g_O','example/benzene/g_O.dx')
</pre>
<h3>show &Delta;G at a coordination point</h3>
<img src="https://github.com/gkxiao/gisttools/blob/master/example/benzene/gist.png">
<pre line="1" lang="python">
>>> from gridData import Grid
>>> g =  Grid("local_dG.dx")
>>> g.interpolated(77.363,25.254,44.668)
array([0.73119007])
>>> g.interpolated(77.882,28.203,40.039)
array([-0.23544697])
>>> g.interpolated(77.46,24.744,40.978)
array([0.00361614])
>>>
</pre>
<h3 id="ph4">Score a pharmacophore feature</h3>
<img src="https://github.com/gkxiao/gisttools/blob/master/example/benzene/gist_feature_score.png" width="400" height="363">
<pre line="1" lang="python">
>>> from gridData import Grid
>>> dG =  Grid("G:/work/3oot_gist/Local_unhappy_water.dx")
>>> # PDB 3OOT xtal-ligand O33 (oxygen of the HBD) 
>>> dG_O33 = dG.interpolated(-8.43,-28.11,-4.07)
>>> print('dG =',dG_O33,'kcal/mol')
dG = [1.52537911] kcal/mol
>>>
</pre>
<ol>
   <li>Hu, B.; Lill, M. A. Protein Pharmacophore Selection Using Hydration-Site Analysis. J. Chem. Inf. Model. 2012, 52 (4), 1046–1060. https://doi.org/10.1021/ci200620h.</li>
   <li>Yoshida, S.; Uehara, S.; Kondo, N.; Takahashi, Y.; Yamamoto, S.; Kameda, A.; Kawagoe, S.; Inoue, N.; Yamada, M.; Yoshimura, N.; et al. Peptide-to-Small Molecule: A Pharmacophore-Guided Small Molecule Lead Generation Strategy from High-Affinity Macrocyclic Peptides. 2022. https://doi.org/10.1021/acs.jmedchem.2c00919.</li>
  <li>Jung, S. W.; Kim, M.; Ramsey, S.; Kurtzman, T.; Cho, A. E. Water Pharmacophore: Designing Ligands Using Molecular Dynamics Simulations with Water. Sci. Rep. 2018, 8 (1), 10400. https://doi.org/10.1038/s41598-018-28546-z.</li>
</ol>
