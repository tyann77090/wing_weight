def read_airfoil_coordinates(airfoilFilePath):
    with open(airfoilFilePath) as airfoilFile:
        airfoilFile.readline() #skip header
        airfoilCoordinates = []
        while True:
            line = airfoilFile.readline()
            if len(line) > 1:
                if line != "End_of_File":
                    split = line.split()
                    airfoilCoordinates.append([float(split[0]), float(split[1])])
                else:
                    break
    return airfoilCoordinates