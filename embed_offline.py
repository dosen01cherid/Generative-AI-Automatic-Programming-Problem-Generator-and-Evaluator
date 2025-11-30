#!/usr/bin/env python3
"""
Embed everything into a single HTML that works on file:// protocol.
Key insight: pyodide.asm.js sets globalThis._createPyodideModule,
and pyodide.js checks for it before dynamic import. So we load
pyodide.asm.js first as inline script, then pyodide.js skips the import!
"""
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
    print("Reading source HTML (using main file with correct emojis)...")
    # Use the main create_problem.html which has correct UTF-8 emojis
    html_path = os.path.join(BASE_DIR, 'create_problem.html')
    html = read_file(html_path)

    print("Reading fonts...")
    font_300 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-300.woff2'))
    font_400 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-400.woff2'))
    font_500 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-500.woff2'))
    font_600 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-600.woff2'))
    font_700 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-700.woff2'))

    print("Reading CSS...")
    mathquill_css = read_file(os.path.join(OFFLINE_LIBS, 'mathquill.min.css'))
    quill_css = read_file(os.path.join(OFFLINE_LIBS, 'quill.snow.css'))

    print("Reading JS libraries...")
    jquery_js = read_file(os.path.join(OFFLINE_LIBS, 'jquery.min.js'))
    mathquill_js = read_file(os.path.join(OFFLINE_LIBS, 'mathquill.min.js'))
    quill_js = read_file(os.path.join(OFFLINE_LIBS, 'quill.js'))
    mathjax_js = read_file(os.path.join(OFFLINE_LIBS, 'tex-mml-chtml.js'))
    ace_js = read_file(os.path.join(OFFLINE_LIBS, 'ace.js'))

    print("Reading Pyodide (this takes a moment)...")
    pyodide_js = read_file(os.path.join(OFFLINE_LIBS, 'pyodide', 'pyodide.js'))
    pyodide_asm_js = read_file(os.path.join(OFFLINE_LIBS, 'pyodide', 'pyodide.asm.js'))
    pyodide_lock = read_file(os.path.join(OFFLINE_LIBS, 'pyodide', 'pyodide-lock.json'))
    pyodide_wasm_b64 = read_binary(os.path.join(OFFLINE_LIBS, 'pyodide', 'pyodide.asm.wasm'))

    print("Reading Python standard library...")
    python_stdlib_b64 = read_binary(os.path.join(OFFLINE_LIBS, 'pyodide', 'python_stdlib.zip'))

    print("Reading Python packages...")
    pkg_sympy = read_binary(os.path.join(OFFLINE_LIBS, 'pyodide', 'sympy-1.12-py3-none-any.whl'))
    pkg_micropip = read_binary(os.path.join(OFFLINE_LIBS, 'pyodide', 'micropip-0.5.0-py3-none-any.whl'))
    pkg_mpmath = read_binary(os.path.join(OFFLINE_LIBS, 'pyodide', 'mpmath-1.3.0-py3-none-any.whl'))
    pkg_packaging = read_binary(os.path.join(OFFLINE_LIBS, 'pyodide', 'packaging-23.1-py3-none-any.whl'))
    pkg_brotli = read_binary(os.path.join(OFFLINE_LIBS, 'pyodide', 'Brotli-1.0.9-cp311-cp311-emscripten_3_1_45_wasm32.whl'))
    pkg_distutils = read_binary(os.path.join(OFFLINE_LIBS, 'pyodide', 'distutils-1.0.0.zip'))
    pkg_lark = read_binary(os.path.join(OFFLINE_LIBS, 'pyodide', 'lark-1.1.9-py3-none-any.whl'))

    # The magic: intercept fetch and provide embedded data as Response objects
    # This works on file:// because we're not actually fetching, just returning data
    fetch_intercept = f'''
<script>
// ============================================================
// EMBEDDED DATA AS BASE64
// ============================================================
const EMBEDDED_B64 = {{
    'pyodide.asm.wasm': "{pyodide_wasm_b64}",
    'pyodide-lock.json': "{base64.b64encode(pyodide_lock.encode('utf-8')).decode('utf-8')}",
    'python_stdlib.zip': "{python_stdlib_b64}",
    'sympy': "{pkg_sympy}",
    'micropip': "{pkg_micropip}",
    'mpmath': "{pkg_mpmath}",
    'packaging': "{pkg_packaging}",
    'brotli': "{pkg_brotli}",
    'distutils': "{pkg_distutils}",
    'lark': "{pkg_lark}"
}};

// Convert base64 to Uint8Array
function b64ToBytes(b64) {{
    const bin = atob(b64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return bytes;
}}

// Convert base64 to string
function b64ToText(b64) {{
    return atob(b64);
}}

// Get lark wheel bytes for direct installation
function getLarkWheelBytes() {{
    return b64ToBytes(EMBEDDED_B64['lark']);
}}

// ============================================================
// INTERCEPT FETCH - Return embedded data as Response
// This is the key to making file:// work!
// ============================================================
const _originalFetch = window.fetch;
window.fetch = async function(url, options) {{
    const urlStr = String(url);
    console.log('[Fetch Intercept]', urlStr);

    // WASM file
    if (urlStr.includes('pyodide.asm.wasm')) {{
        console.log('  -> Returning embedded WASM');
        const bytes = b64ToBytes(EMBEDDED_B64['pyodide.asm.wasm']);
        return new Response(bytes, {{
            status: 200,
            headers: {{ 'Content-Type': 'application/wasm' }}
        }});
    }}

    // Lock file
    if (urlStr.includes('pyodide-lock.json')) {{
        console.log('  -> Returning embedded lock file');
        const text = b64ToText(EMBEDDED_B64['pyodide-lock.json']);
        return new Response(text, {{
            status: 200,
            headers: {{ 'Content-Type': 'application/json' }}
        }});
    }}

    // Python standard library
    if (urlStr.includes('python_stdlib.zip')) {{
        console.log('  -> Returning embedded python_stdlib.zip');
        const bytes = b64ToBytes(EMBEDDED_B64['python_stdlib.zip']);
        return new Response(bytes, {{
            status: 200,
            headers: {{ 'Content-Type': 'application/zip' }}
        }});
    }}

    // Python packages
    if (urlStr.includes('sympy') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded sympy');
        return new Response(b64ToBytes(EMBEDDED_B64['sympy']), {{ status: 200 }});
    }}
    if (urlStr.includes('micropip') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded micropip');
        return new Response(b64ToBytes(EMBEDDED_B64['micropip']), {{ status: 200 }});
    }}
    if (urlStr.includes('mpmath') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded mpmath');
        return new Response(b64ToBytes(EMBEDDED_B64['mpmath']), {{ status: 200 }});
    }}
    if (urlStr.includes('packaging') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded packaging');
        return new Response(b64ToBytes(EMBEDDED_B64['packaging']), {{ status: 200 }});
    }}
    if (urlStr.includes('Brotli') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded brotli');
        return new Response(b64ToBytes(EMBEDDED_B64['brotli']), {{ status: 200 }});
    }}
    if (urlStr.includes('distutils') && urlStr.endsWith('.zip')) {{
        console.log('  -> Returning embedded distutils');
        return new Response(b64ToBytes(EMBEDDED_B64['distutils']), {{ status: 200 }});
    }}
    if (urlStr.includes('lark') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded lark');
        return new Response(b64ToBytes(EMBEDDED_B64['lark']), {{ status: 200 }});
    }}

    // Default: try original fetch (will fail on file://, but some things might not need it)
    console.log('  -> Passing through to original fetch');
    try {{
        return await _originalFetch(url, options);
    }} catch (e) {{
        console.warn('  -> Fetch failed:', e.message);
        throw e;
    }}
}};

console.log('Fetch intercept installed');
</script>

<!-- Load pyodide.asm.js FIRST - this sets globalThis._createPyodideModule -->
<script>
console.log('Loading pyodide.asm.js inline...');
{pyodide_asm_js}
console.log('_createPyodideModule defined:', typeof _createPyodideModule);
</script>

<!-- Now load pyodide.js - it will SKIP dynamic import since _createPyodideModule exists! -->
<script>
console.log('Loading pyodide.js inline...');
{pyodide_js}
console.log('loadPyodide defined:', typeof loadPyodide);
</script>
'''

    # Fonts CSS with embedded base64
    fonts_css = f'''
@font-face {{
  font-family: 'Poppins'; font-style: normal; font-weight: 300; font-display: swap;
  src: url(data:font/woff2;base64,{font_300}) format('woff2');
}}
@font-face {{
  font-family: 'Poppins'; font-style: normal; font-weight: 400; font-display: swap;
  src: url(data:font/woff2;base64,{font_400}) format('woff2');
}}
@font-face {{
  font-family: 'Poppins'; font-style: normal; font-weight: 500; font-display: swap;
  src: url(data:font/woff2;base64,{font_500}) format('woff2');
}}
@font-face {{
  font-family: 'Poppins'; font-style: normal; font-weight: 600; font-display: swap;
  src: url(data:font/woff2;base64,{font_600}) format('woff2');
}}
@font-face {{
  font-family: 'Poppins'; font-style: normal; font-weight: 700; font-display: swap;
  src: url(data:font/woff2;base64,{font_700}) format('woff2');
}}
'''

    print("Replacing CDN references with embedded content...")

    # Replace CDN CSS links with inline styles
    html = html.replace(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mathquill/0.10.1/mathquill.min.css">',
        '<style>/* MathQuill */\n' + mathquill_css + '</style>'
    )
    html = html.replace(
        '<link href="https://cdn.quilljs.com/1.3.7/quill.snow.css" rel="stylesheet">',
        '<style>/* Quill */\n' + quill_css + '</style>'
    )

    # Replace Google Fonts import with embedded fonts
    html = html.replace(
        "@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');",
        fonts_css
    )

    print("Replacing CDN JS with embedded scripts...")

    # Replace CDN JS with inline scripts
    html = html.replace(
        '<script src="https://cdn.quilljs.com/1.3.7/quill.js"></script>',
        '<script>/* Quill */\n' + quill_js + '</script>'
    )
    html = html.replace(
        '<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>',
        '<script>/* MathJax */\n' + mathjax_js + '</script>'
    )
    html = html.replace(
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>',
        '<script>/* jQuery */\n' + jquery_js + '</script>'
    )
    html = html.replace(
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathquill/0.10.1/mathquill.min.js"></script>',
        '<script>/* MathQuill */\n' + mathquill_js + '</script>'
    )

    # Embed Ace editor
    html = html.replace(
        "script.src = 'https://cdnjs.cloudflare.com/ajax/libs/ace/1.32.3/ace.js';",
        f"script.textContent = `{ace_js.replace(chr(92), chr(92)+chr(92)).replace('`', chr(92)+'`').replace('${', chr(92)+'${')}`;"
    )

    print("Updating Pyodide configuration...")

    # Update Pyodide URLs to use embedded versions
    html = html.replace(
        "const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js';",
        "const PYODIDE_URL = 'embedded';"
    )
    html = html.replace(
        "const PYODIDE_INDEX_URL = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/';",
        "const PYODIDE_INDEX_URL = './';"
    )

    # Replace getCachedScript - Pyodide is already loaded inline
    old_getCachedScript = '''async function getCachedScript(url) {
      if (!CACHING_AVAILABLE) {
        updateLoadingStatus('Loading Pyodide from CDN...');
        const response = await fetch(url);
        return await response.text();
      }

      try {
        const cache = await caches.open(CACHE_VERSION);
        let response = await cache.match(url);

        if (!response) {
          updateLoadingStatus('Downloading Pyodide (first time)...');
          response = await fetch(url);
          await cache.put(url, response.clone());
          updateLoadingStatus('Cached for next time!');
        } else {
          updateLoadingStatus('Loading Pyodide from cache...');
        }

        return await response.text();
      } catch (e) {
        updateLoadingStatus('Cache unavailable, using CDN...');
        const response = await fetch(url);
        return await response.text();
      }
    }'''

    new_getCachedScript = '''async function getCachedScript(url) {
      updateLoadingStatus('Using embedded Pyodide...');
      return ''; // Pyodide already loaded inline
    }'''

    html = html.replace(old_getCachedScript, new_getCachedScript)

    # Skip the script loading part
    old_initPyodide_part = '''const scriptText = await getCachedScript(PYODIDE_URL);
      const script = document.createElement('script');
      script.textContent = scriptText;
      document.head.appendChild(script);

      await new Promise(resolve => setTimeout(resolve, 100));'''

    new_initPyodide_part = '''// Pyodide already loaded inline!
      await getCachedScript(PYODIDE_URL);
      updateLoadingStatus('Pyodide ready...');
      await new Promise(resolve => setTimeout(resolve, 50));'''

    html = html.replace(old_initPyodide_part, new_initPyodide_part)

    # Fix loadPyodide call
    old_loadPyodide = '''window.pyodide = await loadPyodide({
        indexURL: PYODIDE_INDEX_URL
      });'''

    new_loadPyodide = '''// Load with embedded resources (fetch intercepted)
      updateLoadingStatus('Initializing Python...');
      window.pyodide = await loadPyodide({
        indexURL: './'
      });'''

    html = html.replace(old_loadPyodide, new_loadPyodide)

    # Replace micropip/lark installation with direct wheel extraction
    old_lark_block = '''      // Load lark via micropip (will use browser HTTP cache)
      updateLoadingStatus('Loading lark...');
      await window.pyodide.loadPackage('micropip');

      await window.pyodide.runPythonAsync(`
import micropip
await micropip.install('lark')
      `);'''

    new_lark_block = '''      // Load lark by directly extracting the wheel (bypasses micropip hash validation)
      updateLoadingStatus('Loading lark...');

      // Get lark wheel bytes and extract directly to site-packages
      const larkBytes = getLarkWheelBytes();
      await window.pyodide.unpackArchive(larkBytes, 'wheel');'''

    html = html.replace(old_lark_block, new_lark_block)

    # Inject fetch intercept and Pyodide AFTER charset declaration (to preserve UTF-8 encoding)
    html = html.replace('<meta charset="utf-8" />', '<meta charset="utf-8" />\n' + fetch_intercept)

    print("Writing output file...")
    output_path = os.path.join(BASE_DIR, 'create_problem_offline_embedded.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\nCreated: {output_path}")
    print(f"File size: {size_mb:.2f} MB")
    print("\n*** This should work on file:// protocol! ***")
    print("Just double-click the HTML file to open it.")

if __name__ == '__main__':
    main()
