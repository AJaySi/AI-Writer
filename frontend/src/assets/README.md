# Assets Directory

This directory contains all static assets used throughout the ALwrity application.

## Structure

```
src/assets/
├── images/           # Image assets
│   ├── alwrity_logo.png      # ALwrity company logo
│   └── AskAlwrity-min.ico    # ALwrity Co-Pilot icon
└── README.md         # This file
```

## Usage

### ALwrity Logo (`alwrity_logo.png`)
- **Location**: `src/assets/images/alwrity_logo.png`
- **Usage**: Company branding in headers, navigation, and branding elements
- **Format**: PNG with transparency
- **Size**: 188KB, optimized for web

### ALwrity Co-Pilot Icon (`AskAlwrity-min.ico`)
- **Location**: `src/assets/images/AskAlwrity-min.ico`
- **Usage**: CopilotKit trigger button icon
- **Format**: ICO format for optimal icon display
- **Size**: 79KB

## Import Examples

```typescript
// In components
import alwrityLogo from '../../assets/images/alwrity_logo.png';
import alwrityIcon from '../../assets/images/AskAlwrity-min.ico';

// In CSS
background-image: url('../../../assets/images/AskAlwrity-min.ico');
```

## Notes

- All assets are optimized for web use
- ICO format is used for the Co-Pilot icon to ensure crisp display at various sizes
- PNG format is used for the logo to maintain transparency
- Assets are organized by type for easy maintenance
