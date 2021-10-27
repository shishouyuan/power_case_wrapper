from typing import Callable, List


class CaseWrapper:
    '''
    A wrapper for pypower case data. 
    Easy way to access and modify case parameters.

    Shouyuan Shi @ South China University of Technology
    Created in 2021/05/28
    '''

    def __init__(self, case_value) -> None:
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
        self.__case_value = value

    @property
    def version(self):
        return self.case_value['version']

    @property
    def baseMVA(self):
        'baseMVA'
        return self.case_value['baseMVA']

    @baseMVA.setter
    def baseMVA(self, val):
        self.case_value['baseMVA'] = val

    @property
    def gen(self):
        'gen and gencost data'
        return self.__gen

    @property
    def bus(self):
        'bus data'
        return self.__bus

    @property
    def branch(self):
        'branch data'
        return self.__branch


class _PropertyGenerator:
    def __init__(self, tab: str, items: List[str]) -> None:
        self.tab = tab
        self.items = items

    @staticmethod
    def __create_property_fun(name, index):
        def get(s):
            if index < s.case.case_value[name].shape[1]:
                return s.case.case_value[name][:, index]
            else:
                return None

        def set(s, val):
            if index < s.case.case_value[name].shape[1]:
                s.case.case_value[name][:, index] = val
        return get, set

    def property(self, fun: Callable):
        get, set = self.__create_property_fun(
            self.tab, self.items.index(fun.__name__))
        return property(fget=get, fset=set, doc=fun.__doc__)


class Bus:
    def __init__(self, case) -> None:
        self.case = case

    _tab = 'bus'
    _members = ['BUS_I', 'BUS_TYPE', 'PD', 'QD', 'GS', 'BS', 'BUS_AREA', 'VM', 'VA',
                'BASE_KV', 'ZONE', 'VMAX', 'VMIN', 'LAM_P', 'LAM_Q', 'MU_VMAX', 'MU_VMIN']

    _dec = _PropertyGenerator(_tab, _members)

    @_dec.property
    def BUS_I(self) -> List[float]: 'bus number (positive integer)'

    @_dec.property
    def BUS_TYPE(
        self) -> List[float]: 'bus type (1 = PQ, 2 = PV, 3 = ref, 4 = isolated)'

    @_dec.property
    def PD(self) -> List[float]: 'real power demand (MW)'

    @_dec.property
    def QD(self) -> List[float]: 'reactive power demand (MVAr)'

    @_dec.property
    def GS(
        self) -> List[float]: 'shunt conductance (MW demanded at V = 1.0 p.u.)'

    @_dec.property
    def BS(
        self) -> List[float]: 'shunt susceptance (MVAr injected at V = 1.0 p.u.)'

    @_dec.property
    def BUS_AREA(self) -> List[float]: 'area number (positive integer)'

    @_dec.property
    def VM(self) -> List[float]: 'voltage magnitude (p.u.)'

    @_dec.property
    def VA(self) -> List[float]: 'voltage angle (degrees)'

    @_dec.property
    def BASE_KV(self) -> List[float]: 'base voltage (kV)'

    @_dec.property
    def ZONE(self) -> List[float]: 'loss zone (positive integer)'

    @_dec.property
    def VMAX(self) -> List[float]: 'maximum voltage magnitude (p.u.)'

    @_dec.property
    def VMIN(self) -> List[float]: 'minimum voltage magnitude (p.u.)'

    @_dec.property
    def LAM_P(
        self) -> List[float]: 'Lagrange multiplier on real power mismatch (u/MW)'

    @_dec.property
    def LAM_Q(
        self) -> List[float]: 'Lagrange multiplier on reactive power mismatch (u/MVAr)'

    @_dec.property
    def MU_VMAX(
        self) -> List[float]: 'Kuhn-Tucker multiplier on upper voltage limit (u/p.u.)'

    @_dec.property
    def MU_VMIN(
        self) -> List[float]: 'Kuhn-Tucker multiplier on lower voltage limit (u/p.u.)'

    @property
    def bus_count(self):
        'total count of buses'
        return self.case.case_value[self._tab].shape[0]


