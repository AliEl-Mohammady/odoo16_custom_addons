url = "http://localhost:8032"
db = 'school'
username = 'admin'
# password = 'f46b11d99a1597755b5a16276b08ec1af4627fa1'    	#we can use API key to connect to database insteed of password
password = 'admin'
full_path='http://localhost:8032/xmlrpc/common'
import xmlrpc.client

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/common')
versiion = common.version()
print("details", versiion)

uid = common.authenticate(db, username, password, {})
print("Uid", uid)

# search method
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
                # models.execute(db, uid, password, model, method, domain)
list_partner_ids=models.execute(db, uid, password, 'res.partner', 'search', ['|',('phone', '!=', False),('mobile', '!=', False)],)
# list_partner_ids=models.execute_kw(db, uid, password, 'res.partner', 'search', [[['phone', '!=', False]]],{'offset': 2, 'limit': 5})
print(list_partner_ids)

count_partner_ids=models.execute(db, uid, password, 'res.partner', 'search_count', ['|',('phone', '!=', False),('mobile', '!=', False),])
print(count_partner_ids)

# read method
partner_records = models.execute(db, uid, password, 'res.partner', 'read', list_partner_ids,["id","name"])
print(partner_records)
for rec in partner_records :
    print(rec["id"],rec["name"])
# fields_get method
fields=models.execute(db, uid, password, 'res.partner', 'fields_get', [],['string', 'help', 'type'])
print(fields)

# search_read method
count_partner_ids=models.execute(db, uid, password, 'res.partner', 'search_read', ['|',('phone', '!=', False),('mobile', '!=', False),])
# print(count_partner_ids)

#create method
create_partner= models.execute(db, uid, password, 'res.partner', 'create', [{'name': "Ali El Mohammady","phone":"01025893594"}])
print("create_partner",create_partner)

#write method
models.execute(db, uid, password, 'res.partner', 'write', create_partner, {'name': "3li El-mohamady from odoo xml-rpc","phone":"0100000000000"})
partner_records=models.execute(db, uid, password, 'res.partner', 'read', create_partner,['name', 'phone',])
print(partner_records)

#unlink method
models.execute(db, uid, password, 'res.partner', 'unlink', create_partner)


# using any custom function in my model
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
data=models.execute(db, uid, password, 'school.profile', 'custom_function_to_xmlrpc', []) #using [] :for any parammeters inside function
print(data)


# Using sql query in xmlrpc
# xmlrpc_sql_query :this method defined in model used below
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object',allow_none=True)
data=models.execute(db, uid, password, 'school.profile', 'xmlrpc_sql_query', [], "select * from school_profile")
# data_2 = models.execute(db, uid, password, 'school.profile', 'xmlrpc_sql_query', [],
#                         "insert into school_profile(name) values('Ali from xmlrpc using query')")
print(data)
