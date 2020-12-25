from argparse import ArgumentParser, ArgumentError, RawDescriptionHelpFormatter
from math import pi, exp, atan, atan2

values = [
    {
        'A': (80,  120, 350, 650, 410, 130, 360, 750, 310, 190),
        'B': (95,  115, 650, 730, 340, 330, 410, 830, 340, 220),
        'C': (100, 80,  450, 810, 190, 220, 220, 720, 260, 180),
        'D': (105, 85,  420, 980, 330, 280, 310, 710, 240, 200),
        'E': (115, 55,  485, 660, 100, 340, 575, 815, 255, 225),
        'F': (125, 65,  510, 500, 550, 250, 300, 800, 330, 250),
        'G': (130, 60,  380, 420, 330, 440, 450, 650, 410, 275),
        'H': (135, 80,  680, 600, 260, 310, 575, 870, 355, 265),
    },
    {
        'A': (50,  100, 525, 620, 210, 530, 100),
        'B': (100, 50,  310, 610, 220, 570, 200),
        'C': (200, 70,  220, 630, 240, 450, 300),
        'D': (150, 200, 200, 660, 200, 550, 400),
        'E': (250, 150, 335, 625, 245, 600, 150),
        'F': (130, 180, 350, 600, 195, 650, 250),
        'G': (180, 250, 315, 615, 180, 460, 350),
        'H': (220, 190, 360, 580, 205, 560, 180),
    },
    {
        'A': (120, 0.9,  0.7,  53, 49, 65, 39, 32),
        'B': (150, 0.7,  0.8,  49, 45, 61, 34, 34),
        'C': (110, 0.85, 0.75, 44, 31, 56, 20, 30),
        'D': (115, 0.6,  0.9,  50, 38, 48, 37, 28),
        'E': (135, 0.55, 0.65, 52, 42, 52, 42, 21),
        'F': (145, 0.75, 0.85, 48, 44, 53, 36, 25),
        'G': (160, 0.65, 0.45, 46, 41, 53, 33, 29),
        'H': (130, 0.95, 0.50, 47, 39, 58, 28, 25),
    },
    {
        'A': (35, 55, 12, 14, 120*10**-3, 100*10**-3, 200*10**-6, 105*10**-6, 70),
        'B': (25, 40, 11, 15, 100*10**-3, 85*10**-3,  220*10**-6, 95*10**-6,  80),
        'C': (35, 45, 10, 13, 220*10**-3, 70*10**-3,  230*10**-6, 85*10**-6,  75),
        'D': (45, 50, 13, 15, 180*10**-3, 90*10**-3,  210*10**-6, 75*10**-6,  85),
        'E': (50, 30, 14, 13, 130*10**-3, 60*10**-3,  100*10**-6, 65*10**-6,  90),
        'F': (20, 35, 12, 10, 170*10**-3, 80*10**-3,  150*10**-6, 90*10**-6,  65),
        'G': (55, 50, 13, 12, 140*10**-3, 60*10**-3,  160*10**-6, 80*10**-6,  60),
        'H': (65, 60, 10, 10, 160*10**-3, 75*10**-3,  155*10**-6, 70*10**-6,  95),
    },
    {
        'A': (40, 50, 10, 16),
        'B': (30, 10, 20, 15),
        'C': (35, 5,  30, 14),
        'D': (25, 5,  25, 12),
        'E': (40, 30, 40, 11),
        'F': (22, 30, 15, 10),
        'G': (20, 50, 25, 8 ),
        'H': (18, 50, 40, 5 ),
    }
]

# --------------------------------------------
# some useful functions ahead

# sums resistivity of parallel resistors
def par(*args):
    if len(args) > 1:
        a, b = args[0], par(*args[1:])
        return a * b / (a + b)
    return args[0]

# computes a determinant of a matrix
def det(mat):
    if len(mat) == 1:
        return mat[0][0]
    return sum((-1 if j%2 else 1) * mat[0][j] * det([line[:j]+line[j+1:] for line in mat[1:]]) for j in range(len(mat)))

