def print_result(result, benchmark=None):
    print(f"Model: {result.model} | seed={result.seed} | paths={result.paths:,} | steps={result.steps}")
    print(f"Estimate: {result.price:.6f}")
    print(f"95% CI: [{result.ci_lower:.6f}, {result.ci_upper:.6f}]")
    print(f"Standard error: {result.standard_error:.6f}")
    print(f"Sample variance: {result.sample_variance:.8f}")
    if benchmark is not None:
        print(f"Analytical benchmark: {benchmark:.6f}")
        print(f"Absolute pricing error: {abs(result.price-benchmark):.6f}")
