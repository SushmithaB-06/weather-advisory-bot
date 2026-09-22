from backend.graph import weather_graph


test_message = (
    "Can I go running in Bangalore today?"
)


result = weather_graph.invoke(
    {
        "user_message": test_message
    }
)


print("\n================================")
print("WEATHER ADVISORY BOT TEST")
print("================================\n")

print("User:")
print(test_message)

print("\nResponse:")
print(result.get("response"))

print("\nActivity:")
print(result.get("activity"))

print("\nLocation:")
print(result.get("location"))

print("\nTime:")
print(result.get("time_reference"))

print("\nRelevant Weather:")
print(result.get("relevant_weather"))

print("\nMatched SOP:")
print(result.get("matched_sop"))

print("\nMatch Reason:")
print(result.get("sop_match_reason"))

print("\n================================\n")