@echo off
mpiexec -n 4 python .\py_scripts\MPI_general.py C:\EPFL\MA4\code\PDM2026\cobaya_chains\half_tracers\1sthalf\1st_half.yaml
mpiexec -n 4 python .\py_scripts\MPI_general.py C:\EPFL\MA4\code\PDM2026\cobaya_chains\half_tracers\2ndhalf\2nd_half.yaml