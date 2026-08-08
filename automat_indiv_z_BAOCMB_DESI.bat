@echo off
for %%z in (1 2 3 4 5 6 7) do (
    mpiexec -n 4 python .\py_scripts\MPI_general.py C:\EPFL\MA4\code\PDM2026\cobaya_chains\individual_z_BAOCMB\DESI_centered\config_files\z%%z.yaml
)