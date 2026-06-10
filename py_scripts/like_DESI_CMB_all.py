from cobaya.likelihoods.bao.desi_dr2.desi_bao_all import desi_bao_all 
# beware of blabla.desi_bao_all import desi_bao_all, not blabla.desi_bao_cmb_all import desi_bao_cmb_all, 
# this is due to the fact that the file (module) is called the same as the class in it.
import numpy as np

class desi_bao_cmb_all(desi_bao_all):
    """
    Desi bao likelihood for all tracers with CMB priors as given in DESI DR2 paper 2503.14738v2 (in Appendix A)
    """
    
    # order [theta_star, omega_b, omega_bc]
    cmb_prior_mean: list    = [0.01041, 0.02223, 0.14208] # from Appendix A DESI DR2 paper
    cmb_prior_cov: list = [
        [0.006621e-9, 0.12444e-9,  -1.1929e-9 ],
        [0.12444e-9,  21.344e-9,   -94.001e-9 ],
        [-1.1929e-9,  -94.001e-9,  1488.4e-9  ]
    ]

    def initialize(self):
        super().initialize()
        self._cmb_mean = np.array(self.cmb_prior_mean)
        cov = np.array(self.cmb_prior_cov)
        self._cmb_cov_inv = np.linalg.inv(cov)

    def get_requirements(self):
        reqs = super().get_requirements()
        reqs["thetastar"] = None
        return reqs

    def logp(self, **params_values):
        logp_bao = super().logp(**params_values)

        if not np.isfinite(logp_bao): # returns driectly -inf if BAO likelihood is already -inf
            return logp_bao
        
        ombh2       = self.provider.get_param("ombh2")
        omch2       = self.provider.get_param("omch2")
        omega_bc    = ombh2 + omch2
        theta_star  = self.provider.get_param("thetastar")
        
        delta_cmb = np.array([theta_star, ombh2, omega_bc]) - self._cmb_mean
        logp_cmb = -0.5 * delta_cmb @ self._cmb_cov_inv @ delta_cmb

        return logp_bao + logp_cmb
        # return logp_bao