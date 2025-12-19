def calculate_bmr(weight, height, age, gender):
    if gender.lower() == "male":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
def calculate_macros(calories):
    protein = calories * 0.30 / 4
    carbs = calories * 0.45 / 4
    fat = calories * 0.25 / 9
    return protein, carbs, fat