# Import the GISTTOOLS package
import gisttools
# Import necessary libraries
from gisttools.gist import load_gist_file
import gisttools as gt  # Optional, for alias use

# Step 1: Load GIST output file and solute structure
# Assume gist.dat is the GIST output file, and solute-centered.pdb is the solute structure file
# Set the reference energy eww_ref (select based on solvent model, e.g., -9.5398 for TIP3P water model)
gist = load_gist_file('streptavidin_gist.dat', struct='streptavidin_first.pdb', eww_ref=-9.5398)

# Step 2: Verify correct data loading (optional)
print(f"Number of frames: {gist.n_frames}")
print(f"Reference density: {gist.rho0}")
# Ensure the A_dens column is automatically calculated (GISTTOOLS derives A_dens from Eww, Esw, and entropy columns)
# The A_dens column represents the free energy density (ΔA_solv_dens) of each voxel, in units of kcal/mol/Å³

# Step 3: Optional step - Handle entropy reference (adjustment may be needed if free energy convergence is poor)
# Section 4.4.4 of the tutoral mentions that entropy may diverge due to sampling bias and can be corrected by referencing a reference value
def reference_entropy(gf):
    if 'dTSsix_unref_norm' not in gf.data.columns:
        gf['dTSsix_unref_norm'] = gf['dTSsix_norm']
        gf['dTSsix_unref_dens'] = gf['dTSsix_dens']
    refval = gf.detect_reference_value('dTSsix_unref_dens')
    gf['dTSsix_norm'] = gf.get_referenced('dTSsix_unref_norm', refval)
    gf['dTSsix_dens'] = gf.get_referenced('dTSsix_unref_dens', refval)

# Apply entropy reference correction (if needed)
reference_entropy(gist)

# Step 4: Export the A_dens column as a DX file
# Use the save_dx method, where the first parameter is the column name ('A_dens') and the second is the output file name
gist.save_dx('A_dens', 'deltaG_density.dx')

print("DX file has been exported as deltaG_density.dx")
