# Professional UI Redesign Plan

## Design System

### Color Palette (Dark Mode First)
```css
Primary: #6366f1 (Indigo)
Secondary: #8b5cf6 (Purple)
Success: #10b981 (Emerald)
Warning: #f59e0b (Amber)
Error: #ef4444 (Red)
Info: #3b82f6 (Blue)

Background: #0a0a0a (Near Black)
Surface: #18181b (Zinc-900)
Card: #27272a (Zinc-800)
Border: #3f3f46 (Zinc-700)

Text Primary: #fafafa (Zinc-50)
Text Secondary: #a1a1aa (Zinc-400)
Text Muted: #71717a (Zinc-500)
```

### Typography
```
Headings: Inter (font-semibold, font-bold)
Body: Inter (font-normal, font-medium)
Code: JetBrains Mono

Sizes:
- xs: 0.75rem (12px)
- sm: 0.875rem (14px)
- base: 1rem (16px)
- lg: 1.125rem (18px)
- xl: 1.25rem (20px)
- 2xl: 1.5rem (24px)
- 3xl: 1.875rem (30px)
- 4xl: 2.25rem (36px)
```

### Spacing System
```
1: 0.25rem (4px)
2: 0.5rem (8px)
3: 0.75rem (12px)
4: 1rem (16px)
5: 1.25rem (20px)
6: 1.5rem (24px)
8: 2rem (32px)
10: 2.5rem (40px)
12: 3rem (48px)
16: 4rem (64px)
```

### Border Radius
```
sm: 0.375rem (6px)
md: 0.5rem (8px)
lg: 0.75rem (12px)
xl: 1rem (16px)
2xl: 1.5rem (24px)
```

## Component Library

### Core Components
1. **Button** - Primary, Secondary, Ghost, Outline variants
2. **Card** - With header, content, footer sections
3. **Badge** - Status indicators
4. **Input** - Text, number, search variants
5. **Select** - Dropdown with search
6. **Tabs** - Horizontal navigation
7. **Modal** - Overlay dialogs
8. **Toast** - Notifications
9. **Table** - Data tables with sorting
10. **Skeleton** - Loading states

### Layout Components
1. **Container** - Max-width wrapper
2. **Grid** - Responsive grid system
3. **Stack** - Vertical/horizontal spacing
4. **Sidebar** - Collapsible navigation
5. **Header** - Top navigation bar

## Page Redesigns

### 1. Judge Page (Priority 1)
**Layout:**
```
┌─────────────────────────────────────────────────┐
│ Header: Logo | Problems | Rooms | Profile      │
├──────────────┬──────────────────────────────────┤
│              │                                  │
│  Problem     │  Editor                          │
│  List        │  ┌────────────────────────────┐ │
│  (Sidebar)   │  │ Code Editor                │ │
│              │  │                            │ │
│  ┌────────┐  │  │                            │ │
│  │Problem │  │  └────────────────────────────┘ │
│  │  #1    │  │                                  │
│  └────────┘  │  ┌────────────────────────────┐ │
│              │  │ Test Cases                 │ │
│  ┌────────┐  │  └────────────────────────────┘ │
│  │Problem │  │                                  │
│  │  #2    │  │  [Submit] [Run Code]            │
│  └────────┘  │                                  │
│              │  Results Panel                   │
└──────────────┴──────────────────────────────────┘
```

**Features:**
- Split-pane layout with resizable panels
- Problem list with difficulty badges
- Monaco editor with theme toggle
- Collapsible test cases
- Real-time submission feedback
- Animated result cards

### 2. Collaborative Room (Priority 2)
**Layout:**
```
┌─────────────────────────────────────────────────┐
│ Room: CODE123 | 3 users | [Leave]              │
├──────┬──────────────────────────────────┬───────┤
│      │                                  │       │
│ Prob │  Editor                          │ Chat  │
│ lem  │  ┌────────────────────────────┐ │       │
│      │  │                            │ │ User1 │
│ Desc │  │  Collaborative Code        │ │ User2 │
│      │  │                            │ │ User3 │
│      │  └────────────────────────────┘ │       │
│      │                                  │ [Send]│
│      │  [Run Code] [Run Tests]         │       │
└──────┴──────────────────────────────────┴───────┘
```

