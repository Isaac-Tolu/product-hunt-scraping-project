import csv

def to_csv(data:list[dict]):
    """Given a list of dictionaries, create a CSV file from the data"""

    with open('result.csv', 'w', newline='') as csvfile:
        fieldnames = data[0].keys()

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in data:
            writer.writerow(i)

