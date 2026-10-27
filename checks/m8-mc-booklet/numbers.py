# Every number in the Module 8 MC booklet (src/m8_mc_booklet/). HSC data sheet values.
from math import *
c, h, e, me, mp, mn = 3.00e8, 6.626e-34, 1.602e-19, 9.109e-31, 1.673e-27, 1.675e-27
u, uMeV, R = 1.661e-27, 931.5, 1.097e7
Mpc, yr = 3.09e22, 3.16e7
def p(l, x): print(f"  {l:46s} {x:.5g}")
print("== Topic 1")
print("Q4 galaxy 120 Mpc, 8400 km/s"); p("H0 km/s/Mpc", 8400/120); p("v*d", 8400*120); p("d/v", 120/8400)
print("Q5 age 1/H0, H0 = 70 km/s/Mpc"); t = Mpc/70e3; p("t s", t); p("t years", t/yr); p("forgot km->m (years)", Mpc/70/yr)
print("Q12 p-p chain mass loss 0.0287 u"); p("E MeV", 0.0287*uMeV); p("E J", 0.0287*u*c*c); p("E MeV /c^2?", 0.0287*uMeV/9e16)
print("== Topic 2")
print("Q16 selector E = 2.0e4, B = 1.0e-3"); v = 2.0e4/1.0e-3; p("v", v); p("E*B", 2e4*1e-3); p("B/E", 1e-3/2e4)
print("Q17 r = 0.114 m in B = 1.0e-3"); p("q/m", v/(1e-3*0.114)); p("q/m with v^2", v*v/(1e-3*0.114)); p("1/(Br)", 1/(1e-3*0.114)); p("m/q", 1e-3*0.114/v)
print("Q18 oil drop m = 4.9e-15, d = 1.5 cm, V = 450"); E = 450/0.015; p("E", E); q = 4.9e-15*9.8/E; p("q", q); p("n", q/e); p("q no g", 4.9e-15/E/e)
print("Q24 proton balanced, E = 5.0e3, then 2v"); p("a = qE/m", e*5e3/mp); p("2qE/m", 2*e*5e3/mp); p("3qE/m", 3*e*5e3/mp)
print("== Topic 3")
print("Q32 Rydberg 3->2"); inv = R*(1/4-1/9); p("lambda nm", 1e9/inv); p("4->2 nm", 1e9/(R*(1/4-1/16))); p("2->1 nm", 1e9/(R*(1-1/4)))
p("using 1/2-1/3 nm", 1e9/(R*(1/2-1/3))); p("using 1/4+1/9 nm", 1e9/(R*(1/4+1/9)))
for ni, nf in ((4,3),(3,2),(2,1),(4,2)): p(f"dE {ni}->{nf} eV", 13.6*(1/nf**2-1/ni**2))
print("Q35 ground -> n=3"); p("E eV", 13.6*(1-1/9)); p("E3 level", -13.6/9); p("ground->2", 13.6*0.75)
print("Q36 electron 2.0e6"); p("lambda", h/(me*2e6)); p("with mp", h/(mp*2e6)); p("h m v", h*me*2e6); p("p", me*2e6)
print("Q37 proton/neutron same v: ratio lambda_p/lambda_n", mn/mp)
print("Q39 table"); 
for name, m, vv in (("electron 1e6", me, 1e6), ("electron 5e6", me, 5e6), ("proton 1e3", mp, 1e3), ("proton 2e4", mp, 2e4)):
    p(name + " lambda", h/(m*vv))
print("== Topic 4")
print("Q50 half-life 4.0 days"); p("lambda /day", log(2)/4.0); p("1/T", 1/4.0); p("ln2*T", log(2)*4)
print("Q52 I-131 8.0 d, 800 Bq, 10 d"); lam = log(2)/8.0; p("A", 800*exp(-lam*10)); p("linear guess 800*(1-10/16)", 800*(1-10/16)); p("800/2^(10/8)", 800/2**(10/8)); p("800*exp(-10/8)", 800*exp(-10/8))
print("Q53 He-4 mass defect"); mpu, mnu, mHe = 1.007276, 1.008665, 4.001506
dm = 2*mpu+2*mnu-mHe; p("dm u", dm); p("BE MeV", dm*uMeV); p("BE per nucleon", dm*uMeV/4); p("dm kg", dm*u); p("BE J", dm*u*c*c)
print("Q55 2H + 3H -> 4He + n: BE 2.22, 8.48, 28.30"); p("Q MeV", 28.30-2.22-8.48); p("sum", 28.30+2.22+8.48); p("BE(3H)-BE(2H)", 8.48-2.22)
print("== Topic 5")
print("Q65 p pbar minimum"); p("2 mp c^2 J", 2*mp*c*c); p("mp c^2 J", mp*c*c); p("2 mp c", 2*mp*c); p("MeV", 2*mp*c*c/e/1e6)
print("Q70 annihilation at rest"); p("each photon J", me*c*c); p("total", 2*me*c*c); p("me c", me*c); p("MeV", me*c*c/e/1e6)
