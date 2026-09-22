from backend.graph import weather_graph


print("\n" + "=" * 60)
print("SESSION MEMORY TEST")
print("=" * 60)


# --------------------------------------------------
# FIRST MESSAGE
# --------------------------------------------------

first_message = (
    "Can I go running in Bangalore today?"
)

first_result = weather_graph.invoke(
    {
        "user_message": first_message
    }
)

print("\nFIRST MESSAGE")
print(first_message)

print("\nActivity:")
print(first_result.get("activity"))

print("\nLocation:")
print(first_result.get("location"))

print("\nTime:")
print(first_result.get("time_reference"))

print("\nResponse:")
print(first_result.get("response"))


# --------------------------------------------------
# SECOND MESSAGE
# --------------------------------------------------

second_message = (
    "What about this evening?"
)

second_result = weather_graph.invoke(
    {
        "user_message": second_message,
        "previous_activity": first_result.get(
            "previous_activity"
        ),
        "previous_location": first_result.get(
            "previous_location"
        ),
    }
)

print("\n" + "-" * 60)

print("\nSECOND MESSAGE")
print(second_message)

print("\nActivity:")
print(second_result.get("activity"))

print("\nLocation:")
print(second_result.get("location"))

print("\nTime:")
print(second_result.get("time_reference"))

print("\nResponse:")
print(second_result.get("response"))


# --------------------------------------------------
# CHECKS
# --------------------------------------------------

assert second_result.get("activity") == "running"

assert second_result.get("location") is not None

assert second_result.get(
    "time_reference"
) == "this evening"


print("\n" + "=" * 60)
print("SESSION MEMORY TEST PASSED")
print("=" * 60)