def read_inputFile():
    filePath = "C:\\Users\\tyann\\OneDrive\\Documents\\Concordia University\\2024 - 08 [Winter]\\AERO 290\\Model\\inputs_nebula.txt"
    with open(filePath) as inputFile:
        inputFile.readline() #skip header
        parameters = dict()
        while True:
            line = inputFile.readline()
            if len(line) > 1:
                if line != "End_of_File":
                    split = line.split()
                    parameters[split[0]] = float(split[2])
                else:
                    break
    return parameters