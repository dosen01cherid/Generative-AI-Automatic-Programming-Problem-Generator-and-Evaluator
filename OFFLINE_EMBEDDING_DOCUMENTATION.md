# Offline Embedding Documentation

## Complete Guide to Creating Offline-Ready HTML Files

**Version:** 1.0
**Last Updated:** December 1, 2025
**Project:** Generative AI Automatic Programming Problem Generator and Evaluator

---

## Table of Contents

1. [Overview](#overview)
2. [The Challenge](#the-challenge)
3. [The Solution](#the-solution)
4. [Prerequisites](#prerequisites)
5. [Directory Structure](#directory-structure)
6. [Architecture](#architecture)
7. [Step-by-Step Process](#step-by-step-process)
8. [Technical Details](#technical-details)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance](#maintenance)
11. [Performance Considerations](#performance-considerations)

---

## Overview

### Purpose

The offline embedding process converts our web-based HTML applications (`create_problem.html` and `solve_problem.html`) into self-contained, fully offline-capable HTML files that work on the `file://` protocol without any internet connection.

### What Gets Embedded

- **Fonts:** Poppins font family (300, 400, 500, 600, 700 weights)
- **CSS Libraries:** MathQuill, Quill editor
- **JavaScript Libraries:** jQuery, MathQuill, Quill, MathJax, Ace Editor
- **Python Runtime:** Complete Pyodide environment (WebAssembly Python)
- **Python Standard Library:** Full Python stdlib
- **Python Packages:** SymPy, mpmath, lark, micropip, packaging, brotli, distutils

### Output Files

- **create_problem_offline_embedded.html** (~51 MB)
- **solve_problem_offline_embedded.html** (~49 MB)

---

## The Challenge

### File Protocol Limitations

The `file://` protocol has significant security restrictions:

1. **No Network Access:** Cannot fetch resources from CDNs or external URLs
2. **No Dynamic Imports:** ES6 modules with `import()` don't work
3. **No Service Workers:** Cannot use browser caching APIs
4. **CORS Restrictions:** Cannot load separate JavaScript/WASM files
5. **Limited Fetch API:** `fetch()` calls to external resources fail

### Traditional Solutions Don't Work

- **Relative paths:** Fail because Pyodide expects specific directory structures
- **Service Workers:** Don't run on `file://` protocol
- **Web Workers:** Have limited functionality on `file://`
- **IndexedDB/LocalStorage:** Cannot store 50MB+ of data reliably

---

## The Solution

### Core Innovation: Fetch Interception

We intercept the browser's `fetch()` function and return embedded base64-encoded data as `Response` objects, making the browser think it's fetching from the network when it's actually using embedded data.

### Pyodide Loading Trick

**Key Insight:** Pyodide consists of two parts:
1. `pyodide.asm.js` - Sets up `globalThis._createPyodideModule`
2. `pyodide.js` - Checks for `_createPyodideModule` before dynamic import

**Solution:** Load `pyodide.asm.js` first as an inline script, so when `pyodide.js` loads, it skips the dynamic import!

```javascript
// Step 1: Load pyodide.asm.js inline
<script>
// ... entire pyodide.asm.js content ...
</script>

// Step 2: Load pyodide.js inline (skips import)
<script>
// ... entire pyodide.js content ...
</script>
```

### Base64 Embedding Strategy

All binary files (WASM, fonts, Python packages) are:
1. Read as binary data
2. Encoded to base64 strings
3. Embedded in JavaScript constants
4. Decoded back to binary when needed

---

## Prerequisites

### Required Files

Before running the embedding scripts, you must have the `offline_libs/` directory with:

```
offline_libs/
├── ace.js                        # Ace code editor
├── jquery.min.js                 # jQuery library
├── mathquill.min.css             # MathQuill CSS
├── mathquill.min.js              # MathQuill JavaScript
├── quill.js                      # Quill rich text editor
├── quill.snow.css                # Quill theme CSS
├── tex-mml-chtml.js              # MathJax for LaTeX rendering
├── fonts/
│   ├── poppins-300.woff2         # Poppins Light
│   ├── poppins-400.woff2         # Poppins Regular
│   ├── poppins-500.woff2         # Poppins Medium
│   ├── poppins-600.woff2         # Poppins Semi-Bold
│   └── poppins-700.woff2         # Poppins Bold
└── pyodide/
    ├── pyodide.js                # Pyodide main runtime
    ├── pyodide.asm.js            # Pyodide module initializer
    ├── pyodide.asm.wasm          # Python compiled to WebAssembly
    ├── pyodide-lock.json         # Package metadata
    ├── python_stdlib.zip         # Python standard library
    ├── sympy-1.12-py3-none-any.whl          # SymPy (symbolic math)
    ├── mpmath-1.3.0-py3-none-any.whl        # Multiple precision math
    ├── lark-1.1.9-py3-none-any.whl          # Parser for LaTeX
    ├── micropip-0.5.0-py3-none-any.whl      # Pyodide package manager
    ├── packaging-23.1-py3-none-any.whl      # Package version utilities
    ├── Brotli-1.0.9-cp311-cp311-emscripten_3_1_45_wasm32.whl  # Compression
    └── distutils-1.0.0.zip        # Python packaging tools
```

### Software Requirements

- **Python 3.7+** with standard library
- **Source HTML files:** `create_problem.html` and `solve_problem.html`
- **At least 1 GB free disk space** for temporary processing
- **Text editor** supporting UTF-8 encoding

---

## Directory Structure

```
project-root/
├── create_problem.html                      # Source file (online version)
├── solve_problem.html                       # Source file (online version)
├── embed_offline.py                         # Embedding script for create_problem
├── embed_solve_offline.py                   # Embedding script for solve_problem
├── create_problem_offline_embedded.html     # Output (~51 MB)
├── solve_problem_offline_embedded.html      # Output (~49 MB)
├── offline_libs/                            # Library files (see Prerequisites)
└── OFFLINE_EMBEDDING_DOCUMENTATION.md       # This file
```

---

## Architecture

### High-Level Flow

```
┌─────────────────────┐
│  Source HTML File   │
│  (create_problem.   │
│   html or solve_    │
│   problem.html)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Embedding Script   │
│  (Python)           │
│  ├── Read source    │
│  ├── Read libraries │
│  ├── Encode base64  │
│  ├── Inject code    │
│  └── Write output   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Offline Embedded    │
│ HTML File           │
│ ├── Fetch intercept │
│ ├── Base64 data     │
│ ├── Pyodide inline  │
│ └── All dependencies│
└─────────────────────┘
```

### Component Interaction

```
User Opens HTML
     │
     ├──> Browser loads HTML
     │
     ├──> Fetch intercept installed
     │
     ├──> Pyodide.asm.js runs inline
     │    └──> Sets globalThis._createPyodideModule
     │
     ├──> Pyodide.js runs inline
     │    └──> Skips dynamic import (already defined)
     │
     ├──> Application calls loadPyodide()
     │
     ├──> Pyodide tries to fetch WASM
     │    └──> Intercepted → returns embedded base64
     │
     ├──> Pyodide tries to fetch packages
     │    └──> Intercepted → returns embedded wheels
     │
     └──> Application fully functional offline!
```

---

## Step-by-Step Process

### Part 1: Preparation

#### 1. Obtain Offline Libraries

Download all required libraries to `offline_libs/`:

```bash
# jQuery
wget https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js

# MathQuill
wget https://cdnjs.cloudflare.com/ajax/libs/mathquill/0.10.1/mathquill.min.js
wget https://cdnjs.cloudflare.com/ajax/libs/mathquill/0.10.1/mathquill.min.css

# Quill
wget https://cdn.quilljs.com/1.3.7/quill.js
wget https://cdn.quilljs.com/1.3.7/quill.snow.css

# MathJax
wget https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

# Ace Editor
wget https://cdnjs.cloudflare.com/ajax/libs/ace/1.32.3/ace.js

# Poppins Fonts (download from Google Fonts)
# Place in offline_libs/fonts/

# Pyodide (download from Pyodide release)
wget https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js
wget https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.asm.js
wget https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.asm.wasm
wget https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide-lock.json
wget https://cdn.jsdelivr.net/pyodide/v0.24.1/full/python_stdlib.zip

# Python packages (wheels)
# Download from Pyodide package index or PyPI
```

#### 2. Verify File Structure

Ensure all files are in place:

```bash
ls -la offline_libs/
ls -la offline_libs/fonts/
ls -la offline_libs/pyodide/
```

### Part 2: Embedding Process

#### For create_problem.html

**Script:** `embed_offline.py`

```bash
python embed_offline.py
```

**What it does:**

1. **Reads source HTML:**
   ```python
   html = read_file('create_problem.html')
   ```

2. **Reads and encodes fonts:**
   ```python
   font_300 = read_binary('offline_libs/fonts/poppins-300.woff2')
   # Returns base64 string
   ```

3. **Reads CSS libraries:**
   ```python
   mathquill_css = read_file('offline_libs/mathquill.min.css')
   quill_css = read_file('offline_libs/quill.snow.css')
   ```

4. **Reads JavaScript libraries:**
   ```python
   jquery_js = read_file('offline_libs/jquery.min.js')
   mathquill_js = read_file('offline_libs/mathquill.min.js')
   quill_js = read_file('offline_libs/quill.js')
   mathjax_js = read_file('offline_libs/tex-mml-chtml.js')
   ace_js = read_file('offline_libs/ace.js')
   ```

5. **Reads Pyodide runtime:**
   ```python
   pyodide_js = read_file('offline_libs/pyodide/pyodide.js')
   pyodide_asm_js = read_file('offline_libs/pyodide/pyodide.asm.js')
   pyodide_wasm_b64 = read_binary('offline_libs/pyodide/pyodide.asm.wasm')
   ```

6. **Reads Python packages:**
   ```python
   pkg_sympy = read_binary('offline_libs/pyodide/sympy-1.12-py3-none-any.whl')
   pkg_lark = read_binary('offline_libs/pyodide/lark-1.1.9-py3-none-any.whl')
   # ... and others
   ```

7. **Creates fetch interceptor:**
   ```javascript
   const EMBEDDED_B64 = {
       'pyodide.asm.wasm': "<base64_data>",
       'sympy': "<base64_data>",
       // ... all packages
   };

   window.fetch = async function(url, options) {
       if (url.includes('pyodide.asm.wasm')) {
           return new Response(b64ToBytes(EMBEDDED_B64['pyodide.asm.wasm']), {
               status: 200,
               headers: { 'Content-Type': 'application/wasm' }
           });
       }
       // ... handle all resources
   };
   ```

8. **Injects Pyodide inline:**
   ```html
   <script>
   // pyodide.asm.js content
   </script>
   <script>
   // pyodide.js content
   </script>
   ```

9. **Replaces CDN links:**
   ```python
   html = html.replace(
       '<script src="https://cdn.../jquery.min.js"></script>',
       '<script>/* jQuery */\n' + jquery_js + '</script>'
   )
   ```

10. **Writes output:**
    ```python
    with open('create_problem_offline_embedded.html', 'w', encoding='utf-8') as f:
        f.write(html)
    ```

#### For solve_problem.html

**Script:** `embed_solve_offline.py`

```bash
python embed_solve_offline.py
```

**Similar process but with solve_problem-specific modifications:**

- Uses regex patterns for more flexible replacement
- Handles different package loading sequence
- Optimized status messages for solving interface

### Part 3: Verification

#### Test the Output

```bash
# Windows
start create_problem_offline_embedded.html
start solve_problem_offline_embedded.html

# Mac/Linux
open create_problem_offline_embedded.html
open solve_problem_offline_embedded.html

# Or drag-and-drop into browser
```

#### Check Browser Console

Expected logs:
```
[Fetch Intercept] <url>
  -> Returning embedded WASM
Loading pyodide.asm.js inline...
_createPyodideModule defined: function
Loading pyodide.js inline...
loadPyodide defined: function
Fetch intercept installed
```

---

## Technical Details

### Fetch Interception Mechanism

#### How It Works

```javascript
// 1. Store original fetch
const _originalFetch = window.fetch;

// 2. Override fetch
window.fetch = async function(url, options) {
    const urlStr = String(url);

    // 3. Check if we have embedded data
    if (urlStr.includes('pyodide.asm.wasm')) {
        // 4. Decode base64 to bytes
        const bytes = b64ToBytes(EMBEDDED_B64['pyodide.asm.wasm']);

        // 5. Return as Response object (browser thinks it's real fetch!)
        return new Response(bytes, {
            status: 200,
            headers: { 'Content-Type': 'application/wasm' }
        });
    }

    // 6. Fallback to original fetch (will fail on file://)
    return await _originalFetch(url, options);
};
```

#### Why This Works on file://

The browser's security model restricts **network access** from `file://`, but it doesn't restrict:
- Calling JavaScript functions
- Creating `Response` objects manually
- Decoding base64 strings

So we "fake" the network request by returning a manually-created `Response` object!

### Base64 Encoding/Decoding

#### Encoding (Python)

```python
def read_binary(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

# Usage
wasm_base64 = read_binary('pyodide.asm.wasm')
# Returns: "AGFzbQEAAAABjYCAgAAC..."
```

#### Decoding (JavaScript)

```javascript
function b64ToBytes(b64) {
    const bin = atob(b64);  // Decode base64 to binary string
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) {
        bytes[i] = bin.charCodeAt(i);
    }
    return bytes;
}

// Usage
const wasmBytes = b64ToBytes(EMBEDDED_B64['pyodide.asm.wasm']);
// Returns: Uint8Array [0, 97, 115, 109, ...]
```

### Pyodide Initialization Sequence

#### Normal (CDN) Flow

```
1. Load pyodide.js from CDN
2. Call loadPyodide()
3. Pyodide dynamically imports pyodide.asm.js
4. Pyodide fetches pyodide.asm.wasm
5. Pyodide fetches python_stdlib.zip
6. Pyodide fetches packages via micropip
```

**Problem:** Steps 1, 3-6 require network access!

#### Offline Embedded Flow

```
1. Load pyodide.asm.js INLINE
   └─> Sets globalThis._createPyodideModule
2. Load pyodide.js INLINE
   └─> Sees _createPyodideModule exists
   └─> SKIPS dynamic import!
3. Call loadPyodide({ indexURL: './' })
4. Pyodide tries to fetch WASM
   └─> INTERCEPTED → returns embedded base64
5. Pyodide tries to fetch stdlib
   └─> INTERCEPTED → returns embedded base64
6. Directly unpack wheel files from memory
   └─> window.pyodide.unpackArchive(wheelBytes, 'wheel')
```

**Solution:** All fetches are intercepted and served from memory!

### Package Installation Without micropip

#### Traditional Method (Requires Network)

```javascript
await window.pyodide.loadPackage('micropip');
await window.pyodide.runPythonAsync(`
    import micropip
    await micropip.install('lark')
`);
```

**Problem:** micropip validates package hashes from PyPI index (requires network)

#### Offline Method (Direct Extraction)

```javascript
// Get wheel bytes from embedded base64
const larkBytes = getLarkWheelBytes();

// Directly extract wheel to site-packages
await window.pyodide.unpackArchive(larkBytes, 'wheel');

// Now the package is available!
```

**Advantage:** Bypasses hash validation, works completely offline

### Font Embedding

#### CSS @font-face with Data URLs

```css
@font-face {
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 400;
    font-display: swap;
    src: url(data:font/woff2;base64,<BASE64_ENCODED_FONT>) format('woff2');
}
```

**Benefits:**
- No external requests
- Browser caches fonts automatically
- Works on all modern browsers

### String Escaping for Inline Scripts

When embedding JavaScript with template literals:

```python
# Escape backslashes, backticks, and template literals
escaped_js = ace_js.replace('\\', '\\\\')    # \ → \\
escaped_js = escaped_js.replace('`', '\\`')  # ` → \`
escaped_js = escaped_js.replace('${', '\\${') # ${ → \${

# Now safe to embed in template literal
html = html.replace(
    "script.src = 'https://...ace.js';",
    f"script.textContent = `{escaped_js}`;"
)
```

---

## Troubleshooting

### Common Issues

#### 1. "Module not found" or "Import error"

**Symptom:**
```
Error: Cannot find module 'lark'
```

**Causes:**
- Package wheel not embedded
- Package not extracted properly
- Wrong package version

**Solution:**
```python
# Verify package is embedded
pkg_lark = read_binary('offline_libs/pyodide/lark-1.1.9-py3-none-any.whl')

# Check extraction code
await window.pyodide.unpackArchive(larkBytes, 'wheel');
```

#### 2. "WASM streaming failed"

**Symptom:**
```
CompileError: WebAssembly.instantiateStreaming(): expected magic word
```

**Causes:**
- WASM file corrupted
- Wrong base64 encoding
- File size mismatch

**Solution:**
```python
# Verify WASM file integrity
import os
original_size = os.path.getsize('offline_libs/pyodide/pyodide.asm.wasm')
print(f"WASM file size: {original_size} bytes")

# Check base64 encoding
import base64
with open('offline_libs/pyodide/pyodide.asm.wasm', 'rb') as f:
    data = f.read()
    encoded = base64.b64encode(data).decode('utf-8')
    decoded = base64.b64decode(encoded)
    assert data == decoded, "Base64 encoding/decoding mismatch!"
```

#### 3. "Fetch failed" for fonts or CSS

**Symptom:**
```
GET file:///... net::ERR_FILE_NOT_FOUND
```

**Causes:**
- CDN link not replaced
- Missing replacement in script

**Solution:**
```python
# Add missing replacement
html = html.replace(
    '<link href="<CDN_URL>" rel="stylesheet">',
    '<style>/* Library */\n' + library_css + '</style>'
)
```

#### 4. File too large for browser

**Symptom:**
- Browser crashes or freezes
- "Out of memory" error

**Causes:**
- Browser memory limits
- Too many large files

**Solution:**
- Use Chrome/Edge (better memory handling)
- Close other tabs
- Increase browser memory: `chrome --js-flags="--max-old-space-size=4096"`

#### 5. UTF-8 encoding issues

**Symptom:**
```
UnicodeDecodeError: 'charmap' codec can't decode byte
```

**Solution:**
```python
# Always use UTF-8 encoding
with open(path, 'r', encoding='utf-8') as f:
    return f.read()

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)
```

### Debugging Tips

#### 1. Check Browser Console

Open Developer Tools (F12) and monitor:
- Fetch intercept logs
- Error messages
- Network tab (should be empty if everything is embedded)

#### 2. Verify Base64 Data

```javascript
// In browser console
console.log(EMBEDDED_B64['pyodide.asm.wasm'].substring(0, 100));
// Should show: "AGFzbQEAAAABjYCAgAAC..."

// Test decoding
const bytes = b64ToBytes(EMBEDDED_B64['pyodide.asm.wasm']);
console.log(bytes.length); // Should be several MB
console.log(bytes.slice(0, 4)); // Should be [0, 97, 115, 109] (WASM magic number)
```

#### 3. Test Pyodide Initialization

```javascript
// After page load
console.log('_createPyodideModule:', typeof _createPyodideModule);  // Should be 'function'
console.log('loadPyodide:', typeof loadPyodide);                    // Should be 'function'
console.log('window.pyodide:', window.pyodide);                     // Should be object after init
```

#### 4. Compare File Sizes

```bash
# Original libraries total size
du -sh offline_libs/
# Should be ~45-50 MB

# Output file size
ls -lh create_problem_offline_embedded.html
# Should be ~51 MB (includes HTML + all libraries)
```

---

## Maintenance

### Updating Libraries

When CDN libraries are updated:

1. **Download new versions:**
   ```bash
   wget <NEW_CDN_URL> -O offline_libs/library.js
   ```

2. **Update version references in scripts:**
   ```python
   # In embed_offline.py or embed_solve_offline.py
   library_js = read_file(os.path.join(OFFLINE_LIBS, 'library.js'))
   ```

3. **Regenerate offline files:**
   ```bash
   python embed_offline.py
   python embed_solve_offline.py
   ```

### Updating Pyodide

To update Pyodide version:

1. **Download new Pyodide release:**
   ```bash
   # Example for v0.25.0
   wget https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js
   wget https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.asm.js
   wget https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.asm.wasm
   wget https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide-lock.json
   wget https://cdn.jsdelivr.net/pyodide/v0.25.0/full/python_stdlib.zip
   ```

2. **Update package wheels** (if needed):
   - Check new package versions in `pyodide-lock.json`
   - Download updated wheels from Pyodide package index

3. **Update source HTML files:**
   ```javascript
   // In create_problem.html and solve_problem.html
   const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js';
   const PYODIDE_INDEX_URL = 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/';
   ```

4. **Update embedding scripts:**
   ```python
   # Update URL patterns to match new version
   html = html.replace(
       "const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js';",
       "const PYODIDE_URL = 'embedded';"
   )
   ```

5. **Test thoroughly** before committing

### Adding New Dependencies

To add a new library:

1. **Download library:**
   ```bash
   wget <LIBRARY_URL> -O offline_libs/new_library.js
   ```

2. **Add to embedding script:**
   ```python
   # Read the library
   new_library_js = read_file(os.path.join(OFFLINE_LIBS, 'new_library.js'))

   # Replace CDN link
   html = html.replace(
       '<script src="<CDN_URL>"></script>',
       '<script>/* New Library */\n' + new_library_js + '</script>'
   )
   ```

3. **Regenerate and test**

### Adding New Python Packages

To add a new Python package:

1. **Download wheel file:**
   ```bash
   # From Pyodide package index or PyPI (must be compatible with emscripten)
   wget <PACKAGE_WHEEL_URL> -O offline_libs/pyodide/package-version.whl
   ```

2. **Add to embedding script:**
   ```python
   # In embed_offline.py or embed_solve_offline.py
   pkg_newpackage = read_binary(os.path.join(OFFLINE_LIBS, 'pyodide', 'package-version.whl'))

   # Add to EMBEDDED_B64
   'newpackage': "{pkg_newpackage}",

   # Add to fetch intercept
   if (urlStr.includes('newpackage') && urlStr.endsWith('.whl')) {
       console.log('  -> Returning embedded newpackage');
       return new Response(b64ToBytes(EMBEDDED_B64['newpackage']), { status: 200 });
   }

   # Add getter function
   function getNewPackageWheelBytes() {
       return b64ToBytes(EMBEDDED_B64['newpackage']);
   }

   # Add extraction code
   const newPackageBytes = getNewPackageWheelBytes();
   await window.pyodide.unpackArchive(newPackageBytes, 'wheel');
   ```

3. **Regenerate and test import:**
   ```python
   # In browser console after loading
   await window.pyodide.runPythonAsync("import newpackage")
   ```

---

## Performance Considerations

### File Size

**Current sizes:**
- `create_problem_offline_embedded.html`: ~51 MB
- `solve_problem_offline_embedded.html`: ~49 MB

**Breakdown:**
- Pyodide WASM: ~15 MB
- Python stdlib: ~10 MB
- Python packages (SymPy, etc.): ~15 MB
- JavaScript libraries: ~5 MB
- Fonts: ~1 MB
- MathJax: ~2 MB
- HTML + inline scripts: ~2 MB

### Loading Time

**Typical load times (on modern hardware):**
- HTML parsing: 2-3 seconds
- Pyodide initialization: 3-5 seconds
- Package extraction: 2-3 seconds
- **Total:** 7-11 seconds

**Optimization tips:**
- Use SSD for faster file reading
- Close other browser tabs
- Use Chrome/Edge (faster WASM compilation)
- Increase browser memory if needed

### Memory Usage

**Peak memory during initialization:**
- ~400 MB for Pyodide
- ~200 MB for packages
- ~100 MB for base64 decoding
- **Total:** ~700 MB RAM

**Minimum requirements:**
- 2 GB RAM (4 GB recommended)
- Modern browser (Chrome 90+, Firefox 88+, Edge 90+)

### Browser Compatibility

**Tested and working:**
- ✅ Chrome 90+ (recommended)
- ✅ Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+ (slower loading)

**Not supported:**
- ❌ Internet Explorer (no WASM support)
- ❌ Very old browsers (pre-2020)

---

## Advanced Topics

### Custom Pyodide Configuration

You can customize Pyodide initialization:

```javascript
window.pyodide = await loadPyodide({
    indexURL: './',
    fullStdLib: true,        // Load entire stdlib
    stdin: /* custom */,     // Custom stdin handler
    stdout: /* custom */,    // Custom stdout handler
    stderr: /* custom */,    // Custom stderr handler
    env: { /* vars */ }      // Environment variables
});
```

### Selective Package Loading

To reduce file size, load packages on-demand:

```javascript
// Instead of loading all packages at startup
// Load only when needed

async function loadSymPyIfNeeded() {
    if (!window.pyodide.pyimport('sympy')) {
        const sympyBytes = getSymPyWheelBytes();
        await window.pyodide.unpackArchive(sympyBytes, 'wheel');
    }
}

// Call before using SymPy
await loadSymPyIfNeeded();
```

### Progressive Enhancement

Start with basic functionality, add features progressively:

```javascript
// Stage 1: Basic HTML/CSS/JS (instant)
document.addEventListener('DOMContentLoaded', () => {
    showBasicInterface();
});

// Stage 2: Math rendering (1-2 seconds)
await loadMathJax();
renderMathEquations();

// Stage 3: Pyodide (5-10 seconds)
await initPyodide();
enableAdvancedFeatures();
```

### Compression

To reduce file size further:

1. **Gzip the HTML file:**
   ```bash
   gzip create_problem_offline_embedded.html
   # Creates .html.gz (reduces to ~25 MB)
   ```

2. **Serve with gzip header** (if hosting on web server)

3. **Note:** Won't work on `file://` protocol without browser extension

---

## Security Considerations

### Content Security Policy

If hosting offline files on a web server, use CSP:

```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:;">
```

**Why `unsafe-inline` and `unsafe-eval`:**
- Pyodide requires `eval()` for Python execution
- Inline scripts are necessary for base64 data

### Data Integrity

Verify files haven't been tampered with:

```python
import hashlib

def verify_file_hash(file_path, expected_hash):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    actual_hash = sha256.hexdigest()
    assert actual_hash == expected_hash, f"Hash mismatch: {actual_hash} != {expected_hash}"

# Verify WASM file
verify_file_hash(
    'offline_libs/pyodide/pyodide.asm.wasm',
    '<EXPECTED_SHA256_HASH>'
)
```

### Sandboxing

Pyodide runs in a sandboxed WebAssembly environment:
- No access to filesystem (except virtual filesystem)
- No access to network (except intercepted fetch)
- No access to system resources

---

## FAQ

### Q: Why is the file so large?

**A:** The file embeds an entire Python runtime (Pyodide WASM) plus all dependencies. This is necessary for offline functionality.

### Q: Can I reduce the file size?

**A:** Yes, by:
1. Removing unused packages
2. Using a smaller Python runtime (not recommended)
3. Compressing with gzip (won't work on file://)
4. Loading packages on-demand instead of at startup

### Q: Will this work on mobile browsers?

**A:** Yes, but:
- May be slower due to less memory/CPU
- Large file size may cause issues on low-end devices
- Test on target devices before deploying

### Q: Can I distribute this file to others?

**A:** Yes! That's the whole point. Users can:
- Download the HTML file
- Open it locally without internet
- Use all features offline

### Q: Do I need to regenerate offline files for every update?

**A:** Yes, whenever you update:
- Source HTML files (create_problem.html, solve_problem.html)
- Library versions
- Python packages
- Matrix functions or other features

### Q: Can I host this on a website?

**A:** Yes, but the original HTML files (non-embedded) are better for web hosting because:
- Faster loading (uses CDN caching)
- Smaller bandwidth usage
- Browser can cache components separately

**Use offline embedded versions for:**
- Distribution to students
- USB drives
- Offline workshops
- Air-gapped environments

---

## Conclusion

The offline embedding process transforms web applications into fully self-contained HTML files that work without internet access. This is achieved through:

1. **Fetch interception** - Serving embedded data as fake network responses
2. **Base64 encoding** - Embedding binary data as text
3. **Pyodide pre-loading** - Loading WASM runtime inline to bypass dynamic imports
4. **Direct wheel extraction** - Installing Python packages without network access

This technique enables true offline functionality while maintaining full feature parity with the online version.

---

## Appendix

### Script Templates

#### Basic Embedding Script Template

```python
#!/usr/bin/env python3
"""Embed resources into HTML for offline use"""
import base64
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OFFLINE_LIBS = os.path.join(BASE_DIR, 'offline_libs')

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def read_binary(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def main():
    # Read source
    html = read_file('source.html')

    # Read libraries
    library_js = read_file(os.path.join(OFFLINE_LIBS, 'library.js'))

    # Replace CDN links
    html = html.replace(
        '<script src="CDN_URL"></script>',
        '<script>\n' + library_js + '\n</script>'
    )

    # Write output
    with open('output_offline.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Done!")

if __name__ == '__main__':
    main()
```

### Useful Commands

```bash
# Check file sizes
du -sh offline_libs/*
du -sh *.html

# Find all CDN references in HTML
grep -n "cdn\|https://" create_problem.html

# Test base64 encoding/decoding
echo "Test" | base64
echo "VGVzdAo=" | base64 -d

# Monitor browser memory usage
# Chrome: chrome://memory-internals/
# Firefox: about:memory

# Clear browser cache
# Chrome: Ctrl+Shift+Del
# Firefox: Ctrl+Shift+Del

# Regenerate both offline files
python embed_offline.py && python embed_solve_offline.py
```

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-30 | Initial implementation with Pyodide 0.24.1 |
| 1.1 | 2025-12-01 | Added all matrix functions (trace, rank, rref, eigenvalues, etc.) |

---

**Document Maintained By:** Claude Code
**Last Updated:** December 1, 2025
**Questions or Issues?** Check the troubleshooting section or create an issue on GitHub.
