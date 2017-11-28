from __future__ import print_function
import cx_Oracle

con = cx_Oracle.connect('hr/hr@127.0.0.1/orcl')

#
# db=my.connect(host="localhost",
# user="saurabh",
# passwd="saurabh",
# db="test"
# )

id=[1,2,3]
name=['a','b','c']
place=['dewas','indore','ujjain']

l=[{'price': ' 18000', 'heading': '1 BHK, Residential Apartment for rent in Kadubeesanahalli', 'super_buildup': '600 Sq.Ft. '}, {'price': ' 11000', 'heading': '1 Bedroom, Independent House/Villa for rent in Kaverappa Layout', 'super_buildup': '600 Sq.Ft. '}, {'price': ' 8500', 'heading': '1 BHK, Residential Apartment for rent in Kadubeesanahalli', 'super_buildup': '600 Sq.Ft. '}, {'price': ' 13000', 'heading': '1 Bedroom, Independent House/Villa for rent in Kadubeesanahalli', 'super_buildup': '1200 Sq.Ft. '}, {'price': ' 35000', 'heading': '2 BHK, Residential Apartment for rent in Kaverappa Layout', 'super_buildup': '1400 Sq.Ft. '}]


list=[]
for i in range(0,id.__len__()):
    list.append([id[i],name[i],place[i]])

print(list)
print(l.__len__())



# # Connect mysql server
# cursor = db.cursor()
# sql = "insert into test3(id,a,b)VALUES(%s,%s,%s)"
# number_of_rows = cursor.executemany(sql,list)
# db.commit()
#
# db.close()

cur = con.cursor()
cur.bindarraysize = 7
cur.setinputsizes(int, 20)
cur.executemany("insert into test3(id,name,place) values (:1, :2,:3)", list)

con.commit()

# cur = con.cursor()
# cur.bindarraysize = 7
# cur.setinputsizes(int, 20)
# for i in range(0,l.__len__()):
#     cur.execute("insert into test4(price,heading) values (l[i]['price'],l[i]['heading'])", list)
#
# con.commit()

# Now query the results back

# cur2 = con.cursor()
# cur2.execute('select * from test3')
# res = cur2.fetchall()
# print(res)
#
# cur.close()
# cur2.close()
con.close()
