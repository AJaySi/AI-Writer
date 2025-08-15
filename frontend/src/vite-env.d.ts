/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_CLERK_PUBLISHABLE_KEY: string
  readonly VITE_API_BASE_URL: string
  readonly VITE_ENV: string
  readonly VITE_ENABLE_EMAIL_AUTH: string
  readonly VITE_ENABLE_GITHUB_AUTH: string
  readonly VITE_ENABLE_GOOGLE_AUTH: string
  readonly VITE_ENABLE_FACEBOOK_AUTH: string
  readonly VITE_GOOGLE_REDIRECT_URI: string
  readonly VITE_GITHUB_REDIRECT_URI: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
