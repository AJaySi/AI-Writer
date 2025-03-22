def get_base_styles():
    """Base styles for common elements"""
    return """
    .card-base {
        background: linear-gradient(135deg, #EBF4FF, #F0F7FF);
        border-radius: 12px;
        border: 1px solid rgba(66, 153, 225, 0.2);
        box-shadow: 0 4px 8px rgba(0, 62, 255, 0.08);
        transition: all 0.3s ease;
    }
    .gradient-text {
        background: linear-gradient(135deg, #2B6CB0, #4299E1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    """

def get_provider_selection_styles():
    """Styles for provider selection section"""
    return """
    .provider-card {
        background: linear-gradient(135deg, #EBF4FF, #F0F7FF);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(0, 62, 255, 0.08);
        border: 1px solid rgba(66, 153, 225, 0.2);
    }
    .provider-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 20px rgba(0, 62, 255, 0.12);
    }
    .provider-header {
        font-size: 24px;
        font-weight: 700;
        color: #2B6CB0;
        margin-bottom: 15px;
        text-align: center;
    }
    """

def get_api_form_styles():
    return """
    /* Base Styles */
    .api-interface {
        background: linear-gradient(135deg, #EBF4FF, #F0F7FF);
        border-radius: 1px;
        padding: 1px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }

    /* Headers and Titles */
    .api-title {
        background: linear-gradient(135deg, #2D3748, #1A202C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 25px;
        letter-spacing: 0.5px;
    }

    .api-subtitle {
        color: #4A5568;
        font-size: 18px;
        font-weight: 500;
        text-align: center;
        margin-bottom: 20px;
        line-height: 1.6;
    }

    /* Input Fields */
    .api-input-container {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(66, 153, 225, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }

    .api-input-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
    }

    .api-input-label {
        color: #2D3748;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 8px;
        display: block;
    }

    /* Help Text */
    .api-help-text {
        color: #718096;
        font-size: 14px;
        margin-top: 6px;
        line-height: 1.5;
    }

    /* Message Styles */
    .api-message {
        padding: 16px 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 4px solid;
    }

    .api-message.info {
        background: #EBF8FF;
        border-left-color: #3182CE;
        color: #2C5282;
    }

    .api-message.warning {
        background: #FFFFF0;
        border-left-color: #D69E2E;
        color: #975A16;
    }

    .api-message.error {
        background: #FFF5F5;
        border-left-color: #C53030;
        color: #9B2C2C;
    }

    /* Group Headers */
    .api-group-header {
        background: linear-gradient(135deg, #2D3748, #4A5568);
        color: #FFFFFF;
        padding: 16px 20px;
        border-radius: 10px;
        margin: 20px 0;
        font-weight: 600;
        font-size: 18px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Required Indicator */
    .api-required {
        color: #C53030;
        margin-left: 4px;
        font-weight: bold;
    }

    /* Status Indicators */
    .api-status {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
    }

    .api-status.active {
        background: #F0FFF4;
        color: #2F855A;
        border: 1px solid #48BB78;
    }

    .api-status.missing {
        background: #FFF5F5;
        color: #9B2C2C;
        border: 1px solid #F56565;
    }

    /* Tooltips */
    .api-tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }

    .api-tooltip:hover::before {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        padding: 8px 12px;
        background: #2D3748;
        color: #FFFFFF;
        border-radius: 6px;
        font-size: 14px;
        white-space: nowrap;
        z-index: 1000;
    }
    """