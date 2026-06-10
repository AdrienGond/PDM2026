from cobaya import run
from cobaya.log import LoggedError
from cobaya.yaml import yaml_load_file
from mpi4py import MPI

def main():
    want_force = True # Set to True to force the run even if output already exists

    yaml_file = "cobaya_test_yaml/base_LCDM_input.yaml" #load yaml config file for LCDM
    path = "C:/EPFL/MA4/code/fake_BAO_data/LCDM"
    path += "/w0=neg1_wa=0_not_random.txt"    
    config = yaml_load_file(yaml_file)

    config['likelihood']['bao.desi_dr2']['measurements_file'] = path
    print(config['likelihood']['bao.desi_dr2']['measurements_file'])

    config['output'] = "cobaya_test_runs/base_LCDM/LCDM_fakedata_not_random_MPItest16"
    config['sampler']['mcmc']['Rminus1_stop'] = 0.001

    config['sampler']['mcmc']['covmat'] = "cobaya_test_runs/base_LCDM/LCDM_fakedata_not_random_MPItest8.covmat"

    config['params']['omch2']['ref'] = 0.125 # Om=0.3, h=0.7 then Oc = Om-Ob = 0.3-0.045 = 0.255, so Oc*h^2 = 0.25*0.7^2 = 0.125

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    print(f"Rank {rank} running")

    # print("File exists:", os.path.exists(path))
    # print("Absolute path:", os.path.abspath(path))

    success = False
    try:
        upd_info, mcmc = run(config, force=want_force)
        success = True
    except LoggedError as err:
        print(rank, err)
        pass

    # Did it work? (e.g. did not get stuck)
    success = all(comm.allgather(success))

    if not success and rank == 0:
        print("Sampling failed!")

if __name__ == "__main__":    
    main()