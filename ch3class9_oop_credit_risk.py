import sys
import numpy as np
from numpy import linalg as lg
import pandas as pd

path_yfrac = 'C://Users//Andrey.Zakharov//PycharmProjects//training//class4'
sys.path.append(path_yfrac)
from yearfrac import yearfrac

path = 'C://Users//Andrey.Zakharov//PycharmProjects//training//class9'
transition_tab = pd.read_excel(path + '//ratings.xlsx', 'ttc')
transition_tab.set_index('From/To:', inplace=True, drop=True)

class Borrower(object):
    def __init__(self, segment, termination_date, dpd, exposure, rating):
        self.segment = segment
        self.termination_date = termination_date
        self.dpd = dpd
        self.exposure = exposure
        self.rating = rating
        if self.dpd < 30:
            self.bucket = 1
        elif self.dpd >= 30 and self.dpd < 90:
            self.bucket = 2
        else:
            self.bucket = 3
    def CalculatePD(self, report_date, pd_df):
        cols = pd_df.columns
        ind = pd_df.index
        self.tenor = yearfrac(report_date, self.termination_date, date_format='%m/%d/%Y')
        if self.bucket == 1:
            self.PD = np.interp(self.tenor, [0.0, 1.0], [0.0, pd_df.loc[self.rating]['D']]) / 100
        elif self.bucket == 2:
            pd_mat = np.array(pd_df, dtype=float) / 100
            pd_lt_lower = lg.matrix_power(pd_mat, int(np.floor(self.tenor)))
            pd_df_lower = pd.DataFrame(data=pd_lt_lower, index=ind, columns=cols)
            pd_lt_upper = lg.matrix_power(pd_mat, int(np.ceil(self.tenor)))
            pd_df_upper = pd.DataFrame(data=pd_lt_upper, index=ind, columns=cols)
            PD_lower = pd_df_lower.loc[self.rating]['D']
            PD_upper = pd_df_upper.loc[self.rating]['D']
            self.PD = np.interp(self.tenor, [np.floor(self.tenor), np.ceil(self.tenor)], [PD_lower, PD_upper])
        else:
            self.PD = 1.0
        return self.PD
    def CalculateLGD(self, lgd=0.7):
        self.lgd = lgd
        return self.lgd
    def CalculateProvision(self):
        return self.exposure * self.lgd * self.PD

corp1 = Borrower(segment='corporate', termination_date='01/01/2020', dpd=0,
                 exposure=5000, rating='Caa1')
print(corp1.CalculatePD('12/21/2017', transition_tab))
print(corp1.CalculateLGD(0.8))
print(corp1.CalculateProvision())

corp2 = Borrower(segment='corporate', termination_date='01/01/2020', dpd=180,
                 exposure=5000, rating='Caa1')
print(corp2.CalculatePD('12/21/2017', transition_tab))
print(corp2.CalculateLGD())
print(corp2.CalculateProvision())

corp3 = Borrower(segment='corporate', termination_date='01/01/2020', dpd=50,
                 exposure=5000, rating='Caa1')
print(corp3.CalculatePD('12/21/2017', transition_tab))

class DefaultedBorrower(Borrower):
    def __init__(self, segment, termination_date, dpd, exposure, rating, default_date):
        self.default_date = default_date
        super().__init__(segment=segment, termination_date=termination_date, dpd=dpd,
                         exposure=exposure, rating=rating)
        self.bucket = 3
        self.PD = 1
    def CalculateLGD(self, report_date, lgd=0.7, recovery_horizon=2.0):
        self.time_default = yearfrac(self.default_date, report_date, date_format='%m/%d/%Y')
        lgd_lower = lgd
        lgd_upper = 1.0
        self.lgd = np.interp(self.time_default, [0.0, recovery_horizon], [lgd_lower, lgd_upper])
        return self.lgd


dcorp1 = DefaultedBorrower(segment='corporate', termination_date='1/1/2022', dpd=95,
                           exposure=10000, rating='Ca1', default_date='6/20/2017')
print(dcorp1.CalculateLGD('12/22/2017'))
print(dcorp1.CalculateProvision())
