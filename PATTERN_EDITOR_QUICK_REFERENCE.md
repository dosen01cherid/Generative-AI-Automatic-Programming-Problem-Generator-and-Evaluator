# Pattern Editor Quick Reference Guide

## Pattern Recognition Cheat Sheet

### All Supported Patterns

| Pattern | Syntax | Example |
|---------|--------|---------|
| **Header 1** | `# Text` | `# Main Title` |
| **Header 2** | `## Text` | `## Section` |
| **Header 3** | `### Text` | `### Subsection` |
| **Header 4-6** | `####+ Text` | `#### Details` |
| **Bold** | `**text**` | `**important**` |
| **Italic** | `*text*` | `*emphasis*` |
| **Code Block** | ` ``` lang` ... ` ``` ` | See below |
| **Inline Code** | `` `code` `` | `` `variable` `` |
| **Unordered List** | `- item` or `* item` or `+ item` | `- Task 1` |
| **Ordered List** | `1. item` | `1. First step` |
| **Blockquote** | `> text` | `> Quote here` |
| **Horizontal Rule** | `---` or `***` or `___` | `---` |
| **Link** | `[text](url)` | `[Google](https://google.com)` |
| **Image** | `![alt](url)` | `![Logo](image.png)` |
| **Table** | `\| col \| col \|` | See below |

---

## Regular Expressions Used

### Pattern Detection Regex

```javascript
// Headers (1-6 levels)
/^#{1,6}\s/

// Horizontal rules
/^(---|\*\*\*|___)$/

// Unordered lists
/^[-*+]\s/

// Ordered lists
/^\d+\.\s/

// Tables
/\|.*\|/

// Blockquotes
startsWith('>')

// Code blocks
startsWith('```')

// Combined pattern for paragraph detection
/^#{1,6}\s|^```|^[-*+]\s|^\d+\.\s|^>\s|^\||^---|^\*\*\*|^___/
```

---

## Code Block Examples

### JavaScript
\`\`\`javascript
function greet(name) {
  return `Hello, ${name}!`;
}
\`\`\`

### Python
\`\`\`python
def greet(name):
    return f"Hello, {name}!"
\`\`\`

### Generic
\`\`\`
No syntax highlighting
\`\`\`

---

## List Examples

### Unordered List with Nesting
```
- Main item 1
- Main item 2
  - Nested item 2a
  - Nested item 2b
- Main item 3
```

### Ordered List with Nesting
```
1. First step
2. Second step
   - Sub-task A
   - Sub-task B
3. Third step
```

---

## Table Examples

### Basic Table
```
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |
```

### Aligned Table
```
| Left | Center | Right |
|:-----|:------:|------:|
| L1   | C1     | R1    |
| L2   | C2     | R2    |
```

---

## Blockquote Examples

### Single Line
```
> This is a quote
```

### Multi-line
```
> This is a quote
> that spans multiple lines
> with continued content
```

### Nested
```
> Level 1
>> Level 2
>>> Level 3
```

---

## Parser Behavior

### Block Separation
- **Empty lines** separate blocks
- **Double empty lines** always terminate current block
- **Pattern change** starts new block

### Indentation
- **2 spaces** or **1 tab** = nested content
- Applies to lists (sub-items)
- Preserves original spacing in code blocks

### Continuation Rules

| Pattern | Continues On |
|---------|-------------|
| Header | Single line only |
| Code | Until closing ` ``` ` |
| Blockquote | `>` prefix or empty line |
| List | List marker or indentation |
| Table | `\|` prefix |
| Paragraph | Until empty line or special syntax |
| Horizontal Rule | Single line only |

---

## Editor Shortcuts

### File Operations
- **Open**: Click "📁 Open MD File" button
- **Save**: Click "💾 Save" button
- **Download**: Click "📥 Download" button

