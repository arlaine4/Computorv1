import sys

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
            self.get_red_eq(argv)
            if self.degre == 2:
                self.calcul_delta()
                if self.delta >= 0:
                    self.calcul_sols()
            self.process_result_infos()
        if self.solvable is False and self.degre > 2:
            self.get_red_eq_high_degre(argv)
            self.process_result_infos()


    def calcul_sols(self):
        if self.delta == 0:
            self.sols.append((((self.eq_elems[1] * self.eq_signs[1] * -1) - self.delta**0.5)) / (2 * (self.eq_elems[0] * self.eq_signs[0])))
        elif self.delta > 0:
            self.sols.append(((-1 * self.eq_elems[1] * self.eq_signs[1]) - self.delta**0.5) / (2 * self.eq_elems[2] * self.eq_signs[2]))
            self.sols.append((((self.eq_elems[1] * self.eq_signs[1] * -1) + self.delta**0.5)) / (2 * (self.eq_elems[2] * self.eq_signs[2])))

    def calcul_delta(self):
        sign = self.assign_signs_elems()
        self.eq_signs = sign
        self.delta = self.eq_elems[1]**2 - (4 * ((self.eq_elems[0] * self.eq_signs[0]) * (self.eq_elems[2] * self.eq_signs[2])))

    def process_result_infos(self):
        print("Reduced form : {}".format(self.red_eq))
        print("Polynomial degree: {}".format(self.degre))
        if self.degre == 1:
            pass
        elif self.degre == 2:
            if self.delta == 0:
                print("Discriminant equals 0, the solution is :\n{:.6}".format(self.sols[0]))
            elif self.delta > 0:
                print("Discriminant is strictly positive, the two solutions are:\n{:.6}\n{:.6}".format(self.sols[0], self.sols[1]))
            elif self.delta < 0:
                print("Discriminant is strictly negative, I can't solve the equation.")
        elif self.degre > 2:
            print("The polynomial degree is strictly greater than 2, I can't solve the equation.")

    def assign_signs_elems(self):
        sign = []
        for elem in self.eq_signs:
            if elem == '-':
                sign.append(-1)
            else:
                sign.append(1)
        return sign

    def get_red_eq(self, argv):
        split_eq = argv.split('=')
        self.get_elems_eq(split_eq)
        elem_to_sub = self.get_elem_to_sub_2nd_part(split_eq[1])
        if len(elem_to_sub) > 1:
            elem_to_sub = float(elem_to_sub)
        else:
            elem_to_sub = int(elem_to_sub)
        new_elem = self.eq_elems[0] - elem_to_sub
        if self.eq_signs[0] == '-':
            new_elem = new_elem * -1
        new_elem = round(new_elem, 1)
        if new_elem > 0 and self.eq_signs[0] == '-':
            self.eq_signs[0] = '+'
        self.eq_elems[0] = new_elem
        self.append_red_eq_elems(new_elem, split_eq)

    def append_red_eq_elems(self, first_elem, split_eq):
        i = 0
        #self.red_eq += str(first_elem)
        if split_eq[0][0] == '-' or split_eq[0][0] == '+':
            i += 2
        while split_eq[0][i] != ' ':
            i += 1
        self.red_eq += str(first_elem)
        while i < len(split_eq[0]):
            self.red_eq += split_eq[0][i]
            i += 1
        self.red_eq += "= 0"
    
    def get_elem_to_sub_2nd_part(self, split_eq):
        i = 1
        elem_to_sub = ''
        if split_eq[i + 1] != ' ':
            while split_eq[i] != ' ':
                elem_to_sub += split_eq[i]
                i += 1
        elif split_eq[i + 1] == ' ':
            elem_to_sub = split_eq[i]
        return elem_to_sub

    def get_elems_eq(self, split_eq):
        if self.degre == 1:
            pass
        elif self.degre == 2:
            self.parse_elems_degre2(split_eq[0])

    def loop_elem_types_degre2(self, i, elem_nb, split_eq):
        elem = ""
        type_ = 'int'
        sign = '+'
        sign_neg = 0
        ### Elem A
        if elem_nb == 1:
            if split_eq[i] == '-':
                sign = '-'; sign_neg = 2
                i += sign_neg
            if split_eq[i + 1] != ' ':
                type_ = 'float'
                while split_eq[i] != ' ':
                    elem += split_eq[i]
                    i += 1
            else:
                elem = split_eq[i]
        ### Elem B et C
        elif elem_nb == 2 or elem_nb == 3:
            if split_eq[i] == '-':
                sign = '-'; sign_neg = 1
            i += 2
            if split_eq[i + 1] != ' ':
                type_ = 'float'
                while split_eq[i] != ' ':
                    elem += split_eq[i]
                    i += 1
            else:
                elem = split_eq[i]
        return elem, type_, sign

    def parse_elems_degre2(self, split_eq):
        i = 0
        elem_a = ""; type_a = 'int'; sing_a = '+'
        elem_b = ""; type_b = 'int'; sign_b = '+'
        elem_c = ""; type_c = 'int'; sign_c = '+'
        elem_a, type_a, sign_a = self.loop_elem_types_degre2(i, 1, split_eq)
        if sign_a == '-':
            i += 2
        if type_a == 'float':
            i += len(elem_a) - 1
        i += 8
        elem_b, type_b, sign_b = self.loop_elem_types_degre2(i, 2, split_eq)
        if type_b == 'float':
            i += len(elem_b) - 1
        i += 10
        elem_c, type_c, sign_c = self.loop_elem_types_degre2(i, 2, split_eq)
        elem_a, elem_b, elem_c = self.convert_type_elems(elem_a, elem_b, elem_c, type_a, type_b, type_c)
        self.append_elems_and_types(elem_a, elem_b, elem_c, sign_a, sign_b, sign_c, type_a, type_b, type_c)

    def append_elems_and_types(self, a, b, c, s_a, s_b, s_c, t_a, t_b, t_c):
        self.eq_elems.append(a)
        self.eq_elems.append(b)
        self.eq_elems.append(c)
        self.eq_signs.append(s_a)
        self.eq_signs.append(s_b)
        self.eq_signs.append(s_c)
        self.eq_types.append(t_a)
        self.eq_types.append(t_b)
        self.eq_types.append(t_c)

    def convert_type_elems(self, a, b, c, type_a, type_b, type_c):
        if type_a == 'float':
            a = float(a)
        else:
            a = int(a)
        if type_b == 'float':
            b = float(b)
        else:
            b = int(b)
        if type_c == 'float':
            c = float(c)
        else:
            c = int(c)
        return a, b, c

    def check_degre(self, argv):
        i = len(argv) - 1
        while argv[i] != '=':
            i -= 1
        self.degre = int(argv[i - 2])
        if self.degre < 0 or self.degre > 2:
            self.solvable = False


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
