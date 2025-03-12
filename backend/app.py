from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import datetime
import traceback

from memory_core.vectorization import Vectorizer
from memory_core.recall import find_relevant_memories
from memory_core.consolidation import calculate_consolidation_factor
from storage import SimpleStorage
from llm import LLMInterface

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.debug = True

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "Server is running"}), 200

# Load environment variables first
load_dotenv()

# Check OpenAI API key before starting
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize components
storage = SimpleStorage()
vectorizer = Vectorizer()
llm = LLMInterface()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        print("Received chat request")  # Debug log
        user_message = request.json.get('message', '')
        print(f"Request data: {request.json}")  # Debug request data
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        print(f"Processing message: {user_message}")  # Debug log
        # Get message embedding
        message_vector = vectorizer.get_embedding(user_message)
        print("Got embedding")  # Debug log
        
        # Load existing memories and chat history
        memories = storage.load_memories()
        chat_history = storage.load_chat_history()
        
        # Store user message
        timestamp = datetime.now().timestamp()
        chat_history.append({
            'role': 'user',
            'content': user_message,
            'timestamp': timestamp
        })
        storage.add_chat_message(chat_history[-1])
        
        # Create memory from user message
        memory_id = len(memories)
        new_memory = {
            'id': memory_id,
            'content': user_message,
            'vector': message_vector,
            'created_at': timestamp,
            'last_recalled': timestamp,
            'recall_count': 0,
            'consolidation_factor': 1.0
        }
        storage.add_memory(new_memory)
        
        # Find relevant memories
        relevant_memories = find_relevant_memories(
            query_vector=message_vector,
            memories=memories
        )
        
        # Update recalled memories
        for memory in relevant_memories:
            memory_id = memory['id']
            elapsed_time = timestamp - memory['last_recalled']
            recall_count = memory['recall_count'] + 1
            current_g = memory['consolidation_factor']
            
            new_g = calculate_consolidation_factor(elapsed_time, current_g)
            
            storage.update_memory(memory_id, {
                'recall_count': recall_count,
                'last_recalled': timestamp,
                'consolidation_factor': new_g
            })
        
        # Generate response
        assistant_response = llm.generate_response(
            user_message=user_message,
            relevant_memories=relevant_memories,
            chat_history=chat_history
        )
        
        # Store assistant response
        chat_history.append({
            'role': 'assistant',
            'content': assistant_response,
            'timestamp': timestamp,
            'memories_used': [m['id'] for m in relevant_memories]
        })
        storage.add_chat_message(chat_history[-1])
        
        return jsonify({
            'response': assistant_response,
            'memories_used': relevant_memories
        })
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        print(traceback.format_exc())  # Print full traceback
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    try:
        history = storage.load_chat_history()
        return jsonify(history)
    except Exception as e:
        print(f"Error loading chat history: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
