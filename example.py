#%% 
import pypower.api as pypower
from power_case_wrapper import CaseWrapper
#%%
case=CaseWrapper(pypower.case14())
# case=CaseWrapper(pypower.runopf(pypower.case14()))

print(case.gen.PG)
print(case.gen.PG[1:3])
#%%
case.gen.PG=0
print(case.gen.PG)
#%%
case.gen.PG=[1,2,3,4,5]
print(case.gen.PG)
#%%
case.gen.PG[1:3]=[100,50]
print(case.gen.PG)


# %%
