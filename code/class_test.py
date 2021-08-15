from midigen import Flow

test_flow = Flow.from_seed_1D(3, 0.5, 'test', None)

print(test_flow)
print(test_flow.stress.size)
