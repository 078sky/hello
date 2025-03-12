# Create root directory
mkdir memory-agent-mvp
cd memory-agent-mvp

# Create backend structure
mkdir -p backend/memory_core backend/data
touch backend/memory_core/__init__.py
touch backend/requirements.txt
touch backend/app.py
touch backend/llm.py
touch backend/storage.py

# Create frontend structure
mkdir -p frontend/src/components
touch frontend/package.json
touch frontend/src/App.js
touch frontend/src/App.css
touch frontend/src/components/ChatApp.jsx
touch frontend/src/components/ChatApp.css
touch frontend/src/components/MessageBubble.jsx
touch frontend/src/components/MessageBubble.css 