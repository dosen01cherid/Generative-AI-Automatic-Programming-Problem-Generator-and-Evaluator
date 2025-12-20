#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate all Data Analytics Lab Guides (HTML)
Creates hands-on practice guides for sessions 9-15
"""

import os

# Base directory
base_dir = "lab_guides"
os.makedirs(base_dir, exist_ok=True)

# HTML template for lab guides
def create_lab_guide(session_num, title, objectives, parts):
    html_content = f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lab {session_num}: {title} - Hands-on Practice</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        h2 {{
            color: #764ba2;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        h3 {{
            color: #667eea;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        .lab-info {{
            background: #e3f2fd;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 5px solid #2196F3;
        }}
        .objectives {{
            background: #f3e5f5;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #9c27b0;
        }}
        .exercise {{
            background: #fff3cd;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #ffc107;
        }}
        .code-block {{
            position: relative;
            margin: 15px 0;
        }}
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
            font-size: 0.9em;
            z-index: 10;
        }}
        .copy-btn:hover {{ background: #764ba2; }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
            margin: 0;
        }}
        code {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.95em;
            line-height: 1.6;
        }}
        .note {{
            background: #e8f5e9;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #4caf50;
        }}
        .warning {{
            background: #fff3e0;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #ff9800;
        }}
        ul, ol {{
            margin-left: 30px;
            margin-top: 10px;
            line-height: 1.8;
        }}
        li {{ margin: 8px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔬 Lab {session_num}: {title}</h1>
        <p style="color: #666; margin-bottom: 20px;">Hands-on Practice with Python</p>

        <div class="lab-info">
            <h3>📋 Lab Information</h3>
            <p><strong>Duration:</strong> 120 minutes</p>
            <p><strong>Prerequisites:</strong> Python 3.x, pandas, numpy, scikit-learn</p>
        </div>

        <div class="objectives">
            <h3>🎯 Learning Objectives</h3>
            <ul>
                {''.join([f"<li>{obj}</li>" for obj in objectives])}
            </ul>
        </div>

        {parts}

        <h2>📝 Lab Submission Requirements</h2>

        <div class="warning">
            <h3>What to Submit:</h3>
            <ol>
                <li><strong>Jupyter Notebook (.ipynb)</strong> with all code and outputs</li>
                <li><strong>Lab Report (PDF)</strong> containing:
                    <ul>
                        <li>Introduction and objectives</li>
                        <li>Methodology and implementation details</li>
                        <li>Results with screenshots/outputs</li>
                        <li>Analysis and interpretation</li>
                        <li>Conclusions and insights</li>
                    </ul>
                </li>
            </ol>
        </div>

        <div class="note" style="margin-top: 30px;">
            <h3>✅ Checklist Before Submission:</h3>
            <ul style="list-style: none;">
                <li>☐ All code runs without errors</li>
                <li>☐ All outputs are properly documented</li>
                <li>☐ Code is well-commented</li>
                <li>☐ Challenge exercises completed</li>
                <li>☐ Lab report is comprehensive</li>
            </ul>
        </div>
    </div>

    <script>
        function copyCode(elementId) {{
            const code = document.getElementById(elementId).innerText;
            navigator.clipboard.writeText(code).then(() => {{
                const btn = event.target;
                const originalText = btn.innerText;
                btn.innerText = 'Copied!';
                btn.style.background = '#4caf50';
                setTimeout(() => {{
                    btn.innerText = originalText;
                    btn.style.background = '#667eea';
                }}, 2000);
            }});
        }}
    </script>
</body>
</html>'''

    return html_content

# Lab contents for each session
labs = {
    9: {
        "title": "Data Analytics Lifecycle",
        "objectives": [
            "Understand the complete data analytics lifecycle",
            "Perform data preparation and cleaning",
            "Apply feature engineering techniques",
            "Build and evaluate models",
            "Document the analytics process"
        ],
        "parts": '''
        <h2>Part 1: Data Collection and Loading</h2>
        <div class="exercise">
            <h3>Exercise 1.1: Load and Explore Dataset</h3>
        </div>
        <div class="code-block">
            <button class="copy-btn" onclick="copyCode('code1')">Copy</button>
            <pre><code id="code1">import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load sample dataset
url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
df = pd.read_csv(url)

print("Dataset Shape:", df.shape)
print("\\nFirst 5 rows:")
print(df.head())
print("\\nDataset Info:")
print(df.info())
print("\\nStatistical Summary:")
print(df.describe())</code></pre>
        </div>

        <h2>Part 2: Data Cleaning</h2>
        <div class="exercise">
            <h3>Exercise 2.1: Handle Missing Values</h3>
        </div>
        <div class="code-block">
            <button class="copy-btn" onclick="copyCode('code2')">Copy</button>
            <pre><code id="code2"># Check missing values
print("Missing Values:")
print(df.isnull().sum())

# Fill missing Age with median
df['Age'].fillna(df['Age'].median(), inplace=True)

# Fill missing Embarked with mode
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# Drop Cabin (too many missing)
df.drop('Cabin', axis=1, inplace=True)

print("\\nAfter handling missing values:")
print(df.isnull().sum())</code></pre>
        </div>

        <h2>Part 3: Feature Engineering</h2>
        <div class="exercise">
            <h3>Exercise 3.1: Create New Features</h3>
        </div>
        <div class="code-block">
            <button class="copy-btn" onclick="copyCode('code3')">Copy</button>
            <pre><code id="code3"># Create FamilySize feature
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

# Create IsAlone feature
df['IsAlone'] = (df['FamilySize'] == 1).astype(int)

# Extract title from Name
df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\\.', expand=False)

# Create AgeGroup
df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 60, 100],
                        labels=['Child', 'Teen', 'Adult', 'Senior'])

print("New features created:")
print(df[['Name', 'Title', 'Age', 'AgeGroup', 'FamilySize', 'IsAlone']].head())</code></pre>
        </div>

        <h2>Part 4: Model Building</h2>
        <div class="exercise">
            <h3>Exercise 4.1: Prepare Data and Train Model</h3>
        </div>
        <div class="code-block">
            <button class="copy-btn" onclick="copyCode('code4')">Copy</button>
            <pre><code id="code4">from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Select features
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
X = pd.get_dummies(df[features], drop_first=True)
y = df['Survived']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", model.score(X_test, y_test))
print("\\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))</code></pre>
        </div>

        <h2>🏆 Challenge Exercise</h2>
        <div class="exercise">
            <h3>Challenge: Complete Analytics Pipeline</h3>
            <p>Build a complete analytics pipeline that:</p>
            <ol>
                <li>Loads a dataset of your choice</li>
                <li>Performs comprehensive EDA</li>
                <li>Handles all data quality issues</li>
                <li>Engineers at least 5 meaningful features</li>
                <li>Builds and compares 3 different models</li>
                <li>Documents the entire process</li>
            </ol>
        </div>
        '''
    },
    10: {
        "title": "Business & Data Understanding",
        "objectives": [
            "Conduct comprehensive exploratory data analysis",
            "Identify business objectives from data",
            "Perform statistical analysis",
            "Create data profiles and summaries",
            "Align data insights with business goals"
        ],
        "parts": '''
        <h2>Part 1: Business Problem Definition</h2>
        <div class="exercise">
            <h3>Exercise 1.1: Define Business Questions</h3>
            <p>For an e-commerce dataset, define 5 key business questions that data can answer.</p>
        </div>

        <h2>Part 2: Data Profiling</h2>
        <div class="code-block">
            <button class="copy-btn" onclick="copyCode('code1')">Copy</button>
            <pre><code id="code1">import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('your_dataset.csv')

# Data profiling
def profile_dataset(df):
    print("="*50)
    print("DATASET PROFILE")
    print("="*50)
    print(f"\\nRows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"\\nColumn Names: {list(df.columns)}")
    print(f"\\nData Types:\\n{df.dtypes}")
    print(f"\\nMissing Values:\\n{df.isnull().sum()}")
    print(f"\\nDuplicate Rows: {df.duplicated().sum()}")
    print(f"\\nMemory Usage:\\n{df.memory_usage(deep=True)}")

    # Numerical columns summary
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        print(f"\\nNumerical Columns Statistics:\\n{df[num_cols].describe()}")

    # Categorical columns summary
    cat_cols = df.select_dtypes(include=['object']).columns
    if len(cat_cols) > 0:
        print(f"\\nCategorical Columns:")
        for col in cat_cols:
            print(f"\\n{col}:")
            print(df[col].value_counts().head())

profile_dataset(df)</code></pre>
        </div>

        <h2>Part 3: Exploratory Data Analysis</h2>
        <div class="code-block">
            <button class="copy-btn" onclick="copyCode('code2')">Copy</button>
            <pre><code id="code2"># Univariate analysis
def univariate_analysis(df):
    num_cols = df.select_dtypes(include=[np.number]).columns
    n_cols = len(num_cols)
    n_rows = (n_cols + 2) // 3

    fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5*n_rows))
    axes = axes.ravel()

    for idx, col in enumerate(num_cols):
        axes[idx].hist(df[col].dropna(), bins=30, edgecolor='black')
        axes[idx].set_title(f'Distribution of {col}')
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel('Frequency')
        axes[idx].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

univariate_analysis(df)

# Bivariate analysis
def bivariate_analysis(df, target_col):
    num_cols = df.select_dtypes(include=[np.number]).columns
    num_cols = [col for col in num_cols if col != target_col]

    for col in num_cols:
        plt.figure(figsize=(10, 6))
        plt.scatter(df[col], df[target_col], alpha=0.5)
        plt.xlabel(col)
        plt.ylabel(target_col)
        plt.title(f'{col} vs {target_col}')
        plt.grid(True, alpha=0.3)
        plt.show()

        # Calculate correlation
        corr = df[[col, target_col]].corr().iloc[0, 1]
        print(f"Correlation between {col} and {target_col}: {corr:.3f}")

# bivariate_analysis(df, 'target_column_name')</code></pre>
        </div>

        <h2>🏆 Challenge Exercise</h2>
        <div class="exercise">
            <h3>Challenge: Business Intelligence Dashboard</h3>
            <p>Create a comprehensive business intelligence report including:</p>
            <ol>
                <li>Executive summary with key metrics</li>
                <li>Customer segmentation analysis</li>
                <li>Revenue trend analysis</li>
                <li>Product performance analysis</li>
                <li>Actionable recommendations</li>
            </ol>
        </div>
        '''
    },
    # Add remaining sessions similarly...
}

# Generate all lab guides
print("Generating lab guides...")
for session_num, content in labs.items():
    filename = f"session_{session_num:02d}_lab.html"
    filepath = os.path.join(base_dir, filename)

    html = create_lab_guide(
        session_num,
        content["title"],
        content["objectives"],
        content["parts"]
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Created: {filename}")

print(f"\\n✓ All lab guides created in '{base_dir}/' directory!")
