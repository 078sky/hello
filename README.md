# Memory-Enhanced Chat Assistant

A chat assistant with human-like memory capabilities, implementing memory consolidation and recall algorithms inspired by cognitive science research.

## 🧠 Key Features

- **Human-like Memory**: Implements a biologically-inspired memory system
- **Dynamic Memory Consolidation**: Memories become stronger through repeated recall
- **Context-Aware Responses**: Assistant uses relevant past conversations
- **Real-time Memory Visualization**: See which memories influence responses
- **Simple Storage**: File-based storage for easy deployment


## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+   

### Backend Setup 
1. Clone the repository
```bash
git clone https://github.com/078sky/hello.git
cd hello
```

### Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

### Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Set environment variables
```bash
cp .env.example .env
```
Edit `.env` file with your OpenAI API key

### Start the server
```bash
python app.py
```

### Frontend Setup
1. Install dependencies
```bash
cd ..
cd frontend
npm install
```

2. Start the development server
```bash
npm start
```


Visit http://localhost:3000 to use the application.

## 🧪 Core Components

### Memory Core

#### Vectorization
- Converts text to embeddings using OpenAI's API
- Implements caching to reduce API calls
- File: `memory_core/vectorization.py`

#### Memory Consolidation
- Implements the consolidation formula: `g_n = g_{n-1} + (1-e^-t)/(1+e^-t)`
- Strengthens memories through repeated recall
- File: `memory_core/consolidation.py`

#### Memory Recall
- Uses vector similarity for initial memory retrieval
- Applies recall probability based on memory strength
- File: `memory_core/recall.py`

### Storage System
- Simple file-based JSON storage
- Thread-safe operations
- Stores both chat history and memory embeddings
- File: `storage.py`

```

## 🔧 Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_api_key_here
```

### Memory Parameters
- Similarity Threshold: 0.86 (configurable in recall.py)
- Consolidation Rate: Adaptive based on recall frequency
- Vector Dimension: 1536 (OpenAI Ada-002)

