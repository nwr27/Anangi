import json

data = """{
  "name": "John",
  "age": 30,
  "isStudent": false,
  "address": {
    "street": "123 Main St",
    "city": "Anytown"
  },
  "courses": ["Math", "Science"]
}"""

parsed_data = json.loads(data)
print(parsed_data["name"])  # Output: John
print(parsed_data["age"])  # Output: 30
print(parsed_data["isStudent"])  # Output: False
print(parsed_data["address"]["street"])  # Output: 123 Main St
print(parsed_data["courses"][0])  # Output: Math
