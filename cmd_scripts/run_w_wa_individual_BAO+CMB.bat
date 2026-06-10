@echo off
for %%z in (1 2 3 4 5 6 7) do (
    mpiexec -n 4 python .\py_scripts\MPI_general.py config_files\fake_data\like_DESI_CMB\exact_LCDM\z%%z_w_wa.yaml
)