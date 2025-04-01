API_KEY_MANAGER_STYLES = """
    <style>
        /* Main container */
        .main .block-container {
            padding-top: 0.5rem;
        }

        /* Step indicator */
        .step-indicator {
            display: flex;
            flex-direction: row;
            gap: 0.25rem;
            margin: 0.5rem 0;
            padding: 0.5rem;
            background: linear-gradient(135deg, #1a365d, #2c5282);
            border-radius: 2px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            width: 100%;
            justify-content: center;
        }

        .step {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.25rem 0.75rem;
            border-radius: 3px;
            transition: all 0.3s ease;
            position: relative;
            font-size: 0.85rem;
            white-space: nowrap;
        }

        .step:not(:last-child)::after {
            content: '';
            position: absolute;
            right: -0.25rem;
            top: 50%;
            transform: translateY(-50%);
            width: 0.5rem;
            height: 2px;
            background: rgba(255, 255, 255, 0.3);
        }

        .step.completed {
            background: rgba(255, 255, 255, 0.1);
        }

        .step.current {
            background: rgba(255, 255, 255, 0.2);
            font-weight: 600;
        }

        .step.upcoming {
            opacity: 0.7;
        }

        .step-number {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            font-weight: 600;
            font-size: 0.5rem;
            flex-shrink: 0;
        }

        .step.completed .step-number {
            background: #4CAF50;
        }

        .step.current .step-number {
            background: #2196F3;
        }

        .step.upcoming .step-number {
            background: rgba(255, 255, 255, 0.3);
        }

        .step-content {
            display: flex;
            flex-direction: row;
            gap: 0.5rem;
            align-items: center;
        }

        .step-title {
            font-weight: 500;
            color: white;
            font-size: 0.85rem;
        }

        .step-description {
            font-size: 0.7rem;
            color: rgba(255, 255, 255, 0.8);
        }

        /* Navigation buttons */
        .nav-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 1rem;
            gap: 1rem;
        }

        .nav-button {
            background: linear-gradient(135deg, #1a365d, #2c5282);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            font-size: 0.9rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .nav-button:hover {
            background: linear-gradient(135deg, #2c5282, #1a365d);
            transform: translateY(-1px);
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        }

        .nav-button:disabled {
            background: #94a3b8;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        /* Form elements */
        .stTextInput input {
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 0.5rem;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }

        .stTextInput input:focus {
            border-color: #2c5282;
            box-shadow: 0 0 0 2px rgba(44, 82, 130, 0.1);
        }

        .stSelectbox select {
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 0.5rem;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }

        .stSelectbox select:focus {
            border-color: #2c5282;
            box-shadow: 0 0 0 2px rgba(44, 82, 130, 0.1);
        }

        /* Success message */
        .success-message {
            background: linear-gradient(135deg, #059669, #10b981);
            color: white;
            padding: 1rem;
            border-radius: 6px;
            margin: 0.75rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            font-size: 0.9rem;
        }

        /* Error message */
        .error-message {
            background: linear-gradient(135deg, #dc2626, #ef4444);
            color: white;
            padding: 1rem;
            border-radius: 6px;
            margin: 0.75rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            font-size: 0.9rem;
        }

        /* Loading spinner */
        .loading-spinner {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1.5rem;
        }

        /* Card styling */
        .card {
            background: white;
            border-radius: 2px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            padding: 0.5rem;
            margin-bottom: 0.5rem;
            transition: all 0.3s ease;
        }

        .card:hover {
            transform: translateY(-1px);
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        }

        /* Glassmorphic effect */
        .glass {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 2px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        /* Gradient text */
        .gradient-text {
            background: linear-gradient(135deg, #1a365d, #2c5282);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
        }

        /* Hide sidebar */
        section[data-testid="stSidebar"] {
            display: none;
        }

        /* AI Provider Cards */
        .ai-provider-card {
            background: white;
            border-radius: 2px;
            padding: 0.5rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            border: 1px solid #e2e8f0;
        }

        .ai-provider-card:hover {
            transform: translateY(-1px);
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        }

        .ai-provider-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.75rem;
        }

        .ai-provider-icon {
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 6px;
            background: linear-gradient(135deg, #1a365d, #2c5282);
            color: white;
            font-size: 16px;
        }

        .ai-provider-title {
            font-size: 1rem;
            font-weight: 600;
            color: #1a365d;
        }

        .ai-provider-description {
            color: #4a5568;
            font-size: 0.85rem;
            margin-bottom: 0.75rem;
        }

        .ai-provider-input {
            margin-top: 0.75rem;
        }

        .ai-provider-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 0.5rem;
            font-size: 0.85rem;
        }

        .status-valid {
            color: #059669;
        }

        .status-invalid {
            color: #dc2626;
        }

        /* Coming Soon Badge */
        .coming-soon-badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            background: linear-gradient(135deg, #4a5568, #2d3748);
            color: white;
            border-radius: 9999px;
            font-size: 0.7rem;
            font-weight: 500;
            margin-left: 0.5rem;
        }

        /* Main container styles */
        .setup-header {
            background: linear-gradient(135deg, #1f77b4 0%, #2ecc71 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .setup-header h2 {
            color: white;
            margin: 0;
            font-size: 2rem;
        }
        
        .setup-header p {
            color: rgba(255, 255, 255, 0.9);
            margin: 0.5rem 0 0;
            font-size: 1.1rem;
        }
        
        /* AI Provider Card styles */
        .ai-provider-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            border: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        .ai-provider-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        
        .ai-provider-card.disabled {
            opacity: 0.7;
            background: #f8f9fa;
            cursor: not-allowed;
        }
        
        .ai-provider-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .ai-provider-icon {
            font-size: 2rem;
            background: #f8f9fa;
            width: 3rem;
            height: 3rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            color: #1f77b4;
        }
        
        .ai-provider-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .ai-provider-content {
            color: #6c757d;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        
        .ai-provider-content p {
            margin: 0 0 1rem 0;
        }
        
        .ai-provider-input {
            margin-top: 1rem;
        }
        
        .ai-provider-status {
            margin-top: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-size: 0.9rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .status-valid {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status-invalid {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
        }
        
        .coming-soon-badge {
            background: #e9ecef;
            color: #6c757d;
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.8rem;
            margin-left: 0.5rem;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            background: #f8f9fa;
            padding: 0.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            transition: all 0.3s ease;
            background: transparent;
            color: #495057;
            font-weight: 500;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: #e9ecef;
            color: #1f77b4;
        }
        
        .stTabs [aria-selected="true"] {
            background: #1f77b4 !important;
            color: white !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Navigation buttons */
        .stButton button {
            background: linear-gradient(135deg, #1f77b4 0%, #2ecc71 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .stButton button:disabled {
            background: #e9ecef;
            color: #adb5bd;
            cursor: not-allowed;
        }
        
        /* Success message */
        .success-message {
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
""" 