# solves a matrix for a vector using Cramer's rule
def solve_cramer(mat, vec):
    dim = len(vec)
    assert (isinstance(mat, (list, tuple)) and isinstance(mat[0], (list, tuple)) and isinstance(vec, (list, tuple)) and
        len(mat) == dim and len(mat[0]) == dim), "can't solve matrix, sizes don't match"
    D = det(mat)
    # print(D)
    mats = [[[mat[i][j] if j != d else vec[i] for j in range(dim)] for i in range(dim)] for d in range(dim)]
    # print(f'\t{tuple(det(m) for m in mats)}')
    return tuple(det(m) / D for m in mats)

# --------------------------------------------

# strategy:
# 1. simplify the circuit keeping r6 unchanged
# 2. calculate total resistance and total current
# 3. calculate current through r6 and thus voltage
def get_1(u1, u2, r1, r2, r3, r4, r5, r6, r7, r8, dump=False):
    r9 = r2 + par(r3, r4)
    ra = r1 * r9 / (r1 + r5 + r9)
    rb = r1 * r5 / (r1 + r5 + r9)
    rc = r9 * r5 / (r1 + r5 + r9)
    r10 = rb + r7
    rekv = ra + par(rc + r6, r10) + r8
    iekv = (u1 + u2) / rekv

    i6 = iekv * r10 / (rc + r6 + r10)

    if dump:
        print(f'\tr9\t{r9:.03f}')
        print(f'\tra\t{ra:.03f}')
        print(f'\trb\t{rb:.03f}')
        print(f'\trc\t{rc:.03f}')
        print(f'\tr10\t{r10:.03f}')
        print(f'\trekv\t{rekv:.03f}')
        print(f'\tiekv\t{iekv:.03f}')
        print(f'\ti6\t{i6:.06f}')
    print(f'    U6 = {i6 * r6:.04f} V, I6 = {i6*1000:.04f} mA')

# strategy: thevenin
def get_2(u, r1, r2, r3, r4, r5, r6, dump=False):
    Rth = par(r2, r6) + par(r4 + r5, r1)
    Uth = u * ((r4 + r5) / (r1 + r4 + r5) - r6 / (r2 + r6))

    i3 = Uth / (Rth + r3)
    u3 = Uth * (r3 / (r3 + Rth))

    if dump:
        print(f'\tRth\t{Rth:.03f}')
        print(f'\tUa = {u*(r4 + r5) / (r1 + r4 + r5):.03f}')
        print(f'\tUb = {u * r6 / (r2 + r6):.03f}')
        print(f'\tUth\t{Uth:.03f}')
        print(f'\ti3\t{i3:.03f}')
        print(f'\tu3\t{u3:.03f}')
    print(f'    Ur3 = {u3:.04f} V, Ir3 = {i3*1000:7.04f} mA')

# strategy:
# 1. create a current equation for each of the three nodes
# 2. substitute differences of voltage / resistance for currents
# 3. solve matrix for voltages at nodes
def get_3(u, i1, i2, r1, r2, r3, r4, r5, dump=False):

    mat = [
        [-(1/r1 + 1/r2 + 1/r3),      1/r3,             0       ],
        [         1/r3,         -(1/r3 + 1/r5),       1/r5     ],
        [          0,                1/r5,       -(1/r4 + 1/r5)]
    ]
    vec = [-u / r1, -i1, i1 - i2]

    Ua, Ub, Uc = solve_cramer(mat, vec)
    if dump:
        print('\t[')
        print(f'\t\t{mat[0]},')
        print(f'\t\t{mat[1]},')
        print(f'\t\t{mat[2]}\n\t]')
        print(f'\tUa = {Ua:.03f} V, Ub = {Ub:.03f} V, Uc = {Uc:.03f} V')
    print(f'    Ur2 = {Ua:.04f} V, Ir2 = {Ua / r2:.04f} A')

