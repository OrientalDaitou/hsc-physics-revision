# Every number in the Module 8 short-answer booklet (src/m8_short_answer/). HSC data values.
from math import *
c, h, e, me, mp, mn = 3.00e8, 6.626e-34, 1.602e-19, 9.109e-31, 1.673e-27, 1.675e-27
u, uMeV, R, g = 1.661e-27, 931.5, 1.097e7, 9.8
Mpc, yr = 3.09e22, 3.16e7
def p(l, x): print(f"  {l:46s} {x:.5g}")
print("Q1 Hubble data")
d = [20, 40, 60, 80, 100]; v = [1300, 2800, 4000, 5500, 6800]
H = sum(a*b for a, b in zip(d, v))/sum(a*a for a in d); p("best-fit gradient through origin", H)
p("gradient from (0,0) to (100, 6800)", 68); H0 = 68
t = Mpc/(H0*1e3); p("1/H0 s", t); p("1/H0 years", t/yr)
print("Q4 4 H atoms -> He-4 atom"); dm = 4*1.007825 - 4.002603; p("dm u", dm); p("E MeV", dm*uMeV); p("E J", dm*uMeV*1e6*e)
print("Q5 Thomson: plates 2.0 cm, 400 V, B = 8.0e-4, r = 0.18 m")
E = 400/0.020; p("E", E); vv = E/8.0e-4; p("v", vv); p("q/m", vv/(8.0e-4*0.18)); p("ratio to H ion e/mp", (vv/(8.0e-4*0.18))/(e/mp))
print("Q6 Millikan: m = 3.27e-15 kg, E = 4.0e4"); q = 3.27e-15*g/4.0e4; p("q", q); p("n", q/e)
print("Q9 4 -> 2"); inv = R*(1/4-1/16); lam = 1/inv; p("lambda nm", lam*1e9); p("E J", h*c/lam); p("E eV", h*c/lam/e); p("dE levels eV", 13.6*(1/4-1/16))
print("Q11 electron through 150 V"); vv = sqrt(2*e*150/me); p("v", vv); p("lambda", h/(me*vv))
print("Q13 A0 = 1200 Bq, T = 6.0 days"); lam = log(2)/6.0; p("lambda", lam); p("A(40)", 1200*exp(-lam*40))
for t in (0, 3, 6, 9, 12, 15, 18, 21, 24): p(f"A({t})", 1200*exp(-lam*t))
print("Q15 U-235 fission -> Ba-141 + Kr-92 + 3n")
mU, mBa, mKr = 235.0439, 140.9144, 91.9262
dm = mU + mn/u - (mBa + mKr + 3*mn/u); p("m_n in u (from kg)", mn/u)
dm = mU + 1.008665 - (mBa + mKr + 3*1.008665); p("dm u", dm); p("E MeV", dm*uMeV); p("E J", dm*uMeV*1e6*e)
N = 1.0/(mU*u); p("nuclei in 1.0 kg", N); p("E total J", N*dm*uMeV*1e6*e)
print("Q17 charges: uud, u dbar"); p("uud", 2/3+2/3-1/3); p("u dbar", 2/3+1/3)
print("Q19 LHC proton 6.8 TeV"); E = 6.8e12*e; p("E J", E); p("mc^2 J", mp*c*c); gm = E/(mp*c*c); p("gamma", gm); p("v/c", sqrt(1-1/gm**2)); p("1 - v/c", 1-sqrt(1-1/gm**2))

# Q14 graph: binding energy per nucleon (MeV) against A, semi-empirical formula for A >= 12,
# measured values for light nuclei.  x = A/40 cm, y = (B/A) cm
def bpa(A):
    Z = A/(1.98 + 0.0155*A**(2/3))
    B = 15.75*A - 17.8*A**(2/3) - 0.711*Z*(Z-1)/A**(1/3) - 23.7*(A-2*Z)**2/A
    return B/A
if __name__ == "__main__":
    pts = [(2, 1.11), (3, 2.57), (6, 5.33), (7, 5.61), (9, 6.46), (12, 7.68), (16, 7.98), (20, 8.03), (30, 8.52),
           (40, 8.55), (56, 8.79), (80, 8.69), (100, 8.60), (120, 8.50), (150, 8.27), (180, 8.05), (210, 7.83), (238, 7.57)]
    for A, b in pts: p(f"B/A at A = {A}", b)
    print("Q14 curve:", ' '.join(f'({A/40:.3f},{b:.2f})' for A, b in pts))
