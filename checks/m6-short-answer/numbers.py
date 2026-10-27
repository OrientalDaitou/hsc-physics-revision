# Every number in the Module 6 short-answer booklet (src/m6_short_answer/).
from math import *
e, me, mp, mu0, g = 1.602e-19, 9.109e-31, 1.673e-27, 4*pi*1e-7, 9.8
D = radians
def p(l, x): print(f"  {l:46s} {x:.4g}")

print("Q1 electron: 500 V across 4.0 cm")
E = 500/0.04; p("E", E); p("v", sqrt(2*e*500/me)); p("a", e*E/me)
print("Q2 electron 2.0e7 m/s, plates 6.0 cm long, 2.0 cm apart, 150 V")
E = 150/0.02; a = e*E/me; t = 0.06/2.0e7; y = 0.5*a*t*t
p("E", E); p("a", a); p("t", t); p("y (m)", y); p("vy", a*t); p("angle deg", degrees(atan(a*t/2e7)))
p("gravity drop in t", 0.5*g*t*t)
print("Q3 proton 4.0e6 m/s in 0.25 T")
p("r", mp*4e6/(e*0.25)); p("T period", 2*pi*mp/(e*0.25))
print("Q4 selector E = 2.0e4, B1 = 0.10 T; B2 = 0.20 T, r = 0.24 m")
v = 2.0e4/0.10; p("v", v); m = e*0.20*0.24/v; p("m", m); p("m in u", m/1.661e-27)
print("Q6 wire 0.25 m, 4.0 A, 0.30 T at 50 deg")
p("F", 0.25*4*0.3*sin(D(50))); p("Fmax", 0.25*4*0.3)
print("Q7 wires 5.0 cm, 8.0 A and 12 A")
p("F/l", 2e-7*8*12/0.05)
print("Q8 balance: l = 0.050 m, B = 0.12 T")
Is = [1, 2, 3, 4, 5]; dm = [0.62, 1.20, 1.85, 2.42, 3.05]
for I, m in zip(Is, dm): print(f"    I={I}  true dm(g)={0.12*0.05*I/g*1000:.3f}  data={m}")
k = sum(a*b for a, b in zip(Is, dm))/sum(a*a for a in Is); p("slope g/A (through origin)", k)
p("F/I (N/A)", k*1e-3*g); p("B", k*1e-3*g/0.05)
print("Q9 rod 30 g, 0.20 m, B = 0.50 T")
p("I for zero tension", 0.03*g/(0.5*0.2)); p("a if I doubled", g)
print("Q10 cable: F/l scaling with I doubled", 4)
print("Q11 50 turns, 8.0 cm square, B 0.20 -> 0.80 T in 0.30 s, R = 4.0 ohm")
A = 0.08**2; dphi = 0.6*A; p("A", A); p("dPhi", dphi); p("emf", 50*dphi/0.3); p("I", 50*dphi/0.3/4)
print("Q13 240 V -> 12 V, 6.0 A load")
p("ratio", 240/12); p("Ip ideal", 12*6/240); p("Pout", 72); p("Pin at 90%", 72/0.9); p("Ip at 90%", 72/0.9/240)
print("Q15 200 kW, line R = 0.50 ohm, 2.0 kV vs 20 kV")
for V in (2.0e3, 20e3):
    I = 200e3/V; p(f"I at {V:.0f} V", I); p(f"loss at {V:.0f} V", I*I*0.5); p(f"% of 200 kW", 100*I*I*0.5/200e3)
print("Q16 200 turns, 5.0 x 4.0 cm, 1.5 A, 0.35 T")
A = 0.05*0.04; p("A", A); p("tau max", 200*1.5*A*0.35); p("tau at 60 deg normal", 200*1.5*A*0.35*sin(D(60)))
print("Q17 12 V motor, R = 1.5 ohm, running 1.2 A")
p("start I", 12/1.5); p("back emf", 12-1.2*1.5); p("P heat at start", 12**2/1.5); p("P heat running", 1.2**2*1.5)
print("Q10 (after review) cable 3.0 mm, 10 A")
p("F/l", 2e-7*10*10/3.0e-3); p("F/l at 20 A", 2e-7*20*20/3.0e-3)
