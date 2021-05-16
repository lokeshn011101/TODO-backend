import sys
n = len(sys.argv)

# checking the number of command line arguments
if n < 2:
    print("No file specified!\nAborting...")
elif n > 2:
    print("Too many files specified!\nAborting...")
else:
    # opening the file in read mode
    file = open(sys.argv[1], 'r')
    print()

    # Initialising all the arrays required for the lists
    highestMarks = [-99999, -99999, -99999, -99999, -99999, -99999]
    toppers = ['', '', '', '', '', '']
    maxMarks = [0, 0, 0]
    maxStudents = ["", "", ""]
    subjects = []

    # This loop executes for at most the number of lines in the file
    # So the time taken by this loop is = O(n * len(line)), where n is the number of lines
    for line in file:
        # Removing new line character at the end of the string. The time complexity for this statement is O(len(line))
        line = line[:-1]

        # Splitting each line from the file with ',' as delimiter. The time complexity for this statement is O(len(line))
        line = line.split(',')

        if line[0] != 'Name':
            # Converting all the marks which are strings to integers.
            # The time complexity for this statement is O(1), which is constant, as there only 7 subjects.
            for j in range(1, 7):
                line[j] = int(line[j])

            student = line[0]

            # Each student's mark is verified with the help of toppers and highestMarks lists.
            # The time complexity for this statement is O(numberOfSubjects).
            for i in range(1, len(line)):
                if highestMarks[i-1] < line[i]:
                    toppers[i-1] = student
                    highestMarks[i-1] = line[i]

            # The sum of all the marks of the current student is taken and compared with the top 3 rank holders with the help of maxMarks and maxStudents list.
            # The time complexity for this statement is O(numberOfSubjects).
            totalMarks = sum(line[1:])

            # All the other statements like insert, pop  take O(1) operation as only first 3 rank holders are being considered.
            # If all the ranks of the students is required, then a separate list for storing the names and the marks can be created and the marks can be appended to it and at the end the sorted list can be printed.
            if totalMarks > maxMarks[0] and totalMarks > maxMarks[1] and totalMarks > maxMarks[2]:
                maxMarks.insert(0, totalMarks)
                maxStudents.insert(0, student)
                maxMarks.pop()
                maxStudents.pop()
            elif totalMarks < maxMarks[0] and totalMarks > maxMarks[1] and totalMarks > maxMarks[2]:
                maxMarks.insert(1, totalMarks)
                maxStudents.insert(1, student)
                maxMarks.pop()
                maxStudents.pop()
            elif totalMarks < maxMarks[0] and totalMarks < maxMarks[1] and totalMarks > maxMarks[2]:
                maxMarks[2] = totalMarks
                maxStudents[2] = student
        else:

            # As the first row in the file consists of only the name of the subjects, it is append to the subjects array here.
            # The time complexity for this statement is O(numberOfSubjects).
            for i in range(1, len(line)):
                subjects.append(line[i])

    # Printing the results
    for i in range(len(subjects)):
        print(
            f"Topper in {subjects[i]} is {toppers[i]} with {highestMarks[i]} marks\n")

    print(
        f"Best students in the class are ({maxStudents[0]}, {maxStudents[1]}, {maxStudents[2]}) with marks as ({maxMarks[0]}, {maxMarks[1]}, {maxMarks[2]}) respectively\n")


# Hence the total time complexity can be determined by considering the maximum time taken in each segment of the code
# The total time complexity is = O(n * numberOfSubjects), which is the maximum time taken among all the three portions of the code
# If O(numberOfSubjects) is considered as a constant time operation, then the total time complexity = O(n).
# So the final time complexity is O(n). (Only if O(numberOfSubjects) is considered as a constant time operation, else it is O(n * numberOfSubjects)).
