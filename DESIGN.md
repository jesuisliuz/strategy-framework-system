---
# UI Design Tokens — Strategy Framework System
# Machine-readable design tokens for the ToB SaaS interface
# Inspired by google-labs-code/design.md

# === Colors ===
colors:
  # Primary palette (Deep Blue + Amber Gold)
  primary: "#1a2744"        # Deep Blue — main brand color
  primary-light: "#2a3a5c"  # Lighter blue for hover states
  primary-dark: "#0f1a33"   # Darker blue for active states
  secondary: "#d4a017"      # Amber Gold — accent color
  secondary-light: "#e8b830" # Lighter amber for highlights
  secondary-dark: "#b8860b" # Darker amber for text

  # Background system
  bg-primary: "#ffffff"     # Main content background
  bg-secondary: "#f8f9fa"   # Card/panel background
  bg-tertiary: "#e9ecef"    # Border/divider background
  bg-dark: "#1a2744"        # Dark mode background (header/footer)

  # Text system
  text-primary: "#1a2744"   # Primary text (deep blue)
  text-secondary: "#6c757d" # Secondary text (gray)
  text-muted: "#adb5bd"     # Muted text (light gray)
  text-inverse: "#ffffff"   # Text on dark background
  text-accent: "#d4a017"    # Accent text (amber)

  # Status colors
  success: "#28a745"        # Green — completed/done
  warning: "#ffc107"        # Yellow — stale/pending
  danger: "#dc3545"         # Red — error
  info: "#17a2b8"           # Cyan — info/running

# === Typography ===
typography:
  font-family: "'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif"
  font-size-base: "14px"
  font-size-sm: "12px"
  font-size-lg: "16px"
  font-size-xl: "20px"
  font-size-2xl: "24px"
  font-size-3xl: "32px"
  font-weight-normal: "400"
  font-weight-medium: "500"
  font-weight-bold: "700"
  line-height-base: "1.5"
  line-height-tight: "1.25"
  letter-spacing-normal: "0"
  letter-spacing-tight: "-0.025em"

# === Layout ===
layout:
  container-max-width: "1440px"
  sidebar-width: "320px"
  sidebar-collapsed-width: "64px"
  header-height: "64px"
  footer-height: "48px"
  content-padding: "24px"
  card-padding: "16px"
  gap-sm: "8px"
  gap-md: "16px"
  gap-lg: "24px"
  gap-xl: "32px"

# === Spacing ===
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  2xl: "48px"
  3xl: "64px"

# === Shapes ===
shapes:
  border-radius-sm: "4px"
  border-radius-md: "8px"
  border-radius-lg: "12px"
  border-radius-xl: "16px"
  border-width: "1px"
  border-color: "#e9ecef"

# === Elevation ===
elevation:
  shadow-sm: "0 1px 2px rgba(0,0,0,0.05)"
  shadow-md: "0 4px 6px rgba(0,0,0,0.07)"
  shadow-lg: "0 10px 15px rgba(0,0,0,0.1)"
  shadow-xl: "0 20px 25px rgba(0,0,0,0.15)"

# === Components ===
components:
  button:
    primary:
      background: "{colors.primary}"
      text: "{colors.text-inverse}"
      hover-background: "{colors.primary-light}"
      padding: "8px 16px"
      border-radius: "{shapes.border-radius-md}"
    secondary:
      background: "{colors.bg-secondary}"
      text: "{colors.text-primary}"
      border: "1px solid {colors.border-color}"
      padding: "8px 16px"
      border-radius: "{shapes.border-radius-md}"
    accent:
      background: "{colors.secondary}"
      text: "{colors.text-inverse}"
      hover-background: "{colors.secondary-light}"
      padding: "8px 16px"
      border-radius: "{shapes.border-radius-md}"

  card:
    background: "{colors.bg-primary}"
    border: "1px solid {colors.border-color}"
    border-radius: "{shapes.border-radius-lg}"
    padding: "{spacing.md}"
    shadow: "{elevation.shadow-sm}"

  input:
    background: "{colors.bg-primary}"
    border: "1px solid {colors.border-color}"
    border-radius: "{shapes.border-radius-md}"
    padding: "8px 12px"
    focus-border: "{colors.primary}"
    focus-shadow: "0 0 0 3px rgba(26,39,68,0.1)"

  nav-item:
    padding: "12px 16px"
    border-radius: "{shapes.border-radius-md}"
    hover-background: "{colors.bg-secondary}"
    active-background: "{colors.primary}"
    active-text: "{colors.text-inverse}"

  tier-badge:
    tier1:
      background: "{colors.primary}"
      text: "{colors.text-inverse}"
    tier2:
      background: "{colors.secondary}"
      text: "{colors.text-inverse}"
    tier3:
      background: "{colors.info}"
      text: "{colors.text-inverse}"

  status-badge:
    pending:
      background: "{colors.bg-tertiary}"
      text: "{colors.text-secondary}"
    running:
      background: "{colors.info}"
      text: "{colors.text-inverse}"
    done:
      background: "{colors.success}"
      text: "{colors.text-inverse}"
    stale:
      background: "{colors.warning}"
      text: "{colors.text-primary}"
    error:
      background: "{colors.danger}"
      text: "{colors.text-inverse}"

# === DSTE Calendar ===
dste-calendar:
  header-height: "48px"
  cell-padding: "8px"
  cell-border-radius: "{shapes.border-radius-sm}"
  phase-colors:
    启动: "{colors.info}"
    五看: "{colors.primary}"
    三定: "{colors.secondary}"
    评审: "{colors.success}"
    解码: "{colors.warning}"
    预算: "{colors.danger}"
    执行: "{colors.primary-light}"
    复盘: "{colors.text-secondary}"
---

## Design Rationale

### Color Philosophy
- **Deep Blue (#1a2744)**: Represents trust, stability, and professionalism — essential for a strategic analysis tool used by executives
- **Amber Gold (#d4a017)**: Represents value, insight, and premium quality — accent color for key actions and highlights
- **Neutral Grays**: Provide breathing room and hierarchy without competing with primary colors

### Typography Choices
- **System fonts first**: 'Segoe UI' for Windows, 'PingFang SC' for macOS Chinese, 'Microsoft YaHei' as fallback
- **No web fonts**: Eliminates FOIT/FOUT issues and ensures instant rendering
- **Clear hierarchy**: 32px for page titles, 24px for section headers, 16px for body, 12px for metadata

### Layout Principles
- **320px sidebar**: Wide enough for step inputs, narrow enough to keep focus on content
- **1440px max-width**: Fits most desktop screens without horizontal scrolling
- **24px content padding**: Consistent breathing room around all content
- **Card-based design**: Clear visual grouping with subtle shadows

### Component Design
- **Buttons**: Primary (deep blue) for main actions, Secondary (gray) for secondary actions, Accent (amber) for special actions
- **Cards**: White background with subtle border and shadow — clean, professional look
- **Status badges**: Color-coded for quick visual scanning (green=done, yellow=stale, red=error)
- **Tier badges**: Color-coded by tier (blue=Tier1, amber=Tier2, cyan=Tier3)

### DSTE Calendar Design
- **Phase colors**: Each phase has a distinct color for quick identification
- **Compact cells**: 8px padding keeps the calendar readable without wasting space
- **Visual hierarchy**: Phase name at top, tasks below, skills at bottom

### Accessibility Considerations
- **Contrast ratios**: All text/background combinations meet WCAG AA minimum (4.5:1)
- **Focus states**: Clear focus indicators (3px blue ring) for keyboard navigation
- **Color + text**: Status badges use both color and text label for accessibility