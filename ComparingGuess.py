
def tael_farver_i_kode(kode, gaet):
    forkerte_kode_tal = [
        kode_tal for kode_tal, gaet_tal in zip(kode, gaet) if kode_tal != gaet_tal
    ]
    forkerte_gaet_tal = [
        gaet_tal for kode_tal, gaet_tal in zip(kode, gaet) if kode_tal != gaet_tal
    ]
    return sum(
        min(forkerte_kode_tal.count(tal), forkerte_gaet_tal.count(tal))
        for tal in set(forkerte_gaet_tal)
    )


def tael_rigtige_pladser(kode, gaet):
     return sum(farve_kode == farve_gaet for farve_kode, farve_gaet in zip(kode, gaet))
    