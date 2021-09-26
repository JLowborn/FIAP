''' ML Glycemic index calculator '''

# Modules
from sklearn import tree    # Classify data

# Main Code
features = [
    [90, 120, 132], [55, 110, 129], [100, 50, 120], [80, 130, 140], [70, 140, 112],         # Normal
    [99, 139, 199], [68, 120, 105], [74, 105, 89],[81, 140, 100], [110, 140, 120],         # Normal
    [101, 145, 156], [110, 160, 189], [120, 180, 135], [126, 190, 186], [111, 199, 145],    # Decreased
    [100, 140, 199], [120, 200, 155], [115, 189, 155], [110, 175, 160], [100, 168, 150],     # Decreased
    [130, 250, 200], [147, 237, 200], [150, 500, 250], [150, 290, 210], [125, 450, 250],    # Diabetes
    [200, 200, 200], [200, 250, 200], [130, 179, 251], [127, 201, 201], [182, 200, 320],    # Diabetes 
    [127, 202, 202], [130, 250, 210], [140, 220, 251], [150, 265, 290], [182, 296, 320]     # Diabetes
    ]    

# 0 Normal
# 1 Decreased
# 2 Mellitus diabetes
labels = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2
        ]

# Classifier
classif = tree.DecisionTreeClassifier()
classif.fit(features, labels)

j = int(input('[+] Enter the glycemic index while fasting: '))          # Fasting
s = int(input('[+] Enter the value of the post-overload glycemic index: '))  # Overload
c = int(input('[+] Enter the day-to-day glycemic index value: '))    # Casual

if j < 55 or s < 55 or c < 55: print('[!] Values are too low!') 

result = classif.predict([[j, s, c]])

if result == 0:
    print('[*] Your glycemic index looks normal')
elif result == 1:
    print('[*] Your glycemic index looks higher than normal')
else:
    print('[*] Your glycemic index is at extreme levels, you may have Mellitus diabetes')
