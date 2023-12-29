f = open("network_nodes.csv", 'r')
next(f)

for line in f:
    items = line.rstrip("\n").split(";")

    num_attributes = len(items)
    i = 0
    j = 0
    insert_line = "INSERT INTO nodes VALUES ("
    while i < num_attributes:
        if num_attributes == 1:
            exit(1)
        item = items[i].replace("'", "''")
        insert_line = insert_line + "'" + item + "'"  # on ne met pas la virgule ici car ???a l'appliquerait ??? tous les attributs, pas seulement ??? g???o

        if i != num_attributes - 1:
            insert_line = insert_line + ", "
        i = i + 1
    
    insert_line = insert_line + ");"

    print(insert_line)
