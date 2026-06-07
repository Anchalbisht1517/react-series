"""Custom CSS style injections and styling definitions for the CarePredict Healthcare Theme."""

import streamlit as st

def get_custom_css():
    """Return the raw CSS string for the CarePredict UI theme."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Overrides */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: #f5f7fa !important;
        color: #374151 !important;
    }

    /* Hide Streamlit elements */
    [data-testid="stHeader"] {
        display: none !important;
    }
    footer {
        display: none !important;
    }
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e6ed !important;
        padding-top: 0rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
    
    /* Top Header Bar */
    .top-header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #ffffff;
        padding: 10px 24px;
        border-bottom: 1px solid #e2e6ed;
        margin-top: -6rem;
        margin-left: -5rem;
        margin-right: -5rem;
        margin-bottom: 2rem;
        position: sticky;
        top: 0;
        z-index: 99;
        height: 60px;
    }
    .top-header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-title {
        font-size: 16px;
        font-weight: 700;
        color: #0f1f3d;
    }
    .brand-accent {
        color: #0ea5e9;
    }
    .breadcrumb-text {
        font-size: 14px;
        color: #94a3b8;
    }
    .top-header-right {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .live-indicator {
        display: flex;
        align-items: center;
        gap: 6px;
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 3px 10px;
        font-size: 12px;
        font-weight: 500;
        color: #16a34a;
    }
    .live-dot {
        width: 6px;
        height: 6px;
        background-color: #16a34a;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.9); opacity: 0.9; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.9; }
    }
    .header-icon {
        color: #64748b;
        font-size: 18px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 6px;
        border: 1px solid #e2e6ed;
        background-color: #ffffff;
    }
    .user-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: #e0f2fe;
        color: #0284c7;
        font-size: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #bae6fd;
    }

    /* Custom Sidebar Nav */
    .sidebar-brand-container {
        padding: 25px 20px 20px 20px;
        border-bottom: 1px solid #e2e6ed;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 12px;
    }
    .sidebar-brand-title {
        font-size: 22px;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #0ea5e9, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    .sidebar-brand-subtitle {
        font-size: 10px;
        color: #94a3b8;
        margin: 4px 0 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        line-height: 1.2;
    }
    .sidebar-nav-container {
        padding: 15px 0 100px 0;
    }
    .sidebar-section-header {
        font-size: 10px;
        font-weight: 700;
        color: #94a3b8;
        padding: 12px 20px 6px 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .sidebar-nav-link {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 20px;
        text-decoration: none !important;
        color: #64748b !important;
        font-size: 13px;
        font-weight: 500;
        border-left: 3px solid transparent;
        transition: all 0.2s ease;
    }
    .sidebar-nav-link:hover {
        background-color: #f8fafc;
        color: #0f1f3d !important;
    }
    .sidebar-nav-link.active {
        background-color: #f0f9ff;
        color: #0284c7 !important;
        border-left-color: #0ea5e9;
        font-weight: 600;
    }
    .sidebar-nav-item-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sidebar-badge {
        font-size: 10px;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: 10px;
        color: #ffffff;
    }
    .sidebar-badge-red {
        background-color: #dc2626;
    }
    .sidebar-badge-amber {
        background-color: #f59e0b;
    }
    
    .sidebar-footer {
        padding: 15px 20px;
        border-top: 1px solid #e2e6ed;
        background-color: #ffffff;
        font-size: 11px;
        color: #64748b;
        margin-top: 20px;
    }
    .sidebar-footer-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
    }

    /* Cards */
    .card {
        background-color: #ffffff;
        border: 0.5px solid #e2e6ed;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        position: relative;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02);
    }
    .card-sky-blue { border-top: 3px solid #0ea5e9; }
    .card-red { border-top: 3px solid #dc2626; }
    .card-teal { border-top: 3px solid #16a34a; }
    .card-amber { border-top: 3px solid #f59e0b; }
    .card-purple { border-top: 3px solid #a855f7; }
    
    .card-large {
        min-height: 480px !important;
        padding: 20px !important;
    }

    /* Streamlit Native Bordered Container styled as Card */
    div[data-testid="stVerticalBlockBordered"],
    [data-testid="stVerticalBlockBordered"] {
        background-color: #ffffff !important;
        border: 0.5px solid #e2e6ed !important;
        border-radius: 8px !important;
        padding: 20px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02) !important;
    }

    /* Flex-table column widths */
    .w-pat { flex: 2.5 !important; display: flex !important; flex-direction: column !important; }
    .w-age { flex: 1 !important; font-size: 12px !important; color: #374151 !important; }
    .w-prob { flex: 2 !important; display: flex !important; align-items: center !important; gap: 8px !important; }
    .w-risk { flex: 1.5 !important; }
    .w-interv { flex: 2 !important; }

    /* Model Performance Table column widths */
    .w-model-alg { flex: 2 !important; font-weight: 600 !important; }
    .w-model-metric { flex: 1 !important; }

    /* Static Donut Chart for Dashboard */
    .donut-gauge {
        position: relative !important;
        width: 150px !important;
        height: 150px !important;
        border-radius: 50% !important;
        background: conic-gradient(#dc2626 0% 7.4%, #f59e0b 7.4% 20.1%, #16a34a 20.1% 100%) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.05) !important;
    }
    .donut-hole-center {
        position: absolute !important;
        background-color: #ffffff !important;
        width: 110px !important;
        height: 110px !important;
        border-radius: 50% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        z-index: 2 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }

    /* Dynamic Donut Chart hole for Patient Check page */
    .dynamic-gauge-hole {
        position: absolute !important;
        background-color: #ffffff !important;
        width: 96px !important;
        height: 96px !important;
        border-radius: 50% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        z-index: 2 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }

    /* Helper Utilities to avoid inline style sanitization */
    .fs-24 { font-size: 24px !important; }
    .fs-9 { font-size: 9px !important; }
    .fs-12 { font-size: 12px !important; }
    .fc-slate { color: #64748b !important; }
    .fw-600 { font-weight: 600 !important; }
    .mr-0 { margin-right: 0px !important; }
    .pb-20 { padding-bottom: 20px !important; }

    /* Flexbox Table styles to bypass Streamlit table sanitization */
    .flex-table {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    .flex-table-header {
        display: flex;
        width: 100%;
        border-bottom: 1px solid #e2e6ed;
        padding: 8px 12px;
        font-weight: 600;
        color: #94a3b8;
        font-size: 10px;
        text-transform: uppercase;
    }
    .flex-table-row {
        display: flex;
        width: 100%;
        border-bottom: 1px solid #f1f5f9;
        padding: 10px 12px;
        align-items: center;
        transition: background-color 0.2s ease;
    }
    .flex-table-row:hover {
        background-color: #f0f9ff;
    }
    
    .card-header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 8px;
    }
    .card-title-text {
        font-size: 13px;
        font-weight: 600;
        color: #0f1f3d;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .card-action-link {
        font-size: 12px;
        color: #0284c7 !important;
        text-decoration: none !important;
        font-weight: 500;
    }

    /* KPI Cards specific styling */
    .kpi-title {
        font-size: 11px;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 600;
        color: #0f1f3d;
        line-height: 1;
        margin-bottom: 6px;
    }
    .kpi-subtitle {
        font-size: 11px;
        color: #64748b;
    }
    .kpi-delta {
        font-size: 11px;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 2px;
    }
    .kpi-delta-up-red { color: #dc2626; }
    .kpi-delta-up-green { color: #16a34a; }
    .kpi-delta-down { color: #64748b; }

    /* Tables & Lists */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        text-align: left;
    }
    .custom-table th {
        font-size: 10px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        padding: 8px 12px;
        border-bottom: 1px solid #e2e6ed;
    }
    .custom-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #f1f5f9;
        font-size: 12px;
        color: #374151;
        vertical-align: middle;
    }
    .custom-table tr:hover {
        background-color: #f0f9ff !important;
        transition: background-color 0.2s ease;
    }
    .patient-cell {
        display: flex;
        flex-direction: column;
    }
    .patient-name {
        font-weight: 600;
        color: #0f1f3d;
    }
    .patient-id {
        font-size: 10px;
        color: #94a3b8;
    }
    
    /* Progress Bars */
    .prob-bar-bg {
        width: 100px;
        height: 6px;
        background-color: #e2e6ed;
        border-radius: 3px;
        overflow: hidden;
        display: inline-block;
        vertical-align: middle;
        margin-right: 8px;
    }
    .prob-bar-fill {
        height: 100%;
        border-radius: 3px;
        transition: width 0.4s ease;
    }
    .prob-bar-red { background-color: #dc2626; }
    .prob-bar-amber { background-color: #f59e0b; }
    .prob-bar-green { background-color: #16a34a; }

    /* Custom Badges/Pills */
    .pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 500;
    }
    .pill-red {
        background-color: #fef2f2;
        color: #dc2626;
        border: 1px solid #fee2e2;
    }
    .pill-amber {
        background-color: #fffbeb;
        color: #d97706;
        border: 1px solid #fef3c7;
    }
    .pill-green {
        background-color: #f0fdf4;
        color: #16a34a;
        border: 1px solid #dcfce7;
    }
    
    .action-badge {
        font-size: 11px;
        font-weight: 500;
        padding: 2px 6px;
        border-radius: 4px;
    }
    .action-call-sms {
        background-color: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
    }
    .action-sms {
        background-color: #fffbeb;
        color: #d97706;
        border: 1px solid #fef3c7;
    }
    .action-standard {
        background-color: #f8fafc;
        color: #475569;
        border: 1px solid #e2e6ed;
    }

    /* Filter Chips */
    .filter-chips-container {
        display: flex;
        gap: 8px;
        margin-bottom: 16px;
    }
    .filter-chip {
        padding: 4px 12px;
        border-radius: 16px;
        border: 1px solid #e2e6ed;
        background-color: #ffffff;
        font-size: 12px;
        font-weight: 500;
        color: #64748b;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .filter-chip:hover {
        border-color: #cbd5e1;
        color: #0f1f3d;
    }
    .filter-chip.active {
        background-color: #f0f9ff;
        border-color: #0ea5e9;
        color: #0284c7;
    }

    /* Alerts and Timeline */
    .alert-item {
        display: flex;
        gap: 10px;
        margin-bottom: 12px;
        font-size: 12px;
    }
    .alert-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-top: 4px;
        flex-shrink: 0;
    }
    .alert-dot-red { background-color: #dc2626; }
    .alert-dot-amber { background-color: #f59e0b; }
    .alert-dot-blue { background-color: #0ea5e9; }
    .alert-content {
        display: flex;
        flex-direction: column;
    }
    .alert-text {
        color: #374151;
        font-weight: 500;
    }
    .alert-time {
        color: #94a3b8;
        font-size: 10px;
        margin-top: 2px;
    }

    /* Interventions Timeline */
    .timeline-item {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding: 10px 0;
        border-bottom: 1px solid #f1f5f9;
    }
    .timeline-item:last-child {
        border-bottom: none;
    }
    .timeline-left {
        display: flex;
        gap: 8px;
    }
    .timeline-info {
        display: flex;
        flex-direction: column;
    }
    .timeline-name {
        font-size: 12px;
        font-weight: 600;
        color: #0f1f3d;
    }
    .timeline-appt {
        font-size: 10px;
        color: #94a3b8;
        margin-top: 2px;
    }
    .timeline-right {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 4px;
    }
    .timeline-badge-time {
        font-size: 10px;
        color: #94a3b8;
    }

    /* Gauge and Circular Widgets */
    .gauge-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    .gauge-container {
        position: relative;
        width: 150px;
        height: 150px;
    }
    .gauge-center {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }
    .gauge-value {
        font-size: 28px;
        font-weight: 700;
        color: #0f1f3d;
    }
    .gauge-label {
        font-size: 11px;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 500;
    }

    /* Banners & Empty States */
    .banner {
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .banner-success {
        background-color: #f0fdf4;
        color: #16a34a;
        border: 1px solid #bbf7d0;
    }
    .banner-danger {
        background-color: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
    }
    .banner-warning {
        background-color: #fffbeb;
        color: #d97706;
        border: 1px solid #fef3c7;
    }

    /* Skeleton loaders */
    .skeleton-bar {
        background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 37%, #f1f5f9 63%);
        background-size: 400% 100%;
        animation: skeleton-loading 1.4s ease infinite;
        border-radius: 4px;
        height: 12px;
        margin-bottom: 8px;
    }
    @keyframes skeleton-loading {
        0% { background-position: 100% 50%; }
        100% { background-position: 0 50%; }
    }
    
    /* Fix Streamlit column spacing */
    [data-testid="column"] {
        width: 100%;
    }
    
    /* Hide native Streamlit table borders */
    div.stDataFrame {
        border: none !important;
    }

    /* ============================================================
       STREAMLIT NATIVE BUTTON OVERRIDES
       ============================================================ */

    /* Primary / Default Buttons */
    div.stButton > button {
        background-color: #0ea5e9 !important;
        color: #ffffff !important;
        border: 1px solid #0284c7 !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        padding: 6px 14px !important;
        cursor: pointer !important;
        transition: background-color 0.2s ease, box-shadow 0.2s ease !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.4 !important;
    }
    div.stButton > button:hover {
        background-color: #0284c7 !important;
        box-shadow: 0 2px 6px rgba(14, 165, 233, 0.35) !important;
        border-color: #0369a1 !important;
        color: #ffffff !important;
    }
    div.stButton > button:active {
        background-color: #0369a1 !important;
        color: #ffffff !important;
    }
    div.stButton > button:focus {
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.3) !important;
        color: #ffffff !important;
    }

    /* Disabled Buttons */
    div.stButton > button:disabled,
    div.stButton > button[disabled] {
        background-color: #e2e8f0 !important;
        color: #94a3b8 !important;
        border-color: #cbd5e1 !important;
        cursor: not-allowed !important;
        box-shadow: none !important;
    }

    /* Form Submit Button */
    div.stForm button[kind="primaryFormSubmit"],
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #0f1f3d !important;
        color: #ffffff !important;
        border: 1px solid #0f1f3d !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
        width: 100% !important;
        font-family: 'Inter', sans-serif !important;
        transition: background-color 0.2s ease !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #1e3a5f !important;
        color: #ffffff !important;
        border-color: #1e3a5f !important;
    }

    /* Download Button */
    div.stDownloadButton > button {
        background-color: #f0fdf4 !important;
        color: #16a34a !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        padding: 6px 14px !important;
        font-family: 'Inter', sans-serif !important;
        transition: background-color 0.2s ease !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #dcfce7 !important;
        color: #15803d !important;
        border-color: #86efac !important;
    }

    /* ============================================================
       STREAMLIT PILLS / FILTER CHIPS — aggressive overrides
       ============================================================ */

    /* Target ALL pill containers */
    div[data-testid="stButtonGroup"],
    [data-testid="stButtonGroup"],
    div[data-testid="stPills"],
    [data-testid="stPills"] {
        gap: 6px !important;
        flex-wrap: wrap !important;
    }

    /* Every button inside pills — unselected state */
    div[data-testid="stButtonGroup"] button,
    [data-testid="stButtonGroup"] button,
    [data-testid="stButtonGroup"] button[kind="pills"],
    [data-testid="stButtonGroup"] button[data-selected="false"],
    [data-testid="stButtonGroup"] button[aria-pressed="false"],
    [data-testid="stButtonGroup"] button[aria-checked="false"],
    div[data-testid="stPills"] button,
    [data-testid="stPills"] button,
    [data-testid="stPills"] button[kind="pills"],
    [data-testid="stPills"] button[data-selected="false"],
    [data-testid="stPills"] button[aria-pressed="false"] {
        padding: 5px 14px !important;
        border-radius: 20px !important;
        border: 1px solid #d1d5db !important;
        background-color: #f8fafc !important;
        background: #f8fafc !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #475569 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: none !important;
        outline: none !important;
        min-height: 0 !important;
        height: auto !important;
    }

    /* Text/paragraph inside pill buttons */
    div[data-testid="stButtonGroup"] button p,
    div[data-testid="stButtonGroup"] button span,
    div[data-testid="stButtonGroup"] button div,
    [data-testid="stButtonGroup"] button p,
    [data-testid="stButtonGroup"] button span,
    [data-testid="stButtonGroup"] button div,
    div[data-testid="stPills"] button p,
    div[data-testid="stPills"] button span,
    div[data-testid="stPills"] button div,
    [data-testid="stPills"] button p,
    [data-testid="stPills"] button span,
    [data-testid="stPills"] button div {
        color: #475569 !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Hover state */
    div[data-testid="stButtonGroup"] button:hover,
    [data-testid="stButtonGroup"] button:hover,
    div[data-testid="stPills"] button:hover,
    [data-testid="stPills"] button:hover {
        border-color: #0ea5e9 !important;
        color: #0284c7 !important;
        background-color: #f0f9ff !important;
        background: #f0f9ff !important;
    }
    div[data-testid="stButtonGroup"] button:hover p,
    div[data-testid="stButtonGroup"] button:hover span,
    div[data-testid="stButtonGroup"] button:hover div,
    [data-testid="stButtonGroup"] button:hover p,
    [data-testid="stButtonGroup"] button:hover span,
    [data-testid="stButtonGroup"] button:hover div,
    div[data-testid="stPills"] button:hover p,
    div[data-testid="stPills"] button:hover span,
    div[data-testid="stPills"] button:hover div,
    [data-testid="stPills"] button:hover p,
    [data-testid="stPills"] button:hover span,
    [data-testid="stPills"] button:hover div {
        color: #0284c7 !important;
    }

    /* Selected / active pill */
    div[data-testid="stButtonGroup"] button[aria-checked="true"],
    div[data-testid="stButtonGroup"] button[data-selected="true"],
    div[data-testid="stButtonGroup"] button[aria-pressed="true"],
    [data-testid="stButtonGroup"] button[aria-checked="true"],
    [data-testid="stButtonGroup"] button[data-selected="true"],
    [data-testid="stButtonGroup"] button[aria-pressed="true"],
    div[data-testid="stPills"] button[aria-checked="true"],
    div[data-testid="stPills"] button[data-selected="true"],
    div[data-testid="stPills"] button[aria-pressed="true"],
    [data-testid="stPills"] button[aria-checked="true"],
    [data-testid="stPills"] button[data-selected="true"],
    [data-testid="stPills"] button[aria-pressed="true"],
    [data-testid="stPills"] button[kind="pills"][data-selected="true"] {
        background-color: #0ea5e9 !important;
        background: #0ea5e9 !important;
        border-color: #0284c7 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 6px rgba(14, 165, 233, 0.3) !important;
    }
    div[data-testid="stButtonGroup"] button[aria-checked="true"] p,
    div[data-testid="stButtonGroup"] button[aria-checked="true"] span,
    div[data-testid="stButtonGroup"] button[aria-checked="true"] div,
    [data-testid="stButtonGroup"] button[aria-checked="true"] p,
    [data-testid="stButtonGroup"] button[aria-checked="true"] span,
    [data-testid="stButtonGroup"] button[aria-checked="true"] div,
    div[data-testid="stPills"] button[aria-checked="true"] p,
    div[data-testid="stPills"] button[aria-checked="true"] span,
    div[data-testid="stPills"] button[aria-checked="true"] div,
    [data-testid="stPills"] button[aria-checked="true"] p,
    [data-testid="stPills"] button[aria-checked="true"] span,
    [data-testid="stPills"] button[aria-checked="true"] div,
    div[data-testid="stPills"] button[data-selected="true"] p,
    div[data-testid="stPills"] button[data-selected="true"] span,
    div[data-testid="stPills"] button[data-selected="true"] div,
    [data-testid="stPills"] button[data-selected="true"] p,
    [data-testid="stPills"] button[data-selected="true"] span,
    [data-testid="stPills"] button[data-selected="true"] div,
    [data-testid="stPills"] button[aria-pressed="true"] p,
    [data-testid="stPills"] button[aria-pressed="true"] span,
    [data-testid="stPills"] button[aria-pressed="true"] div {
        color: #ffffff !important;
    }

    /* ============================================================
       STREAMLIT METRICS
       ============================================================ */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 0.5px solid #e2e6ed !important;
        border-radius: 8px !important;
        padding: 14px 16px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
    }
    div[data-testid="stMetricLabel"] > div,
    div[data-testid="stMetricLabel"] p {
        font-size: 11px !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.4px !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricValue"] {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #0f1f3d !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stMetricDelta"] > div,
    div[data-testid="stMetricDelta"] {
        font-size: 11px !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ============================================================
       STREAMLIT FORM INPUTS (selectbox, text_input, number_input)
       ============================================================ */
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        border: 1px solid #e2e6ed !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        color: #374151 !important;
        background-color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        padding: 6px 10px !important;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stNumberInput"] input:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.15) !important;
        outline: none !important;
    }
    div[data-testid="stSelectbox"] > div > div {
        border: 1px solid #e2e6ed !important;
        border-radius: 6px !important;
        background-color: #ffffff !important;
        font-size: 13px !important;
        color: #374151 !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stSelectbox"] svg {
        color: #94a3b8 !important;
    }

    /* Label text for form fields */
    div[data-testid="stTextInput"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #475569 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ============================================================
       STREAMLIT FILE UPLOADER
       ============================================================ */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #e2e6ed !important;
        border-radius: 8px !important;
        background-color: #f8fafc !important;
        padding: 20px !important;
        text-align: center !important;
        transition: border-color 0.2s ease !important;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: #0ea5e9 !important;
        background-color: #f0f9ff !important;
    }
    div[data-testid="stFileUploader"] label {
        font-size: 13px !important;
        color: #64748b !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stFileUploader"] button {
        background-color: #0ea5e9 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stFileUploader"] button:hover {
        background-color: #0284c7 !important;
        color: #ffffff !important;
    }

    /* ============================================================
       STREAMLIT EXPANDER
       ============================================================ */
    div[data-testid="stExpander"] {
        border: 1px solid #e2e6ed !important;
        border-radius: 8px !important;
        background-color: #ffffff !important;
        overflow: hidden !important;
    }
    div[data-testid="stExpander"] summary {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #0f1f3d !important;
        padding: 12px 16px !important;
        background-color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stExpander"] summary:hover {
        background-color: #f0f9ff !important;
        color: #0284c7 !important;
    }

    /* ============================================================
       STREAMLIT SPINNER & STATUS MESSAGES
       ============================================================ */
    div[data-testid="stSpinner"] p {
        color: #64748b !important;
        font-size: 13px !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Warning / Info / Error / Success messages */
    div[data-testid="stAlert"] {
        border-radius: 6px !important;
        font-size: 13px !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Markdown headings used in pages */
    h4 {
        color: #0f1f3d !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ============================================================
       MISSING ALERT DOT GREEN (was referenced but not defined)
       ============================================================ */
    .alert-dot-green { background-color: #16a34a; }

    </style>
    """

def inject_styles():
    """Inject CarePredict styling into the current Streamlit app page."""
    st.html(get_custom_css())