**Features:**
- Real-time cursor tracking
- User presence indicators
- Integrated chat
- Problem panel toggle
- Test results overlay

### 3. Room Lobby (Priority 3)
**Layout:**
```
┌─────────────────────────────────────────────────┐
│ Collaborative Rooms                              │
├─────────────────────────────────────────────────┤
│                                                  │
│  [Create Room]  [Join Room]                     │
│                                                  │
│  Active Rooms                                    │
│  ┌──────────────────────────────────────────┐  │
│  │ Room: ABC123  |  3/10 users  | [Join]   │  │
│  │ Problem: Two Sum                         │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │ Room: XYZ789  |  2/5 users   | [Join]   │  │
│  │ Problem: Fibonacci                       │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### 4. Profile Dashboard (Priority 4)
**Layout:**
```
┌─────────────────────────────────────────────────┐
│ Profile: John Doe                                │
├─────────────────────────────────────────────────┤
│                                                  │
│  Stats Cards                                     │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐          │
│  │ 45   │ │ 89%  │ │ 234  │ │ #12  │          │
│  │Solved│ │ Rate │ │Points│ │ Rank │          │
│  └──────┘ └──────┘ └──────┘ └──────┘          │
│                                                  │
│  Recent Submissions                              │
│  ┌──────────────────────────────────────────┐  │
│  │ Two Sum | Accepted | 100/100 | 2h ago   │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  Activity Chart                                  │
│  [Recharts visualization]                        │
└─────────────────────────────────────────────────┘
```

## Implementation Strategy

### Phase 1: Core Components (Day 1)
- Create `components/ui/` folder
- Implement Button, Card, Badge, Input
- Set up Tailwind config
- Create design tokens

### Phase 2: Judge Page (Day 2)
- Redesign problem list
- Improve editor layout
- Better test case display
- Animated submission results

### Phase 3: Collaborative Features (Day 3)
- Redesign Room Lobby
- Improve Collaborative Room UI
- Better chat interface
- User presence UI

### Phase 4: Profile & Analytics (Day 4)
- Profile dashboard
- Stats visualization
- Submission history
- Activity charts

### Phase 5: Polish (Day 5)
- Animations with Framer Motion
- Loading states
- Error states
- Responsive design
- Dark mode refinements

## Key Improvements

1. **Visual Hierarchy**
   - Clear content sections
   - Proper spacing
   - Consistent typography
   - Strategic use of color

2. **User Experience**
   - Smooth transitions
   - Loading skeletons
   - Error handling
   - Success feedback

3. **Performance**
   - Code splitting
   - Lazy loading
   - Optimized re-renders
   - Efficient animations

4. **Accessibility**
   - Keyboard navigation
   - Screen reader support
   - Focus indicators
   - ARIA labels

5. **Responsiveness**
   - Mobile-first approach
   - Breakpoint system
   - Flexible layouts
   - Touch-friendly

## File Structure
```
frontend/src/
├── components/
│   ├── ui/
│   │   ├── button.jsx
│   │   ├── card.jsx
│   │   ├── badge.jsx
│   │   ├── input.jsx
│   │   ├── select.jsx
│   │   ├── tabs.jsx
│   │   ├── modal.jsx
│   │   ├── toast.jsx
│   │   ├── table.jsx
│   │   └── skeleton.jsx
│   ├── layout/
│   │   ├── header.jsx
│   │   ├── sidebar.jsx
│   │   └── container.jsx
│   └── features/
│       ├── problem-list.jsx
│       ├── code-editor.jsx
│       ├── test-cases.jsx
│       └── submission-result.jsx
├── pages/
│   ├── Judge.jsx (redesigned)
│   ├── RoomLobby.jsx (redesigned)
│   ├── CollaborativeRoom.jsx (redesigned)
│   └── Profile.jsx (new)
├── hooks/
│   ├── use-toast.js
│   └── use-media-query.js
├── lib/
│   └── utils.js (cn helper)
└── styles/
    └── globals.css
```

## Next Steps

1. Set up Tailwind config with design tokens
2. Create utility functions (cn helper)
3. Build core UI components
4. Redesign Judge page
5. Implement remaining pages
6. Add animations
7. Test responsiveness
8. Polish and optimize
