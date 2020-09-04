import sys
import math

class Equation():
    def __init__(self, argv):
        self.solvable = True
        self.degre = 0
        self.red_eq = ""
        self.delta = 0
        self.eq_elems = []
        self.eq_signs = []
        self.eq_types = []
        self.sols = []

    def main(self, argv):
        self.check_degre(argv)
        self.get_red_eq(argv)
        if self.solvable is True:
            self.calcul_delta()
            if self.delta >= 0:
                self.calcul_sols()
        self.print_result()

    def print_result(self):
        print("Reduced form: {}\nPolynomial degree: {}".format(self.red_eq, self.degre))
        if self.solvable is False:
            """degre 0 ???"""
            if self.degre > 2:
                if self.delta < 0:
                    print("The polynomial degree is strictly greater than 2, I can't solve.\nAnd the discriminant is strictly negative.")
                else:
                    print("The polynomial degree is strictly greater than 2, I can't solve.")
            elif self.delta < 0:
                print("The discriminant is striclty negative, there is no solutions.")
        elif self.solvable is True:
            if self.delta > 0:
                print("Discriminant is strictly positive, the two solutions are:\n{:.6}\n{:.6}".format(self.sols[0], self.sols[1]))
            elif self.delta == 0:
                print("Discriminant equals zero, the solution is:\n{:.6}".format(self.sols[0]))

    def calcul_delta(self):
        for i in range(len(self.eq_elems)):
            self.eq_elems[i] = self.eq_elems[i] * self.eq_signs[i]
        if self.degre == 2:
            self.delta = self.eq_elems[1] * self.eq_elems[1] - 4 * (self.eq_elems[0] * self.eq_elems[2])
        """
        delta for degree 1
        """

    def calcul_sols(self):
        """solutions for degree 1 to do without delta"""
        if self.degre == 1:
            self.sols.append(((-1 * self.eq_elems[0]) - self.delta ** 0.5) / (2 * self.eq_elems[1]))
        elif self.degre == 2:
            self.sols.append(((-1 * self.eq_elems[1]) - self.delta ** 0.5) / (2 * self.eq_elems[2]))
            if self.delta > 0:
                self.sols.append(((-1 * self.eq_elems[1]) + self.delta ** 0.5) / (2 * self.eq_elems[2]))

    def check_degre(self, argv):
        i = len(argv) - 1
        while argv[i] != '=':
            i -= 1
        i -= 2
        self.degre = int(argv[i])
        if self.degre < 1 or self.degre > 2:
            self.solvable = False

    def get_red_eq(self, argv):
        split_eq = argv.split('=')
        self.get_elems_and_signs(split_eq[0])
        first_elem, sign_first_elem = self.get_first_elem(split_eq[1])
        if '.' in first_elem:
            first_elem = float(first_elem)
        else:
            first_elem = int(first_elem)
        if sign_first_elem == '-':
            first_elem *= -1
        self.loop_cast_elems_eq()
        self.eq_elems[0] = self.eq_elems[0] * self.eq_signs[0] - first_elem
        if self.eq_elems[0] < 0:
            self.red_eq += '- {}'.format(self.eq_elems[0] * -1)
        else:
            self.red_eq += str(self.eq_elems[0])
        i = 2 + (len(str(self.eq_elems[0])) - 2)
        if self.eq_signs[0] == -1:
            i += 1
        while i < len(split_eq[0]):
            self.red_eq += split_eq[0][i]
            i += 1
        self.red_eq += '= 0'

    def loop_cast_elems_eq(self):
        for i in range(len(self.eq_elems)):
            if '.' in self.eq_elems[i]:
                self.eq_elems[i] = float(self.eq_elems[i])
            else:
                self.eq_elems[i] = int(self.eq_elems[i])

    def get_first_elem(self, split_eq):
        elem = ''
        sign = ''
        i = 1
        if split_eq[i] == '-':
            sign = '-'
            i += 2
        else:
            sign = '+'
        while split_eq[i] != ' ':
            elem += split_eq[i]
            i += 1
        return elem, sign

    def get_elems_and_signs(self, split_eq):
        i = 0
        elem = ''
        if split_eq[0] == '-':
            self.eq_signs.append(-1)
            i += 2
        else:
            self.eq_signs.append(1)
        elem, i = self.get_elem(split_eq, i)
        self.eq_elems.append(elem)
        i += 7
        if split_eq[i] == '-':
            self.eq_signs.append(-1)
        else:
            self.eq_signs.append(1)
        i += 2
        elem, i = self.get_elem(split_eq, i)
        self.eq_elems.append(elem)
        if self.degre >= 2:
            i += 7
            if split_eq[i] == '-':
                self.eq_signs.append(-1)
            else:
                self.eq_signs.append(1)
            elem, i = self.get_elem(split_eq, i + 2)
            self.eq_elems.append(elem)

    def get_elem(self, split_eq, i):
        elem = ''
        while split_eq[i] != ' ':
            elem += split_eq[i]
            i += 1
        return elem, i

def error(error=1):
    if error == 1:
        print("Missing equation.")
        sys.exit()
    elif error == 2:
        print("Too many arguments.")
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        error(1)
    elif len(sys.argv) > 2:
        error(2)
    eq = Equation(sys.argv[1])
    eq.main(sys.argv[1])
