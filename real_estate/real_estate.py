import xmlrpc.client

db = "db_enterprise"
username = "admin"
password = "admin"

common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if uid:
    print ("Connection Successful")

models = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/object')



#create = models.execute_kw(db, uid, password, 'estate.property', 'create', [{'name':'sardardham','expected_price':1100000,'description':'Record creted through xmlrpc'}])
#print ("\n\nrecord created successfully ::: ")

#search = models.execute_kw(db, uid, password, 'estate.property', 'search', [[['state','=','new']]] )
#print(search)

#read = models.execute_kw(db, uid, password, 'estate.property', 'read', [search],{'fields': ['name','description','expected_price']})
#print(read)

#write = models.execute_kw(db, uid, password, 'estate.property', 'write', [[create], {'name': "XMLRPC property"}])
#print(write) ` `

search_read = models.execute_kw(db, uid, password, 'estate.property', 'search_read', [[], ['name', 'description', 'state']])
print(search_read)



