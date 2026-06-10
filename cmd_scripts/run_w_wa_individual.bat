@echo off
for %%z in (2) do (
    mpiexec -n 4 python MPI_general.py config_files/DESI_data/w_wa_individual/z%%z.yaml
)