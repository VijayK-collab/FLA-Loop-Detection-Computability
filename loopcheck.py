"""Task 4 - Infinite-loop detection: what is decidable and what is not.

A toy register machine.  Instructions:
    ("add", r, k)   r := r + k   (wraps mod `modulus` if a modulus is given)
    ("jnz", r, t)   if r != 0 jump to instruction t, else fall through
    ("halt",)
The checker answers with THREE verdicts, never a false claim:
    HALTS   - the machine reached `halt`
    LOOPS   - a configuration (pc, registers) repeated  => deterministic => runs forever (a PROOF)
    UNKNOWN - step budget exhausted without either (the honest answer for an undecidable question)
With a finite memory (modulus set) the configuration space is finite, so the checker is a
true decider once the budget exceeds the number of configurations.  With unbounded integers it
is only a semi-decider for halting (it can say HALTS, or LOOPS if a configuration repeats)."""

HALTS, LOOPS, UNKNOWN = "HALTS", "LOOPS", "UNKNOWN"


def check(program, regs, budget=10_000, modulus=None):
    pc, regs, seen = 0, dict(regs), set()
    for step in range(budget):
        cfg = (pc, tuple(sorted(regs.items())))
        if cfg in seen:
            return LOOPS, step
        seen.add(cfg)
        ins = program[pc]
        if ins[0] == "halt":
            return HALTS, step
        if ins[0] == "add":
            _, r, k = ins
            regs[r] = regs[r] + k
            if modulus:
                regs[r] %= modulus
            pc += 1
        elif ins[0] == "jnz":
            _, r, t = ins
            pc = t if regs[r] != 0 else pc + 1
    return UNKNOWN, budget


# P1: count down from 5 to 0, then halt
P1 = [("add", "x", -1), ("jnz", "x", 0), ("halt",)]
# P2: x = 1 forever (jnz on a non-zero register with no change)
P2 = [("jnz", "x", 0), ("halt",)]
# P3: add 2 each time and loop until x == 0.  Mod 256 and odd start => x is never 0 (LOOPS);
#     over unbounded integers the state never repeats, so we can only say UNKNOWN.
P3 = [("add", "x", 2), ("jnz", "x", 0), ("halt",)]
# P4: add 1 each time; mod 256 it wraps to 0 and halts
P4 = [("add", "x", 1), ("jnz", "x", 0), ("halt",)]

DEMOS = [
    ("P1 countdown from 5",              P1, {"x": 5},  None),
    ("P2 jnz on constant 1",             P2, {"x": 1},  None),
    ("P3 x+=2, unbounded ints, x0=1",    P3, {"x": 1},  None),
    ("P3 x+=2, 8-bit wraparound, x0=1",  P3, {"x": 1},  256),
    ("P4 x+=1, 8-bit wraparound, x0=1",  P4, {"x": 1},  256),
]

if __name__ == "__main__":
    for name, prog, regs, mod in DEMOS:
        verdict, steps = check(prog, regs, budget=5_000, modulus=mod)
        print(f"{name:38} -> {verdict:8} (after {steps} steps)")
