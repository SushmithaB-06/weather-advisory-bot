from backend.state import WeatherBotState


def extract_location_and_activity(
    state: WeatherBotState,
) -> dict:

    message = state["user_message"].lower()

    # --------------------------------------------------
    # Previous session context
    # --------------------------------------------------

    previous_location = state.get(
        "previous_location"
    )

    previous_activity = state.get(
        "previous_activity"
    )

    # --------------------------------------------------
    # Activity detection
    # --------------------------------------------------

    activity = None

    if any(word in message for word in [
        "running",
        "run",
        "jogging",
        "jog",
    ]):
        activity = "running"

    elif any(word in message for word in [
        "cycling",
        "cycle",
        "biking",
        "bike",
    ]):
        activity = "cycling"

    elif "picnic" in message:
        activity = "picnic"

    elif any(word in message for word in [
        "drive",
        "driving",
    ]):
        activity = "driving"

    elif any(word in message for word in [
        "travel",
        "travelling",
        "traveling",
    ]):
        activity = "travel"

    # --------------------------------------------------
    # Use previous activity for follow-up questions
    # --------------------------------------------------

    if not activity:
        activity = previous_activity

    # --------------------------------------------------
    # Time detection
    # --------------------------------------------------

    time_reference = "today"

    if "tomorrow" in message:
        time_reference = "tomorrow"

    elif "this evening" in message:
        time_reference = "this evening"

    elif "tonight" in message:
        time_reference = "tonight"

    elif "this afternoon" in message:
        time_reference = "this afternoon"

    elif "morning" in message:
        time_reference = "morning"

    # --------------------------------------------------
    # Location detection
    # --------------------------------------------------

    location = None

    known_locations = [
        "bangalore",
        "bengaluru",
        "mysore",
        "mysuru",
        "mumbai",
        "delhi",
        "hyderabad",
        "chennai",
        "pune",
        "kolkata",
    ]

    for city in known_locations:

        if city in message:
            location = city
            break

    # --------------------------------------------------
    # Use previous location for follow-up questions
    # --------------------------------------------------

    if not location:
        location = previous_location

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    if not activity:

        return {
            "error": (
                "Could not identify the outdoor activity."
            )
        }

    if not location:

        return {
            "activity": activity,
            "time_reference": time_reference,
            "error": (
                "No location was identified."
            ),
        }

    return {
        "location": location,
        "activity": activity,
        "time_reference": time_reference,

        # Save context for the next message
        "previous_location": location,
        "previous_activity": activity,
    }