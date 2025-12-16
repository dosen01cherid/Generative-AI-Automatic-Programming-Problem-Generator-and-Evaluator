# Pattern Editor Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Markdown Editor (md_editor.html)            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐         ┌──────────────┐                   │
│  │  File Input   │────────▶│   Preview    │                   │
│  │  (Load .md)   │         │   Panel      │                   │
│  └───────────────┘         │  (Rendered)  │                   │
│         │                  └──────────────┘                   │
│         │                         │                            │
│         ▼                         │                            │
│  ┌────────────────────────────────▼──────────────┐            │
│  │      parseMarkdownToElements()                │            │
│  │   Pattern Detection Engine (Core Logic)       │            │
│  └────────────────────────────────────────────────┘            │
│         │                                                       │
│         ├──────┬──────┬──────┬──────┬──────┬──────┬──────┐   │
│         ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼   │
│    Pattern Pattern Pattern Pattern Pattern Pattern Pattern Pattern
│       1      2      3      4      5      6      7      8   │
│   Headers  Code   HR   Quotes  UL     OL   Tables  Paras  │
│         │      │      │      │      │      │      │      │   │
│         └──────┴──────┴──────┴──────┴──────┴──────┴──────┘   │
│                         │                                      │
│                         ▼                                      │
│         ┌───────────────────────────────┐                     │
│         │  Element Array with Metadata  │                     │
│         │  {content, startLine,         │                     │
│         │   endLine, type}              │                     │
│         └───────────────────────────────┘                     │
│                         │                                      │
│                         ▼                                      │
│         ┌───────────────────────────────┐                     │
│         │    Marked.js (Renderer)       │                     │
│         │    Converts MD → HTML         │                     │
│         └───────────────────────────────┘                     │
│                         │                                      │
│         ┌───────────────▼───────────────┐                     │
│         │  Edit Mode: Click-to-Edit     │                     │
│         │  Maps HTML ↔ MD Elements      │                     │
│         └───────────────┬───────────────┘                     │
│                         │                                      │
│                         ▼                                      │
│         ┌───────────────────────────────┐                     │
│         │    Ace Editor Panel           │                     │
│         │  (Syntax-highlighted editing) │                     │
│         └───────────────────────────────┘                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Pattern Detection Flow

