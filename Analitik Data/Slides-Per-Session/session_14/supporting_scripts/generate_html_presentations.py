#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate all Data Analytics HTML Presentations
Creates 24 HTML files (8 sessions x 3 parts each)
"""

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Session {session_num} Part {part_num}: {session_title}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            overflow-y: scroll;
            overflow-x: hidden;
        }}
        .slide {{
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 60px 40px;
            background: white;
            margin: 20px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{ font-size: 3em; color: #667eea; margin-bottom: 30px; text-align: center; }}
        h2 {{ font-size: 2.2em; color: #764ba2; margin: 30px 0 20px 0; }}
        h3 {{ font-size: 1.8em; color: #667eea; margin: 25px 0 15px 0; }}
        p, li {{ font-size: 1.2em; line-height: 1.8; margin: 15px 0; }}
        .content {{ max-width: 1200px; width: 100%; }}
        .math-block {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #667eea;
        }}
        .code-container {{ position: relative; margin: 25px 0; }}
        .copy-btn {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            z-index: 10;
        }}
        .copy-btn:hover {{ background: #764ba2; }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 25px;
            border-radius: 10px;
            overflow-x: auto;
        }}
        code {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 1em;
            line-height: 1.6;
            display: block;
        }}
        code .line {{ display: block; min-height: 1.6em; }}
        .keyword {{ color: #ff79c6; }}
        .function {{ color: #50fa7b; }}
        .string {{ color: #f1fa8c; }}
        .comment {{ color: #6272a4; }}
        .number {{ color: #bd93f9; }}
        .example-box {{
            background: #e3f2fd;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #2196F3;
        }}
        .definition-box {{
            background: #f3e5f5;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #9c27b0;
        }}
        .plot-container {{ margin: 30px 0; width: 100%; }}
        ul, ol {{ margin-left: 30px; }}
        .highlight {{
            background: #fff3cd;
            padding: 3px 8px;
            border-radius: 3px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="slide">
        <div class="content">
            <h1>Session {session_num}: {session_title}</h1>
            <h2>Part {part_num}: {part_title}</h2>
            {content}
        </div>
    </div>
    <script>
        function copyCode(elementId) {{
            const code = document.getElementById(elementId).innerText;
            navigator.clipboard.writeText(code).then(() => {{
                const btn = event.target;
                const originalText = btn.innerText;
                btn.innerText = 'Copied!';
                setTimeout(() => {{ btn.innerText = originalText; }}, 2000);
            }});
        }}
    </script>
</body>
</html>'''

# Simple content generator - will be expanded
def generate_content(session_num, part_num):
    # Basic content structure
    return f"""
    <div class="definition-box">
        <h3>Overview</h3>
        <p>This section covers key concepts for Session {session_num}, Part {part_num}.</p>
    </div>

    <div class="example-box">
        <h3>Key Topics</h3>
        <ul>
            <li>Topic 1: Fundamental concepts</li>
            <li>Topic 2: Practical applications</li>
            <li>Topic 3: Best practices</li>
        </ul>
    </div>

    <div class="code-container">
        <button class="copy-btn" onclick="copyCode('code1')">Copy</button>
        <pre><code id="code1"><span class="line"><span class="keyword">import</span> pandas <span class="keyword">as</span> pd</span>
<span class="line"><span class="keyword">import</span> numpy <span class="keyword">as</span> np</span>
<span class="line"></span>
<span class="line"><span class="comment"># Example code for Session {session_num}</span></span>
<span class="line">df = pd.read_csv(<span class="string">'data.csv'</span>)</span>
<span class="line"><span class="function">print</span>(df.head())</span></code></pre>
    </div>
    """

# Session details
sessions_config = {
    7: {
        "title": "Visualisasi Multivariat",
        "parts": ["Pengantar Visualisasi Multivariat", "Teknik Visualisasi Lanjutan", "Implementasi dengan Python"]
    },
    9: {
        "title": "Data Analytics Lifecycle",
        "parts": ["Discovery Phase", "Data Preparation & Model Planning", "Model Building & Deployment"]
    },
    10: {
        "title": "Business & Data Understanding",
        "parts": ["Business Understanding", "Data Understanding", "Integration: Business + Data"]
    },
    11: {
        "title": "Modeling: Regresi & Klasifikasi",
        "parts": ["Regression Models", "Classification Models", "Model Evaluation"]
    },
    12: {
        "title": "Modeling: Clustering",
        "parts": ["Konsep Clustering", "Clustering Algorithms", "Implementasi & Evaluasi"]
    },
    13: {
        "title": "Evaluasi Akurasi Model",
        "parts": ["Metrics untuk Klasifikasi", "Metrics untuk Regresi", "Model Selection & Tuning"]
    },
    14: {
        "title": "Mini Project Planning",
        "parts": ["Project Scoping", "Methodology Selection", "Documentation & Deliverables"]
    },
    15: {
        "title": "Mini Project Presentation",
        "parts": ["Presentation Structure", "Visualization & Storytelling", "Q&A and Delivery"]
    }
}

# Generate all files
for session_num, session_info in sessions_config.items():
    for part_num in range(1, 4):
        filename = f"session_{session_num:02d}_part{part_num}.html"

        content = generate_content(session_num, part_num)

        html = HTML_TEMPLATE.format(
            session_num=session_num,
            part_num=part_num,
            session_title=session_info["title"],
            part_title=session_info["parts"][part_num-1],
            content=content
        )

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"Created: {filename}")

print(f"\n✓ Successfully created all 24 HTML files!")
