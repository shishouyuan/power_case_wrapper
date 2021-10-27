# %% 
import pypower.api as pypower
from power_case_wrapper import CaseWrapper

case=CaseWrapper(pypower.case14())
print(case.gen.GEN_BUS)

# %%
