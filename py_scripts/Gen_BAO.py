import numpy as np
import camb
import sys
import os

def expansion_rate(z, Omega_m, Omega_Lambda, w0=-1.0, wa=0): # by default lambdaCDM
    """    
    Parameters:
    z Redshift
    Omega_m Matter density parameter
    Omega_Lambda DE density parameter
    w0 constant equation of state parameter for DE
    wa varying equation of state parameter for DE

    Returns: E(z) = H(z)/H0
    """
    Omega_DE = Omega_Lambda * (1 + z)**(3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))

    Omega_total = Omega_m * (1 + z)**3 + Omega_DE

    E_z = np.sqrt(Omega_total)
    return E_z

def trans_comoving_dist_array(z, par):
    """
    Returns: Transverse comoving distance D_M(z) in units of h^-1 Mpc
    """
    c = 299792.458  # km/s
    from scipy.integrate import quad

    Omega_m, w0, wa = par
    Omega_Lambda = 1 - Omega_m  # Assuming a flat universe

    def integrand(z_prime):
        return 1 / expansion_rate(z_prime, Omega_m, Omega_Lambda, w0, wa)

    # check if z is a scalar or an array
    if np.isscalar(z):
        integral, _ = quad(integrand, 0, z)
        return c/100 * integral
    
    integral1, _ = quad(integrand, 0, z[0])
    integrals = []
    for i in range(len(z)):
        part_int = quad(integrand, z[i-1], z[i])[0] if i > 0 else integral1
        integrals.append(part_int + (integrals[i-1] if i > 0 else 0))
    return [c/100 * el for el in integrals]

def Hubble_dist(z, par):# Omega_m, Omega_Lambda, w0=-1.0, wa=0):
    """
    Returns: Hubble distance D_H(z) in units of h^-1 Mpc
    """
    Omega_m, w0, wa = par
    Omega_Lambda = 1 - Omega_m  # Assuming a flat universe
    c = 299792.458  # km/s
    return c/100 / expansion_rate(z, Omega_m, Omega_Lambda, w0, wa)

# def sound_horizon_approx(par):
#     '''
#     Need par = H0, Omega_m, Omega_b; returns h*r_d with an approximation formula Eq. 3.4 from 2212.04522
#     '''
#     a = -0.23
#     b = -0.1
#     c = -0.13
#     Omega_m, H0 = par
#     Omega_b = 0.02236/(H0/100)**2
#     Neff = 3.04
#     h = H0/100
#     return h * 147.05 * ((Omega_m * h**2)/ 0.1432 )**a * ((Omega_b * h**2)/ 0.02236 )**b * (Neff/ 3.04)**c

def sound_horizon(par):
    '''
    Need par = H0, Omega_m, Omega_b; returns h*r_d
    '''
    H0, Om, Ob, w0, wa = par
    h = H0/100
    params = camb.CAMBparams()
    params.set_cosmology(H0=H0, ombh2=(Ob*h**2), omch2=((Om-Ob)*h**2), mnu=0.06, omk=0, tau=0.06)
    params.WantTransfer = False
    params.WantTensors = False
    params.WantDerivedParameters  = False
    params.Want_cl_2D_array = False
    params.Want_CMB_lensing = False
    params.DoLensing = False
    params.want_zdrag  = False
    params.want_zstar  = False

    params.set_dark_energy(w=w0, wa=wa, dark_energy_model='ppf')
    results = camb.get_results(params)

    return results.sound_horizon(1060) * h

def compute_DV(z, par):
    '''
    Returns D_V(z) in units of h^-1 Mpc, D_V = (z * D_M^2(z) * D_H(z))^(1/3)
    '''
    DM = trans_comoving_dist_array(z, par)
    DH = Hubble_dist(z, par)
    return (z * DM**2 * DH)**(1/3)

