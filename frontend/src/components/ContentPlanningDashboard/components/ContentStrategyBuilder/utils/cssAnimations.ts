export const setupCSSAnimations = () => {
  const style = document.createElement('style');
  style.textContent = `
    @keyframes pulse {
      0% { transform: scale(1); }
      50% { transform: scale(1.1); }
      100% { transform: scale(1); }
    }
    @keyframes shimmer {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(100%); }
    }
    @keyframes rotate {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
  `;
  document.head.appendChild(style);
  return style;
};

export const cleanupCSSAnimations = (style: HTMLStyleElement) => {
  if (document.head.contains(style)) {
    document.head.removeChild(style);
  }
};
