import pathlib
import copy

#Ex1

def extract_coefficient(line: str, var_pos: int) -> float:
    if var_pos == -1:
        return 0.0
    start = var_pos - 1
    while start > 0 and line[start] not in "+-":
        start -= 1
    coef_str = line[start : var_pos].strip()
    if coef_str in ("", "+"):
        return 1.0
    elif coef_str == "-":
        return -1.0
    else:
        return float(coef_str)

def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    lines = path.read_text().strip().splitlines()
    lines = [line.replace(" ", "") for line in lines]
    A = []
    B = []
    for line in lines:
        B.append(float(line.split("=")[1]))
        x = line.find("x")
        y = line.find("y")
        z = line.find("z")
        coef_x = extract_coefficient(line, x)
        coef_y = extract_coefficient(line, y)
        coef_z = extract_coefficient(line, z)
        A.append([coef_x, coef_y, coef_z])
    return A, B

A, B = load_system(pathlib.Path("system.txt"))
print(f"{A=} {B=}")


#Ex2
def determinant(matrix: list[list[float]]) -> float:
    return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
            - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
            + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))

def determinant_two(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0] 

#Ex 2.3
def trace(matrix: list[list[float]]) -> float:
    return sum(matrix[i][i] for i in range(len(matrix)))

print(f"{trace(A)=}")


#Ex 2.4
def norm(vector: list[float]) -> float:
    summ = sum(vector[i] ** 2 for i in range (len(vector)))
    return summ ** 0.5

print(f"{norm(B)=}")

#Ex 2.5

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    transp = []
    for j in range(0, len(matrix[0])):
        column = []
        for i in range(0, len(matrix)):
            column.append(matrix[i][j])
        transp.append(column)
    
    return transp


print(f"{transpose(A)=}")


#Ex 3

def replace(matrix: list[list[float]], index, vector: list[float]):
    for i in range(0, len(matrix)):
        matrix[i][index] = vector[i]
    return matrix

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    matrix_x = replace(copy.deepcopy(matrix), 0, vector)
    matrix_y = replace(copy.deepcopy(matrix), 1, vector)
    matrix_z = replace(copy.deepcopy(matrix), 2, vector)
    det = determinant(copy.deepcopy(matrix))
    return [
        determinant(matrix_x) / det,
        determinant(matrix_y) / det,
        determinant(matrix_z) / det
    ]


print(f"{solve_cramer(A, B)=}")

# Ex 4

def mul_scalar(value, matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            matrix[i][j] *= value
    return matrix
    

def dot_prod(matrix: list[list[float]], vector: list[float]):
    result = []
    for i in range(0, len(matrix)):
        elem = 0
        for j in range(0, len(matrix[0])):
            elem += matrix[i][j] * vector[j]
        result.append(elem)
    return result

def inverse(matrix: list[list[float]]):
    return mul_scalar(1 / determinant(matrix), adjoint(copy.deepcopy(matrix)))

def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    minor_mat = copy.deepcopy(matrix)
    #print(f"Before minor : {minor_mat}")
    minor_mat.pop(i)
    for line in minor_mat:
        line.pop(j)
    #print(f"After minor : {minor_mat}")
    return minor_mat
    

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    cof_matrix = copy.deepcopy(matrix)
    for i in range(0, len(cof_matrix)):
        for j in range(0, len(cof_matrix[0])):
            cof_matrix[i][j] = (-1) ** (i + j) * determinant_two(minor(matrix, i, j))
    return cof_matrix

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    return transpose(cofactor(matrix))

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return dot_prod(inverse(matrix), vector)

print(f"solve(A, B) = {solve(A, B)}")