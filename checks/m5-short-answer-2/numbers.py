# Every number in the Module 5 short-answer booklet, Set 2 (src/m5_short_answer_2/).
from math import *
g, G, ME, rE = 9.8, 6.67e-11, 6.0e24, 6.371e6
GM = G*ME
D = radians
def p(l, x): print(f"  {l:44s} {x:.5g}")

print("Q1 basketball 8.5 m/s at 52 deg from 2.0 m")
uy, ux = 8.5*sin(D(52)), 8.5*cos(D(52)); p("uy", uy); p("ux", ux)
p("rise", uy**2/(2*g)); p("max height above ground", 2.0+uy**2/(2*g)); p("time to top", uy/g)
print("Q4 plane 70 m/s at 500 m")
t = sqrt(2*500/g); p("t", t); p("x", 70*t)
print("Q5 launcher u = 5.0 m/s, predicted ranges")
for a in (15, 30, 45, 60, 75): p(f"R({a})", 25*sin(D(2*a))/g)
print("Q6 20 m/s at 60 deg, wall 24 m away")
ux, uy = 20*cos(D(60)), 20*sin(D(60)); t = 24/ux
p("t", t); p("y", uy*t-0.5*g*t*t); p("vy at wall", uy-g*t)
print("Q8 car over hill r = 40 m, 1500 kg, 15 m/s")
p("N top", 1500*g-1500*225/40); p("v max", sqrt(g*40)); p("mv^2/r", 1500*225/40)
print("Q9 seesaw")
p("tau child 30 kg at 1.5 m", 30*g*1.5); p("r for 45 kg", 30*1.5/45)
print("Q10 drum r = 0.25 m at 1200 rpm")
w = 1200*2*pi/60; p("omega", w); p("a", w*w*0.25); p("a / g", w*w*0.25/g); p("v", w*0.25)
print("Q11 0.50 kg, r = 0.80 m, T = 0.40 s; max tension 150 N")
v = 2*pi*0.8/0.4; p("v", v); p("tension", 0.5*v*v/0.8); p("T min", 2*pi*sqrt(0.5*0.8/150))
print("Q12 F vs 1/r at v = 3.0 m/s, m = 0.050 kg")
rs = [0.40, 0.50, 0.60, 0.80, 1.00]; Fm = [1.14, 0.89, 0.76, 0.55, 0.46]
inv = [1/r for r in rs]; print("    1/r:", [round(x, 3) for x in inv]); print("    F true:", [round(0.05*9/r, 4) for r in rs])
k0 = sum(a*b for a, b in zip(inv, Fm))/sum(a*a for a in inv); p("slope thru origin (= m v^2)", k0); p("m", k0/9)
n = 5; mx = sum(inv)/n; my = sum(Fm)/n; k = sum((a-mx)*(b-my) for a, b in zip(inv, Fm))/sum((a-mx)**2 for a in inv)
p("LSQ slope", k); p("LSQ intercept", my-k*mx); p("m from LSQ", k/9)
print("Q14 Earth-Moon")
Mm, d = 7.35e22, 3.84e8; F = G*ME*Mm/d**2; p("F", F); p("v Moon", sqrt(GM/d)); p("v from F", sqrt(F*d/Mm))
p("T Moon (days)", 2*pi*d/sqrt(GM/d)/86400)
print("Q15 g = 4.9 altitude; g at rE, 2rE, 4rE")
r = sqrt(GM/4.9); p("r", r); p("altitude", r-rE); p("altitude via rE*sqrt2", rE*sqrt(2)-rE)
for k_ in (1, 2, 3, 4): p(f"g at {k_} rE", GM/(k_*rE)**2)
print("Q16 Galilean moons r^3/T^2")
moons = [("Io", 4.22e8, 1.53e5), ("Europa", 6.71e8, 3.07e5), ("Ganymede", 1.07e9, 6.18e5), ("Callisto", 1.88e9, 1.44e6)]
ks = []
for nm, r, T in moons:
    k_ = r**3/T**2; ks.append(k_); p(f"{nm} r^3/T^2", k_)
kav = sum(ks)/4; p("mean", kav); p("M Jupiter", 4*pi**2*kav/G)
print("Q17 1200 kg at 600 km")
r = rE+6.0e5; p("r", r); p("v", sqrt(GM/r)); p("E", -GM*1200/(2*r)); p("U", -GM*1200/r); p("K", GM*1200/(2*r))
print("Q18 Kepler 2: v_a = v_p r_p / r_a", 30*1.0e11/1.5e11)
a = 1.25e11; GMs = (30e3)**2/(2/1.0e11-1/a); p("implied GM of star", GMs); p("implied M star", GMs/G)
p("check v_a vis-viva", sqrt(GMs*(2/1.5e11-1/a)))
print("Q19 escape from Earth")
p("v_esc", sqrt(2*GM/rE)); p("equator speed", 2*pi*rE/86164)
print("Q20 areostationary orbit")
Mm, Rm, T = 6.42e23, 3.39e6, 24.6*3600
r = (G*Mm*T**2/(4*pi**2))**(1/3); p("T s", T); p("r", r); p("altitude", r-Rm); p("v", 2*pi*r/T)
print("Added after review: Q5(c) real launch speed from R(45) = 2.44 m; Q11(d) tension with 2r; Q14(b) Moon period")
p("u = sqrt(R g)", sqrt(2.44*g))
p("tension at 2r, same T", 4*pi**2*0.5*1.6/0.4**2)
p("Moon period (days)", 2*pi*sqrt(3.84e8**3/GM)/86400)