```
Input: Markdown Text
  │
  ▼
Split into lines ────────────────┐
  │                              │
  ▼                              │
Loop through lines               │
  │                              │
  ├─ Empty line? ────Yes────▶ Skip
  │      │                       │
  │      No                      │
  │      │                       │
  ▼      ▼                       │
Check Pattern Priority:          │
  │                              │
  ├─ 1. Headers (/^#{1,6}\s/)   │
  │    └─ Match? ──Yes─┐        │
  │                     │        │
  ├─ 2. Code (```)      │        │
  │    └─ Match? ──Yes─┤        │
  │                     │        │
  ├─ 3. HR (---/***/__) │        │
  │    └─ Match? ──Yes─┤        │
  │                     │        │
  ├─ 4. Blockquote (>)  │        │
  │    └─ Match? ──Yes─┤        │
  │                     │        │
  ├─ 5. UL (-/*/+)      │        │
  │    └─ Match? ──Yes─┤        │
  │                     │        │
  ├─ 6. OL (1./2./3.)   │        │
  │    └─ Match? ──Yes─┤        │
  │                     │        │
  ├─ 7. Table (|...|)   │        │
  │    └─ Match? ──Yes─┤        │
  │                     │        │
  └─ 8. Paragraph       │        │
       (default)        │        │
             │          │        │
             └──────────┘        │
                  │               │
                  ▼               │
        Capture Block Content    │
        Track Start/End Lines    │
        Detect Block Type        │
                  │               │
                  ▼               │
        Store in Elements[]      │
                  │               │
                  └───────────────┘
                  │
                  ▼
Return Elements Array
```

## Pattern Matching Details

### Single-line Patterns
```
# Header        (/^#{1,6}\s/)
   │
   └─▶ Capture 1 line
        Store and continue

---            (/^(---|\*\*\*|___)$/)
   │
   └─▶ Capture 1 line
        Store and continue
```

### Multi-line Patterns
```
```code       (startsWith('```'))
   │
   └─▶ Start capture
        │
        ├─▶ Loop until closing ```
        │   Collect all lines
        │
        └─▶ End capture
             Store and continue

> Quote        (startsWith('>'))
   │
   └─▶ Start capture
        │
        ├─▶ While line starts with > or is empty
        │   Collect lines
        │
        └─▶ Stop at double empty or non->
             Store and continue

- List         (/^[-*+]\s/)
   │
   └─▶ Start capture
        │
        ├─▶ While:
        │   - List marker OR
        │   - Indented (2 spaces/tab) OR
        │   - Empty line (single)
        │
        └─▶ Stop at double empty or non-list
             Store and continue
```

## Element Structure

```
┌─────────────────────────────────┐
│      Element Object             │
├─────────────────────────────────┤
│  content: "# My Header"         │  ◀── Raw markdown text
│  startLine: 5                   │  ◀── First line (0-indexed)
│  endLine: 5                     │  ◀── Last line (0-indexed)
│  type: "heading"                │  ◀── Semantic type
└─────────────────────────────────┘
```

## Edit Mode Flow

```
User clicks element in preview
         │
         ▼
Get element index from DOM
         │
         ▼
Look up in markdownElements[]
         │
         ▼
Load content into Ace Editor
         │
         ▼
User edits in Ace Editor
         │
         ▼
Click "Apply Changes"
         │
         ▼
Update element in array
         │
         ▼
Reconstruct full markdown
         │
         ▼
Re-parse and re-render
         │
         ▼
Updated preview shown
```

## Pattern Priority Order

```
Priority: High → Low

1. Headers        (/^#{1,6}\s/)        [PRIORITY 10]
2. Code Blocks    (startsWith('```'))  [PRIORITY 9]
3. Horizontal Rules (/^(---|***|___)$/) [PRIORITY 8]
4. Blockquotes    (startsWith('>'))    [PRIORITY 7]
5. Unordered Lists (/^[-*+]\s/)        [PRIORITY 6]
6. Ordered Lists  (/^\d+\.\s/)         [PRIORITY 5]
7. Tables         (/\|.*\|/)           [PRIORITY 4]
8. Paragraphs     (default)            [PRIORITY 1]

Note: Checked in this order to avoid conflicts
```

## Dependencies Graph

```
┌───────────────────────────────────────────────┐
│            External Dependencies              │
├───────────────────────────────────────────────┤
│                                               │
│  ┌─────────────┐    ┌─────────────┐          │
│  │  Marked.js  │    │ Ace Editor  │          │
│  │  (v5.0+)    │    │  (v1.32.2)  │          │
│  └──────┬──────┘    └──────┬──────┘          │
│         │                  │                  │
│         │                  │                  │
│  ┌──────▼──────────────────▼──────┐          │
│  │    GitHub Markdown CSS         │          │
│  │        (v5.5.0)                │          │
│  └─────────────────────────────────┘          │
│                                               │
└───────────────────────────────────────────────┘
         │         │         │
         └─────────┴─────────┘
                   │
         ┌─────────▼──────────┐
         │   md_editor.html   │
         │  (Pattern Editor)  │
         └────────────────────┘
```

## Data Flow

```
┌─────────┐
│ .md File│
└────┬────┘
     │
     ▼
┌─────────────────┐
│ FileReader API  │
└────┬────────────┘
     │
     ▼
┌──────────────────────────┐
│ Raw Markdown String      │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────────┐
│ parseMarkdownToElements()    │
│ (Pattern Detection Engine)   │
└────┬─────────────────────────┘
     │
     ▼
┌──────────────────────────────┐
│ Element Array                │
│ [{content, start, end, type}]│
└────┬─────────────────────────┘
     │
     ├────────────────┬──────────────┐
     │                │              │
     ▼                ▼              ▼
┌─────────┐    ┌──────────┐   ┌──────────┐
│Marked.js│    │Edit Mode │   │Download  │
│Renderer │    │Mapping   │   │/Save     │
└────┬────┘    └─────┬────┘   └──────────┘
     │               │
     ▼               ▼
┌─────────┐    ┌──────────┐
│HTML     │    │Ace Editor│
│Preview  │    │Panel     │
└─────────┘    └──────────┘
```

## Performance Characteristics

```
File Size         Parse Time      Recommendation
────────────────────────────────────────────────
< 100 KB          < 10ms          ✓ Optimal
100 KB - 1 MB     10-50ms         ✓ Good
1 MB - 5 MB       50-100ms        ✓ Acceptable
5 MB - 10 MB      100-500ms       ⚠ May lag
> 10 MB           > 500ms         ✗ Not recommended

Time Complexity: O(n) where n = number of lines
Space Complexity: O(n) for element storage
```

## Browser Compatibility Matrix

```
Browser         Min Version    Status
─────────────────────────────────────
Chrome          60+            ✓
Firefox         60+            ✓
Safari          12+            ✓
Edge            79+            ✓
Opera           47+            ✓
IE              Any            ✗

Required Features:
- ES6+ JavaScript
- FileReader API
- Modern Regex
- Fetch/XHR
```

## State Management

```
┌────────────────────────────────────────┐
│         Application State              │
├────────────────────────────────────────┤
│                                        │
│  currentFile: File | null              │
│  currentFileName: string               │
│  isEditMode: boolean                   │
│  fullMarkdownContent: string           │
│  currentEditingElement: HTMLElement    │
│  markdownElements: Array<Element>      │
│                                        │
└────────────────────────────────────────┘
```

---

## Legend

```
┌─────┐
│ Box │  = Component/Module
└─────┘

  │
  ▼     = Data flow direction

 ─┐
  ├─    = Branch/Decision point
 ─┘

/regex/ = Regular expression pattern

✓       = Supported/Working
✗       = Not supported
⚠       = Warning/Caution
```

---

**For detailed technical documentation, see:**
- `PATTERN_EDITOR_DOCUMENTATION.md`
- `PATTERN_EDITOR_REVIEW.md`
- `PATTERN_EDITOR_QUICK_REFERENCE.md`
