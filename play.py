factors = ['description', 'location', 'status', 'userid', 'date_applied', 'url', 'platform', 'salary', 'contract_length', 'company_size']

str = ''

for i in factors:
    str += "'{}': data['{}'],".format(i, i)
    str += '\n'

print(str)