def get_data_cov_mat():
    path_data = r"C:\EPFL\MA4\code\COBAYA_packages\data\bao_data\desi_bao_dr2"
    data_filename = "desi_gaussian_bao_ALL_GCcomb_mean.txt"

    data = np.loadtxt(path_data +"\\"+ data_filename, dtype=str)

    cov_file = data_filename.replace("mean", "cov")
    cov_mat = np.loadtxt(path_data +"\\"+ cov_file) # mat with first term 0, 0 being sig**2 for DV/rd, then 2x2 blocks for the 6 pairs of DM/rd and DH/rd
                                            # beware of the last one that can actually be inversed (DH/rs first) following the order in data file

    return data, cov_mat

def save_file(fake_data, w0, wa, n, add_random): # download the data in a txt file
    pres = None # precision for w0 wa
    spec = f"_n{n}" # specifier 

    filename = f''

    if w0 < 0:
        filename += f'w0=neg{-round(w0, pres)}_'
    else:
        filename += f'w0={round(w0, pres)}_'

    if wa < 0:
        filename += f'wa=neg{-round(wa, pres)}_'
    else:    
        filename += f'wa={round(wa, pres)}'

    if not add_random:
        filename += '_not_random'
    filename += spec
    filename += '.txt'

    folder = "./fake_BAO_data/"
    filename = folder + filename

    print("Saving fake data in file:", filename)
    if os.path.exists(filename):
        print("File already exists")
        # n += 1
        # save_file(fake_data, w0, wa, n)
    else:
        np.savetxt(filename, fake_data, fmt="%s")


############################ Main function ############################

def main():
    Omega_m, H0, w0, wa, n, add_random = sys.argv[1:]
    Omega_m = float(Omega_m)
    H0 = float(H0)
    w0 = float(w0)
    wa = float(wa)
    n = int(n)
    if add_random == 'False':
        add_random = False
    elif add_random == 'True':
        add_random ='True'
    else:
        print("Error: add_random should be either 'True' or 'False'")
        return

    Ob = 0.02236/(H0/100)**2

    data_typ = ['DH_over_rs', 'DM_over_rs', 'DV_over_rs']
    real_data, cov_mat = get_data_cov_mat()

    redshifts = real_data[:, 0]
    redshifts = set(redshifts)
    redshifts = list(redshifts)
    redshifts = np.sort(redshifts)

    param_ = [Omega_m, w0, wa]

    z = [float(e) for e in redshifts[1:]]
    z = np.array(z)

    rd = sound_horizon([H0, Omega_m, Ob, w0, wa])

    DM_rd = [e/rd for e in trans_comoving_dist_array(z, param_)] # let's take same redshift as DESI data for now
    DH_rd = [Hubble_dist(zi, param_)/rd for zi in z]
    DV_rd = compute_DV(float(redshifts[0]), param_)/rd

    fake_data = []
    for i in range(len(z)):
        line = [z[i], DM_rd[i], data_typ[1]]
        fake_data.append(line)
        line = [z[i], DH_rd[i], data_typ[0]]
        fake_data.append(line)

    line = [float(redshifts[0]), DV_rd, data_typ[2]]
    fake_data.insert(0, line)

    fake_data = np.array(fake_data)

    add_random = False

    if add_random:
        for i in range(len(fake_data)):
            if i == 0:
                # print("DV/rd:", fake_data[i])
                rand = np.random.normal(float(fake_data[i][1]), np.sqrt(cov_mat[0, 0]))
                # print("Randomly drawn value for DV/rd at z =", fake_data[i][0], ":\n", rand)
                fake_data[i][1] = rand
            elif i%2 == 0:
                cov = [[cov_mat[i-1, i-1], cov_mat[i-1, i]], [cov_mat[i, i-1], cov_mat[i, i]]]
                rand = np.random.multivariate_normal([float(fake_data[i-1][1]), float(fake_data[i][1])], cov)
                fake_data[i-1][1] = rand[0]
                fake_data[i][1] = rand[1]

    save_file(fake_data, w0, wa, n, add_random)

    # print("Redshifts:", redshifts, '\n', "Data types:", data_typ, '\n', "Covariance matrix shape:", cov_mat.shape)
    # print("data", real_data)

if __name__ == "__main__":
    main()