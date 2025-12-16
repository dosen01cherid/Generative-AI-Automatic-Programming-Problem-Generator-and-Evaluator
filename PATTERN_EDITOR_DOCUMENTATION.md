# Pattern Editor Code Documentation

## Overview

The pattern editor is implemented in `md_editor.html` and provides a sophisticated markdown parsing and editing system. It allows users to view and edit markdown files with a live preview, using pattern recognition to identify different markdown elements.

## Key Components

### 1. Pattern Detection System

The core of the pattern editor is the `parseMarkdownToElements()` function, which uses regular expressions to identify and parse different markdown block types.

#### Supported Markdown Patterns

The editor recognizes the following markdown patterns:

1. **Headers** (`^#{1,6}\s`)
   - Pattern: One to six `#` symbols followed by a space
   - Examples: `# H1`, `## H2`, `### H3`, etc.
   - Single line blocks

2. **Code Blocks** (` ``` `)
   - Pattern: Lines starting with triple backticks
   - Multi-line blocks enclosed between opening and closing ` ``` `
   - Preserves all content between delimiters

3. **Horizontal Rules** (`^(---|\*\*\*|___)$`)
   - Pattern: Three or more dashes, asterisks, or underscores
   - Examples: `---`, `***`, `___`
   - Single line blocks

4. **Blockquotes** (`^>`)
   - Pattern: Lines starting with `>`
   - Multi-line blocks that can include empty lines
   - Stops at double empty line or when `>` is no longer present

5. **Unordered Lists** (`^[-*+]\s`)
   - Pattern: Lines starting with `-`, `*`, or `+` followed by a space
   - Supports nested items with indentation (2 spaces or tab)
   - Stops at double empty line or non-list content

6. **Ordered Lists** (`^\d+\.\s`)
   - Pattern: Lines starting with numbers followed by `.` and a space
   - Supports nested items with indentation
   - Stops at double empty line or non-list content

7. **Tables** (`^\|` or `/\|.*\|/`)
   - Pattern: Lines starting with `|` or containing `|...|`
   - Multi-line blocks
   - Continues while lines match the table pattern

8. **Paragraphs**
   - Default fallback for any content not matching above patterns
   - Continues until:
     - Empty line is encountered
     - Start of a special block pattern is detected

### 2. Pattern Matching Logic

#### Line-by-Line Processing

```javascript
function parseMarkdownToElements(markdown) {
  const lines = markdown.split('\n');
  const elements = [];
  let i = 0;

  while (i < lines.length) {
    // Process each line
    // Identify pattern type
    // Capture complete block
    // Track line numbers
  }
  
  return elements;
}
```

#### Block Extraction Strategy

For each markdown element:
- **startLine**: The first line of the block
- **endLine**: The last line of the block  
- **content**: The complete text content
- **type**: The detected block type (heading, code, ul, ol, etc.)

### 3. Regular Expression Patterns

| Pattern | Regex | Description |
|---------|-------|-------------|
| Headers | `/^#{1,6}\s/` | 1-6 hash symbols + space |
| Code blocks | `startsWith('```')` | Triple backticks |
| Horizontal rules | `/^(---|\*\*\*|___)$/` | Three dashes, asterisks, or underscores |
| Blockquotes | `startsWith('>')` | Greater-than symbol |
| Unordered lists | `/^[-*+]\s/` | Dash, asterisk, or plus + space |
| Ordered lists | `/^\d+\.\s/` | Number + dot + space |
| Tables | `/\|.*\|/` | Contains pipe symbols |
| Special blocks | `/^#{1,6}\s|^```|^[-*+]\s|^\d+\.\s|^>\s|^\||^---|^\*\*\*|^___/` | Combined pattern for detection |

### 4. Block Type Detection

The `detectBlockType()` function provides semantic identification:

```javascript
function detectBlockType(content) {
  const firstLine = content.split('\n')[0].trim();
  
  if (/^#{1,6}\s/.test(firstLine)) return 'heading';
  if (firstLine.startsWith('```')) return 'code';
  if (firstLine.startsWith('>')) return 'blockquote';
  if (/^[-*+]\s/.test(firstLine)) return 'ul';
  if (/^\d+\.\s/.test(firstLine)) return 'ol';
  if (firstLine.startsWith('|') || /\|.*\|/.test(firstLine)) return 'table';
  if (/^(---|\*\*\*|___)$/.test(firstLine)) return 'hr';
  
  return 'paragraph';
}
```

## Editor Features

### Edit Mode

- Click on any rendered markdown element to edit it
- Uses Ace Editor for syntax-highlighted editing
- Live preview updates after applying changes

### Pattern-Based Element Mapping

The editor maintains a one-to-one mapping between:
- HTML rendered elements in the preview pane
- Original markdown text blocks
- Ace editor content

This mapping enables precise element editing without affecting other parts of the document.

## Implementation Details

### Multi-line Block Handling

For multi-line blocks (lists, blockquotes, code blocks):

1. Detect the start pattern
2. Continue collecting lines while they match the continuation criteria
3. Track both first and last line numbers
4. Handle edge cases:
   - Empty lines within blocks
   - Nested content (indented list items)
   - Block termination conditions

### Example: List Processing

```javascript
// Unordered lists
if (/^[-*+]\s/.test(trimmedLine)) {
  blockContent = line + '\n';
  i++;
  
  while (i < lines.length) {
    const nextLine = lines[i].trim();
    
    // Continue if: list item OR indented content OR empty line
    if (/^[-*+]\s/.test(nextLine) ||
        (nextLine !== '' && (lines[i].startsWith('  ') || lines[i].startsWith('\t'))) ||
        nextLine === '') {
      blockContent += lines[i] + '\n';
      if (nextLine !== '') {
        endLine = i;
      }
      i++;
      
      // Stop at double empty line
      if (nextLine === '' && i < lines.length && lines[i].trim() === '') {
        break;
      }
    } else {
      break;
    }
  }
}
```

## Code Quality Observations

### Strengths

1. **Comprehensive Pattern Coverage**: Handles all major markdown syntax elements
2. **Robust Multi-line Processing**: Properly handles complex blocks with continuation logic
3. **Line Tracking**: Maintains accurate startLine/endLine for precise editing
4. **Type Detection**: Semantic block type identification for debugging and UI features
5. **Edge Case Handling**: Deals with empty lines, nested content, and block boundaries

### Potential Improvements

1. **Performance**: For very large documents, consider chunking or lazy parsing
2. **Pattern Conflicts**: Some edge cases where table patterns might conflict with other syntax
3. **Indentation**: Could be more sophisticated in handling varied indentation styles
4. **Special Characters**: May need escaping for certain regex special characters in content
5. **Comments**: Could benefit from more inline documentation for complex logic

## Testing Recommendations

To ensure the pattern editor works correctly:

1. Test with documents containing all markdown element types
2. Verify multi-line blocks with nested content
3. Test edge cases:
   - Empty documents
   - Documents with only one element type
   - Mixed indentation styles
   - Tables with complex formatting
   - Code blocks with markdown-like syntax inside
4. Verify edit mode maintains correct element mapping
5. Test with very large documents for performance

## Usage

The pattern editor is accessed via `md_editor.html`:

1. Open the file in a web browser
2. Load a markdown file using "Open MD File"
3. Toggle "Edit Mode" to enable editing
4. Click on any element in the preview to edit it
5. Save changes using "Save" or "Download"

## Dependencies

- **Marked.js**: Markdown parsing and rendering
- **Ace Editor**: Code editor with syntax highlighting
- **GitHub Markdown CSS**: Styling for rendered markdown

## Browser Compatibility

The pattern editor uses modern JavaScript features:
- Regular expressions
- Array methods (map, forEach)
- ES6+ syntax (const, let, arrow functions)

Recommended browsers: Chrome, Firefox, Edge, Safari (latest versions)
