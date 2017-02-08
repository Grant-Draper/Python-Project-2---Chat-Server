names = ["sherlock holmes", "john watson", "john adler", "irene adler"]
ages = range(20, 30)

#1

upper_names = [name.upper() for name in names]
print(upper_names)

#2

twice_ages = [age*2 for age in ages]
print(twice_ages)

#3

first_names = [n.split()[0] for n in names]
print(first_names)

#4

is_adler = ["adler" in name for name in names]
print(is_adler)