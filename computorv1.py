import sys

class Equation():
    def __init__(self):
        self.delta = 0
        self.degre = 0
        self.eq_elems_signs = [[], []]
        self.sols = []
        self.solvable = True
        self.reduced_eq = ""

    def main(self, argv):
        """Main de parsing et resolution de l'equation"""
        split_eq = argv.split('=')
        split_eq[0] = split_eq[0].split(' ')
        split_eq[1] = split_eq[1].split(' ')
        pos = self.check_degree(split_eq)
        split_eq = pop_useless_elems_in_eq(split_eq)
        self.get_elems_eq(split_eq, pos)
        self.get_reduced_eq()
        if self.degre >= 0 and self.degre <= 2:
            self.calcul_sols(split_eq)
        self.print_result()
        #print("degre = ", self.degre)
        #print("position = ", pos)
        #print("Reduced form:", self.reduced_eq)
        #print(self.sols)

    def print_result(self):
        pass

    def calcul_sols(self, split_eq):
        if self.degre == 2:
            self.eq_elems_signs[0] = multiply_elems_with_signs(self.eq_elems_signs[0], self.eq_elems_signs[1])
            self.delta = self.eq_elems_signs[0][1] * self.eq_elems_signs[0][1] - 4 * (self.eq_elems_signs[0][0] * self.eq_elems_signs[0][2])
            if self.delta >= 0:
                self.sols.append(((-1 * self.eq_elems_signs[0][1]) - self.delta ** 0.5) / (2 * self.eq_elems_signs[0][2]))
                if self.delta > 0:
                    self.sols.append(((-1 * self.eq_elems_signs[0][1]) + self.delta ** 0.5) / (2 * self.eq_elems_signs[0][2]))
            if self.delta < 0:
                self.sols.append(None)
        elif self.degre == 1:
            self.sols.append(self.eq_elems_signs[0][0] / self.eq_elems_signs[0][1] * -1)
            if self.sols[0] == -0.0:
                self.sols[0] = 0
        elif self.degre == 0:
            self.sols.append(self.handle_degree_zero(split_eq))
            if self.sols[0] == -0.0 or self.sols[0] == -0:
                self.sols[0] = 0

    def handle_degree_zero(self, split_eq):
        left_elem = 0
        right_elem = 0
        if split_eq[0][0] == '-':
            left_elem = return_var_cast(split_eq[0][1]) * -1
        else:
            left_elem = return_var_cast(split_eq[0][0])
        if split_eq[1][0] == '-':
            right_elem = return_var_cast(split_eq[1][1]) * -1
        else:
            right_elem = return_var_cast(split_eq[1][0])
        return left_elem - right_elem

    def get_reduced_eq(self):
        """Recuperation de la forme reduite de l'equation"""
        if self.eq_elems_signs[1][0] == -1:
            self.reduced_eq += '- {} * X^0 '.format(self.eq_elems_signs[0][0])
        if self.eq_elems_signs[1][0] == 1:
            self.reduced_eq += '{} * X^0 '.format(self.eq_elems_signs[0][0])
        i = 1
        while i < len(self.eq_elems_signs[0]):
            if i == 0:
                i += 1
            if self.eq_elems_signs[1][i] == -1:
                self.reduced_eq += '- {} * X^{} '.format(self.eq_elems_signs[0][i], i)
            elif self.eq_elems_signs[1][i] == 1:
                self.reduced_eq += '+ {} * X^{} '.format(self.eq_elems_signs[0][i], i)
            i += 1
        self.reduced_eq += '= 0'
            

    def get_elems_eq(self, split_eq, pos):
        """Recuperation des elements de l'equation et mise en place de la form
        ax2 + bx + c = 0"""
        skip = False
        if pos == 'right':
            split_eq[0], split_eq[1] = split_eq[1], split_eq[0]
        if split_eq[0][0] == '-':
            self.eq_elems_signs[1].append(-1)
        else:
            self.eq_elems_signs[1].append(1)
        if self.eq_elems_signs[1][0] != '':
            skip = True
        for i in range(len(split_eq[0])):
            if (split_eq[0][i] == '-' or split_eq[0][i] == '+') and skip is False:
                if split_eq[0][i] == '-':
                    self.eq_elems_signs[1].append(-1)
                else:
                    self.eq_elems_signs[1].append(1)
            elif 'X^' in split_eq[0][i]:
                if i - 1 >= 0:
                    self.eq_elems_signs[0].append(return_var_cast(split_eq[0][i - 1]))
            skip = False
        right_elems = self.get_right_elems(split_eq)
        remove_elem = self.check_if_elem_needs_to_be_removed()
        if remove_elem is True:
            self.re_adjust_reduced_eq_and_elems()
        self.reduce_left_side_with_right_side(right_elems)

    def re_adjust_reduced_eq_and_elems(self):
        if self.degre == 2:
            self.eq_elems_signs[0].pop(2)
            self.eq_elems_signs[1].pop(2)
            self.degre = 1
        elif self.degre == 1:
            self.eq_elems_signs[0].pop(1)
            self.eq_elems_signs[1].pop(1)
            self.degre = 0

    def check_if_elem_needs_to_be_removed(self):
        if self.degre == 2:
            if self.eq_elems_signs[0][2] == 0:
                return True
        elif self.degre == 1:
            if self.eq_elems_signs[0][1] == 0:
                return True
        else:
            return False

    def get_right_elems(self, split_eq):
        """Recuperation elements a droite de l'equation"""
        right_elems = []
        for i in range(len(split_eq[1])):
            if 'X^' in split_eq[1][i]:
                if i - 1 >= 0:
                    if i - 2 >= 0 and split_eq[1][i - 2] == '-':
                        right_elems.append(return_var_cast(split_eq[1][i - 1]) * -1)
                    else:
                        right_elems.append(return_var_cast(split_eq[1][i - 1]))
        return right_elems

    def reduce_left_side_with_right_side(self, right_elems):
        """Soustraction elements de droite aux correspondants a gauche"""
        for i in range(len(right_elems)):
            self.eq_elems_signs[0][i] *= self.eq_elems_signs[1][i]
            self.eq_elems_signs[0][i] -= right_elems[i]
            if self.eq_elems_signs[0][i] < 0:
                self.eq_elems_signs[1][i] = -1
            elif self.eq_elems_signs[0][i] >= 0:
                self.eq_elems_signs[1][i] = 1

    def check_degree(self, split_eq):
        """Recuperation degre de l'equation"""
        degre = 0
        pos = 'left'
        for elem in split_eq[0]:
            if 'X' in elem:
                if int(elem[len(elem) - 1]) > self.degre:
                    pos = 'left'
                    self.degre = int(elem[len(elem) - 1])
        for elem in split_eq[1]:
            if 'X' in elem and int(elem[len(elem) - 1]) > self.degre:
                pos = 'right'
                self.degre = int(elem[len(elem) - 1])
        return pos

#####################################################################

def multiply_elems_with_signs(elems, signs):
    for i in range(len(elems)):
        if signs[i] == -1:
            elems[i] *= -1
    return elems

def return_var_cast(elem):
    """Cast de string en float ou int en fonction du contenu de celle-ci"""
    if '.' in elem:
        elem = float(elem)
    else:
        elem = int(elem)
    return elem

def pop_useless_elems_in_eq(split_eq):
    """Enlever les elements inutiles dans l'equation pour rendre la
    recuperation des elements plus facile"""
    items_to_pop = ['', '*']
    new_eq = [[], []]
    for i in range(len(split_eq)):
        for j in range(len(split_eq[i])):
            if split_eq[i][j] in items_to_pop:
                pass
            else:
                new_eq[i].append(split_eq[i][j])
    return new_eq

#####################################################################

if __name__ == "__main__":
    eq = Equation()
    eq.main(sys.argv[1])
