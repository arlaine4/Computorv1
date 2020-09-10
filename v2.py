import sys

class Equation():
    def __init__(self):
        self.delta = None
        self.sols = []
        self.elems = [] #Liste imbriquee
        self.solvable = False
        self.degre = 0
        self.reduced_eq = ""
        self.elems_eq = [] #Liste imbriquee

    def main(self, argv):
        """Main fonction for equation resolution"""
        split_eq = self.get_split_eq(argv)
        self.get_degree(split_eq)
        print("Degree = ", self.degre)
        self.parse_elems_in_equation(split_eq)

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
        i = 0
        while split_eq[i] != '=':
            left.append(split_eq[i])
            i += 1
        i += 1
        while i < len(split_eq):
            right.append(split_eq[i])
            i += 1
        elems = self.append_elems_in_one_list(left, right)
        if self.degre >= 2:
            elems = self.reduce_and_substract_elems_in_eq(elems)
        elif self.degre == 1:
            elems = self.reduce_eq_degree_one(elems)
        self.get_str_reduced_eq(elems)
        print(elems)

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

    def reduce_eq_degree_one(self, elems):
        return elems

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
        elems = self.remove_x_zero(elems)
        return elems

    def remove_x_zero(self, elems):
        index_l = elems[0].index('X^0') - 1
        index_r = elems[1].index('X^0') - 1
        elem_l = elems[0][index_l]
        elem_r = elems[1][index_r]
        if index_r - 1 > 0 and elems[1][index_r - 1] == '-':
            elem_r *= -1
        if index_l - 1 > 0 and elems[0][index_l - 1] == '-':
            elem_l *= -1
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
    eq = Equation()
    eq.main(sys.argv[1])
