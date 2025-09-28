def data_str(data:str):
    if 'T' in data:
        x = data.split('T')
        data_01 = x[0].split('-')
        data_01_x = []
        for y in reversed(data_01):
            data_01_x.append(y)
        data_f = ""
        for i in range(len(data_01_x)):
            if i+1>=len(data_01_x):
                data_f+=data_01_x[i]
                break
            data_f+=f'{data_01_x[i]}/'
        data = f'{data_f} {x[1]}'
    else:
        x = data.split(' ')
        data_01 = x[0].split('-')
        data_01_x = []
        for y in reversed(data_01):
            data_01_x.append(y)
        data_f = ""
        for i in range(len(data_01_x)):
            if i+1>=len(data_01_x):
                data_f+=data_01_x[i]
                break
            data_f+=f'{data_01_x[i]}/'
        data = f'{data_f} {x[1][:5]}'
    return data

b = data_str("2025-09-01T17:32")
a = data_str("2025-09-27 17:34:48.793571")

print(a)
print(b)
