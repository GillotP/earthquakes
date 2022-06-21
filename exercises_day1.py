import math
#import numpy as np
from tqdm import tqdm

def exercise_1(ub, vals, show_multiples=bool(0)):

	def multiples(x, vals):
		for val in vals:
			if x % val == 0:
				return True
		return False

	multiples_3_5 = [x for x in range(ub) if multiples(x, vals)]
	if show_multiples:
		print("Multiples:", multiples_3_5)
	print("Sum multiples:", sum(multiples_3_5))

#exercise_1(ub=1000, vals=[3, 5])

def exercise_2(limit_value):
	fibonnaci = [1, 2]
	sum_fibonnci_even = 2
	while fibonnaci[-1] < limit_value:
		fibonnaci.append(fibonnaci[-2] + fibonnaci[-1])
		if fibonnaci[-1] % 2 == 0:
			sum_fibonnci_even += fibonnaci[-1]
	print(sum_fibonnci_even)

#exercise_2(4000000)


def exercise_3(n):

	found_primes = [2]

	# def is_prime(n):
	# 	if n <= 3:
	# 		return n > 1
	# 	if not n%2 or not n%3:
	# 		return False
	# 	i = 5
	# 	stop = int(n**0.5)
	# 	while i <= stop:
	# 		if not n%i or not n%(i + 2):
	# 			return False
	# 		i += 6
	# 	return True

	def dumb_is_prime(found_primes, n):
		if n == 0:
			return False

		
		#print(found_primes + list(range(found_primes[-1]+1, int(math.sqrt(n))+1)))
		for i in range(2, int(math.sqrt(n))+1):
		#for i in found_primes + list(range(found_primes[-1]+1, int(math.sqrt(n))+1)):
			#print(n, i, n % i)
			if n % i == 0:
				return False
		return True

	largest_prime_factor = None
	for i in tqdm(range(3, n)):
		# print()
		# print(i)
		i_is_prime = dumb_is_prime(found_primes, i)
		if i_is_prime:
			found_primes.append(i)
			#print(found_primes)
		if i_is_prime and n % i == 0:
		#if is_prime(i) and n % i == 0:
			largest_prime_factor = i
	print(found_primes)
	print(largest_prime_factor)

#exercise_3(117)
#exercise_3(13195)
exercise_3(600851475143)

