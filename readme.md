# Introduction
- Wrap matpower/pypower case data into a class in order to access parameters conveniently.

- 将matpower/pypower的case包装成类以便于访问各个参数。

# Example

```python
import pypower.api as pypower
from power_case_wrapper import CaseWrapper

# create a CaseWrapper by passing the case data
case=CaseWrapper(pypower.case14())
# case=CaseWrapper(pypower.runopf(pypower.case14()))

print(case.gen.PG)
print(case.gen.PG[2:4])

# [232.4  40.    0.    0.    0. ]
# [0. 0.]
```



```python
case.gen.PG=0
print(case.gen.PG)
# [0. 0. 0. 0. 0.]
```
```python
case.gen.PG=[1,2,3,4,5]
print(case.gen.PG)
# [1. 2. 3. 4. 5.]
```

```python
case.gen.PG[1:3]=[100,50]
print(case.gen.PG)
# [  1. 100.  50.   4.   5.]
```

