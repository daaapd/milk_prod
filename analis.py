# -*- coding: utf8 -*-
def analis_image():
    import os
    import sqlite3
    import modules
    path = './upload/'
    conn = sqlite3.connect('./db/mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("delete from milk")
    conn.commit()

    #print(basedir)
    #basedir = os.getcwd()
    #print(os.getcwd())
    #print(basedir)
    #print(os.listdir(path))
    for filename_ in os.listdir(path):
        t = []
        templ = []
        temp = {}
        price = {}
        if filename_.find('jpg') != -1:
            group = filename_[0:filename_.find('(')]
            print(filename_)
            try:
                temp, price = modules.find_milk(path, filename_)
                #print(path+filename_)
                print(price)
            except Exception as ex:
                print(filename_,ex, ' Нету товаров')
                continue
            templ.append(filename_)
            templ.append(group)

            for i in range(0, 9):
                templ.append(temp[i])
                templ.append(price.setdefault(i + 9, 'нет цены'))
                # print(i,temp[i])
            tupl = tuple(templ)
            t.append(tupl)
            # print(templ)
            cursor.executemany("INSERT INTO milk VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", t)
            # Сохраняем изменения
            conn.commit()
    conn.close()
    import csv

    import sqlite3

    path = './upload/'
    filename = 'wub.csv'
    conn = sqlite3.connect('./db/mydatabase.db')
    # conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sqlSelect ="SELECT group_,sum(p1),sum(p2),sum(p3),sum(p4),sum(p5),sum(p6),sum(p7),sum(p8),sum(p9) FROM milk group by group_"
    #",min(c1),min(c2),min(c3),min(c4),min(c5),min(c6),min(c7),min(c8),min(c9)  "
    try:
     # Execute query.
     cursor.execute(sqlSelect)
     # Fetch the data returned.
     results = cursor.fetchall()
     # Extract the table headers.
     #headers = [i[0] for i in cursor.description]
     headers = ['Дата-Магазин','Фруаете, йогурт, персик-груша','Фруаете, йогурт, клубника-киви', 'Волжские просторы, масло сливочное','Волжские просторы, молоко пастеризованное 2,5%','Волжские просторы, творог обезжиренный 0,5%','Волжские просторы, творог  9%','Волжские просторы, кефир  2,5%','Волжские просторы, сметана  25%','Вкуснотеево, молоко пастеризованное 3,2%']
     # Open CSV file for writing.
     csvFile = csv.writer(open(path + filename,'w+',encoding='cp1251',errors='replace', newline=''),
                               delimiter=';', lineterminator='\r\n',
                               quoting=csv.QUOTE_ALL, escapechar='\\')
     # Add the headers and data to the CSV file.
     csvFile.writerow(headers)
     csvFile.writerows(results)
     # Message stating export successful.
     print("Data export successful.")
    except sqlite3.DatabaseError as e:
            # Message stating export unsuccessful.
            print("Data export unsuccessful.",e)
            quit()

    finally:
      # Close database connection.
      conn.close()



