from typing import Any, Dict, List

class CaseWrapper:
    '''
    A wrapper for pypower case data. 
    Easy way to access and modify case parameters.

    Shouyuan Shi @ South China University of Technology
    Created in 2021/05/28
    '''

    def __init__(self, case_value: Dict[str, Any]) -> None:
        self.case_value = case_value
        self.__bus = Bus(self)
        self.__gen = Gen(self)
        self.__branch = Branch(self)

    @property
    def case_value(self):
        return self.__case_value

    @case_value.setter
    def case_value(self, value):
        if value['version'] != '2':
            raise ValueError("Value version error, only for version 2.")
        # for cls in [Bus, Gen, Branch]:
        #     if value[cls._name].shape[1] != len(cls.members):
        #         raise ValueError(cls._name + " value size error.")
        self.__case_value = value

    @property
    def version(self):
        return self.case_value['version']

    @property
    def baseMVA(self):
        return self.case_value['baseMVA']

    @baseMVA.setter
    def baseMVA(self, val):
        self.case_value['baseMVA'] = val

    @property
    def gen(self):
        return self.__gen

    @property
    def bus(self):
        return self.__bus

    @property
    def branch(self):
        return self.__branch


def __create_property_fun(name, index):
    def get(s):
        if index<s.case.case_value[name].shape[1]:
            return s.case.case_value[name][:, index]
        else:
            return None
    def set(s, val):
        if index<s.case.case_value[name].shape[1]:
            s.case.case_value[name][:, index] = val
    return get, set


def dec(cls):
    if "_name" not in cls.__dict__:
        raise ValueError(str(cls)+" dose not have field '_name'.")
    elif "members" not in cls.__dict__:
        raise ValueError(str(cls)+" dose not have field 'members'.")
    for i, (member, doc) in enumerate(cls.members.items()):
        get, set = __create_property_fun(cls._name, i)
        setattr(cls, member, property(fget=get, fset=set, doc=doc))
    return cls


@dec
class Bus:
    def __init__(self, case) -> None:
        self.case = case

    _name = 'bus'
    members = {'BUS_I': 'bus number (positive integer)',
               'BUS_TYPE': 'bus type (1 = PQ, 2 = PV, 3 = ref, 4 = isolated)',
               'PD': 'real power demand (MW)',
               'QD': 'reactive power demand (MVAr)',
               'GS': 'shunt conductance (MW demanded at V = 1.0 p.u.)',
               'BS': 'shunt susceptance (MVAr injected at V = 1.0 p.u.)',
               'BUS AREA': 'area number (positive integer)',
               'VM': 'voltage magnitude (p.u.)',
               'VA': 'voltage angle (degrees)',
               'BASE_KV': 'base voltage (kV)',
               'ZONE': 'loss zone (positive integer)',
               'VMAX': 'maximum voltage magnitude (p.u.)',
               'VMIN': 'minimum voltage magnitude (p.u.)',
               'LAM_P': 'Lagrange multiplier on real power mismatch (u/MW)',
               'LAM_Q': 'Lagrange multiplier on reactive power mismatch (u/MVAr)',
               'MU_VMAX': 'Kuhn-Tucker multiplier on upper voltage limit (u/p.u.)',
               'MU_VMIN': 'Kuhn-Tucker multiplier on lower voltage limit (u/p.u.)',
               }

    @property
    def count(self):
        return self.case.case_value[self._name].shape[0]
   

@dec
class Gen:
    def __init__(self, case) -> None:
        self.case = case

    _name = 'gen'
    _costName = "gencost"

    members = {
        'GEN_BUS': 'bus number',
        'PG': 'real power output (MW)',
        'QG': 'reactive power output (MVAr)',
        'QMAX': 'maximum reactive power output (MVAr)',
        'QMIN': 'minimum reactive power output (MVAr)',
        'VG': 'voltage magnitude setpoint (p.u.)',
        'MBASE': 'total MVA base of machine, defaults to baseMVA',
        'GEN_STATUS': 'machine status, > 0 = machine in-service, ≤ 0 = machine out-of-service',
        'PMAX': 'maximum real power output (MW)',
        'PMIN': 'minimum real power output (MW)',
        'PC1': 'lower real power output of PQ capability curve (MW)',
        'PC2': 'upper real power output of PQ capability curve (MW)',
        'QC1MIN': 'minimum reactive power output at PC1 (MVAr)',
        'QC1MAX': 'maximum reactive power output at PC1 (MVAr)',
        'QC2MIN': 'minimum reactive power output at PC2 (MVAr)',
        'QC2MAX': 'maximum reactive power output at PC2 (MVAr)',
        'RAMP_AGC': 'ramp rate for load following/AGC (MW/min)',
        'RAMP_10': 'ramp rate for 10 minute reserves (MW)',
        'RAMP_30': 'ramp rate for 30 minute reserves (MW)',
        'RAMP_Q': 'ramp rate for reactive power (2 sec timescale) (MVAr/min)',
        'APF': 'area participation factor',
        'MU_PMAX': 'Kuhn-Tucker multiplier on upper Pg limit (u/MW)',
        'MU_PMIN': 'Kuhn-Tucker multiplier on lower Pg limit (u/MW)',
        'MU_QMAX': 'Kuhn-Tucker multiplier on upper Qg limit (u/MVAr)',
        'MU_QMIN': 'Kuhn-Tucker multiplier on lower Qg limit (u/MVAr)'

    }

    @property
    def cost_type(self):
        return self.case.case_value[self._costName][0]

    @property
    def startup_cost(self):
        return self.case.case_value[self._costName][1]

    @property
    def shutdown_cost(self):
        return self.case.case_value[self._costName][2]

    @property
    def cost_constants(self):
        return self.case.case_value[self._costName][:, 4:]

    @property
    def count(self):
        return self.case.case_value[self._name].shape[0]

@dec
class Branch:
    def __init__(self, case) -> None:
        self.case = case

    _name = 'branch'
    members = {
        'F_BUS': '“from” bus number',
        'T_BUS': '“to” bus number',
        'BR_R': 'resistance (p.u.)',
        'BR_X': 'reactance (p.u.)',
        'BR_B': 'total line charging susceptance (p.u.)',
        'RATE_A': 'MVA rating A (long term rating), set to 0 for unlimited',
        'RATE_B': 'MVA rating B (short term rating), set to 0 for unlimited',
        'RATE_C': 'MVA rating C (emergency rating), set to 0 for unlimited',
        'TAP': 'transformer off nominal turns ratio, if non-zero',
        'SHIFT': 'transformer phase shift angle (degrees), positive ⇒ delay',
        'BR_STATUS': 'initial branch status, 1 = in-service, 0 = out-of-service',
        'ANGMIN': 'minimum angle difference, θf − θt (degrees)',
        'ANGMAX': 'maximum angle difference, θf − θt (degrees)',
        'PF': 'real power injected at “from” bus end (MW)',
        'QF': 'reactive power injected at “from” bus end (MVAr)',
        'PT': 'real power injected at “to” bus end (MW)',
        'QT': 'reactive power injected at “to” bus end (MVAr)',
        'MU_SF': 'Kuhn-Tucker multiplier on MVA limit at “from” bus (u/MVA)',
        'MU_ST': 'Kuhn-Tucker multiplier on MVA limit at “to” bus (u/MVA)',
        'MU_ANGMIN': 'Kuhn-Tucker multiplier lower angle difference limit (u/degree)',
        'MU_ANGMAX': 'Kuhn-Tucker multiplier upper angle difference limit (u/degree)',
    }

    @property
    def count(self):
        return self.case.case_value[self._name].shape[0]
