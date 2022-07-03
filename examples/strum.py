import frzpop
from frzpop.scales import major
from frzpop.dynamics import f
from frzpop.generators import sweep
from frzpop.quantize import quantizer

A = 69
Astrum = quantizer(major(A))

print(major(A))

sweep1 = sweep(60, 70, 16)
sweep2 = sweep(65, 80, 16)
sweep3 = sweep(55, 75, 16)
sweep4 = sweep(40, 85, 16)

contour1 = [sweep1() for _ in range(16)]
contour2 = [sweep2() for _ in range(16)]
contour3 = [sweep3() for _ in range(16)]
contour4 = [sweep4() for _ in range(16)]

print(contour1)

bar1 = [[Astrum(val), f, None] for val in contour1]
bar2 = [[Astrum(val), f, None] for val in contour2]
bar3 = [[Astrum(val), f, None] for val in contour3]
bar4 = [[Astrum(val), f, None] for val in contour4]

section = [bar1, bar2, bar3, bar4]

frzpop.freeze_section(section, name="strum")
