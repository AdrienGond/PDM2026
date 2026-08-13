@echo off
@REM mpiexec -n 4 python .\py_scripts\MPI_general.py C:\EPFL\MA4\code\PDM2026\wwa_pair_chains\fixed\Mirage\fixed_mirage.yaml
mpiexec -n 4 python .\py_scripts\MPI_general.py C:\EPFL\MA4\code\PDM2026\wwa_pair_chains\free\Mirage\free_mirage.yaml
@REM mpiexec -n 4 python .\py_scripts\MPI_general.py C:\EPFL\MA4\code\PDM2026\wwa_pair_chains\fixed\NEC\fixed_nec.yaml
mpiexec -n 4 python .\py_scripts\MPI_general.py C:\EPFL\MA4\code\PDM2026\wwa_pair_chains\free\NEC\free_nec.yaml
@REM mpiexec -n 4 python .\py_scripts\MPI_general.py C:\EPFL\MA4\code\PDM2026\wwa_pair_chains\fixed\Steep\fixed_steep.yaml
mpiexec -n 4 python .\py_scripts\MPI_general.py C:\EPFL\MA4\code\PDM2026\wwa_pair_chains\free\Steep\free_steep.yaml