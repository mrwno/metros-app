f = open("network_subway.csv", 'r')
next(f)

for line in f:
    items = line.rstrip("\n").split(";")

    num_attributes = len(items)
    i = 0
    j = 0
    insert_line = "INSERT INTO subway VALUES ("
    while i < num_attributes:
        if num_attributes == 1:
            exit(1)
        item = items[i].replace("'", "''")
        insert_line = insert_line + "'" + item + "'"  # on ne met pas la virgule ici car ç?a l'appliquerait à? tous les attributs, pas seulement à? gé?o
        if i == num_attributes-1 :
            lst = items[i].split(",")
            insert_line = insert_line + ", '{"
            print("mon lst est",lst)
            print("la taille de mon tableau est",len(lst))
            for j in range (0,len(lst)):
                print("Mon j est",j)
                coco = lst[j].split(":")
                print("mon lst est",lst)
                print("mon coco est",coco[j])
                insert_line = insert_line + coco[0] + ","  # la virgule sert à? sé?parer les diffé?rents attributs
                if(j==len(lst)-1):
                    insert_line = insert_line + coco[1]   # la virgule sert à? sé?parer les diffé?rents attributs
                else:
                    insert_line = insert_line + coco[1] + ','   # la virgule sert à? sé?parer les diffé?rents attributs
                if(j==len(lst)-1):
                    insert_line = insert_line + "}'"

        if i != num_attributes - 1:
            insert_line = insert_line + ", "
        i = i + 1
    
    insert_line = insert_line + ");"

    print(insert_line)

