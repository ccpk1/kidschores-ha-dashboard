# KidsChores HA Dashboard - AI Agent Guide

ONLY FOR DASHBOARD AGENT USE - DO NOT USE UNLESS ASSIGNED DASHBOARD TASK

**Fully-featured Home Assistant dashboard UI** for [KidsChores Integration](https://github.com/ad-ha/kidschores-ha). Single YAML file (`kc_dashboard_all.yaml`, 1919 lines) with Jinja2 templates that render kid & parent control panels via auto-entities cards.

## Critical Architecture: Dashboard Helper Sensor (v0.5.0+)

The `sensor.kc_<kid>_ui_dashboard_helper` is the **single source of truth**:

- **Pre-sorted entity lists**: `chores`, `rewards`, `bonuses`, `penalties`, `achievements`, `challenges`, `badges` — backend computes sorting/filtering once, frontend just iterates
- **`ui_translations` dict**: All 40+ localization keys from backend integration JSON (no language-specific YAML variants needed)
- **Aggregated metrics**: Badge maintenance, achievement progress, reward claim counts

**Why?** Eliminates expensive frontend list iterations. Missing "err-\*" strings? Dashboard helper sensor attributes don't exist or aren't populated.

## Entity Naming Convention

All entities: `<type>.kc_<kid_slug>_<purpose>` (e.g., `sensor.kc_sarah_points`, `sensor.kc_sarah_ui_dashboard_helper`)

- Kid slug = name lowercased + slugified (Home Assistant normalizes accents/spaces)
- **Exact match required** — renaming integration entities breaks dashboard

## Template Patterns (All Cards Follow This)

### Fetch-From-Helper Pattern

```jinja2
{%- set dashboard_helper = 'sensor.kc_' ~ Kid_name_normalize ~ '_ui_dashboard_helper' -%}
{%- set ui = state_attr(dashboard_helper, 'ui_translations') or {} -%}
{%- set chore_list = state_attr(dashboard_helper, 'chores') | default([], true) -%}
```

### 5-Step Template Structure

1. **User Configuration** — Set `pref_*` variables (column count, grouping toggles, label filters)
2. **Initialize Variables** — Build entity IDs, slugify names
3. **Collect Data** — Fetch from helper sensor & entity states
4. **Build Display** — Transform data (dates, colors, state mapping)
5. **Render** — Output YAML dicts (heading, grid, mushroom-template-card)

### Frontend vs Backend Philosophy

- **Backend handles**: List sorting/filtering, complex calculations (badge maintenance, aggregations), multi-card logic
- **Frontend handles**: Display preferences (`pref_column_count`, grouping toggles), state-to-color mapping, single-card conditionals
- **Rule**: If logic repeats across cards or becomes expensive → move to backend helper sensor

## Key Conventions

**State coloring**: `green`=approved, `orange`=claimed, `red`=overdue, `blue`=multi-approved, `purple`=shared-partial, `yellow`=partial

**Chore suffixes**: `(S)`=shared, `(M)`=multi-claim (appended in template, not from backend)

**Translation pattern**: `ui.get('welcome', 'err-welcome')` — missing keys show "err-\*" for debugging

**Card rendering**: All chore/reward cards use `custom:mushroom-template-card` with:

- `primary` = name (include suffixes S/M)
- `secondary` = multiline details (points, streak, status, due date)
- `icon_color` = state-based coloring
- `tap_action` = button.press service call
- `hold_action` = more-info modal

## Card Locations (by line range)

- Welcome: ~18-70 | Chores: ~82-317 | Rewards: ~327-425 | Showcase: ~437-610 | Badge maintenance: ~617-870 | Approvals: ~878-1086 | Admin: ~1100-1919

## Working with the Code

**Debug missing data (first troubleshooting steps):**

1. States view: confirm `sensor.kc_<kid>_ui_dashboard_helper` exists
2. Click entity → expand attributes: verify `chores`, `rewards`, `ui_translations` populated (not empty)
3. If "err-\*" fallback text shows → missing translation key in backend helper
4. Test snippet in Developer Tools → Templates to validate Jinja2 logic

**Add new chore grouping:**

1. Add `pref_use_<name>` variable at template top
2. Add conditional in "Collect Data" to sort into namespace list
3. Add group dict to `button_groups` in "Build Display"

**Add translation:**
Edit KidsChores Integration JSON → dashboard auto-picks via helper sensor (no frontend change needed)

**Optimize slow card:**
Move sorting/filtering from template loop to backend helper sensor as pre-sorted attribute (backend runs once; frontend just iterates)

## Performance Guidance

- **Each template loop is expensive**: Avoid iterating same list multiple times
- **Prefer backend pre-sorting**: If card sorts by multiple attributes, ask backend helper to pre-sort
- **State queries are cheap**: `states()` and `state_attr()` are fast; use freely

## File Organization

- `kc_dashboard_all.yaml` — Universal dashboard (all features, all languages via helper)
- `kc-dashboard-uihelpers.yaml` — Optional automation & datetime helper

## Adding New Child Dashboard

1. Duplicate `kc_dashboard_all.yaml`, replace `Kidname` with actual name (case-sensitive)
2. Paste into Home Assistant dashboard view
3. Verify: integration created matching slug entities, `sensor.kc_<kid>_ui_dashboard_helper` exists & populated
