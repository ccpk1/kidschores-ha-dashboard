# Dashboard Testing Documentation

This directory contains test files and documentation for validating the KidsChores dashboard error handling and functionality.

## Files Overview

### `DASHBOARD_ERROR_HANDLING_COMPLETE.md`

**Purpose:** Complete documentation of all error handling improvements made to the dashboard.

**Contents:**

- Summary of all 16 card sections with validation
- Error message patterns and improvements
- Type coercion implementations
- Translation fallback system
- Testing instructions and verification steps
- Statistics and technical implementation details

**Use:** Reference document for understanding what was implemented and why.

---

### `test_validation_snippet.jinja2`

**Purpose:** Quick validation tests using Jinja2 template syntax.

**How to Use:**

1. Open Home Assistant
2. Go to Developer Tools → Template
3. Copy ONE test section from the file
4. Paste into template editor and click "Render"

**What It Tests:**

- ✅ Wrong kid name detection (should show validation error)
- ✅ Correct kid name validation (should pass)
- ✅ Type coercion for preferences (string '2' → int 2)
- ✅ Translation fallbacks (missing keys → English defaults)

**Expected Results:** All tests show ✅ PASS or ✅ SUCCESS

---

### `test_validation.jinja2`

**Purpose:** Comprehensive Jinja2 template validation testing with detailed output.

**How to Use:**

1. Open Home Assistant
2. Go to Developer Tools → Template
3. Copy and paste the entire file contents
4. Review the formatted test results

**What It Tests:**

- Entity existence checks for multiple kids
- Dashboard helper state validation
- Type coercion demonstrations
- Translation fallback behavior
- Detailed pass/fail reporting

**Expected Results:** Formatted table showing test status for each kid, plus type coercion and translation tests.

---

### `test_dashboard_validation.md`

**Purpose:** Detailed testing scenarios and step-by-step instructions.

**Contents:**

- Validation pattern explanation
- Complete list of all 16 protected cards
- Type coercion details for each card
- Step-by-step manual testing instructions
- Expected results for each test scenario

**Use:** Follow this guide when performing manual testing of the dashboard.

---

## Quick Testing Guide

### Fast Test (5 minutes)

1. Open `test_validation_snippet.jinja2` in Developer Tools → Template
2. Copy one test section and paste into template editor
3. Verify test shows ✅ or appropriate validation message
4. Done!

### Complete Manual Test (15 minutes)

1. Follow instructions in `test_dashboard_validation.md`
2. Test with wrong kid name: Change 'Kidname' to 'WrongName'
3. Test with correct kid name: Change 'Kidname' to 'Zoe' (or your kid's name)
4. Test preference type changes: Change `2` to `'2'` in preferences
5. Verify no errors in Home Assistant logs

### Comprehensive Test (30 minutes)

1. Read `DASHBOARD_ERROR_HANDLING_COMPLETE.md` for full context
2. Run both Developer Tools tests (`test_validation_snippet.jinja2` and `test_validation.jinja2`)
3. Follow all manual test scenarios in `test_dashboard_validation.md`
4. Check Home Assistant logs for any template rendering errors
5. Verify error messages display correctly for each card section

---

## Integration Testing Prerequisites

Before running tests, ensure:

- ✅ KidsChores integration is installed and configured
- ✅ At least one kid exists in the integration (e.g., Zoe, Max, or Lila)
- ✅ Dashboard helper sensor exists: `sensor.kc_<kidname>_ui_dashboard_helper`
- ✅ Dashboard file `kc_dashboard_all.yaml` is accessible

---

## What the Tests Validate

### 1. Entity Validation

- Dashboard helper sensor must exist for each kid
- Missing entities trigger user-friendly error messages
- Error messages guide users to fix configuration

### 2. Type Safety

- Preference variables automatically coerce to correct types
- String '2' converts to integer 2
- Invalid types don't break rendering

### 3. Translation Fallbacks

- Missing translation keys use English defaults
- No "err-xxx" strings displayed to users
- Graceful degradation in all languages

### 4. Error Message Quality

- Clear, actionable guidance for users
- Points to "User Configuration" section (not line numbers)
- Suggests checking integration settings
- Shows exact entity ID that's missing

---

## Debugging Failed Tests

### If `test_validation_snippet.jinja2` fails:

1. Check that KidsChores integration is loaded
2. Verify sensor.kc_zoe_ui_dashboard_helper exists (or Max/Lila)
3. Check entity registry in Settings → Devices & Services → Entities
4. Look for any disabled entities

### If manual dashboard test shows errors:

1. Verify 'Kidname' placeholder is changed to actual kid name
2. Check kid name spelling matches exactly (case-sensitive after normalization)
3. Ensure dashboard helper sensor exists for that kid
4. Check Home Assistant logs for template errors

### If type coercion test fails:

1. Verify preference variable has `| int(default=X)` filter
2. Check Jinja2 syntax is correct (no typos)
3. Test in Developer Tools → Template first

---

## Test Coverage

### Cards with Complete Validation (16/16)

1. Welcome Card
2. Chores Card
3. Rewards Card
4. Showcase Card
5. Cumulative Badge Card
6. General Badge Card
7. Achievements Card
8. Challenges Card
9. Parent Dashboard
10. Approval Actions Card
11. Admin Actions Card
12. Plus/Minus Points
13. Plus/Minus Bonus
14. Plus/Minus Points Buttons
15. Plus/Minus Penalty
16. 7 Day Activity Log

### Type Coercion Coverage (4 cards, 18 variables)

- **Chores Card:** 10 preferences
- **Rewards Card:** 4 preferences
- **Showcase Card:** 1 preference
- **Approval Actions:** 1 preference

---

## Expected Test Results

### All Tests Pass ✅

- No Home Assistant log errors
- User-friendly error messages when kid name wrong
- Dashboard renders correctly with valid kid name
- Type changes handled gracefully
- Translations fall back to English when needed

### What Success Looks Like

1. Wrong kid name → Shows error card with fix instructions
2. Correct kid name → Dashboard displays all data normally
3. Type errors → Automatic conversion, no rendering failure
4. Missing translations → English text shown instead of "err-xxx"

---

## Contributing Test Cases

When adding new dashboard cards:

1. Add validation block (check dashboard_helper exists)
2. Add skip_render flag
3. Add type coercion for any preference variables
4. Update test documentation
5. Test with wrong kid name to verify error message

---

## Support

If you encounter issues with testing:

1. Check this README for troubleshooting steps
2. Review `DASHBOARD_ERROR_HANDLING_COMPLETE.md` for implementation details
3. Test in Developer Tools → Template for isolated debugging
4. Check Home Assistant logs for specific error messages
5. Verify KidsChores integration is properly configured
