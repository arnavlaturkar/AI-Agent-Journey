import json

memory = ["find Tesla stock data", "analyze last 5 years"]

with open("memory.json", "w") as f:
    json.dump(memory, f)

print("memory saved!")

with open("memory.json", "r") as f:
    loaded_memory = json.load(f)

print(loaded_memory)
print(type(loaded_memory))