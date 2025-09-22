# Cache Status Check

This page helps verify that the latest deployment is visible.

## Current Build Information

- **Generated at**: {{ generation_time }}
- **Build Version**: {{ build_version }}
- **Component Count**: {{ component_count }}
- **Level 1 Cost**: {{ level1_cost }}

## Automated Values Check

| Metric | Value |
|--------|-------|
| Level 1 Cost | ~$13,988 |
| Level 2 Cost | ~$21,681 |
| Level 3 Cost | ~$38,187 |
| Level 4 Cost | ~$79,732 |

If these values don't match the expected automated calculations, the cache may be stale.

## Force Refresh Instructions

1. **Hard Refresh**: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
2. **Clear Cache**: Open Developer Tools → Application → Clear Storage
3. **Incognito Mode**: Open the site in a private/incognito window

---
*This is a cache verification page*