class Gen:
    def __init__(self, case) -> None:
        self.case = case

    _tab = 'gen'
    _members = ['GEN_BUS', 'PG', 'QG', 'QMAX', 'QMIN', 'VG', 'MBASE', 'GEN_STATUS', 'PMAX', 'PMIN', 'PC1', 'PC2', 'QC1MIN',
                'QC1MAX', 'QC2MIN', 'QC2MAX', 'RAMP_AGC', 'RAMP_10', 'RAMP_30', 'RAMP_Q', 'APF', 'MU_PMAX', 'MU_PMIN', 'MU_QMAX', 'MU_QMIN']

    _dec = _PropertyGenerator(_tab, _members)

    @_dec.property
    def GEN_BUS(self) -> List[float]: 'bus number'

    @_dec.property
    def PG(self) -> List[float]: 'real power output (MW)'

    @_dec.property
    def QG(self) -> List[float]: 'reactive power output (MVAr)'

    @_dec.property
    def QMAX(self) -> List[float]: 'maximum reactive power output (MVAr)'

    @_dec.property
    def QMIN(self) -> List[float]: 'minimum reactive power output (MVAr)'

    @_dec.property
    def VG(self) -> List[float]: 'voltage magnitude setpoint (p.u.)'

    @_dec.property
    def MBASE(
        self) -> List[float]: 'total MVA base of machine, defaults to baseMVA'

    @_dec.property
    def GEN_STATUS(
        self) -> List[float]: 'machine status, > 0 = machine in-service, ≤ 0 = machine out-of-service'

    @_dec.property
    def PMAX(self) -> List[float]: 'maximum real power output (MW)'

    @_dec.property
    def PMIN(self) -> List[float]: 'minimum real power output (MW)'

    @_dec.property
    def PC1(
        self) -> List[float]: 'lower real power output of PQ capability curve (MW)'

    @_dec.property
    def PC2(
        self) -> List[float]: 'upper real power output of PQ capability curve (MW)'

    @_dec.property
    def QC1MIN(
        self) -> List[float]: 'minimum reactive power output at PC1 (MVAr)'

    @_dec.property
    def QC1MAX(
        self) -> List[float]: 'maximum reactive power output at PC1 (MVAr)'

    @_dec.property
    def QC2MIN(
        self) -> List[float]: 'minimum reactive power output at PC2 (MVAr)'

    @_dec.property
    def QC2MAX(
        self) -> List[float]: 'maximum reactive power output at PC2 (MVAr)'

    @_dec.property
    def RAMP_AGC(
        self) -> List[float]: 'ramp rate for load following/AGC (MW/min)'

    @_dec.property
    def RAMP_10(self) -> List[float]: 'ramp rate for 10 minute reserves (MW)'

    @_dec.property
    def RAMP_30(self) -> List[float]: 'ramp rate for 30 minute reserves (MW)'

    @_dec.property
    def RAMP_Q(
        self) -> List[float]: 'ramp rate for reactive power (2 sec timescale) (MVAr/min)'

    @_dec.property
    def APF(self) -> List[float]: 'area participation factor'

    @_dec.property
    def MU_PMAX(
        self) -> List[float]: 'Kuhn-Tucker multiplier on upper Pg limit (u/MW)'

    @_dec.property
    def MU_PMIN(
        self) -> List[float]: 'Kuhn-Tucker multiplier on lower Pg limit (u/MW)'

    @_dec.property
    def MU_QMAX(
        self) -> List[float]: 'Kuhn-Tucker multiplier on upper Qg limit (u/MVAr)'

    @_dec.property
    def MU_QMIN(
        self) -> List[float]: 'Kuhn-Tucker multiplier on lower Qg limit (u/MVAr)'

    _costtab = "gencost"

    @property
    def cost_MODEL(self):
        'MODEL in matpower: cost model, 1 = piecewise linear, 2 = polynomial'
        return self.case.case_value[self._costtab][0]

    @property
    def cost_STARTUP(self):
        'STARTUP in matpower: startup cost in US dollars'
        return self.case.case_value[self._costtab][1]

    @property
    def cost_SHUTDOWN(self):
        'SHUTDOWN in matpower: shutdown cost in US dollars'
        return self.case.case_value[self._costtab][2]

    @property
    def cost_COST(self):
        '''
        COST in matpowr:
        parameters defining total cost function f(p) begin in this column,
        units of f and p are $/hr and MW (or MVAr), respectively

        (MODEL = 1) ⇒ p1, f1, p2, f2, . . . , pN , fN
            where p1 < p2 < · · · < pN and the cost f(p) is defined by
            the coordinates (p1, f1), (p2, f2), . . . , (pN , fN )
            of the end/break-points of the piecewise linear cost

        (MODEL = 2) ⇒ cn, . . . , c1, c0
            N coefficients of n-th order polynomial cost function, starting
            with highest order, where cost is f(p) = cnp
            n + · · · + c1p + c0
        '''
        return self.case.case_value[self._costtab][:, 4:]

    @property
    def gen_count(self):
        'total count of generators'
        return self.case.case_value[self._tab].shape[0]


