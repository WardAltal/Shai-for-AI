user_input = input("Enter numerical grades separated by commas (e.g., 95,85,74): ")

grades = list(map(int, user_input.split(',')))

letter_grades = list(map(lambda grade: "A" if grade >= 90 else
                                     "B" if grade >= 80 else
                                     "C" if grade >= 70 else
                                     "D" if grade >= 60 else
                                     "F", grades))

print("Numerical Grades:", grades)
print("Letter Grades:", letter_grades)
