#!/usr/bin/env python3
"""
Final Boolean Coercion Pattern Test
Pattern: (pref | default('true') | string | lower) == 'true'

This is the cleanest, simplest, most robust pattern for boolean preferences.
"""

from jinja2 import Environment


def test_pattern(default_value="true"):
    """Test the boolean coercion pattern with given default."""
    env = Environment()
    template_str = (
        f"{{{{ (pref | default('{default_value}') | string | lower) == 'true' }}}}"
    )
    template = env.from_string(template_str)

    test_cases = [
        ("Boolean True", True, True),
        ("Boolean False", False, False),
        ("String 'true'", "true", True),
        ("String 'false'", "false", False),
        ("String 'TRUE'", "TRUE", True),
        ("Empty string", "", False),
        ("Undefined", None, default_value == "true"),  # Uses default
        ("Partial 't'", "t", False),
        ("Partial 'fa'", "fa", False),
        ("Number 1", 1, False),
    ]

    print(f"\nPattern: (pref | default('{default_value}') | string | lower) == 'true'")
    print("=" * 70)

    passed = 0
    failed = 0

    for name, value, expected in test_cases:
        if value is None:
            result = template.render()
        else:
            result = template.render(pref=value)
        result_bool = result == "True"
        status = "✓" if result_bool == expected else "✗"

        if result_bool == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} {name:20s} → {result_bool:5} (expected {expected})")

    return passed, failed


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("FINAL BOOLEAN COERCION PATTERN TEST")
    print("=" * 70)

    # Test default='true' (for preferences like pref_use_overdue_grouping)
    print("\n📋 Testing preferences that default to TRUE")
    p1, f1 = test_pattern("true")

    # Test default='false' (for preferences like pref_exclude_approved)
    print("\n📋 Testing preferences that default to FALSE")
    p2, f2 = test_pattern("false")

    passed_count = p1 + p2
    failed_count = f1 + f2

    print("\n" + "=" * 70)
    print(f"RESULTS: {passed_count} passed, {failed_count} failed")

    if failed_count == 0:
        print("\n✅ SUCCESS! Pattern is clean, simple, and robust.")
        print("\n💡 Key Benefits:")
        print("   • One-line pattern: (pref | default('X') | string | lower) == 'true'")
        print("   • Explicit defaults: Clear what undefined values become")
        print("   • Handles all edge cases: boolean, string, empty, undefined, partial")
        print("   • More readable: Direct comparison is clearer than membership test")
        print("\n⚠️  Known Limitation:")
        print("   • Live-editing syntax error when clearing value (HA UI limitation)")
        print("   • Error disappears once value is completed - not fixable in template")
    else:
        print("\n❌ FAILED - Pattern needs adjustment")

    print("=" * 70)
