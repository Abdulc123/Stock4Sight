import json

def main():
    with open("stock_dict.json", "r") as file:
        data = json.load(file)
    
    reversed_data = {value: key for key, value in data.items()}

    with open("stock_dict.json", "w", encoding="utf-8") as file:
        json.dump(reversed_data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()