# strategy: (same as in 3, but with currents and complex numbers)
# 1. create a voltage equation for each of the three loops
# 2. substitute differences of current * resistance for voltages
# 3. solve matrix for currents in loops
# 4. calculate voltage amplitude and offset
def get_4(u1, u2, r1, r2, l1, l2, c1, c2, f, dump=False):
    o = 2 * pi * f
    zc1 = complex(0, -1 / (o * c1))
    zc2 = complex(0, -1 / (o * c2))
    zl1 = complex(0, o * l1)
    zl2 = complex(0, o * l2)

    matrix = [
        [r1 + zc1 + zl2,       -zl2,            -zc1     ],
        [      -zl2,      r2 + zc2 + zl2,       -r2      ],
        [      -zc1,           -r2,        r2 + zc1 + zl1]
    ]
    vec = [-u1, -u2, 0]
    i1, i2, i3 = solve_cramer(matrix, vec)

    il2 = i1 - i2
    ul2 = il2 * zl2
    ul2_s = abs(ul2)
    angle = atan2(ul2.imag, ul2.real)
    angle_deg = angle * 180 / pi

    if dump:
        print(f'\tzcs: {zc1:.03f} \t| {zc2:.03f}')
        print(f'\tzls: {zl1:.03f} \t| {zl2:.03f}')
        print(f'\tdet: {det(matrix):.03f}')
        print('\t[')
        print(f'\t\t{matrix[0]},')
        print(f'\t\t{matrix[1]},')
        print(f'\t\t{matrix[2]}\n\t]')
        print(f'\tcrs: ({i1:.03f}, {i2:.03f}, {i3:.03f})')
        print(f'\til2\t{il2:.03f}')
        print(f'\tul2\t{ul2:.03f}')
        print(f'\tul2_s\t{ul2_s:.03f}')
    print(f'    |Ul2| = {ul2_s:.04f} ({ul2:.04f}) V, phi = {angle:.04f} rad ({angle_deg:.02f}°)')

# strategy:
# 1. lol can't calculate this
def get_5(u, l, r, i0, dump=False):
    i = lambda t: u / r + (i0 - u / r) * exp(-r / l * t)
    print(f'\t   U/R + (i(0) - U/R) * exp(-R/L * t) <=> {u/r} + {i0 - u/r} * exp({-r/l} * t)')




test_codes = {
}

# --------------------------------------------

functions = [get_1, get_2, get_3, get_4, get_5]

class _ArgumentParser(ArgumentParser):

    # override automatic short-help-printing on error
    def error(self, message):
        raise SystemExit(message)

    # override printing help twice on -h
    def print_help(self, *args):
        return self.format_help()

if __name__ == '__main__':

    # functions for argument conversion ahead
    def int_range(s):
        if '-' in s:
            x, y = map(int, s.split('-'))
            bot, top = x-1, y
        else:
            bot, top = int(s)-1, int(s)
        if not (top > bot and bot >= 0 and top <= 5):
            print(f"Invalid task range: '{bot+1, top}', should follow this rule: 1 <= a <= b <= 5")
            exit(1)
        return bot, top

    def task_code(s):
        if not all(c in '_ABCDEFGH' for c in s):
            print(f"Invalid character in tasks ({repr(s)})")
            exit(1)
        elif not (len(s) == 1 or len(s) == 5):
            print(f"Invalid tasks length ({len(s)})")
            exit(1)

        return s * (5 if len(s) == 1 else 1)

    def preset(s):
        if s not in test_codes:
            print(f"Preset {repr(s)} not found")
            exit(1)
        return s

    example_text = '''example usage:
  python3 iel_solver.py -p me\t\t(define your preset inside the script first)
  python3 iel_solver.py -p me -t 1-3\tsolve for your preset, but only first 3 tasks
  python3 iel_solver.py FCDGA\t\tsolve the tasks for these letters
  python3 iel_solver.py C -t 3\t\tsolve third task of group C'''

    # parser definition
    parser = _ArgumentParser(
        description='Script that solves all your IEL equations for you, as long as you define them :)',
        epilog=example_text,
        formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-t', '--task_range', metavar='{n|n-m}', default=(0, 5), type=int_range, help='select with test(s) get printed (digit or range n-m)')
    parser.add_argument('-d', '--dump', action='store_true', help='debug output')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--preset', type=preset, help='execute preset tasks')
    group.add_argument('tasks', nargs='?', type=task_code, help='combination of 5 letters A-H or underscores (_ for everything)')

    # parse arguments
    try:
        parsed = parser.parse_args()
    except SystemExit as e:
        if e.code != 1:
            print(parser.format_help())
        exit()

    # retrieve preset tasks if they exist
    tasks = test_codes.get(parsed.preset) or parsed.tasks

    # run tasks
    for i in range(*parsed.task_range):

        sequence = tasks[i]
        if sequence == '_':
            sequence = 'ABCDEFGH'
        
        for letter in sequence:
            print(f'({i + 1})[{letter}] ', end='')
            functions[i](*values[i][letter], dump=parsed.dump)

