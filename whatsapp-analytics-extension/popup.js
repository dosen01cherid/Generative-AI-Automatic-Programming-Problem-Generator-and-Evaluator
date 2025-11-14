/**
 * WhatsApp Analytics Extension - Popup Script
 * Handles the popup UI and user interactions
 */

let capturedReports = [];
let settings = {};

// DOM elements
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');
const reportCount = document.getElementById('reportCount');
const sessionCount = document.getElementById('sessionCount');
const enabledToggle = document.getElementById('enabledToggle');
const viewReportsBtn = document.getElementById('viewReportsBtn');
const exportBtn = document.getElementById('exportBtn');
const clearBtn = document.getElementById('clearBtn');
const analyticsUrl = document.getElementById('analyticsUrl');
const saveSettingsBtn = document.getElementById('saveSettingsBtn');
const reportsSection = document.getElementById('reportsSection');
const reportsList = document.getElementById('reportsList');

/**
 * Load current settings and reports
 */
function loadData() {
    // Load settings
    chrome.storage.sync.get(['enabled', 'analyticsUrl'], (result) => {
        settings = result;
        enabledToggle.checked = result.enabled !== false;
        analyticsUrl.value = result.analyticsUrl || '';
        updateStatus();
    });

    // Load reports
    chrome.runtime.sendMessage({ type: 'GET_ALL_REPORTS' }, (response) => {
        if (response && response.reports) {
            capturedReports = response.reports;
            updateUI();
        }
    });
}

/**
 * Update status indicator
 */
function updateStatus() {
    if (enabledToggle.checked) {
        statusIndicator.className = 'status-indicator status-active';
        statusText.textContent = 'Active - Monitoring messages';
    } else {
        statusIndicator.className = 'status-indicator status-inactive';
        statusText.textContent = 'Inactive - Auto-capture disabled';
    }
}

/**
 * Update UI with current data
 */
function updateUI() {
    // Update counts
    reportCount.textContent = capturedReports.length;
    sessionCount.textContent = capturedReports.length > 0 ? '1' : '0';

    // Enable/disable export button
    exportBtn.disabled = capturedReports.length === 0;

    // Show/hide reports section
    if (capturedReports.length > 0) {
        reportsSection.style.display = 'block';
        renderReports();
    } else {
        reportsSection.style.display = 'none';
    }
}

/**
 * Render reports list
 */
function renderReports() {
    if (capturedReports.length === 0) {
        reportsList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <div class="empty-state-text">No reports captured yet</div>
            </div>
        `;
        return;
    }

    // Show last 5 reports
    const recentReports = capturedReports.slice(-5).reverse();

    reportsList.innerHTML = recentReports.map((report, index) => `
        <div class="report-item">
            <div class="report-item-header">
                <span class="report-sender">${escapeHtml(report.sender)}</span>
                <span class="report-time">${report.timestamp}</span>
            </div>
            <div class="report-phone">${report.phone || 'Unknown phone'}</div>
        </div>
    `).join('');
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Event: Toggle enabled state
 */
enabledToggle.addEventListener('change', () => {
    const enabled = enabledToggle.checked;

    chrome.storage.sync.set({ enabled }, () => {
        updateStatus();
        showToast(enabled ? 'Auto-capture enabled' : 'Auto-capture disabled');
    });
});

/**
 * Event: View reports (open detailed view)
 */
viewReportsBtn.addEventListener('click', () => {
    if (capturedReports.length === 0) {
        showToast('No reports to view');
        return;
    }

    // Create a new page showing all reports
    const reportsData = encodeURIComponent(JSON.stringify(capturedReports));
    chrome.tabs.create({
        url: `reports.html?data=${reportsData}`
    });
});

/**
 * Event: Export to analytics
 */
exportBtn.addEventListener('click', () => {
    if (capturedReports.length === 0) {
        showToast('No reports to export');
        return;
    }

    if (!analyticsUrl.value) {
        showToast('Please set Analytics App URL in settings');
        return;
    }

    // Combine all base64 data
    const combinedData = capturedReports.map(r => r.data).join('\n\n');

    // Copy to clipboard
    navigator.clipboard.writeText(combinedData).then(() => {
        showToast(`Copied ${capturedReports.length} reports to clipboard!`);

        // Open analytics app
        chrome.tabs.create({ url: analyticsUrl.value }, (tab) => {
            // Show instruction
            setTimeout(() => {
                alert(`✅ Copied ${capturedReports.length} reports to clipboard!\n\nThe Analytics App is opening. Paste (Ctrl+V) the data into the text area and click "Analyze & Add Submissions".`);
            }, 500);
        });
    }).catch(err => {
        showToast('Failed to copy to clipboard');
        console.error('Clipboard error:', err);
    });
});

/**
 * Event: Clear all reports
 */
clearBtn.addEventListener('click', () => {
    if (capturedReports.length === 0) {
        showToast('No reports to clear');
        return;
    }

    if (confirm(`Are you sure you want to clear all ${capturedReports.length} captured reports?`)) {
        chrome.runtime.sendMessage({ type: 'CLEAR_REPORTS' }, (response) => {
            if (response.success) {
                capturedReports = [];
                updateUI();
                showToast('All reports cleared');
            }
        });
    }
});

/**
 * Event: Save settings
 */
saveSettingsBtn.addEventListener('click', () => {
    const url = analyticsUrl.value.trim();

    if (!url) {
        showToast('Please enter a valid URL');
        return;
    }

    chrome.storage.sync.set({ analyticsUrl: url }, () => {
        showToast('Settings saved!');
    });
});

/**
 * Show toast notification
 */
function showToast(message) {
    // Create toast element
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: #0f172a;
        color: white;
        padding: 12px 24px;
        border-radius: 6px;
        font-size: 13px;
        z-index: 10000;
        animation: slideUp 0.3s ease;
    `;

    document.body.appendChild(toast);

    // Remove after 2 seconds
    setTimeout(() => {
        toast.style.animation = 'slideDown 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }
    @keyframes slideDown {
        from {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
        to {
            opacity: 0;
            transform: translateX(-50%) translateY(20px);
        }
    }
`;
document.head.appendChild(style);

// Initialize on load
loadData();

// Refresh data every 2 seconds
setInterval(loadData, 2000);
