# Quick Deployment Steps

## 7-Step Deployment (15 Minutes)

### Step 1: Backup Old Files
```bash
mkdir backup_old_code
copy app.py backup_old_code\
copy RouteMap.py backup_old_code\
```

### Step 2: Create .env File
```bash
copy .env.example .env
Edit .env and add your API keys:
- OPENROUTE_API_KEY=your_key
- DROPBOX_MODEL_URL=your_url
- WEATHER_API_KEY=your_key (optional)
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Clean Old Database
```bash
del user_data.db
```

### Step 5: Start Application
```bash
python app.py
```

### Step 6: Test
- Open http://localhost:5000
- Register new account
- Login with account
- Test predictions

### Step 7: Deploy to Production
- Revoke old exposed API keys
- Deploy to Heroku/AWS/etc
- Monitor logs

## Security Checklist

- [ ] .env file created with your keys
- [ ] No hardcoded secrets in code
- [ ] Old API keys revoked
- [ ] Old Dropbox token revoked
- [ ] Passwords are bcrypt hashed
- [ ] All validation working
- [ ] No console errors

## Support

See README_DEPLOYMENT_READY.txt for detailed instructions.
See SECURITY.md for complete security documentation.