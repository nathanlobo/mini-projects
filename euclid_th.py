# Extended Euclidean with full back‑substitution trace

def euclidean_steps(a, b):
    steps = []
    while b != 0:
        q = a // b
        r = a - q * b
        steps.append((a, b, q, r))  # a = q*b + r
        a, b = b, r
    return steps  # last step has remainder 0; gcd is the last divisor

def _format_linear(expr):
    parts = []
    for k, v in sorted(expr.items(), key=lambda kv: (abs(kv[0]), kv[0])):
        if v == 0:
            continue
        if v == 1:
            parts.append(f"{k}")
        elif v == -1:
            parts.append(f"-{k}")
        else:
            parts.append(f"{v}*{k}")
    s = " + ".join(parts) or "0"
    return s.replace("+ -", "- ")

def _format_with_replacement(expr, rem, r1, q, r2):
    parts = []
    for k, v in sorted(expr.items(), key=lambda kv: (abs(kv[0]), kv[0])):
        if v == 0:
            continue
        if k == rem:  # show the substitution in parentheses
            if v == 1:
                parts.append(f"({r1} - {q}*{r2})")
            elif v == -1:
                parts.append(f"-({r1} - {q}*{r2})")
            else:
                parts.append(f"{v}({r1} - {q}{r2})")
        else:
            if v == 1:
                parts.append(f"{k}")
            elif v == -1:
                parts.append(f"-{k}")
            else:
                parts.append(f"{v}*{k}")
    s = " + ".join(parts) or "0"
    return s.replace("+ -", "- ")

def extended_gcd_backsub(a, b):
    steps = euclidean_steps(a, b)

    # Euclidean steps
    print("Euclidean Algorithm steps:")
    for (r1, r2, q, r) in steps:
        print(f"{r1} = {q}*{r2} + {r}")

    # Start from the gcd = last non-zero divisor
    gcd = steps[-1][1]
    expr = {gcd: 1}

    print("\nBack-substitution steps:")
    for (r1, r2, q, rem) in reversed(steps):
        if rem in expr and rem != 0:
            # Show the substitution explicitly
            print(f"{gcd} = " + _format_with_replacement(expr, rem, r1, q, r2))
            coeff = expr.pop(rem)
            # Replace coeff*rem with coeff*r1 - coeff*q*r2
            expr[r1] = expr.get(r1, 0) + coeff
            expr[r2] = expr.get(r2, 0) - coeff * q
            # Show simplified linear combo
            print(f"{gcd} = " + _format_linear(expr))

    m = expr.get(a, 0)
    n = expr.get(b, 0)
    print(f"\nFinal: {gcd} = {a}({m}) + {b}({n})")
    return gcd, m, n

# ---- run here ----
print("Code to solve gcd and find m & n")
a = int(input("Enter a: "))
b = int(input("Enter b: "))
print()
gcd, m, n = extended_gcd_backsub(a, b)

print(f"\nGCD({a}, {b}) = {gcd}")
print(f"-> {a}(m)+ {b}(n) = {a*m + b*n}")
print(f"-> {a}({m})+ {b}({n}) = {a*m + b*n}")
print(f".'. m = {m}, n = {n}")





def extended_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    i=1
    while r != 0:
        q = old_r // r
        if i>=2:
        	print(f"{old_r} = {q} x {r} + ",end="")
        old_r, r = r, old_r - q * r
        if i>=2:
        	print(r)
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
        i+=1
    return old_r, old_s, old_t

print("Code to solve gcd(a,b) and find m & n")
a = int(input("Enter a: "))
b = int(input("Enter b: "))
print()
gcd, m, n = extended_gcd(a, b)

print(f"\nGCD({a}, {b}) = {gcd}")
print(f"-> {a}(m)+ {b}(n) = {a*m + b*n}")
print(f"-> {a}({m})+ {b}({n}) = {a*m + b*n}")
print(f".'. m = {m}, n = {n}")

input("Enter to close")