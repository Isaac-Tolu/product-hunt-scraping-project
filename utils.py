
def to_csv(data:list[dict]):
    """Given a list of dictionaries, create a CSV file from the data"""

    keys = data[0].keys()
    header = ','.join(keys)

    with open("result.csv", 'w') as f:
        f.write(header+'\n')

    for i in data:
        #row = ','.join(i.values())
        row = ""
        for val in i.values():
            row = row + str(val) + ','
        with open("result.csv", 'a') as f:
            f.write(row.rstrip(',')+'\n')

