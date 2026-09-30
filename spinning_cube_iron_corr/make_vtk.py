#!/usr/bin/env python3
# usage: python3 make_vtk.py data_basalt
# braucht: pip install pyvista h5py
import sys, glob, os
import numpy as np, h5py, pyvista as pv

d = sys.argv[1] if len(sys.argv) > 1 else "."
out = os.path.join(d, "data_basalt_corr_vtk")
os.makedirs(out, exist_ok=True)
entries = []

for path in sorted(glob.glob(os.path.join(d, "data_basalt_corr/*.h5"))):
    base = os.path.splitext(os.path.basename(path))[0]
    with h5py.File(path, "r") as f:
        x = np.asarray(f["x"], dtype=np.float64)
        n = x.shape[0]
        if x.shape[1] == 2:
            x = np.column_stack([x, np.zeros(n)])
        mesh = pv.PolyData(x)          # erzeugt automatisch Vertex-Zellen
        for name, ds in f.items():
            if name in ("x", "time") or not isinstance(ds, h5py.Dataset):
                continue
            if ds.shape[0] == n:
                mesh.point_data[name] = np.asarray(ds)
        t = float(f["time"][0])
    fn = base + ".vtp"
    mesh.save(os.path.join(out, fn))
    entries.append((t, fn))

with open(os.path.join(out, "series.pvd"), "w") as fh:
    fh.write('<?xml version="1.0"?>\n<VTKFile type="Collection" version="0.1">\n<Collection>\n')
    for t, fn in entries:
        fh.write(f'<DataSet timestep="{t}" file="{fn}"/>\n')
    fh.write('</Collection>\n</VTKFile>\n')
print(f"{len(entries)} Dateien -> {out}/series.pvd")