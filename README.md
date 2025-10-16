# SkillPath AI

**Personalized 7-Day Learning Path Generator with RAG Integration**

SkillPath AI is an intelligent learning companion that generates personalized, structured 7-day learning plans for any topic. Powered by Google's Gemini AI and enhanced with real-time resource retrieval using Serper API, it provides a comprehensive learning experience with curated resources from YouTube, articles, blogs, and documentation.

## ✨ Features

### 🧠 **AI-Powered Learning Plans**
- **Intelligent Curriculum Design**: Uses Google Gemini to create structured 7-day learning paths
- **Topic Flexibility**: Generate plans for any subject (programming, data science, design, etc.)
- **Progressive Learning**: Each day builds upon previous knowledge with logical progression

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI        │    │   External APIs │
│   Frontend      │◄──►│   Backend        │◄──►│                 │
│                 │    │                  │    │ • Gemini AI     │
│ • User Interface│    │ • Plan Generation│    │ • Serper API    │
│ • Navigation    │    │ • Resource Merge │    │                 │
│ • Display Logic │    │ • Error Handling │    └─────────────────┘
└─────────────────┘    └──────────────────┘
```

### **Core Components:**
- **Frontend** (`app.py`): Streamlit interface with session management
- **Backend** (`backend/main.py`): FastAPI server with REST endpoints
- **LLM Service** (`services/llm_client.py`): Gemini AI integration
- **RAG Service** (`services/serper_client.py`): Real-time resource retrieval

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API Key
- Serper API Key (optional, for enhanced resources)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/deepanshu-iitm/skillpathAI.git
   cd skillpathAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   ```

4. **Start the backend server**
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

5. **Launch the frontend**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 🎯 How to Use

1. **Enter Your Learning Topic**
   - Type any subject you want to learn (e.g., "Python for Data Analysis", "React Development", "Machine Learning")

2. **Generate Your Plan**
   - Click "Generate 7-Day Learning Plan"
   - Wait for AI to create your personalized curriculum

3. **Explore the Overview**
   - Review all 7 days with key topics and 3 curated resources each
   - Get a high-level understanding of your learning journey

4. **Dive Deep into Any Day**
   - Click "Start Learning - Day X" for comprehensive details
   - Access step-by-step guides, challenges, and extensive resources
   - Follow structured learning objectives



















