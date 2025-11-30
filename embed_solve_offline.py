#!/usr/bin/env python3
"""
Embed everything into a single HTML for solve_problem that works on file:// protocol.
Key insight: pyodide.asm.js sets globalThis._createPyodideModule,
and pyodide.js checks for it before dynamic import. So we load
pyodide.asm.js first as inline script, then pyodide.js skips the import!
"""
import base64
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OFFLINE_LIBS = os.path.join(BASE_DIR, 'offline_libs')

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def read_binary(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def main():
    print("Reading source HTML...")
    html_path = os.path.join(BASE_DIR, 'solve_problem.html')
    html = read_file(html_path)

    print("Reading CSS...")
    mathquill_css = read_file(os.path.join(OFFLINE_LIBS, 'mathquill.min.css'))

    print("Reading JS libraries...")
    jquery_js = read_file(os.path.join(OFFLINE_LIBS, 'jquery.min.js'))
    mathquill_js = read_file(os.path.join(OFFLINE_LIBS, 'mathquill.min.js'))
    mathjax_js = read_file(os.path.join(OFFLINE_LIBS, 'tex-mml-chtml.js'))

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

    # Fetch intercept for Pyodide resources
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

// Get wheel bytes for direct installation
function getSymPyWheelBytes() {{
    return b64ToBytes(EMBEDDED_B64['sympy']);
}}
function getMpMathWheelBytes() {{
    return b64ToBytes(EMBEDDED_B64['mpmath']);
}}
function getLarkWheelBytes() {{
    return b64ToBytes(EMBEDDED_B64['lark']);
}}
function getBrotliWheelBytes() {{
    return b64ToBytes(EMBEDDED_B64['brotli']);
}}

// ============================================================
// INTERCEPT FETCH - Return embedded data as Response
// ============================================================
const _originalFetch = window.fetch;
window.fetch = async function(url, options) {{
    const urlStr = String(url);
    console.log('[Fetch Intercept]', urlStr);

    if (urlStr.includes('pyodide.asm.wasm')) {{
        console.log('  -> Returning embedded WASM');
        const bytes = b64ToBytes(EMBEDDED_B64['pyodide.asm.wasm']);
        return new Response(bytes, {{
            status: 200,
            headers: {{ 'Content-Type': 'application/wasm' }}
        }});
    }}

    if (urlStr.includes('pyodide-lock.json')) {{
        console.log('  -> Returning embedded lock file');
        const text = b64ToText(EMBEDDED_B64['pyodide-lock.json']);
        return new Response(text, {{
            status: 200,
            headers: {{ 'Content-Type': 'application/json' }}
        }});
    }}

    if (urlStr.includes('python_stdlib.zip')) {{
        console.log('  -> Returning embedded python_stdlib.zip');
        const bytes = b64ToBytes(EMBEDDED_B64['python_stdlib.zip']);
        return new Response(bytes, {{
            status: 200,
            headers: {{ 'Content-Type': 'application/zip' }}
        }});
    }}

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

<!-- Load pyodide.asm.js FIRST - sets globalThis._createPyodideModule -->
<script>
console.log('Loading pyodide.asm.js inline...');
{pyodide_asm_js}
console.log('_createPyodideModule defined:', typeof _createPyodideModule);
</script>

<!-- Load pyodide.js - skips dynamic import since _createPyodideModule exists -->
<script>
console.log('Loading pyodide.js inline...');
{pyodide_js}
console.log('loadPyodide defined:', typeof loadPyodide);
</script>
'''

    print("Replacing CDN references with embedded content...")

    # Replace MathQuill CSS
    html = html.replace(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mathquill/0.10.1/mathquill.min.css">',
        '<style>/* MathQuill */\n' + mathquill_css + '</style>'
    )

    # Replace jQuery
    html = html.replace(
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>',
        '<script>/* jQuery */\n' + jquery_js + '</script>'
    )

    # Replace MathQuill JS
    html = html.replace(
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathquill/0.10.1/mathquill.min.js"></script>',
        '<script>/* MathQuill */\n' + mathquill_js + '</script>'
    )

    # Replace MathJax
    html = html.replace(
        '<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>',
        '<script>/* MathJax */\n' + mathjax_js + '</script>'
    )

    print("Updating Pyodide configuration...")

    # Update Pyodide URL constant
    html = html.replace(
        "const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js';",
        "const PYODIDE_URL = 'embedded';"
    )

    # Use regex to replace getCachedScript function (handles varying whitespace)
    getCachedScript_pattern = r"(async function getCachedScript\(url\) \{[\s\S]*?return await response\.text\(\);\s*\}\s*\})"
    getCachedScript_replacement = '''async function getCachedScript(url) {
        updateStatus('⚡ Using embedded Pyodide...');
        return ''; // Pyodide already loaded inline
      }'''

    html = re.sub(getCachedScript_pattern, getCachedScript_replacement, html, count=1)
    print("  - Replaced getCachedScript function")

    # Use regex to replace initPyodide script loading part
    initPyodide_pattern = r"const scriptText = await getCachedScript\(PYODIDE_URL\);[\s\S]*?indexURL: 'https://cdn\.jsdelivr\.net/pyodide/v0\.24\.1/full/'\s*\}\);"
    initPyodide_replacement = '''// Pyodide already loaded inline!
        await getCachedScript(PYODIDE_URL);
        updateStatus('⚡ Pyodide ready...');
        await new Promise(resolve => setTimeout(resolve, 50));

        // Load with embedded resources (fetch intercepted)
        window.pyodide = await loadPyodide({
          indexURL: './'
        });'''

    html = re.sub(initPyodide_pattern, initPyodide_replacement, html, count=1)
    print("  - Replaced initPyodide loading part")

    # Use regex to replace micropip package installation
    packages_pattern = r"updateStatus\('✅ Pyodide ready!'\);[\s\S]*?await micropip\.install\(\[[\s\S]*?\], keep_going=True\)[\s\S]*?updateStatus\('✅ All packages loaded and cached!'\);"
    packages_replacement = '''updateStatus('✅ Pyodide ready!');
        updateStatus('📦 Loading packages (sympy, lark, brotli)...');

        // Load packages by directly extracting wheels (bypasses micropip hash validation)
        // This works offline because all wheels are embedded in this HTML

        // Extract mpmath first (sympy dependency)
        updateStatus('📦 Loading mpmath...');
        const mpMathBytes = getMpMathWheelBytes();
        await window.pyodide.unpackArchive(mpMathBytes, 'wheel');

        // Extract sympy
        updateStatus('📦 Loading sympy...');
        const symPyBytes = getSymPyWheelBytes();
        await window.pyodide.unpackArchive(symPyBytes, 'wheel');

        // Extract lark
        updateStatus('📦 Loading lark...');
        const larkBytes = getLarkWheelBytes();
        await window.pyodide.unpackArchive(larkBytes, 'wheel');

        // Extract brotli
        updateStatus('📦 Loading brotli...');
        const brotliBytes = getBrotliWheelBytes();
        await window.pyodide.unpackArchive(brotliBytes, 'wheel');

        console.log("✅ All packages extracted from embedded wheels");

        updateStatus('✅ All packages loaded!');'''

    html = re.sub(packages_pattern, packages_replacement, html, count=1)
    print("  - Replaced micropip package installation")

    # Inject fetch intercept AFTER charset declaration
    html = html.replace('<meta charset="utf-8" />', '<meta charset="utf-8" />\n' + fetch_intercept)

    print("Writing output file...")
    output_path = os.path.join(BASE_DIR, 'solve_problem_offline_embedded.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\nCreated: {output_path}")
    print(f"File size: {size_mb:.2f} MB")
    print("\n*** This should work on file:// protocol! ***")
    print("Just double-click the HTML file to open it.")

if __name__ == '__main__':
    main()
