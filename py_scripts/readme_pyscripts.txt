MCMC_cobaya.py :
    obsolete now (see MPI version below), used to run MCMC on specific generated data. 
    Need to change the source code to find the right path of the fake data considered. 
    Pass n as argument when executing to specify n-ieme mcmc run.

MPI_implementation.py :
    new version of the MCMC code, using MPI to run 4 chains in parallel. 
    Need to change the source code to find the right path of the fake data considered. 
    No argument to be passed, need to change the code to make change to config file.
    Used to test MPI implementation and used to investigate convergence.
    Execution : mpiexec -n 4 python MPI_implementation.py (need to activate the right env before)

MPI_general.py :
    more general version of the MPI code, can be used for any config file and any number of chains. 
    The path to the config file must be given as argument when executing.
    Execution : mpiexec -n 4 python MPI_general.py path\to\config.yaml (need to activate the right env before)