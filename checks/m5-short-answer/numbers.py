# Every number in the Module 5 short-answer booklet (src/m5_short_answer/).
from math import *
g, G, ME, rE = 9.8, 6.67e-11, 6.0e24, 6.371e6
GM = G*ME
D = radians
def p(l, x): print(f"  {l:42s} {x:.5g}")

print("Q1 golf ball 28 m/s at 35 deg")
u, th = 28, D(35); uy, ux = u*sin(th), u*cos(th)
p("uy", uy); p("ux", ux); p("h max", uy**2/(2*g)); t = 2*uy/g; p("t flight", t); p("range", ux*t)

print("Q2 horizontal 15 m/s from 30 m")
t = sqrt(2*30/g); vy = g*t; p("t", t); p("vy", vy); p("v", hypot(15, vy)); p("angle below horiz", degrees(atan(vy/15)))

print("Q5 range investigation, h = 0.90 m")
h = 0.90; tf = sqrt(2*h/g); p("t flight", tf)
us = [1.0, 1.5, 2.0, 2.5, 3.0]; Rm = [0.43, 0.63, 0.87, 1.06, 1.29]
for u_, r_ in zip(us, Rm): print(f"    u={u_}  predicted={u_*tf:.3f}  measured={r_}")
k0 = sum(a*b for a, b in zip(us, Rm))/sum(a*a for a in us); p("slope through origin", k0); p("g from it", 2*h/k0**2)
n = len(us); mx = sum(us)/n; my = sum(Rm)/n
k = sum((a-mx)*(b-my) for a, b in zip(us, Rm))/sum((a-mx)**2 for a in us); c = my-k*mx
p("LSQ slope", k); p("LSQ intercept", c); p("g from LSQ slope", 2*h/k**2)
for kk in (0.42, 0.43, 0.44): p(f"g if slope {kk}", 2*h/kk**2)

print("Q6 12 m/s at 40 deg from 25 m cliff")
uy, ux = 12*sin(D(40)), 12*cos(D(40)); t = (uy+sqrt(uy*uy+2*g*25))/g
p("uy", uy); p("ux", ux); p("t", t); p("x", ux*t)

print("Q8 banked r = 80 m, 15 deg")
p("v design", sqrt(80*g*tan(D(15)))); p("v km/h", sqrt(80*g*tan(D(15)))*3.6)

print("Q9 conical pendulum 0.25 kg, L = 0.80 m, 30 deg")
m, L, th = 0.25, 0.80, D(30); T = m*g/cos(th); r = L*sin(th); v = sqrt(r*g*tan(th))
p("tension", T); p("r", r); p("v", v); p("period", 2*pi*r/v)

print("Q10 vertical circle 0.20 kg, r = 0.60 m")
p("v min top", sqrt(g*0.6)); p("T bottom at 6.0", 0.2*g + 0.2*36/0.6); p("v top if 6.0 at bottom", sqrt(36-4*g*0.6))

print("Q11 torque 150 N, 0.35 m, 70 deg")
p("tau", 0.35*150*sin(D(70))); p("F needed perp for 65", 65/0.35); p("length needed with 150 N perp", 65/150)

print("Q12 centripetal investigation r = 0.60 m")
v2 = [16, 25, 36, 49, 64]; Fm = [0.82, 1.24, 1.78, 2.47, 3.18]  # F well above the stopper weight (0.29 N); print("    v^2:", v2); print("    F true (m=0.030):", [round(0.03*x/0.6, 4) for x in v2])
k0 = sum(a*b for a, b in zip(v2, Fm))/sum(a*a for a in v2); p("slope thru origin", k0); p("m = slope*r", k0*0.6)
mx = sum(v2)/5; my = sum(Fm)/5; k = sum((a-mx)*(b-my) for a, b in zip(v2, Fm))/sum((a-mx)**2 for a in v2)
p("LSQ slope", k); p("LSQ intercept", my-k*mx); p("m from LSQ", k*0.6)

print("Q14 Mars")
M, r = 6.42e23, 3.39e6; gm = G*M/r**2; p("g Mars", gm); p("weight 70 kg", 70*gm); p("ratio to Earth", gm/9.8)

print("Q15 GEO radius")
rg = (GM*86400**2/(4*pi**2))**(1/3); p("r", rg); p("altitude", rg-rE)

print("Q17 500 kg from 7.0e6 to 1.4e7 m")
m, r1, r2 = 500, 7.0e6, 1.4e7
p("dU", GM*m*(1/r1-1/r2)); p("dK", GM*m/2*(1/r2-1/r1)); p("dE", GM*m/2*(1/r1-1/r2))
p("U1", -GM*m/r1); p("U2", -GM*m/r2); p("K1", GM*m/(2*r1)); p("K2", GM*m/(2*r2))

print("Q18 Mars escape")
p("v_esc Mars", sqrt(2*G*6.42e23/3.39e6))

print("Q20 ISS at 420 km")
r = rE+4.2e5; p("g at ISS", GM/r**2); p("fraction of 9.8", GM/r**2/9.8); p("v ISS", sqrt(GM/r)); p("T min", 2*pi*r/sqrt(GM/r)/60)
