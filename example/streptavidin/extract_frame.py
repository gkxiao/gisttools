import MDAnalysis as mda
from MDAnalysis.coordinates.PDB import PDBWriter

# Load topology and trajectory files
u = mda.Universe(
    "streptavidin.parm7",  # Topology file
    "streptavidin.nc"      # Trajectory file
)

# ---------------------- Extract the first frame ----------------------
# Navigate to the first frame (index 0)
u.trajectory[0]
# Write the first frame to a PDB file
with PDBWriter("streptavidin_first.pdb") as writer:
    writer.write(u.atoms)
print("The first frame has been saved as streptavidin_first.pdb")

# ---------------------- Extract the last frame ----------------------
# Navigate to the last frame (index = total number of frames - 1)
last_frame_idx = len(u.trajectory) - 1
u.trajectory[last_frame_idx]
# Write the last frame to a PDB file
with PDBWriter("streptavidin_last.pdb") as writer:
    writer.write(u.atoms)
print(f"The last frame (Frame {last_frame_idx+1}) has been saved as streptavidin_last.pdb")
