# Light/Dark Theme Feature

## Overview
Implemented a complete light/dark theme toggle feature using React Context API and Tailwind CSS. Users can switch between light mode, dark mode, and system preference.

## Features
- ✅ Light theme
- ✅ Dark theme (default)
- ✅ System preference detection
- ✅ Persistent theme selection (localStorage)
- ✅ Smooth theme transitions
- ✅ Theme toggle button with dropdown menu
- ✅ Accessible theme switcher

## Implementation

### 1. Theme Provider (`frontend/src/components/theme-provider.jsx`)
React Context provider that manages theme state and applies theme classes to the document root.

**Features:**
- Stores theme preference in localStorage
- Applies theme class to `<html>` element
- Supports system preference detection
- Provides `useTheme` hook for components

**Usage:**
```jsx
import { ThemeProvider } from './components/theme-provider';

<ThemeProvider defaultTheme="dark" storageKey="ui-theme">
  <App />
</ThemeProvider>
```

### 2. Theme Toggle Component (`frontend/src/components/theme-toggle.jsx`)
Dropdown button component for switching themes.

**Features:**
- Sun/Moon icon that animates on theme change
- Dropdown menu with three options: Light, Dark, System
- Uses shadcn/ui Button and DropdownMenu components
- Accessible with keyboard navigation

**Usage:**
```jsx
import { ThemeToggle } from '@/components/theme-toggle';

<ThemeToggle />
```

### 3. CSS Variables (`frontend/src/index.css`)
Defined color variables for both light and dark themes.

**Light Theme Variables:**
- Background: White (#FFFFFF)
- Foreground: Dark gray
- Card: White with subtle borders
- Muted: Light gray backgrounds
- Primary: Purple/Blue gradient (unchanged)

**Dark Theme Variables:**
- Background: Very dark gray (#0A0A0A)
- Foreground: Off-white
- Card: Dark gray with borders
- Muted: Medium gray backgrounds
- Primary: Purple/Blue gradient (unchanged)

### 4. Integration Points

**App.jsx:**
- Wrapped entire app with `ThemeProvider`
- Default theme set to "dark"
- Theme persisted in localStorage with key "ui-theme"

**Judge.jsx:**
- Added `ThemeToggle` button in header
- Positioned next to Rooms, History, and Logout buttons

**RoomLobby.jsx:**
- Added `ThemeToggle` button in header
- Positioned on the right side of the header

**CollaborativeRoom.jsx:**
- Added `ThemeToggle` button in header
- Positioned before the panel toggle buttons

## Theme Options

### Light Mode
- Clean, bright interface
- White backgrounds
- Dark text for readability
- Subtle shadows and borders

### Dark Mode (Default)
- Dark backgrounds reduce eye strain
- High contrast for code readability
- Vibrant accent colors
- Ideal for coding environments

### System Mode
- Automatically matches OS theme preference
- Respects user's system-wide dark/light mode setting
- Updates when system preference changes

## Technical Details

### Theme Persistence
- Theme choice saved to `localStorage` with key `ui-theme`
- Persists across browser sessions
- Automatically applied on page load

### Theme Application
- Theme class added to `<html>` element
- Tailwind's `dark:` variant used throughout components
- CSS variables automatically switch based on theme class

### Accessibility
- Keyboard navigation supported
- Screen reader friendly
- Clear visual indicators for current theme
- Smooth transitions between themes

## Files Created
1. `frontend/src/components/theme-provider.jsx` - Theme context provider
2. `frontend/src/components/theme-toggle.jsx` - Theme toggle button component
3. `frontend/src/components/ui/dropdown-menu.jsx` - Dropdown menu component (shadcn/ui)

## Files Modified
1. `frontend/src/App.jsx` - Added ThemeProvider wrapper
2. `frontend/src/index.css` - Added light theme CSS variables
3. `frontend/src/Judge.jsx` - Added ThemeToggle button
4. `frontend/src/pages/RoomLobby.jsx` - Added ThemeToggle button
5. `frontend/src/pages/CollaborativeRoom.jsx` - Added ThemeToggle button

## Usage Instructions

### For Users
1. Click the sun/moon icon button in the header
2. Select your preferred theme:
   - **Light** - Bright, clean interface
   - **Dark** - Dark mode for reduced eye strain
   - **System** - Match your OS preference
3. Theme preference is automatically saved

### For Developers
To add theme toggle to a new page:

```jsx
import { ThemeToggle } from '@/components/theme-toggle';

// In your component's header/navbar:
<ThemeToggle />
```

To use theme in custom components:

```jsx
import { useTheme } from '@/components/theme-provider';

function MyComponent() {
  const { theme, setTheme } = useTheme();
  
  return (
    <div>
      Current theme: {theme}
      <button onClick={() => setTheme('dark')}>Dark</button>
      <button onClick={() => setTheme('light')}>Light</button>
    </div>
  );
}
```

## Testing Checklist
- [x] Theme toggle button appears on all main pages
- [x] Light theme applies correctly
- [x] Dark theme applies correctly
- [x] System theme detects OS preference
- [x] Theme persists after page reload
- [x] Theme persists across browser sessions
- [x] Smooth transitions between themes
- [x] All components render correctly in both themes
- [x] Monaco editor remains dark (code editor)
- [x] No console errors
- [x] Dropdown menu works correctly
- [x] Icons animate on theme change

## Browser Compatibility
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari
- ✅ All modern browsers with CSS variables support

## Future Enhancements
- [ ] Add more theme options (e.g., high contrast, colorblind-friendly)
- [ ] Custom color scheme builder
- [ ] Per-page theme preferences
- [ ] Theme preview before applying
- [ ] Animated theme transitions
- [ ] Theme sync across tabs

## Notes
- Monaco editor (code editor) remains in dark theme for optimal code readability
- Primary brand colors (purple/blue gradient) remain consistent across themes
- All shadcn/ui components automatically support theming via CSS variables
- Theme toggle uses lucide-react icons (Sun and Moon)
