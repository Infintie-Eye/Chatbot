# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 3.x (current) | ✅ Yes |
| 2.x | ⚠️ Critical fixes only |
| 1.x | ❌ No |

---

## Reporting a Vulnerability

**Please do NOT open a public GitHub issue for security vulnerabilities.**

Instead, report them privately:

1. **Email:** security@blacifer.com  
2. **Subject:** `[SECURITY] Conrux AI — <short description>`
3. Include:
   - A clear description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested fix (optional but appreciated)

We will acknowledge your report within **48 hours** and aim to release a patch within **7 days** for critical issues.

---

## Security Best Practices for Deployment

### API Key Protection
- **Never** commit your `.env` file — it is in `.gitignore`
- Rotate your `GEMINI_API_KEY` immediately if accidentally exposed
- Store secrets in environment variables or a secrets manager (e.g., AWS Secrets Manager, Vault)

### Authentication
- Set `CHATBOT_API_KEY` in `.env` to enable `X-API-Key` authentication on all endpoints
- Without this variable, the API is publicly accessible — **always set it in production**

### Rate Limiting
- Default limits: 30 chat requests/min, 10 analysis requests/min
- Adjust `RATE_LIMIT_CHAT` and `RATE_LIMIT_ANALYSIS` in `.env` for your use case

### CORS
- `ALLOWED_ORIGINS` defaults to `["*"]` — restrict this to your frontend domain in production:
  ```
  ALLOWED_ORIGINS=["https://yourdomain.com"]
  ```

### File Uploads
- Max upload size is 20 MB (`MAX_FILE_SIZE_MB`)
- Only allowlisted MIME types are accepted (see `supported_image_formats` and `supported_text_formats`)

### Prompt Injection
- The input pipeline stage (`input_stage.py`) includes basic prompt injection detection and sanitisation
- Review and extend the patterns for your deployment context
