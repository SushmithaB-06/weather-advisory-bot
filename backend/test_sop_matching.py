from backend.nodes.sop_matcher import match_sop


def run_test(name, state):
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    result = match_sop(state)

    print("\nMatched SOP:")
    print(result.get("matched_sop"))

    print("\nAll Matching SOPs:")
    for sop in result.get("matched_sops", []):
        print(
            f"- {sop.get('id')} "
            f"| severity={sop.get('severity')}"
        )

    print("\nReason:")
    print(result.get("sop_match_reason"))

    return result


# ============================================================
# TEST 1: SOP DEFINITELY MATCHES
# ============================================================

test_1 = {
    "activity": "running",
    "relevant_weather": {
        "period": "current",
        "temperature": 40,
        "wind_speed": 10,
        "precipitation": 0,
        "weather_code": 0,
        "uv_index": 5,
    },
}

result_1 = run_test(
    "TEST 1 - DEFINITE SOP MATCH",
    test_1,
)

assert result_1.get("matched_sop") is not None
assert result_1["matched_sop"]["id"] == "EXERCISE_HEAT_001"

print("\nPASS: Heat SOP matched correctly.")


# ============================================================
# TEST 2: MULTIPLE SOPs MATCH
# ============================================================

test_2 = {
    "activity": "running",
    "relevant_weather": {
        "period": "current",
        "temperature": 40,
        "wind_speed": 10,
        "precipitation": 20,
        "weather_code": 0,
        "uv_index": 5,
    },
}

result_2 = run_test(
    "TEST 2 - MULTIPLE SOP MATCH",
    test_2,
)

assert len(result_2.get("matched_sops", [])) >= 2

assert result_2["matched_sop"]["severity"] == "high"

print(
    "\nPASS: Multiple SOPs matched and "
    "highest severity SOP was selected."
)


# ============================================================
# TEST 3: NO SOP MATCH
# ============================================================

test_3 = {
    "activity": "running",
    "relevant_weather": {
        "period": "current",
        "temperature": 25,
        "wind_speed": 10,
        "precipitation": 0,
        "weather_code": 0,
        "uv_index": 3,
    },
}

result_3 = run_test(
    "TEST 3 - NO SOP MATCH",
    test_3,
)

assert result_3.get("matched_sop") is None
assert len(result_3.get("matched_sops", [])) == 0

print("\nPASS: No-SOP case handled correctly.")


# ============================================================
# FINAL RESULT
# ============================================================

print("\n")
print("=" * 60)
print("ALL SOP MATCHING TESTS PASSED")
print("=" * 60)