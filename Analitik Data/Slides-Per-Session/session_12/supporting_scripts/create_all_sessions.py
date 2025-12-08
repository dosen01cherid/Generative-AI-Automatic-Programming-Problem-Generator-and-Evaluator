"""
Script to create all Data Analytics HTML presentations
Sessions 7, 9, 10, 11, 12, 13, 14, 15 with 3 parts each
"""

# Session content definitions
sessions = {
    7: {
        "title": "Visualisasi Multivariat",
        "parts": [
            {
                "subtitle": "Pengantar Visualisasi Multivariat",
                "topics": ["Konsep visualisasi multivariat", "Jenis-jenis plot multivariat", "Pentingnya visualisasi data"]
            },
            {
                "subtitle": "Teknik Visualisasi Lanjutan",
                "topics": ["Scatter plot matrix", "Parallel coordinates", "Heatmaps dan correlation matrix"]
            },
            {
                "subtitle": "Implementasi dengan Python",
                "topics": ["Matplotlib & Seaborn", "Plotly untuk visualisasi interaktif", "Studi kasus praktis"]
            }
        ]
    },
    9: {
        "title": "Data Analytics Lifecycle",
        "parts": [
            {
                "subtitle": "Discovery Phase",
                "topics": ["Problem understanding", "Data requirements", "Initial hypothesis"]
            },
            {
                "subtitle": "Data Preparation & Model Planning",
                "topics": ["Data cleaning", "Feature engineering", "Model selection"]
            },
            {
                "subtitle": "Model Building & Deployment",
                "topics": ["Model training", "Validation", "Deployment strategies"]
            }
        ]
    },
    10: {
        "title": "Business & Data Understanding",
        "parts": [
            {
                "subtitle": "Business Understanding",
                "topics": ["Business objectives", "Success criteria", "Stakeholder analysis"]
            },
            {
                "subtitle": "Data Understanding",
                "topics": ["Data exploration", "Data quality assessment", "Initial insights"]
            },
            {
                "subtitle": "Integration: Business + Data",
                "topics": ["Aligning data with business", "KPIs and metrics", "Practical examples"]
            }
        ]
    },
    11: {
        "title": "Modeling: Regresi & Klasifikasi",
        "parts": [
            {
                "subtitle": "Regression Models",
                "topics": ["Linear regression", "Multiple regression", "Polynomial regression"]
            },
            {
                "subtitle": "Classification Models",
                "topics": ["Logistic regression", "Decision trees", "Random forests"]
            },
            {
                "subtitle": "Model Evaluation",
                "topics": ["Metrics for regression", "Metrics for classification", "Cross-validation"]
            }
        ]
    },
    12: {
        "title": "Modeling: Clustering",
        "parts": [
            {
                "subtitle": "Konsep Clustering",
                "topics": ["Unsupervised learning", "Distance metrics", "Types of clustering"]
            },
            {
                "subtitle": "Clustering Algorithms",
                "topics": ["K-Means", "Hierarchical clustering", "DBSCAN"]
            },
            {
                "subtitle": "Implementasi & Evaluasi",
                "topics": ["Elbow method", "Silhouette score", "Practical applications"]
            }
        ]
    },
    13: {
        "title": "Evaluasi Akurasi Model",
        "parts": [
            {
                "subtitle": "Metrics untuk Klasifikasi",
                "topics": ["Confusion matrix", "Accuracy, Precision, Recall", "F1-Score dan ROC-AUC"]
            },
            {
                "subtitle": "Metrics untuk Regresi",
                "topics": ["MAE, MSE, RMSE", "R² Score", "Adjusted R²"]
            },
            {
                "subtitle": "Model Selection & Tuning",
                "topics": ["Hyperparameter tuning", "Grid search", "Cross-validation strategies"]
            }
        ]
    },
    14: {
        "title": "Mini Project Planning",
        "parts": [
            {
                "subtitle": "Project Scoping",
                "topics": ["Problem definition", "Data requirements", "Timeline & milestones"]
            },
            {
                "subtitle": "Methodology Selection",
                "topics": ["Choosing algorithms", "Tools & technologies", "Evaluation criteria"]
            },
            {
                "subtitle": "Documentation & Deliverables",
                "topics": ["Project proposal", "Technical documentation", "Expected outcomes"]
            }
        ]
    },
    15: {
        "title": "Mini Project Presentation",
        "parts": [
            {
                "subtitle": "Presentation Structure",
                "topics": ["Executive summary", "Methodology overview", "Key findings"]
            },
            {
                "subtitle": "Visualization & Storytelling",
                "topics": ["Effective charts", "Data storytelling", "Insight communication"]
            },
            {
                "subtitle": "Q&A and Delivery",
                "topics": ["Handling questions", "Professional delivery", "Lessons learned"]
            }
        ]
    }
}

print(f"Total sessions to create: {len(sessions)}")
print(f"Total HTML files to create: {len(sessions) * 3}")
print("\nSession outline:")
for session_num, session_data in sessions.items():
    print(f"\nSession {session_num}: {session_data['title']}")
    for i, part in enumerate(session_data['parts'], 1):
        print(f"  Part {i}: {part['subtitle']}")
