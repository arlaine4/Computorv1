import sys

class Equation():
    def __init__(self):
        self.delta = None
        self.sols = []
        self.elems = [] #Liste imbriquee
        self.solvable = True
        self.degre = 0
        self.reduced_eq = ""
        self.elems_eq = [] #Liste imbriquee

    def main(self, argv):
        """Main fonction for equation resolution"""
        split_eq = self.get_split_eq(argv)
        self.get_degree(split_eq)
        if self.degre == 0:
            result = self.get_infos_degre_zero(split_eq)
            self.result_degre_zero(result)
        else:
            self.parse_elems_in_equation(split_eq)

############
# Degre zero
############

    def get_infos_degre_zero(self, split_eq):
        left_elem = split_eq[0]
        right_elem = split_eq[3]
        if '.' in left_elem:
            left_elem = float(left_elem)
        else:
            left_elem = int(left_elem)
        if '.' in right_elem:
            right_elem = float(right_elem)
        else:
            right_elem = int(right_elem)
        result = left_elem - right_elem
        return result

    def result_degre_zero(self, result):
        if result == 0:
            print("All real numbers are a solution.")
        else:
            print("There is no solutions, this equation is impossible to solve.")

############
# Degre zero
############

    def get_split_eq(self, argv):
        """Split equation to get elements and degree easier"""
        split_argv = argv.split('=')
        split_argv = argv.split(' ')
        for elem in split_argv:
            if elem == '*':
                split_argv.remove(elem)
        return split_argv

    def parse_elems_in_equation(self, split_eq):
        left = []
        right = []
        elem_zero = None
        elem_one = None
        elem_two = None
        i = 0
        while split_eq[i] != '=':
            left.append(split_eq[i])
            i += 1
        i += 1
        while i < len(split_eq):
            right.append(split_eq[i])
            i += 1
        elems = self.append_elems_in_one_list(left, right)
        if self.degre > 2:
            self.solvable = False
        elif self.degre >= 2:
            elems = self.reduce_and_substract_elems_in_eq(elems)
            elem_zero, elem_one, elem_two = self.calcul_delta(elems)
        elif self.degre == 1:
            elems = self.reduce_eq_degree_one(elems)
        if self.solvable is True:
            self.calcul_sols(elems, elem_zero, elem_one, elem_two)
        self.get_str_reduced_eq(elems)
        self.print_result(elem_one, elem_two)

    def get_elems_zero_one_first_degree(self, elems):
        elem_zero = 0
        elem_one = 0
        if '.' in elems[0]:
            elem_zero = float(elems[0])
        else:
            elem_zero = int(elems[0])
        if '.' in elems[1]:
            elem_one = float(elems[1])
        else:
            elem_one = int(elems[1])
        return elem_zero, elem_one

    def print_result(self, one, two):
        print("Reduced form:", self.reduced_eq)
        print("Polynomial degree:", self.degre)
        if self.solvable is True:
            if self.degre == 1:
                print("The solution is: {:.6}".format(self.sols[0]))
            elif self.degre == 2:
                if self.delta > 0:
                    print("Discriminant is strictly positive, the two solutions are:\n{:.6}\n{:.6}".format(self.sols[0], self.sols[1]))
                elif self.delta == 0:
                    print("Discriminant equals zero, the solution is:\n{:.6}".format(self.sols[0]))
        elif self.solvable is False:
            if self.degre == 1:
                if self.elems_eq[1] == 0:
                    print("Element 'X^1' can't be zero, there is no solutions to this equation.")
            elif self.degre == 2:
                if self.delta < 0:
                    print("Discriminant in stricly negative, there is no real solutions for this equation.")
                elif two == 0:
                    print("Element 'X^2' can't be zero, there is no solutions to this equation.")
            elif self.degre > 2:
                print("The polynomial degree is strictly greater than 2, I can't solve.")

    def calcul_sols(self, elems, elem_z, elem_o, elem_t):
        if self.degre == 1:
            self.calcul_sol_degre_one(elems)
        elif self.degre == 2:
            if elem_t != 0:
                if self.delta > 0:
                    self.sols.append(((-1 * elem_o) - self.delta ** 0.5) / (2 * elem_t))
                self.sols.append(((-1 * elem_o) + self.delta ** 0.5) / (2 * elem_t))
            elif elem_t == 0:
                self.solvable = False

    def calcul_delta(self, elems):
        index_two = elems[0].index('X^2') - 1
        index_one = elems[0].index('X^1') - 1
        index_zero = elems[0].index('X^0') - 1
        elem_two = elems[0][index_two]
        elem_one = elems[0][index_one]
        elem_zero = elems[0][index_zero]
        ### >=
        elem_zero, elem_one, elem_two = self.cast_delta(elem_zero, elem_one, elem_two)
        if index_zero - 1 >= 0 and elems[0][index_zero - 1] == '-':
            elem_zero *= -1
        if index_one - 1 >= 0 and elems[0][index_one - 1] == '-':
            elem_one *= -1
        if index_two - 1 >= 0 and elems[0][index_two - 1] == '-':
            elem_two *= -1 
        self.delta = elem_one * elem_one - 4 * (elem_zero * elem_two)
        if self.delta >= 0:
            self.solvable = True
        else:
            self.solvable = False
        return elem_zero, elem_one, elem_two

    def cast_delta(self, elem_zero, elem_one, elem_two):
        if type(elem_zero) is str:
            if '.' in elem_zero:
                elem_zero = float(elem_zero)
            else:
               elem_zero = int(elem_zero)
        if type(elem_one) is str:
            if '.' in elem_one: 
                elem_one = float(elem_one)
            else:
                elem_one = int(elem_one)
        if type(elem_two) is str:
            if '.' in elem_two:
                elem_two = float(elem_two)
            else:
                elem_two = int(elem_two)
        return elem_zero, elem_one, elem_two

    def get_str_reduced_eq(self, elems):
        i = 0
        while i < len(elems[0]):
            if 'X' in str(elems[0][i]):
                self.reduced_eq += '* '
            if type(elems[0][i]) is not str:
                self.reduced_eq += str(elems[0][i]) + ' '
            else:
                self.reduced_eq += elems[0][i] + ' '
            i += 1
        self.reduced_eq += '= 0'

