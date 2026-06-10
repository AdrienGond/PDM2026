@echo off
for %%z in (2 3 4 5 6 7) do (
    mpiexec -n 4 python py_scripts\MPI_general.py config_files\DESI_data\base_w_wa\all_but_one_z\all_but_z%%z.yaml
)