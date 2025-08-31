# Rex AI Assistant - Deployment Guide

## 🌐 Web Deployment (Render.com)

### Prerequisites
- GitHub account
- Render.com account (free tier available)

### Step 1: Upload to GitHub
1. Create a new repository on GitHub
2. Upload all Rex files to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial Rex AI Assistant"
   git branch -M main
   git remote add origin https://github.com/yourusername/rex-ai-assistant.git
   git push -u origin main
   ```

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure deployment:
   - **Name**: `rex-ai-assistant`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: `Free` (or paid for better performance)

### Step 3: Environment Variables
Add these environment variables in Render dashboard:
- `OPENROUTER_API_KEY`: `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`
- `FLASK_ENV`: `production`

### Step 4: Custom Domain (Optional)
- Add custom domain in Render dashboard
- Update DNS settings to point to Render

---

## 📱 Play Store Deployment (PWA to APK)

### Method 1: PWA Builder (Recommended)
1. Go to [PWABuilder.com](https://www.pwabuilder.com)
2. Enter your web app URL: `https://your-rex-app.onrender.com`
3. Click "Start" to analyze your PWA
4. Download the Android package
5. Sign the APK for Play Store submission

### Method 2: Capacitor (Advanced)
1. Install Capacitor:
   ```bash
   npm install -g @capacitor/cli
   npx cap init "Rex AI Assistant" com.yourcompany.rex
   ```
2. Add Android platform:
   ```bash
   npx cap add android
   ```
3. Build and generate APK

### Play Store Requirements
- **Developer Account**: $25 one-time fee
- **App Icon**: 512x512 PNG
- **Screenshots**: Various sizes for phones/tablets
- **Privacy Policy**: Required for AI apps
- **Content Rating**: Complete questionnaire

---

## 🎯 Production Checklist

### Before Deployment
- [ ] Test all features locally
- [ ] Verify API key is working
- [ ] Check mobile responsiveness
- [ ] Test PWA functionality
- [ ] Update manifest.json with final branding

### Security
- [ ] Use environment variables for API keys
- [ ] Enable HTTPS in production
- [ ] Add rate limiting if needed
- [ ] Review data storage security

### Performance
- [ ] Optimize images and assets
- [ ] Enable compression (gzip)
- [ ] Add CDN if needed
- [ ] Monitor API usage

---

## 🚀 Quick Start Commands

### Local Development
```bash
cd rex-ai-assistant
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
set OPENROUTER_API_KEY=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
python main.py
```

### Test PWA Features
1. Open http://localhost:5000 in Chrome
2. Open DevTools → Application → Manifest
3. Test "Add to Home Screen"
4. Test offline functionality

---

## 📋 App Store Assets Needed

### Icons (Generate from logo)
- 72x72, 96x96, 128x128, 144x144, 152x152, 192x192, 384x384, 512x512

### Screenshots
- Phone: 1080x1920, 1440x2560
- Tablet: 1200x1920, 2048x2732

### Marketing Materials
- Feature graphic: 1024x500
- App description (max 4000 characters)
- Short description (max 80 characters)

---

## 💡 Showcase Features for Recruiters

### Technical Highlights
- **Direct API Integration**: Efficient DeepSeek V3.1 calls via OpenRouter
- **Mobile-First PWA**: Progressive Web App with offline capabilities
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Production Ready**: Environment-based configuration and error handling
- **Modern Stack**: Flask, vanilla JavaScript, CSS Grid/Flexbox

### Demo Script
1. **Mobile Experience**: Show responsive design and PWA features
2. **AI Conversations**: Demonstrate natural language processing
3. **Performance**: Show fast response times and error handling
4. **Code Quality**: Highlight clean architecture and best practices

---

## 🔧 Troubleshooting

### Common Issues
- **API Errors**: Check OpenRouter API key in environment variables
- **CORS Issues**: Ensure proper headers in production
- **PWA Not Installing**: Verify manifest.json and HTTPS requirement
- **Slow Response**: Check API rate limits and server location

### Debug Mode
Add `FLASK_ENV=development` to enable debug mode locally.

---

## 📞 Support

For deployment support or technical questions:
- Check GitHub Issues
- Review Render.com documentation
- PWA Builder support forums
