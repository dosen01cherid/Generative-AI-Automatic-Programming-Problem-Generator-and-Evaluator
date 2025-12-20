#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate remaining lab guides (11-15) and all PDF report templates
"""

import os
from fpdf import FPDF

# Ensure directories exist
os.makedirs('lab_guides', exist_ok=True)
os.makedirs('lab_reports', exist_ok=True)

# Lab guide HTML template
def create_lab_html(session, title, exercises):
    html = f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Lab {session}: {title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{ color: #667eea; font-size: 2.5em; margin-bottom: 20px; }}
        h2 {{ color: #764ba2; margin: 30px 0 15px; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
        h3 {{ color: #667eea; margin: 20px 0 10px; }}
        .lab-info, .objectives, .exercise {{ padding: 20px; border-radius: 10px; margin: 20px 0; }}
        .lab-info {{ background: #e3f2fd; border-left: 5px solid #2196F3; }}
        .objectives {{ background: #f3e5f5; border-left: 5px solid #9c27b0; }}
        .exercise {{ background: #fff3cd; border-left: 5px solid #ffc107; }}
        .code-block {{ position: relative; margin: 15px 0; }}
        .copy-btn {{
            position: absolute; top: 10px; right: 10px;
            background: #667eea; color: white; border: none;
            padding: 8px 16px; border-radius: 5px; cursor: pointer; z-index: 10;
        }}
        .copy-btn:hover {{ background: #764ba2; }}
        pre {{ background: #2d2d2d; color: #f8f8f2; padding: 20px; border-radius: 10px; overflow-x: auto; }}
        code {{ font-family: 'Courier New', monospace; font-size: 0.95em; line-height: 1.6; }}
        ul, ol {{ margin-left: 30px; margin-top: 10px; line-height: 1.8; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Lab {session}: {title}</h1>

        <div class="lab-info">
            <h3>Lab Information</h3>
            <p><strong>Duration:</strong> 120 minutes</p>
            <p><strong>Prerequisites:</strong> Python, pandas, numpy, scikit-learn</p>
        </div>

        {exercises}

        <h2>Submission</h2>
        <div class="exercise">
            <h3>What to Submit:</h3>
            <ul>
                <li>Jupyter Notebook (.ipynb) with all code and outputs</li>
                <li>Lab Report (PDF) with analysis and conclusions</li>
            </ul>
        </div>
    </div>

    <script>
        function copyCode(id) {{
            navigator.clipboard.writeText(document.getElementById(id).innerText);
            event.target.innerText = 'Copied!';
            event.target.style.background = '#4caf50';
            setTimeout(() => {{ event.target.innerText = 'Copy'; event.target.style.background = '#667eea'; }}, 2000);
        }}
    </script>
</body>
</html>'''
    return html

# Lab content definitions
labs = {
    11: {
        "title": "Modeling: Regresi & Klasifikasi",
        "exercises": '''
        <h2>Part 1: Linear Regression</h2>
        <div class="exercise">
            <h3>Exercise 1: Build Regression Model</h3>
        </div>
        <div class="code-block">
            <button class="copy-btn" onclick="copyCode('code1')">Copy</button>
            <pre><code id="code1">from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load data
# X, y = ...

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print("R2 Score:", r2_score(y_test, y_pred))
print("RMSE:", mean_squared_error(y_test, y_pred, squared=False))</code></pre>
        </div>

        <h2>Part 2: Classification</h2>
        <div class="code-block">
            <button class="copy-btn" onclick="copyCode('code2')">Copy</button>
            <pre><code id="code2">from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Train classifier
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
print("Confusion Matrix:\\n", confusion_matrix(y_test, y_pred))</code></pre>
        </div>
        '''
    },
    12: {
        "title": "Modeling: Clustering",
        "exercises": '''
        <h2>Part 1: K-Means Clustering</h2>
        <div class="code-block">
            <button class="copy-btn" onclick="copyCode('code1')">Copy</button>
            <pre><code id="code1">from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

# Visualize
plt.scatter(X[:,0], X[:,1], c=clusters, cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1],
            marker='X', s=200, c='red')
plt.title('K-Means Clustering')
plt.show()</code></pre>
        </div>

        <h2>Part 2: Elbow Method</h2>
        <div class="code-block">
            <button class="copy-btn" onclick="copyCode('code2')">Copy</button>
            <pre><code id="code2">inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

plt.plot(range(1,11), inertias, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()</code></pre>
        </div>
        '''
    },
    13: {
        "title": "Evaluasi Akurasi Model",
        "exercises": '''
        <h2>Part 1: Classification Metrics</h2>
        <div class="code-block">
            <button class="copy-btn" onclick="copyCode('code1')">Copy</button>
            <pre><code id="code1">from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import roc_auc_score, roc_curve

# Calculate metrics
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1-Score:", f1_score(y_test, y_pred))

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
plt.plot(fpr, tpr)
plt.plot([0,1], [0,1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()</code></pre>
        </div>

        <h2>Part 2: Cross-Validation</h2>
        <div class="code-block">
            <button class="copy-btn" onclick="copyCode('code2')">Copy</button>
            <pre><code id="code2">from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5)
print("CV Scores:", scores)
print("Mean CV Score:", scores.mean())</code></pre>
        </div>
        '''
    },
    14: {
        "title": "Mini Project Planning",
        "exercises": '''
        <h2>Part 1: Define Project Scope</h2>
        <div class="exercise">
            <h3>Exercise: Create Project Proposal</h3>
            <p>Write a project proposal including:</p>
            <ul>
                <li>Problem statement</li>
                <li>Objectives (SMART)</li>
                <li>Data requirements</li>
                <li>Methodology</li>
                <li>Timeline</li>
            </ul>
        </div>

        <h2>Part 2: Project Planning</h2>
        <div class="exercise">
            <h3>Create Work Breakdown Structure</h3>
            <p>List all tasks and subtasks for your project.</p>
        </div>
        '''
    },
    15: {
        "title": "Mini Project Presentation",
        "exercises": '''
        <h2>Part 1: Presentation Structure</h2>
        <div class="exercise">
            <h3>Create Presentation Slides</h3>
            <p>Include:</p>
            <ul>
                <li>Executive Summary</li>
                <li>Problem Statement</li>
                <li>Methodology</li>
                <li>Results & Findings</li>
                <li>Recommendations</li>
            </ul>
        </div>

        <h2>Part 2: Practice Delivery</h2>
        <div class="exercise">
            <h3>Prepare for Q&A</h3>
            <p>Anticipate questions about:</p>
            <ul>
                <li>Methodology choices</li>
                <li>Data limitations</li>
                <li>Model assumptions</li>
                <li>Business impact</li>
            </ul>
        </div>
        '''
    }
}

# Generate lab guides
print("Generating lab guides...")
for session, content in labs.items():
    filename = f"lab_guides/session_{session:02d}_lab.html"
    html = create_lab_html(session, content["title"], content["exercises"])

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Created: session_{session:02d}_lab.html")

print("\\nLab guides completed!")

# Create PDF Report Templates
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Data Analytics - Lab Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_report_template(session, title):
    pdf = PDFReport()
    pdf.add_page()

    # Title
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f'Lab {session}: {title}', 0, 1)
    pdf.ln(5)

    # Student Info
    pdf.set_font('Arial', '', 11)
    pdf.cell(40, 8, 'Name:', 1)
    pdf.cell(150, 8, '', 1, 1)
    pdf.cell(40, 8, 'NIM:', 1)
    pdf.cell(150, 8, '', 1, 1)
    pdf.cell(40, 8, 'Class:', 1)
    pdf.cell(150, 8, '', 1, 1)
    pdf.cell(40, 8, 'Date:', 1)
    pdf.cell(150, 8, '', 1, 1)
    pdf.ln(10)

    # Sections
    sections = [
        ('1. Introduction', 'Describe the purpose and objectives of this lab.'),
        ('2. Methodology', 'Explain the approach and methods used.'),
        ('3. Implementation', 'Document key code and implementation details.'),
        ('4. Results', 'Present findings with visualizations and outputs.'),
        ('5. Analysis', 'Analyze and interpret the results.'),
        ('6. Conclusions', 'Summarize key findings and insights.'),
        ('7. Recommendations', 'Provide actionable recommendations.'),
    ]

    for section, desc in sections:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, section, 0, 1)
        pdf.set_font('Arial', 'I', 10)
        pdf.multi_cell(0, 6, desc)
        pdf.ln(5)

    return pdf

# Generate report templates
print("\\nGenerating PDF report templates...")
sessions_info = {
    7: "Visualisasi Multivariat",
    9: "Data Analytics Lifecycle",
    10: "Business & Data Understanding",
    11: "Modeling: Regresi & Klasifikasi",
    12: "Modeling: Clustering",
    13: "Evaluasi Akurasi Model",
    14: "Mini Project Planning",
    15: "Mini Project Presentation"
}

for session, title in sessions_info.items():
    pdf = create_report_template(session, title)
    filename = f"lab_reports/Lab_{session:02d}_{title.replace(' ', '_').replace(':', '')}_Report_Template.pdf"
    pdf.output(filename)
    print(f"Created: {filename}")

print("\\nAll files generated successfully!")
print("- Lab guides: lab_guides/")
print("- Report templates: lab_reports/")
