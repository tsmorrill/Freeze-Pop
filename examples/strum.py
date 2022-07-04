import frzpop
from frzpop.scales import major
from frzpop.dynamics import f
from frzpop.generators import sweep
from frzpop.quantize import quantizer

A = 69
A_maj = quantizer(major(A))

sweep1 = sweep(40, 70, 16)
sweep2 = sweep(45, 80, 16)
sweep3 = sweep(35, 75, 16)
sweep4 = sweep(30, 85, 16)

bar1 = [[A_maj(sweep1()), f, None] for _ in range(16)]
bar2 = [[A_maj(sweep2()), f, None] for _ in range(16)]
bar3 = [[A_maj(sweep3()), f, None] for _ in range(16)]
bar4 = [[A_maj(sweep4()), f, None] for _ in range(16)]

section = [bar1, bar2, bar3, bar4]

frzpop.freeze_section(section, name="strum")
