import getdist.plots as gdplt
import cobaya
from cobaya.yaml import yaml_load_file
from cobaya.run import run
import numpy as np
import os
from scipy import stats
import pandas as pd
from cobaya.yaml import yaml_dump_file
import shutil
import subprocess
import sys

def main():
    # path = sys.argv[1]
    n = int(sys.argv[1])
    path = "C:/EPFL/MA4/code/fake_BAO_data"
    path += "/w0=neg1_wa=0_n"
    path += str(n) + ".txt"

    yaml_file = "cobaya_test_yaml/base_LCDM_input.yaml" #load yaml config file for LCDM
    config = yaml_load_file(yaml_file)

    config['likelihood']['bao.desi_dr2']['measurements_file'] = path
    # print(config['likelihood']['bao.desi_dr2']['measurements_file'])

    config['output'] = f"cobaya_test_runs/base_LCDM/LCDM_fakedata_n{n}"
    config['sampler']['mcmc']['Rminus1_stop'] = 0.01

    new_yaml = f"cobaya_test_yaml/base_LCDM_fakedata_n{n}.yaml"

    # print(config['params'])

    # save config file
    overwrite = True
    run = True

    if os.path.exists(new_yaml) and overwrite:
        shutil.copy(new_yaml, new_yaml + ".bak")
        os.remove(new_yaml)
    
    yaml_dump_file(new_yaml, config)

    if run:
        subprocess.run(
            ["conda", "run", "-n", "cobaya", "cobaya-run", new_yaml],
            check=True
        )

    return

if __name__ == "__main__":
    main()