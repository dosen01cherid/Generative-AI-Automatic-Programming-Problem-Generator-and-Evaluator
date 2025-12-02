#!/usr/bin/env python3
"""
Embed resources into HTML for offline use.
This script takes the source HTML files and creates self-contained offline versions.
"""
import base64
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OFFLINE_LIBS = os.path.join(BASE_DIR, 'offline_libs')

def read_file(path):
    """Read a text file with UTF-8 encoding."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def read_binary(path):
    """Read a binary file and return base64-encoded string."""
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def safe_replace(html, pattern, replacement):
    """Replace pattern with replacement using simple string replace after finding match."""
    import re
    match = re.search(pattern, html)
    if match:
        return html[:match.start()] + replacement + html[match.end():]
    return html

def embed_create_problem():
    """Generate create_problem_offline_embedded.html"""
    print("Embedding create_problem.html...")

    # Read source
    html = read_file(os.path.join(BASE_DIR, 'create_problem.html'))

    # Read fonts
    print("  - Embedding fonts...")
    font_300 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-300.woff2'))
    font_400 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-400.woff2'))
    font_500 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-500.woff2'))
    font_600 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-600.woff2'))
    font_700 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-700.woff2'))

    # Create embedded font CSS
    font_css = f'''
    @font-face {{
        font-family: 'Poppins';
        font-style: normal;
        font-weight: 300;
        font-display: swap;
        src: url(data:font/woff2;base64,{font_300}) format('woff2');
    }}
    @font-face {{
        font-family: 'Poppins';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(data:font/woff2;base64,{font_400}) format('woff2');
    }}
    @font-face {{
        font-family: 'Poppins';
        font-style: normal;
        font-weight: 500;
        font-display: swap;
        src: url(data:font/woff2;base64,{font_500}) format('woff2');
    }}
    @font-face {{
        font-family: 'Poppins';
        font-style: normal;
        font-weight: 600;
        font-display: swap;
        src: url(data:font/woff2;base64,{font_600}) format('woff2');
    }}
    @font-face {{
        font-family: 'Poppins';
        font-style: normal;
        font-weight: 700;
        font-display: swap;
        src: url(data:font/woff2;base64,{font_700}) format('woff2');
    }}
    '''

    # Replace Google Fonts link with embedded fonts
    html = safe_replace(html,
        r'<link[^>]*href="https://fonts\.googleapis\.com[^"]*"[^>]*>',
        f'<style>{font_css}</style>'
    )

    # Read and embed CSS libraries
    print("  - Embedding CSS libraries...")
    mathquill_css = read_file(os.path.join(OFFLINE_LIBS, 'mathquill.min.css'))
    quill_css = read_file(os.path.join(OFFLINE_LIBS, 'quill.snow.css'))

    html = safe_replace(html,
        r'<link[^>]*href="[^"]*mathquill[^"]*\.css"[^>]*>',
        f'<style>/* MathQuill CSS */\n{mathquill_css}</style>'
    )
    html = safe_replace(html,
        r'<link[^>]*href="[^"]*quill\.snow\.css"[^>]*>',
        f'<style>/* Quill CSS */\n{quill_css}</style>'
    )

    # Read and embed JavaScript libraries
    print("  - Embedding JavaScript libraries...")
    jquery_js = read_file(os.path.join(OFFLINE_LIBS, 'jquery.min.js'))
    mathquill_js = read_file(os.path.join(OFFLINE_LIBS, 'mathquill.min.js'))
    quill_js = read_file(os.path.join(OFFLINE_LIBS, 'quill.js'))
    mathjax_js = read_file(os.path.join(OFFLINE_LIBS, 'tex-mml-chtml.js'))
    ace_js = read_file(os.path.join(OFFLINE_LIBS, 'ace.js'))

    # Replace CDN script tags with inline scripts
    html = safe_replace(html,
        r'<script[^>]*src="[^"]*jquery[^"]*\.js"[^>]*></script>',
        f'<script>/* jQuery */\n{jquery_js}</script>'
    )
    html = safe_replace(html,
        r'<script[^>]*src="[^"]*mathquill[^"]*\.js"[^>]*></script>',
        f'<script>/* MathQuill */\n{mathquill_js}</script>'
    )
    html = safe_replace(html,
        r'<script[^>]*src="[^"]*quill\.js"[^>]*></script>',
        f'<script>/* Quill */\n{quill_js}</script>'
    )

    # Read Pyodide files
    print("  - Embedding Pyodide runtime...")
    pyodide_dir = os.path.join(OFFLINE_LIBS, 'pyodide')
    pyodide_js = read_file(os.path.join(pyodide_dir, 'pyodide.js'))
    pyodide_asm_js = read_file(os.path.join(pyodide_dir, 'pyodide.asm.js'))
    pyodide_wasm = read_binary(os.path.join(pyodide_dir, 'pyodide.asm.wasm'))
    pyodide_lock = read_file(os.path.join(pyodide_dir, 'pyodide-lock.json'))
    python_stdlib = read_binary(os.path.join(pyodide_dir, 'python_stdlib.zip'))

    # Read Python packages
    print("  - Embedding Python packages...")
    pkg_sympy = read_binary(os.path.join(pyodide_dir, 'sympy-1.12-py3-none-any.whl'))
    pkg_mpmath = read_binary(os.path.join(pyodide_dir, 'mpmath-1.3.0-py3-none-any.whl'))
    pkg_lark = read_binary(os.path.join(pyodide_dir, 'lark-1.1.9-py3-none-any.whl'))
    pkg_micropip = read_binary(os.path.join(pyodide_dir, 'micropip-0.5.0-py3-none-any.whl'))
    pkg_packaging = read_binary(os.path.join(pyodide_dir, 'packaging-23.1-py3-none-any.whl'))

    # Check for optional packages
    brotli_path = os.path.join(pyodide_dir, 'Brotli-1.0.9-cp311-cp311-emscripten_3_1_45_wasm32.whl')
    pkg_brotli = read_binary(brotli_path) if os.path.exists(brotli_path) else ""

    distutils_path = os.path.join(pyodide_dir, 'distutils-1.0.0.zip')
    pkg_distutils = read_binary(distutils_path) if os.path.exists(distutils_path) else ""

    # Create fetch interceptor and embedded data
    fetch_intercept = f'''
<script>
// Embedded base64 data for offline use
const EMBEDDED_B64 = {{
    'pyodide.asm.wasm': "{pyodide_wasm}",
    'python_stdlib.zip': "{python_stdlib}",
    'sympy': "{pkg_sympy}",
    'mpmath': "{pkg_mpmath}",
    'lark': "{pkg_lark}",
    'micropip': "{pkg_micropip}",
    'packaging': "{pkg_packaging}",
    'brotli': "{pkg_brotli}",
    'distutils': "{pkg_distutils}",
    'pyodide-lock.json': `{pyodide_lock}`
}};

// Base64 to bytes decoder
function b64ToBytes(b64) {{
    const bin = atob(b64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) {{
        bytes[i] = bin.charCodeAt(i);
    }}
    return bytes;
}}

// Store original fetch
const _originalFetch = window.fetch;

// Install fetch interceptor
window.fetch = async function(url, options) {{
    const urlStr = String(url);
    console.log('[Fetch Intercept]', urlStr);

    if (urlStr.includes('pyodide.asm.wasm')) {{
        console.log('  -> Returning embedded WASM');
        return new Response(b64ToBytes(EMBEDDED_B64['pyodide.asm.wasm']), {{
            status: 200,
            headers: {{ 'Content-Type': 'application/wasm' }}
        }});
    }}

    if (urlStr.includes('python_stdlib.zip')) {{
        console.log('  -> Returning embedded stdlib');
        return new Response(b64ToBytes(EMBEDDED_B64['python_stdlib.zip']), {{
            status: 200,
            headers: {{ 'Content-Type': 'application/zip' }}
        }});
    }}

    if (urlStr.includes('pyodide-lock.json')) {{
        console.log('  -> Returning embedded lock file');
        return new Response(EMBEDDED_B64['pyodide-lock.json'], {{
            status: 200,
            headers: {{ 'Content-Type': 'application/json' }}
        }});
    }}

    if (urlStr.includes('sympy') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded sympy');
        return new Response(b64ToBytes(EMBEDDED_B64['sympy']), {{ status: 200 }});
    }}

    if (urlStr.includes('mpmath') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded mpmath');
        return new Response(b64ToBytes(EMBEDDED_B64['mpmath']), {{ status: 200 }});
    }}

    if (urlStr.includes('lark') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded lark');
        return new Response(b64ToBytes(EMBEDDED_B64['lark']), {{ status: 200 }});
    }}

    if (urlStr.includes('micropip') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded micropip');
        return new Response(b64ToBytes(EMBEDDED_B64['micropip']), {{ status: 200 }});
    }}

    if (urlStr.includes('packaging') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded packaging');
        return new Response(b64ToBytes(EMBEDDED_B64['packaging']), {{ status: 200 }});
    }}

    // Fallback to original fetch
    try {{
        return await _originalFetch(url, options);
    }} catch (e) {{
        console.warn('Fetch failed (expected on file://):', urlStr);
        throw e;
    }}
}};

// Getter functions for wheel bytes
function getSymPyWheelBytes() {{ return b64ToBytes(EMBEDDED_B64['sympy']); }}
function getMpmathWheelBytes() {{ return b64ToBytes(EMBEDDED_B64['mpmath']); }}
function getLarkWheelBytes() {{ return b64ToBytes(EMBEDDED_B64['lark']); }}
function getMicropipWheelBytes() {{ return b64ToBytes(EMBEDDED_B64['micropip']); }}
function getPackagingWheelBytes() {{ return b64ToBytes(EMBEDDED_B64['packaging']); }}

console.log('Fetch intercept installed');
</script>

<script>
// Pyodide ASM.js (sets up _createPyodideModule)
console.log('Loading pyodide.asm.js inline...');
{pyodide_asm_js}
console.log('_createPyodideModule defined:', typeof _createPyodideModule);
</script>

<script>
// Pyodide.js (main runtime)
console.log('Loading pyodide.js inline...');
{pyodide_js}
console.log('loadPyodide defined:', typeof loadPyodide);
</script>
'''

    # Insert fetch interceptor after <head>
    html = html.replace('<head>', '<head>\n' + fetch_intercept, 1)

    # Remove CDN Pyodide script tags
    html = re.sub(r'<script[^>]*src="[^"]*pyodide[^"]*\.js"[^>]*></script>', '', html)

    # Write output
    output_path = os.path.join(BASE_DIR, 'create_problem_offline_embedded.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Created: {output_path} ({size_mb:.1f} MB)")

def embed_solve_problem():
    """Generate solve_problem_offline_embedded.html"""
    print("\nEmbedding solve_problem.html...")

    # Read source
    html = read_file(os.path.join(BASE_DIR, 'solve_problem.html'))

    # Read fonts
    print("  - Embedding fonts...")
    font_300 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-300.woff2'))
    font_400 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-400.woff2'))
    font_500 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-500.woff2'))
    font_600 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-600.woff2'))
    font_700 = read_binary(os.path.join(OFFLINE_LIBS, 'fonts', 'poppins-700.woff2'))

    # Create embedded font CSS
    font_css = f'''
    @font-face {{
        font-family: 'Poppins';
        font-style: normal;
        font-weight: 300;
        font-display: swap;
        src: url(data:font/woff2;base64,{font_300}) format('woff2');
    }}
    @font-face {{
        font-family: 'Poppins';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(data:font/woff2;base64,{font_400}) format('woff2');
    }}
    @font-face {{
        font-family: 'Poppins';
        font-style: normal;
        font-weight: 500;
        font-display: swap;
        src: url(data:font/woff2;base64,{font_500}) format('woff2');
    }}
    @font-face {{
        font-family: 'Poppins';
        font-style: normal;
        font-weight: 600;
        font-display: swap;
        src: url(data:font/woff2;base64,{font_600}) format('woff2');
    }}
    @font-face {{
        font-family: 'Poppins';
        font-style: normal;
        font-weight: 700;
        font-display: swap;
        src: url(data:font/woff2;base64,{font_700}) format('woff2');
    }}
    '''

    # Replace Google Fonts link with embedded fonts
    html = safe_replace(html,
        r'<link[^>]*href="https://fonts\.googleapis\.com[^"]*"[^>]*>',
        f'<style>{font_css}</style>'
    )

    # Read and embed CSS libraries
    print("  - Embedding CSS libraries...")
    mathquill_css = read_file(os.path.join(OFFLINE_LIBS, 'mathquill.min.css'))
    quill_css = read_file(os.path.join(OFFLINE_LIBS, 'quill.snow.css'))

    html = safe_replace(html,
        r'<link[^>]*href="[^"]*mathquill[^"]*\.css"[^>]*>',
        f'<style>/* MathQuill CSS */\n{mathquill_css}</style>'
    )
    html = safe_replace(html,
        r'<link[^>]*href="[^"]*quill\.snow\.css"[^>]*>',
        f'<style>/* Quill CSS */\n{quill_css}</style>'
    )

    # Read and embed JavaScript libraries
    print("  - Embedding JavaScript libraries...")
    jquery_js = read_file(os.path.join(OFFLINE_LIBS, 'jquery.min.js'))
    mathquill_js = read_file(os.path.join(OFFLINE_LIBS, 'mathquill.min.js'))
    quill_js = read_file(os.path.join(OFFLINE_LIBS, 'quill.js'))
    mathjax_js = read_file(os.path.join(OFFLINE_LIBS, 'tex-mml-chtml.js'))
    ace_js = read_file(os.path.join(OFFLINE_LIBS, 'ace.js'))

    # Replace CDN script tags with inline scripts
    html = safe_replace(html,
        r'<script[^>]*src="[^"]*jquery[^"]*\.js"[^>]*></script>',
        f'<script>/* jQuery */\n{jquery_js}</script>'
    )
    html = safe_replace(html,
        r'<script[^>]*src="[^"]*mathquill[^"]*\.js"[^>]*></script>',
        f'<script>/* MathQuill */\n{mathquill_js}</script>'
    )
    html = safe_replace(html,
        r'<script[^>]*src="[^"]*quill\.js"[^>]*></script>',
        f'<script>/* Quill */\n{quill_js}</script>'
    )

    # Read Pyodide files
    print("  - Embedding Pyodide runtime...")
    pyodide_dir = os.path.join(OFFLINE_LIBS, 'pyodide')
    pyodide_js = read_file(os.path.join(pyodide_dir, 'pyodide.js'))
    pyodide_asm_js = read_file(os.path.join(pyodide_dir, 'pyodide.asm.js'))
    pyodide_wasm = read_binary(os.path.join(pyodide_dir, 'pyodide.asm.wasm'))
    pyodide_lock = read_file(os.path.join(pyodide_dir, 'pyodide-lock.json'))
    python_stdlib = read_binary(os.path.join(pyodide_dir, 'python_stdlib.zip'))

    # Read Python packages
    print("  - Embedding Python packages...")
    pkg_sympy = read_binary(os.path.join(pyodide_dir, 'sympy-1.12-py3-none-any.whl'))
    pkg_mpmath = read_binary(os.path.join(pyodide_dir, 'mpmath-1.3.0-py3-none-any.whl'))
    pkg_lark = read_binary(os.path.join(pyodide_dir, 'lark-1.1.9-py3-none-any.whl'))
    pkg_micropip = read_binary(os.path.join(pyodide_dir, 'micropip-0.5.0-py3-none-any.whl'))
    pkg_packaging = read_binary(os.path.join(pyodide_dir, 'packaging-23.1-py3-none-any.whl'))

    # Check for optional packages
    brotli_path = os.path.join(pyodide_dir, 'Brotli-1.0.9-cp311-cp311-emscripten_3_1_45_wasm32.whl')
    pkg_brotli = read_binary(brotli_path) if os.path.exists(brotli_path) else ""

    distutils_path = os.path.join(pyodide_dir, 'distutils-1.0.0.zip')
    pkg_distutils = read_binary(distutils_path) if os.path.exists(distutils_path) else ""

    # Create fetch interceptor and embedded data
    fetch_intercept = f'''
<script>
// Embedded base64 data for offline use
const EMBEDDED_B64 = {{
    'pyodide.asm.wasm': "{pyodide_wasm}",
    'python_stdlib.zip': "{python_stdlib}",
    'sympy': "{pkg_sympy}",
    'mpmath': "{pkg_mpmath}",
    'lark': "{pkg_lark}",
    'micropip': "{pkg_micropip}",
    'packaging': "{pkg_packaging}",
    'brotli': "{pkg_brotli}",
    'distutils': "{pkg_distutils}",
    'pyodide-lock.json': `{pyodide_lock}`
}};

// Base64 to bytes decoder
function b64ToBytes(b64) {{
    const bin = atob(b64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) {{
        bytes[i] = bin.charCodeAt(i);
    }}
    return bytes;
}}

// Store original fetch
const _originalFetch = window.fetch;

// Install fetch interceptor
window.fetch = async function(url, options) {{
    const urlStr = String(url);
    console.log('[Fetch Intercept]', urlStr);

    if (urlStr.includes('pyodide.asm.wasm')) {{
        console.log('  -> Returning embedded WASM');
        return new Response(b64ToBytes(EMBEDDED_B64['pyodide.asm.wasm']), {{
            status: 200,
            headers: {{ 'Content-Type': 'application/wasm' }}
        }});
    }}

    if (urlStr.includes('python_stdlib.zip')) {{
        console.log('  -> Returning embedded stdlib');
        return new Response(b64ToBytes(EMBEDDED_B64['python_stdlib.zip']), {{
            status: 200,
            headers: {{ 'Content-Type': 'application/zip' }}
        }});
    }}

    if (urlStr.includes('pyodide-lock.json')) {{
        console.log('  -> Returning embedded lock file');
        return new Response(EMBEDDED_B64['pyodide-lock.json'], {{
            status: 200,
            headers: {{ 'Content-Type': 'application/json' }}
        }});
    }}

    if (urlStr.includes('sympy') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded sympy');
        return new Response(b64ToBytes(EMBEDDED_B64['sympy']), {{ status: 200 }});
    }}

    if (urlStr.includes('mpmath') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded mpmath');
        return new Response(b64ToBytes(EMBEDDED_B64['mpmath']), {{ status: 200 }});
    }}

    if (urlStr.includes('lark') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded lark');
        return new Response(b64ToBytes(EMBEDDED_B64['lark']), {{ status: 200 }});
    }}

    if (urlStr.includes('micropip') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded micropip');
        return new Response(b64ToBytes(EMBEDDED_B64['micropip']), {{ status: 200 }});
    }}

    if (urlStr.includes('packaging') && urlStr.endsWith('.whl')) {{
        console.log('  -> Returning embedded packaging');
        return new Response(b64ToBytes(EMBEDDED_B64['packaging']), {{ status: 200 }});
    }}

    // Fallback to original fetch
    try {{
        return await _originalFetch(url, options);
    }} catch (e) {{
        console.warn('Fetch failed (expected on file://):', urlStr);
        throw e;
    }}
}};

// Getter functions for wheel bytes
function getSymPyWheelBytes() {{ return b64ToBytes(EMBEDDED_B64['sympy']); }}
function getMpmathWheelBytes() {{ return b64ToBytes(EMBEDDED_B64['mpmath']); }}
function getLarkWheelBytes() {{ return b64ToBytes(EMBEDDED_B64['lark']); }}
function getMicropipWheelBytes() {{ return b64ToBytes(EMBEDDED_B64['micropip']); }}
function getPackagingWheelBytes() {{ return b64ToBytes(EMBEDDED_B64['packaging']); }}

console.log('Fetch intercept installed');
</script>

<script>
// Pyodide ASM.js (sets up _createPyodideModule)
console.log('Loading pyodide.asm.js inline...');
{pyodide_asm_js}
console.log('_createPyodideModule defined:', typeof _createPyodideModule);
</script>

<script>
// Pyodide.js (main runtime)
console.log('Loading pyodide.js inline...');
{pyodide_js}
console.log('loadPyodide defined:', typeof loadPyodide);
</script>
'''

    # Insert fetch interceptor after <head>
    html = html.replace('<head>', '<head>\n' + fetch_intercept, 1)

    # Remove CDN Pyodide script tags
    html = re.sub(r'<script[^>]*src="[^"]*pyodide[^"]*\.js"[^>]*></script>', '', html)

    # Write output
    output_path = os.path.join(BASE_DIR, 'solve_problem_offline_embedded.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Created: {output_path} ({size_mb:.1f} MB)")

def main():
    print("=" * 60)
    print("Offline HTML Embedding Script")
    print("=" * 60)

    # Check prerequisites
    if not os.path.exists(OFFLINE_LIBS):
        print(f"ERROR: {OFFLINE_LIBS} directory not found!")
        return

    if not os.path.exists(os.path.join(BASE_DIR, 'create_problem.html')):
        print("ERROR: create_problem.html not found!")
        return

    if not os.path.exists(os.path.join(BASE_DIR, 'solve_problem.html')):
        print("ERROR: solve_problem.html not found!")
        return

    # Embed both files
    embed_create_problem()
    embed_solve_problem()

    print("\n" + "=" * 60)
    print("Done! Offline embedded HTML files have been generated.")
    print("=" * 60)

if __name__ == '__main__':
    main()
