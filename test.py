import json

def load_data():
    with open("students.json" , "r") as f:
        data = json.load(f)
    return data


def show_sub(id):
    data = load_data()
    
    print(data[id].get("subjects"))
    
show_sub("1")