### Edit Mode
- **Toggle Edit Mode**: Click "✏️ Edit Mode" button
- **Edit Element**: Click any rendered element (in edit mode)
- **Apply Changes**: Click "Apply Changes" in editor panel
- **Cancel**: Toggle back to "👁️ View Mode"

---

## Tips & Tricks

### Best Practices
1. Use consistent list markers (`-` recommended)
2. Add blank lines between different block types
3. Use fenced code blocks (` ``` `) instead of indentation
4. Keep table column widths consistent for readability
5. Use semantic header levels (don't skip levels)

### Troubleshooting

**Problem:** Element not editable  
**Solution:** Ensure you're in Edit Mode (button shows "👁️ View Mode")

**Problem:** Changes not applied  
**Solution:** Click "Apply Changes" button after editing

**Problem:** List items not grouping  
**Solution:** Remove extra blank lines between items

**Problem:** Table not rendering  
**Solution:** Ensure each row has same number of `|` separators

**Problem:** Code block shows as text  
**Solution:** Check closing ` ``` ` is on its own line

---

## Element Types Returned

Each parsed element has this structure:

```javascript
{
  content: "# Header",     // Raw markdown text
  startLine: 0,           // First line (0-indexed)
  endLine: 0,            // Last line (0-indexed)
  type: "heading"        // Semantic type
}
```

### Type Values
- `"heading"` - Headers (H1-H6)
- `"code"` - Code blocks
- `"blockquote"` - Blockquotes
- `"ul"` - Unordered lists
- `"ol"` - Ordered lists
- `"table"` - Tables
- `"hr"` - Horizontal rules
- `"paragraph"` - Regular paragraphs

---

## Advanced Usage

### Custom Pattern Detection

To add new patterns, modify `parseMarkdownToElements()`:

```javascript
// Add after existing patterns, before paragraph handling
else if (/* your pattern test */) {
  // Your parsing logic
  blockContent = line;
  i++;
}
```

### Extending Block Types

Add to `detectBlockType()`:

```javascript
if (/* your test */) return 'your-type';
```

---

## Performance Guidelines

### File Size Recommendations
- **Optimal:** < 1 MB (instant parsing)
- **Good:** 1-5 MB (fast parsing)
- **Acceptable:** 5-10 MB (may lag slightly)
- **Not recommended:** > 10 MB (significant lag)

### Optimization Tips
1. Split very large documents into smaller files
2. Minimize unnecessary re-parsing
3. Close unused browser tabs
4. Use modern browser versions

---

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| Marked.js | Latest | Markdown → HTML conversion |
| Ace Editor | 1.32.2+ | Code editor with syntax highlighting |
| GitHub Markdown CSS | 5.5.0+ | Rendering styles |

---

## Browser Support

| Browser | Minimum Version |
|---------|----------------|
| Chrome | 60+ |
| Firefox | 60+ |
| Safari | 12+ |
| Edge | 79+ |
| Opera | 47+ |

**Not supported:** Internet Explorer

---

## Common Patterns Examples

### Documentation Header
```markdown
# Project Name

## Description
Brief description of the project.

## Installation
\`\`\`bash
npm install package-name
\`\`\`

## Usage
\`\`\`javascript
const pkg = require('package-name');
\`\`\`
```

### Meeting Notes
```markdown
# Meeting Notes - 2025-12-16

## Attendees
- John Doe
- Jane Smith

## Agenda
1. Project updates
2. New requirements
3. Timeline review

## Action Items
- [ ] Review documentation
- [ ] Update tests
- [ ] Deploy to staging
```

### Technical Specification
```markdown
# API Specification

## Endpoints

### GET /api/users
Returns list of users.

| Parameter | Type | Required |
|-----------|------|----------|
| limit | int | No |
| offset | int | No |

**Response:**
\`\`\`json
{
  "users": [],
  "total": 0
}
\`\`\`
```

---

**For more details, see:** `PATTERN_EDITOR_DOCUMENTATION.md`
