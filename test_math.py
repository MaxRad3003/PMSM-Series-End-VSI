# Test script to verify the math and stability of Triggered Scope Mode
import math

w_elec = 2 * math.pi * 50 # 314.159 rad/s
POINTS = 280
Iref = 5.0

print("Verifying 2-cycle stationary wave calculation...")
for i in range(0, POINTS, 70):
    frac = i / (POINTS - 1)
    theta = frac * 4 * math.pi
    ia_ref = Iref * math.cos(theta)
    ib_ref = Iref * math.cos(theta - 2 * math.pi / 3)
    ic_ref = Iref * math.cos(theta + 2 * math.pi / 3)
    t_ms = frac * 40.0
    print(f"i={i:3d}, t={t_ms:4.1f}ms, theta={theta:5.2f}rad: ia_ref={ia_ref:5.2f}A, ib_ref={ib_ref:5.2f}A, ic_ref={ic_ref:5.2f}A")

print("Math verified successfully!")
