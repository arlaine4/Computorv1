import sys

class Equation():

	def __init__(self, av):
		self.full_eq = av
		self.degre = self.get_degree()
		self.split_eq, self.red_eq = self.get_red_eq()
		self.get_equation_elements()
		if self.degre == 2:
			self.get_delta()
		self.nb_sols = 0
		self.sols = []
	
	def get_degree(self):
		i = len(self.full_eq) - 1
		while self.full_eq[i] != '=':
			i -= 1
		degre = int(self.full_eq[i - 2])
		return degre

	def get_red_eq(self):
		split_eq = self.full_eq.split('=')
		split_eq[0] = split_eq[0].split(' ') ; split_eq[0].remove('')
		split_eq[1] = split_eq[1].split(' ') ; split_eq[1].remove('')
		if len(split_eq[0][0]) > 1:
			new_elem = float(split_eq[0][0])
		else:
			new_elem = int(split_eq[0][0])
		if len(split_eq[1][0]) > 1:
			new_elem -= float(split_eq[1][0])
		else:
			new_elem -= int(split_eq[1][0])
		split_eq[0][0] = str(new_elem)
		split_eq[1] = ['0']
		reduced_eq = ""
		for elem in split_eq[0]:
			reduced_eq += elem
			reduced_eq += ' '
		reduced_eq += ' = 0'
		return split_eq, reduced_eq

	def get_equation_elements(self):
		if self.degre == 1:
			self.get_for_degre_one()
		elif self.degre == 2:
			self.get_for_degre_two()

	def get_for_degre_one(self):
		self.a = float(self.split_eq[0][4])
		if self.split_eq[0][3] == '-':
			self.a *= -1
		self.b = float(self.split_eq[0][0])

	def get_for_degre_two(self):
		self.a = float(self.split_eq[0][8])
		if self.split_eq[0][7] == '-':
			self.a *= -1
		self.b = float(self.split_eq[0][4])
		if self.split_eq[0][3] == '-':
			self.b *= -1
		self.c = float(self.split_eq[0][0])

	def get_delta(self):
		self.delta = ((self.b * self.b) - (4 * (self.a * self.c)))

	def __str__(self):
		return 'Reduced form : {}\nPolynomial degree : {}\nsolutions : {}' \
	.format(self.split_eq, self.red_eq, self.degre, self.sols)


def get_solutions(eq):
	if eq.delta < 0:
		return ['Discriminant is strictly negative, there is no solutions']
	elif eq.delta == 0:
		x1 = (((eq.b * -1) - (eq.delta**0.5)) / (2 * eq.a))
		return [x1]
	elif eq.delta > 0:
		x1 = (((eq.b * -1) - (eq.delta**0.5)) / (2 * eq.a))
		x2 = (((eq.b * -1) + (eq.delta**0.5)) / (2 * eq.a))
		return [x1, x2]

if __name__ == "__main__":
	eq = Equation(sys.argv[1])
	if eq.degre == 1:
		eq.sols = (eq.b * -1) / eq.a
	elif eq.degre == 2:
		eq.sols = get_solutions(eq)
	print(eq)
