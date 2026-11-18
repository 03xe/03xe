"""Wraps the snk output in the same panel as the rest of the profile (dark bg, grid, chamfered border).
usage: style_snake.py in.svg out.svg"""
import re, sys
src = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'<svg[^>]*viewBox="([-\d.\s]+)"[^>]*>', src)
x, y, w, h = [float(v) for v in m.group(1).split()]
px, py, c = 12, 12, 16
bx, by, bw, bh = x - px, y - py, w + 2 * px, h + 2 * py
new_vb = f"{bx} {by} {bw} {bh}"
tag = m.group(0).replace(m.group(1), new_vb)
tag = re.sub(r'\swidth="[^"]*"', f' width="{bw:g}"', tag)
tag = re.sub(r'\sheight="[^"]*"', f' height="{bh:g}"', tag)
chamfer = (f"M{bx+c} {by+2}H{bx+bw-c}L{bx+bw-2} {by+c}V{by+bh-c}L{bx+bw-c} {by+bh-2}H{bx+c}L{bx+2} {by+bh-c}V{by+c}Z")
deco = (f'<defs><pattern id="sg" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#111"/></pattern></defs>'
        f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#050505"/><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="url(#sg)"/>'
        f'<path d="{chamfer}" fill="none" stroke="#3a3a3a" stroke-width="2"/>')
out = src.replace(m.group(0), tag + deco, 1)
open(sys.argv[2], "w", encoding="utf-8").write(out)
print("styled", sys.argv[2])
