# Every number in the Module 7 short-answer booklet (src/m7_short_answer/). HSC data values.
from math import *
c, h, e, me, mp, b = 3.00e8, 6.626e-34, 1.602e-19, 9.109e-31, 1.673e-27, 2.898e-3
mu0, eps0 = 4*pi*1e-7, 8.854e-12
def p(l, x): print(f"  {l:46s} {x:.5g}")
def gam(v): return 1/sqrt(1-v*v)

print("Q1 c from mu0 eps0"); p("c", 1/sqrt(mu0*eps0))
print("Q2 Fizeau: 500 teeth, d = 7500 m, first dark at 20 rev/s")
t = 1/(2*500*20); p("t (half a tooth gap)", t); p("c = 2d/t", 2*7500/t)
print("Q3 star X peak 414 nm, star Y 4500 K")
p("T_X", b/414e-9); p("lambda_Y nm", b/4500*1e9); p("peak ratio (TX/TY)^5", (7000/4500)**5)
print("Q6 633 nm, d = 0.25 mm, L = 3.0 m"); p("dy mm", 633e-9*3.0/0.25e-3*1e3)
print("Q7 grating 300 lines/mm"); d = 1/300e3; p("d", d); p("theta 656 nm", degrees(asin(656e-9/d)))
p("lambda at 8.4 deg nm", d*sin(radians(8.4))*1e9); p("max order 656", d/656e-9)
print("Q8 60 W/m2 unpolarised, then 30 deg"); p("after 1", 30); p("after 2", 30*cos(radians(30))**2)
print("Q11 Sun 5800 K"); p("lambda", b/5800)
print("Q12 400 nm on 2.3 eV"); E = h*c/400e-9; p("E J", E); p("E eV", E/e); K = E/e-2.3; p("K eV", K); p("K J", K*e)
p("v", sqrt(2*K*e/me))
print("Q13 graph: f0 = 5.5e14, (10e14, 3.0e-19)"); hh = 3.0e-19/(10e14-5.5e14); p("h from graph", hh); p("phi J", hh*5.5e14); p("phi eV", hh*5.5e14/e)
for f in (6, 7, 8, 9, 10): p(f"K at f = {f}e14 (1e-19 J)", hh*(f-5.5)*1e14/1e-19)
p("phi J with h = 6.626e-34", h*5.5e14); p("eV", h*5.5e14/e)
print("Q15 532 nm, 2.0 mW; 1200 nm")
E = h*c/532e-9; p("E J", E); p("E eV", E/e); p("N per s", 2.0e-3/E); E2 = h*c/1200e-9; p("E IR J", E2); p("E IR eV", E2/e)
print("Q17 muons 0.998c, 10 km, 2.2 us"); g = gam(0.998); p("gamma", g); p("d classical m", 0.998*c*2.2e-6)
p("t dilated us", g*2.2); p("d dilated km", 0.998*c*2.2e-6*g/1e3); p("atmosphere in muon frame km", 10/g)
print("Q18 4.2 ly at 0.80c"); g = gam(0.8); p("gamma", g); p("t Earth y", 4.2/0.8); p("t ship y", 4.2/0.8/g); p("L ship ly", 4.2/g); p("check", 4.2/g/0.8)
print("Q19 proton 0.95c"); g = gam(0.95); p("gamma", g); p("p rel", g*mp*0.95*c); p("p classical", mp*0.95*c); p("E0", mp*c*c)

# Q3 graph: Planck curves (relative), x in cm = lambda/250 nm, X peak drawn 3.6 cm high
def planck(lam_nm, T):
    lam = lam_nm*1e-9; return lam**-5/(exp(h*c/(lam*1.381e-23*T))-1)
if __name__ == "__main__":
    pk = planck(414, 7000)
    for T in (7000, 4500):
        pts = [(x, 3.6*planck(x*250, T)/pk) for x in [0.4+0.1*i for i in range(77)]]
        print(f"Q3 curve {T} K:", ' '.join(f'({x:.1f},{y:.3f})' for x, y in pts))
