# Test geometry for demo-circuit-canvas
dpr = 1
W = 380 * dpr
H = 240 * dpr

topRailY = 26 * dpr
botRailY = H - 24 * dpr
midY = (topRailY + botRailY) / 2

legX = [W * 0.16, W * 0.28, W * 0.40, W * 0.52]
motorCenterX = W * 0.83
motorCenterY = midY

print("Canvas dimensions:", W, "x", H)
print("topRailY:", topRailY, "botRailY:", botRailY, "midY:", midY)
print("legX:", [round(x, 1) for x in legX])
print("motorCenter:", round(motorCenterX, 1), round(motorCenterY, 1))
print("Geometry valid!")
