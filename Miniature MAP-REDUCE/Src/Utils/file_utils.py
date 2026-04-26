# function to convert the csv file into a map reducer digestable python object format

# importing libs
import csv

def load_csv(file_path):
    data = []
    
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Convert numeric fields
            row["HelpfulnessNumerator"] = int(row["HelpfulnessNumerator"])
            row["HelpfulnessDenominator"] = int(row["HelpfulnessDenominator"])
            row["Score"] = int(row["Score"])
            
            data.append(row)
    
    return data