###########
# Degre One
###########

    def calcul_sol_degre_one(self, elems, skip=False):
        if skip is False:
            index_zero = elems[0].index('X^0') - 1
            index_one = elems[0].index('X^1') - 1
            elem_zero = elems[0][index_zero]
            elem_one = elems[0][index_one]
            if type(elem_zero) is str:
                if '.' in elem_zero:
                    elem_zero = float(elem_zero)
                else:
                    elem_zero = int(elem_zero)
            if type(elem_one) is str:
                if '.' in elem_one:
                    elem_one = float(elem_one)
                else:
                    elem_one = int(elem_one)
            ### >= not sure
            if index_zero - 1 >= 0 and elems[0][index_zero] == '-':
                elem_zero *= -1
            if index_one - 1 >= 0 and elems[0][index_one] == '-':
                elem_one *= -1
            ###
            self.elems_eq.append(elem_zero)
            self.elems_eq.append(elem_one)
            if elem_one != 0:
                self.solvable = True
                self.sols.append(elem_zero / elem_one * -1)
            else:
                self.solvable = False
                self.sols.append("No solution, 'X^1' elem can't be zero")

    def reduce_eq_degree_one(self, elems):
        place_degre_one = self.get_place_degre_one(elems)
        if place_degre_one == 'right':
            elems = self.adjust_place_elems_in_eq(elems)
        elems = self.reduce_and_substract_elems_in_eq(elems)
        return elems

    def adjust_place_elems_in_eq(self, elems):
        new_elems = []
        new_elems.append(elems[1])
        new_elems.append(elems[0])
        return new_elems

    def get_place_degre_one(self, elems):
        if 'X^1' in elems[0]:
            #if len(elems[0]) <= len(elems[1]) and 'X^1' in elems[1]:
            #    return 'right'
            #else:
            return 'left'
        elif 'X^1' in elems[1]:
            return 'right'

###########
# Degre one
###########

    def reduce_and_substract_elems_in_eq(self, elems):
        index_left = 0
        index_right = 0
        elem_l = 0
        elem_r = 0
        neg_l = 1
        neg_r = 1
        new_elem = 0
        if 'X^1' in elems[1]:
            index_left = elems[0].index('X^1') - 1
            if elems[0][index_left - 1] == '-':
                neg_l = -1
            index_right = elems[1].index('X^1') - 1
            if elems[1][index_right - 1] == '-':
                neg_r = -1
            elem_l, elem_r = self.cast_elems_index(index_left, index_right, elems)
            elem_l = elem_l - elem_r * neg_r
            elems[0][index_left] = elem_l
            if neg_l == -1:
                elem_l *= -1
                if elem_l >= 0:
                    elems[0][index_left - 1] = '+'
            elems[1] = self.pop_elems_right_part(elems[1], index_right)
        elif 'X^1' not in elems[1] and self.degre == 1:
            self.calcul_sol_degre_one(elems, skip=True)
        elems = self.remove_x_zero(elems)
        return elems

    def remove_x_zero(self, elems):
        index_l = elems[0].index('X^0') - 1
        index_r = elems[1].index('X^0') - 1
        elem_l = elems[0][index_l]
        elem_r = elems[1][index_r]
        ###maybe add >= instead of >
        if index_r - 1 > 0 and elems[1][index_r - 1] == '-':
            elem_r *= -1
        if index_l - 1 > 0 and elems[0][index_l - 1] == '-':
            elem_l *= -1
        ####
        elem_l, elem_r = self.cast_elems_index(index_l, index_r, elems)
        elem_l -= elem_r
        elems[0][index_l] = elem_l
        elems[1].remove('X^0')
        # Are you sure about that ?
        if len(elems[1]) > 1:
            elems[1].pop(0)
        elems[1][0] = '0'
        return elems

    def pop_elems_right_part(self, elems, index_right):
        for i in range(3):
            if index_right == len(elems):
                index_right -= 1
            elems.pop(index_right)
        return elems

    def cast_elems_index(self, index_l, index_r, elems):
        if '.' in elems[0][index_l]:
            index_l = float(elems[0][index_l])
        else:
            index_l = int(elems[0][index_l])
        if '.' in elems[1][index_r]:
            index_r = float(elems[1][index_r])
        else:
            index_r = int(elems[1][index_r])
        return index_l, index_r


    def append_elems_in_one_list(self, left, right):
        elems = []
        elems.append(left)
        elems.append(right)
        return elems

    def get_degree(self, split_eq):
        degre = None
        for elem in split_eq:
            if elem[0] == 'X':
                if (degre is not None and degre < int(elem[len(elem) - 1])) or (degre is None):
                    degre = int(elem[len(elem) - 1])
                else:
                    pass
        self.degre = degre

if __name__ == "__main__":
    if len(sys.argv) == 2:
        eq = Equation()
        eq.main(sys.argv[1])
    elif len(sys.argv) > 2:
        print("Too many arguments.")
    elif len(sys.argv) == 1:
        print("Missing equation.")
