from backend.nodes.location import extract_location_and_activity


result = extract_location_and_activity({
    "user_message": "Is it safe to go running in Bangalore today?"
})

print("\n========== LOCATION TEST ==========")
print(result)
print("===================================\n")