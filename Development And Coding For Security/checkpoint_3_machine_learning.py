'''
FIAP
Defesa Cibernética - 1TDCF - 2021
Development e Coding for Security
Prof. Ms. Fábio H. Cabrini
Atividade: Check Point 3  
Alunos
Carlos Washington - RM87187
'''

# Modules
from sklearn import tree

# Main Code
features = [
    [90, 120, 132], [55, 110, 129], [100, 50, 120], [80, 130, 140], [70, 140, 112],         # Normal
    [99, 139, 199], [68, 120, 105], [74, 105, 89],[81, 140, 100], [110, 140, 120],         # Normal
    [101, 145, 156], [110, 160, 189], [120, 180, 135], [126, 190, 186], [111, 199, 145],    # Diminuida
    [100, 140, 199], [120, 200, 155], [115, 189, 155], [110, 175, 160], [100, 168, 150],     # Diminuida
    [130, 250, 200], [147, 237, 200], [150, 500, 250], [150, 290, 210], [125, 450, 250],    # Diabete
    [200, 200, 200], [200, 250, 200], [130, 179, 251], [127, 201, 201], [182, 200, 320],    # Diabete 
    [127, 202, 202], [130, 250, 210], [140, 220, 251], [150, 265, 290], [182, 296, 320]     # Diabete   
    ]    

# 0 Normal
# 1 Diminuida
# 2 Diabete Mellitus
labels = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2
        ]
        
# Classificador
classif = tree.DecisionTreeClassifier()
classif.fit(features, labels)

j = int(input('[+] Informe o índice glicêmico durante o jejum: '))          # Jejum
s = int(input('[+] Informe o valor do índice glicêmico pós-sobrecarga: '))  # Sobrecarga
c = int(input('[+] Informe o valor do índice glicêmico do dia-a-dia: '))    # Casualmente

if j < 55 or s < 55 or c < 55: print('[!] Os valores estão muito baixos!') 

result = classif.predict([[j, s, c]])

if result == 0:
    print(f'[*] Seu índice glicêmico está em nível normal')
elif result == 1:
    print(f"[*] Seu índice glicêmico está em nível alto")
else:
    print(f"[*] Seu índice glicêmico está em níveis extremos, pode ser que você esteja com diabetes de Mellitus")
