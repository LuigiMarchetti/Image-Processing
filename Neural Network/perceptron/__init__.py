# Luigi Garcia Marchetti

import pandas as pd

data_training = {
    'Atleta': ['Neymar', 'Messi', 'Barichello', 'Massa'],
    'Ciência': [1, 1, 1, 1],
    'Física': [0, 0, 1, 1],
    'Filosofia': [0, 1, 0, 1],
    'Classe': [0, 0, 1, 1]
}

df = pd.DataFrame(data_training)
print("Training:")
print(df)

data_matrix = df.drop(columns='Atleta').values

likes_science = data_matrix[:, 0]
likes_physics = data_matrix[:, 1]
likes_philosophy = data_matrix[:, 2]
classes = data_matrix[:, 3]

def activation_function(e1, weight1, e2, weight2, e3, weight3):
    return e1 * weight1 + e2 * weight2 + e3 * weight3

weight1 = 0
weight2 = 0
weight3 = 0
print("\nInitial Weights:", weight1, weight2, weight3)
for athlete in data_matrix:
    athlete_class = athlete[3]
    class_resulted = activation_function(athlete[0], weight1, athlete[1], weight2, athlete[2], weight3)
    if class_resulted != athlete_class:
        if class_resulted == 1:
            weight1 -= athlete[0]
            weight2 -= athlete[1]
            weight3 -= athlete[2]
        elif class_resulted == 0:
            weight1 += athlete[0]
            weight2 += athlete[1]
            weight3 += athlete[2]

print("Weights after training:", weight1, weight2, weight3)

data_test = {
    'Participante': ['Jogador 1', 'Jogador 2', 'Piloto 1', 'Piloto 2'],
    'Ciência': [0, 0, 0, 0],
    'Física': [0, 0, 1, 1],
    'Filosofia': [0, 1, 1, 0],
    'Classe': [0, 0, 1, 1]
}

df = pd.DataFrame(data_test)
print("\n\nTest:")
print(df)

print("\nResults in test:")
for athlete in df.values:
    athlete_name = athlete[0]
    athlete_class = athlete[4]
    class_resulted = activation_function(athlete[1], weight1, athlete[2], weight2, athlete[3], weight3)
    print(athlete_name, "\nExpected value: " + str(athlete_class), "\nReturned value: " + str(class_resulted), "\n")
