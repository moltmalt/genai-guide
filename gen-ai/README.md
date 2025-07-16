# Gen AI Internship Project

Welcome to my Gen AI Internship Project! This repository documents my work and learning experience during my internship, where I built a full-stack t-shirt ordering system powered by FastAPI and React, with a focus on integrating generative AI features.

## 🚀 Project Overview
This project is a t-shirt e-commerce platform with a built-in AI chat assistant. Users can browse products, manage their cart and orders, and interact with an AI assistant for help and recommendations. The backend is built with FastAPI, and the frontend uses React and TypeScript.

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI
- **Frontend:** React, TypeScript, Vite
- **Data:** JSON mock database
- **AI Integration:** OpenAI API (for chatbot)

## 📁 Folder Structure
```
gen-ai/
  func-call-chatbot/
    backend/
      main.py           # FastAPI app entry point
      func.py           # Business logic and data operations
      models/           # Business logic classes
      routers/          # API endpoints (FastAPI routers)
      schemas/          # Pydantic models (request/response schemas)
    frontend/
      src/              # React components, styles, and assets
    mock-db/            # JSON files for products, cart, and orders
```

## ✨ Main Features
- Product catalog with stock and variant management
- Shopping cart and order placement
- Real-time AI chat assistant for user support
- Robust error handling and modular backend structure
- Clean, modern frontend UI

## 📚 What I Learned & Contributed
- **API Design:** Learned to structure a FastAPI backend using routers, schemas, and modular code.
- **Frontend Integration:** Built a responsive React UI and connected it to the backend API.
- **AI Integration:** Integrated OpenAI's API to create a helpful chatbot assistant.
- **Error Handling:** Implemented centralized error handling for a robust API.
- **Best Practices:** Used docstrings, clear commit messages, and professional project organization.
- **Team Feedback:** Incorporated feedback from my internship adviser to refactor and improve code quality.

## 📝 How to Run
1. **Backend:**
   - Navigate to `func-call-chatbot/backend/`
   - Install dependencies: `pip install -r requirements.txt`
   - Run: `uvicorn main:app --reload`
2. **Frontend:**
   - Navigate to `func-call-chatbot/frontend/`
   - Install dependencies: `npm install`
   - Run: `npm run dev`

## 🙋 About Me
This project was completed as part of my Gen AI internship. It reflects my growth as a developer and my ability to build real-world applications with modern tools and AI integration.

Feel free to explore the code, try out the app, and reach out if you have any questions! 