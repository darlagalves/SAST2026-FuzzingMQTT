from scipy.stats import binomtest

def mcnemar_exact(name_a, name_b, both_killed, only_a, only_b, neither):
    discordant = only_a + only_b

    print(f"\n{name_a} vs {name_b}")
    print(f"Both killed: {both_killed}")
    print(f"Only {name_a}: {only_a}")
    print(f"Only {name_b}: {only_b}")
    print(f"Neither: {neither}")
    print(f"Discordant pairs: {discordant}")

    if discordant == 0:
        print("McNemar exact test: not informative; no discordant pairs.")
        print("Interpretation: the two fuzzers killed exactly the same mutants.")
    else:
        result = binomtest(
            k=only_a,
            n=discordant,
            p=0.5,
            alternative="two-sided"
        )
        print(f"McNemar exact p-value: {result.pvalue:.4f}")

        if result.pvalue < 0.05:
            print("Interpretation: statistically significant difference.")
        else:
            print("Interpretation: no statistically significant difference.")

# sensor.py
mcnemar_exact(
    name_a="FUME",
    name_b="BooFuzz",
    both_killed=17,
    only_a=2,
    only_b=0,
    neither=107
)

mcnemar_exact(
    name_a="FUME",
    name_b="Scapy",
    both_killed=17,
    only_a=2,
    only_b=0,
    neither=107
)

mcnemar_exact(
    name_a="BooFuzz",
    name_b="Scapy",
    both_killed=17,
    only_a=0,
    only_b=0,
    neither=109
)

# template.py
mcnemar_exact(
    name_a="FUME",
    name_b="BooFuzz",
    both_killed=127,
    only_a=0,
    only_b=0,
    neither=1325
)

mcnemar_exact(
    name_a="FUME",
    name_b="Scapy",
    both_killed=127,
    only_a=0,
    only_b=0,
    neither=1325
)

mcnemar_exact(
    name_a="BooFuzz",
    name_b="Scapy",
    both_killed=127,
    only_a=0,
    only_b=0,
    neither=1325
)
