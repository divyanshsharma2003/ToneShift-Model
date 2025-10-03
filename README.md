# 🎭 ToneShift Model

**Transform any text into any tone with AI-powered precision**

A Streamlit web application that leverages Google's Gemini 2.5 Flash model to intelligently rewrite text in different tones and styles while preserving meaning and accuracy.

**🚀 [Try Live Demo](https://toneshift.streamlit.app/)**

## ✨ Features

- **Smart Tone Detection**: Automatically identifies and transforms text tone
- **Real-time Processing**: Instant text transformation with live preview
- **One-Click Copy**: Built-in clipboard functionality
- **Style Analytics**: Detailed tone matching and transformation reports
- **Session Memory**: Maintains chat history throughout your session
- **Clean UI**: Modern interface with conversation starters

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **AI Engine**: Google Gemini 2.5 Flash API
- **Backend**: Python with advanced prompt engineering
- **Deployment**: Streamlit Community Cloud

## 🚀 Quick Start

### Use Live App (Recommended)
Visit **[https://toneshift.streamlit.app/](https://toneshift.streamlit.app/)** - No installation required!

### Run Locally
```bash
# Clone repository
git clone https://github.com/divyanshsharma2003/ToneShift-Model.git
cd ToneShift-Model

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run application
streamlit run app.py
```

## 🎮 Usage Examples

- **"Make this sound like [@Wendys]"** → Sassy social media tone
- **"Explain this to a 5-year-old"** → Child-friendly simplification
- **"Turn this into a LinkedIn post"** → Professional networking style
- **Academic papers → TikTok content**
- **Legal documents → Plain English**
- **Corporate speak → Casual conversation**

## 🎯 Transformation Examples

| Original | Target | Result |
|----------|--------|---------|
| "Theoretical framework indicates..." | Gen-Z Social Media | "Here's why this idea absolutely slaps..." |
| "Liability clause states..." | 5th Grade Level | "You're responsible if you break it" |
| "Synergize deliverables..." | Stand-up Comedy | "Get your team to actually work together" |

## 📁 Project Structure

```
ToneShift-Model/
├── app.py                    # Main Streamlit application
├── prompts.py               # AI prompt engineering
├── requirements.txt         # Dependencies
└── ToneShift-Model_-Knowledge-Bank.pdf  # Tone reference guide
```

## 🧠 How It Works

1. **Input Analysis**: Identifies original tone and target requirements
2. **Style Processing**: Applies linguistic patterns and cultural relevance
3. **Quality Assurance**: Preserves factual accuracy while adapting style
4. **Output Generation**: Delivers transformed text with style reports

## 🔧 Configuration

Create a `.env` file with your Google Gemini API key:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

## 🚀 Deployment

Currently deployed on Streamlit Community Cloud. To deploy your own version:

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Add `GOOGLE_API_KEY` to app secrets
4. Deploy

Alternative platforms: Render, Railway, Heroku

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/name`)
5. Open Pull Request

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/divyanshsharma2003/ToneShift-Model/issues)
- **Email**: divyanshsharma2003@gmail.com

---

**Made with ❤️ by [Divyansh Sharma]([https://github.com/divyanshsharma2003](https://www.linkedin.com/in/divyansh-sharma-b4793026b/))**

*Transform your communication, one tone at a time.*
