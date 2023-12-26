f = open("network_walk.csv", 'r')
next(f)

for line in f:
    items = line.rstrip("\n").split(";")

    num_attributes = len(items)
    i = 0
    j = 0
    insert_line = "INSERT INTO walk VALUES ("
    while i < num_attributes:
        if num_attributes == 1:
            exit(1)
        item = items[i].replace("'", "''")
        insert_line = insert_line + "'" + item + "'"  # on ne met pas la virgule ici car ???a l'appliquerait ??? tous les attributs, pas seulement ??? g???o
        if i == num_attributes-1 :
            lst = items[i].split(",")
            insert_line = insert_line + ", '{"
            insert_line2 = ", '{"

            for j in range (0,len(lst)):
                coco = lst[j].split(":")
                if(j==len(lst)-1):
                    insert_line = insert_line + coco[0]   # la virgule sert ??? s???parer les diff???rents attributs
                    insert_line = insert_line + "}'"
                    insert_line2 = insert_line2 + coco[1]
                    insert_line2 = insert_line2 + "}'"
                else:
                    insert_line = insert_line + coco[0] + ","
                    insert_line2 = insert_line2 + coco[1] + ','   # la virgule sert ??? s???parer les diff???rents attributs  # la virgule sert ??? s???parer les diff???rents attributs

            insert_line = insert_line + insert_line2

        if i != num_attributes - 1:
            insert_line = insert_line + ", "
        i = i + 1
    
    insert_line = insert_line + ");"

    print(insert_line)

