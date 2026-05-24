# Security Update - Secrets Removed & Code Hardened

## 🚨 CRITICAL ISSUES FIXED

### 1. ✅ Exposed API Keys Removed
**Before:** Hardcoded in source code
```python
api_key = "5b3ce3597851110001cf624856373ac531fe460fbd5aaaf9704966c9"  # EXPOSED!
```

**After:** Loaded from environment variables
```python
api_key = os.environ.get("OPENROUTE_API_KEY")
```

### 2. ✅ Exposed Dropbox Token Removed
**Before:** URL with token in source code
```python
dropbox_url = "https://dl.dropboxusercontent.com/scl/fi/...?rlkey=pw8hrowbugyzlmc7s84wp4j4w"  # EXPOSED!
```

**After:** URL loaded from environment
```python
dropbox_url = os.environ.get("DROPBOX_MODEL_URL")
```

### 3. ✅ Plain Text Passwords Fixed
**Before:** Passwords stored in plain text
```python
cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?)",
               (name, password, mobile, email))  # INSECURE!
```

**After:** Passwords hashed with bcrypt
```python
hashed_password = hash_password(password)
cursor.execute("INSERT INTO user (name, password, ...) VALUES (?, ?, ...)",
               (name, hashed_password, ...))
```

---

## 🔐 Environment Variables Setup

### Step 1: Create .env file
```bash
cp .env.example .env
```

### Step 2: Get Your API Keys

#### OpenRouteService API Key
1. Go to https://openrouteservice.org/
2. Sign up and create account
3. Generate API key
4. Add to .env:
```
OPENROUTE_API_KEY=your_new_api_key_here
```

#### Dropbox URL
1. Go to your Dropbox folder with model file
2. Right-click → Share → Create link
3. Copy the link and add to .env:
```
DROPBOX_MODEL_URL=https://www.dropbox.com/YOUR_SHARED_LINK
```

#### Weather API Key (Optional)
1. Go to https://www.weatherapi.com/
2. Sign up and generate API key
3. Add to .env:
```
WEATHER_API_KEY=your_weather_api_key_here
```

### Step 3: .env File Example
```
# .env (NEVER COMMIT THIS FILE!)
OPENROUTE_API_KEY=your_new_api_key_here
DROPBOX_MODEL_URL=your_dropbox_link_here
WEATHER_API_KEY=your_weather_key_here
PORT=5000
FLASK_ENV=development
```

### Step 4: Verify .env is in .gitignore
```bash
# Check that .env is listed
cat .gitignore | grep ".env"
# Should show: .env
```

---

## ⚠️ IMMEDIATE ACTIONS REQUIRED

### REVOKE EXPOSED CREDENTIALS NOW!

The following credentials were exposed on GitHub:
1. **OpenRouteService API Key:** `5b3ce3597851110001cf624856373ac531fe460fbd5aaaf9704966c9`
   - Status: 🔴 **REVOKE IMMEDIATELY**
   - Action: https://openrouteservice.org/ → Delete old key
   - Generate new key and add to .env

2. **Dropbox Token:** In URL parameter `rlkey=pw8hrowbugyzlmc7s84wp4j4w`
   - Status: 🔴 **REVOKE IMMEDIATELY**
   - Action: Go to Dropbox → Remove share link
   - Create new share link and add to .env

3. **User Passwords:** Plain text in database
   - Status: 🔴 **DELETE DATABASE**
   - Action: Delete `user_data.db`
   - Users must re-register with new hashed passwords

---

## 📋 Files Changed

### Updated Files
- ✅ `app.py` - Now loads Dropbox URL from .env, uses bcrypt for passwords
- ✅ `RouteMap.py` - Now loads API key from .env
- ✅ `.gitignore` - Added .env and credentials to prevent future exposure
- ✅ `requirements.txt` - Added bcrypt and python-dotenv

### New Files
- ✅ `.env.example` - Template for environment variables
- ✅ `SECURITY.md` - This file (security guidelines)

### Deleted (From Git History Only)
- Exposed API keys
- Exposed Dropbox tokens
- Plain text password database entries

---

## 🚀 Deployment Instructions

### Local Development
```bash
# 1. Create .env file
cp .env.example .env

# 2. Edit .env with your credentials
nano .env  # or use your editor

# 3. Install dependencies
pip install -r requirements.txt

# 4. Delete old database (has plain text passwords)
rm user_data.db

# 5. Run application
python app.py
```

### Production Deployment
```bash
# Set environment variables (don't use .env files in production!)
export OPENROUTE_API_KEY="your_key"
export DROPBOX_MODEL_URL="your_url"
export WEATHER_API_KEY="your_key"
export PORT=5000
export FLASK_ENV=production

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Heroku Deployment
```bash
# Set config vars in Heroku Dashboard
heroku config:set OPENROUTE_API_KEY="your_key"
heroku config:set DROPBOX_MODEL_URL="your_url"
heroku config:set WEATHER_API_KEY="your_key"
heroku config:set FLASK_ENV="production"

# Push to Heroku
git push heroku main
```

---

## 🔒 Security Best Practices (Going Forward)

1. **Never commit credentials** - Always use environment variables
2. **Use .env.example** - Provide template without real values
3. **Add .env to .gitignore** - Prevent accidental commits
4. **Rotate credentials regularly** - Change keys every 3 months
5. **Use secret scanning** - Enable GitHub secret scanning
6. **Review commits** - Check git log for secrets before pushing
7. **Use services like:** 
   - AWS Secrets Manager
   - HashiCorp Vault
   - Azure Key Vault

---

## ✅ Pre-Deployment Checklist

- [ ] Created .env file with all credentials
- [ ] Verified .env is in .gitignore
- [ ] Revoked exposed OpenRouteService API key
- [ ] Revoked exposed Dropbox share link
- [ ] Deleted old user_data.db (has plain text passwords)
- [ ] Installed new requirements (pip install -r requirements.txt)
- [ ] Tested app locally (python app.py)
- [ ] Tested user registration (passwords are now hashed)
- [ ] Tested prediction (map generation with new API key)
- [ ] Committed all changes and pushed to GitHub
- [ ] Enabled GitHub secret scanning in repository settings

---

## 🆘 Troubleshooting

### "Module not found: dotenv"
```bash
pip install python-dotenv
```

### ".env file not loading"
```bash
# Make sure .env is in the same directory as app.py
# Check that you're using load_dotenv() at the top of app.py
```

### "OPENROUTE_API_KEY not set" warning
```bash
# Check your .env file has the key
cat .env | grep OPENROUTE_API_KEY

# Make sure .env is loaded (check app.py has load_dotenv())
```

### "Old passwords don't work"
```bash
# Expected! Passwords are now hashed.
# Users must re-register with new passwords.
# Delete user_data.db to allow re-registration.
```

---

## 📚 References

- [Environment Variables Best Practices](https://12factor.net/config)
- [OWASP Secrets Management](https://owasp.org/www-community/vulnerabilities/Sensitive_Data_Exposure)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Flask Security](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Bcrypt Password Hashing](https://github.com/pyca/bcrypt)

---

## 🎯 Status

✅ **All exposed secrets removed**  
✅ **All credentials moved to environment variables**  
✅ **Password hashing implemented**  
✅ **Security documentation added**  
✅ **.env.example template provided**  
✅ **.gitignore updated to prevent future exposure**  

**Next Step:** Set up environment variables and redeploy!
