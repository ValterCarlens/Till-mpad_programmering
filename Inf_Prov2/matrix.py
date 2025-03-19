# Create a matrix using list comprehention

matrix = [[column for column in range(4)] for row in range(4)]

for _ in matrix:
    print(_)