class Branch:
    def __init__(self, case) -> None:
        self.case = case

    _tab = 'branch'
    _members = ['F_BUS', 'T_BUS', 'BR_R', 'BR_X', 'BR_B', 'RATE_A', 'RATE_B', 'RATE_C', 'TAP', 'SHIFT',
                'BR_STATUS', 'ANGMIN', 'ANGMAX', 'PF', 'QF', 'PT', 'QT', 'MU_SF', 'MU_ST', 'MU_ANGMIN', 'MU_ANGMAX']

    _dec = _PropertyGenerator(_tab, _members)

    @_dec.property
    def F_BUS(self) -> List[float]: '“from” bus number'

    @_dec.property
    def T_BUS(self) -> List[float]: '“to” bus number'

    @_dec.property
    def BR_R(self) -> List[float]: 'resistance (p.u.)'

    @_dec.property
    def BR_X(self) -> List[float]: 'reactance (p.u.)'

    @_dec.property
    def BR_B(self) -> List[float]: 'total line charging susceptance (p.u.)'

    @_dec.property
    def RATE_A(
        self) -> List[float]: 'MVA rating A (long term rating), set to 0 for unlimited'

    @_dec.property
    def RATE_B(
        self) -> List[float]: 'MVA rating B (short term rating), set to 0 for unlimited'

    @_dec.property
    def RATE_C(
        self) -> List[float]: 'MVA rating C (emergency rating), set to 0 for unlimited'

    @_dec.property
    def TAP(
        self) -> List[float]: 'transformer off nominal turns ratio, if non-zero'

    @_dec.property
    def SHIFT(
        self) -> List[float]: 'transformer phase shift angle (degrees), positive ⇒ delay'

    @_dec.property
    def BR_STATUS(
        self) -> List[float]: 'initial branch status, 1 = in-service, 0 = out-of-service'

    @_dec.property
    def ANGMIN(
        self) -> List[float]: 'minimum angle difference, θf − θt (degrees)'

    @_dec.property
    def ANGMAX(
        self) -> List[float]: 'maximum angle difference, θf − θt (degrees)'

    @_dec.property
    def PF(self) -> List[float]: 'real power injected at “from” bus end (MW)'

    @_dec.property
    def QF(
        self) -> List[float]: 'reactive power injected at “from” bus end (MVAr)'

    @_dec.property
    def PT(self) -> List[float]: 'real power injected at “to” bus end (MW)'

    @_dec.property
    def QT(
        self) -> List[float]: 'reactive power injected at “to” bus end (MVAr)'

    @_dec.property
    def MU_SF(
        self) -> List[float]: 'Kuhn-Tucker multiplier on MVA limit at “from” bus (u/MVA)'

    @_dec.property
    def MU_ST(
        self) -> List[float]: 'Kuhn-Tucker multiplier on MVA limit at “to” bus (u/MVA)'

    @_dec.property
    def MU_ANGMIN(
        self) -> List[float]: 'Kuhn-Tucker multiplier lower angle difference limit (u/degree)'

    @_dec.property
    def MU_ANGMAX(
        self) -> List[float]: 'Kuhn-Tucker multiplier upper angle difference limit (u/degree)'

    @property
    def branch_count(self):
        'total count of branches'
        return self.case.case_value[self._tab].shape[0]
