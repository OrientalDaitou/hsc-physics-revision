# Every number in the M5T3 gravity MC booklet (src/m5t3_booklet/).
from math import pi, sqrt
G, ME, rE = 6.67e-11, 6.0e24, 6.371e6
GM = G*ME
def p(label, x): print(f"{label:45s} {x:.4g}")

print("== A4 Mars-Phobos force")
Mm, mp, r, T = 6.42e23, 1.07e16, 9.38e6, 2.75e4
p("F = GMm/r^2", G*Mm*mp/r**2)
p("check m 4pi^2 r/T^2", mp*4*pi**2*r/T**2)
p("r not squared", G*Mm*mp/r)
p("field GM/r^2 (N/kg)", G*Mm/r**2)
p("r in km", G*Mm*mp/(r/1e3)**2)

print("== A6 neutral point: fraction from Earth", 9/10)

print("== B9 ISS v at 420 km")
h = 4.20e5
p("v correct", sqrt(GM/(rE+h)))
p("v using h only", sqrt(GM/h))
p("v escape at that r", sqrt(2*GM/(rE+h)))
p("v using rE only", sqrt(GM/rE))
p("T check (min)", 2*pi*(rE+h)/sqrt(GM/(rE+h))/60)

print("== B10 GEO altitude, T = 24 h")
T = 24*3600
rg = (GM*T**2/(4*pi**2))**(1/3)
p("r", rg); p("altitude", rg-rE)
p("no cube root r^3", GM*T**2/(4*pi**2))
p("T in hours: r", (GM*24**2/(4*pi**2))**(1/3))
p("square root instead of cube root", sqrt(GM*T**2/(4*pi**2)))
p("v GEO", 2*pi*rg/T)

print("== B11 Jupiter mass from Io")
r, T = 4.22e8, 1.53e5
p("M = 4pi^2 r^3/(G T^2)", 4*pi**2*r**3/(G*T**2))
p("no 4pi^2", r**3/(G*T**2))
p("T not squared", 4*pi**2*r**3/(G*T))
p("r^2 not r^3", 4*pi**2*r**2/(G*T**2))

print("== B8 asteroid 9.0 AU", 9.0**1.5)

print("== C5 U of 1200 kg sat at 3500 km altitude")
m, h = 1.20e3, 3.50e6
p("U correct", -GM*m/(rE+h))
p("U using h only", -GM*m/h)
p("U using rE only", -GM*m/rE)
p("E total (half)", -GM*m/(2*(rE+h)))

print("== C6 U graph: m = 200 kg")
m = 200
for alt in [0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 20000]:
    p(f"U at {alt} km (1e9 J)", -GM*m/(rE+alt*1e3)/1e9)
U2, U12 = -GM*m/(rE+2.0e6), -GM*m/(rE+12.0e6)
p("dU 2000 -> 12000 km", U12-U2)
p("sum of mags", -(U12+U2))

print("== C10 escape Mercury")
M, r = 3.30e23, 2.44e6
p("v_esc", sqrt(2*G*M/r)); p("v_orb", sqrt(G*M/r))
p("no sqrt", 2*G*M/r); p("r in km", sqrt(2*G*M/(r/1e3)))

print("== C9 escape table (M/r)")
for n, M, d in [("X", 2.0e24, 8000), ("Y", 6.0e24, 20000), ("Z", 1.0e24, 3000)]:
    p(f"{n} v_esc (m/s)", sqrt(2*G*M/(d*1e3/2)))

print("== C12 work 800 kg 7.0e6 -> 2.1e7 m")
m, r1, r2 = 800, 7.0e6, 2.1e7
dE = GM*m/2*(1/r1-1/r2)
p("dE total (correct)", dE)
p("dU", GM*m*(1/r1-1/r2))
p("dKE", GM*m/2*(1/r2-1/r1))
p("|U1|", GM*m/r1)
p("|E1|", GM*m/(2*r1))
p("|E2|", GM*m/(2*r2))
