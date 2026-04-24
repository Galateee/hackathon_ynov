#!/usr/bin/env python3
"""
TechCorp AI Chat - Backend Flask API Gateway
Multi-mode backend: supports Local, Ollama, and Triton inference
"""

import os
import json
import torch
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
INFERENCE_MODE = os.getenv('INFERENCE_MODE', 'local').lower()  # local, ollama, or triton
INFERENCE_SERVER = os.getenv('INFERENCE_SERVER', 'http://localhost:11434')
MODEL_NAME = os.getenv('MODEL_NAME', 'phi3.5-financial')
MODEL_PATH = os.getenv('MODEL_PATH', '../models/phi3_financial')
BASE_MODEL_NAME = os.getenv('BASE_MODEL_NAME', 'microsoft/Phi-3-mini-4k-instruct')
BACKEND_PORT = int(os.getenv('BACKEND_PORT', 5000))
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 60))  # Default to 60 seconds

# In-memory conversation history (replace with database in production)
conversation_history = []

# Global models for local inference
local_tokenizer = None
local_model = None
local_model_loaded = False

def initialize_local_model():
    """Initialize local model for inference"""
    global local_tokenizer, local_model, local_model_loaded
    
    if local_model_loaded:
        return True
    
    try:
        print("🤖 Initializing local Phi-3.5 model...")
        
        # Load tokenizer
        print("📝 Loading tokenizer...")
        local_tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME, trust_remote_code=True)
        if local_tokenizer.pad_token is None:
            local_tokenizer.pad_token = local_tokenizer.eos_token
        
        # Setup quantization for GPU if available
        quantization_config = None
        if torch.cuda.is_available():
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )
            print("🔧 4-bit quantization enabled (GPU available)")
        else:
            print("💻 Running in CPU mode")
        
        # Load base model
        print("🧠 Loading base model...")
        model_kwargs = {
            "torch_dtype": torch.float16 if torch.cuda.is_available() else torch.float32,
            "trust_remote_code": True,
            "low_cpu_mem_usage": True,
        }
        
        if quantization_config:
            model_kwargs["quantization_config"] = quantization_config
            model_kwargs["device_map"] = "auto"
        
        local_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_NAME,
            **model_kwargs
        )
        
        # Move to GPU if not using quantization
        if not quantization_config and torch.cuda.is_available():
            local_model = local_model.cuda()
        
        # Try to load fine-tuned adapter if available
        if os.path.exists(MODEL_PATH):
            print(f"🔧 Loading fine-tuned adapter from {MODEL_PATH}...")
            try:
                local_model = PeftModel.from_pretrained(local_model, MODEL_PATH)
                print("✅ Fine-tuned adapter loaded")
            except Exception as e:
                print(f"⚠️  Could not load fine-tuned adapter: {e}")
                print("✅ Using base model instead")
        
        print("✅ Local model initialized!")
        local_model_loaded = True
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize local model: {e}")
        return False

def check_server_health():
    """Check if inference server is running"""
    if INFERENCE_MODE == 'local':
        return local_model_loaded
    
    try:
        if INFERENCE_MODE == 'triton':
            # Triton health check endpoint
            response = requests.get(f"{INFERENCE_SERVER}/v2/health/ready", timeout=2)
        elif INFERENCE_MODE == 'ollama':
            # Ollama health check
            response = requests.get(f"{INFERENCE_SERVER}/api/tags", timeout=2)
        else:
            return False
        return response.status_code == 200
    except:
        return False

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get connection status to inference server"""
    is_healthy = check_server_health()
    
    status_msg = {
        'local': '🖥️ Local Model',
        'ollama': '🐪 Ollama Server',
        'triton': '🔷 Triton Server'
    }
    
    return jsonify({
        "connected": is_healthy,
        "mode": INFERENCE_MODE,
        "server": INFERENCE_SERVER if INFERENCE_MODE != 'local' else 'Local',
        "model": MODEL_NAME,
        "backend": status_msg.get(INFERENCE_MODE, 'Unknown'),
        "status": "✅ Connected" if is_healthy else "❌ Disconnected"
    }), 200 if is_healthy else 503

@app.route('/api/chat', methods=['POST'])
def chat():
    """Send message to AI model and get response"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Empty message"}), 400
        
        # Add user message to history
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response based on mode
        if INFERENCE_MODE == 'local':
            response = call_local_model(user_message)
        elif INFERENCE_MODE == 'triton':
            response = call_triton_api(user_message)
        elif INFERENCE_MODE == 'ollama':
            response = call_ollama_api(user_message)
        else:
            response = None
        
        if response is None:
            return jsonify({"error": "Failed to get response from model"}), 500
        
        # Add assistant response to history
        conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return jsonify({
            "reply": response,
            "history": conversation_history,
            "status": "connected",
            "mode": INFERENCE_MODE
        }), 200
        
    except Exception as e:
        print(f"❌ Error in /api/chat: {str(e)}")
        return jsonify({"error": str(e)}), 500

def call_local_model(message, max_tokens=150):
    """Call local model for response"""
    try:
        if not local_model_loaded:
            print("❌ Local model not initialized")
            return None
        
        # Format input
        formatted_input = f"<|user|>\n{message}<|end|>\n<|assistant|>\n"
        
        # Tokenize
        inputs = local_tokenizer(
            formatted_input,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        
        # Move to device
        if torch.cuda.is_available() and next(local_model.parameters()).is_cuda:
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        # Generate response
        local_model.eval()
        with torch.no_grad():
            outputs = local_model.generate(
                input_ids=inputs['input_ids'],
                attention_mask=inputs.get('attention_mask'),
                max_new_tokens=max_tokens,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=local_tokenizer.eos_token_id,
                eos_token_id=local_tokenizer.eos_token_id,
                use_cache=False,
            )
        
        # Decode response
        input_length = inputs['input_ids'].shape[1]
        new_tokens = outputs[0][input_length:]
        response = local_tokenizer.decode(new_tokens, skip_special_tokens=True)
        
        # Clean up
        response = response.strip()
        if response.endswith("<|end|>"):
            response = response[:-7].strip()
        
        return response if response else "I'm not sure how to respond to that."
        
    except Exception as e:
        print(f"❌ Local model error: {str(e)}")
        return None

def call_ollama_api(message):
    """Call Ollama API for response"""
    try:
        response = requests.post(
            f"{INFERENCE_SERVER}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": message,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.9,
            },
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        result = response.json()
        return result.get('response', 'No response generated')
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama API error: {str(e)}")
        return None

def call_triton_api(message):
    """Call Triton Inference Server API for response"""
    try:
        response = requests.post(
            f"{INFERENCE_SERVER}/v2/models/{MODEL_NAME}/infer",
            json={
                "inputs": [
                    {
                        "name": "text_input",
                        "shape": [1],
                        "datatype": "BYTES",
                        "data": [message]
                    }
                ]
            },
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        result = response.json()
        # Extract response from Triton output
        if 'outputs' in result and len(result['outputs']) > 0:
            output_data = result['outputs'][0]['data']
            if isinstance(output_data, list) and len(output_data) > 0:
                return output_data[0]
        return 'No response generated'
    except requests.exceptions.RequestException as e:
        print(f"❌ Triton API error: {str(e)}")
        return None

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get full conversation history"""
    return jsonify({"history": conversation_history}), 200

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({"message": "History cleared"}), 200

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "mode": INFERENCE_MODE}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    mode_info = {
        'local': '🖥️  Local Model (GPU/CPU optimized)',
        'ollama': '🐪 Ollama Server Gateway',
        'triton': '🔷 Triton Inference Server Gateway'
    }
    
    print(f"""
    🚀 TechCorp AI Chat Backend
    📊 Mode: {mode_info.get(INFERENCE_MODE, 'Unknown')}
    """)
    
    # Initialize local model if using local mode
    if INFERENCE_MODE == 'local':
        print("⏳ Loading model (this may take 1-2 minutes on first start)...")
        if not initialize_local_model():
            print("⚠️  Failed to load local model - API will not respond")
    else:
        print(f"📡 Server: {INFERENCE_SERVER}")
        print(f"🤖 Model: {MODEL_NAME}")
    
    print(f"🌐 Backend running on http://localhost:{BACKEND_PORT}")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, port=BACKEND_PORT, host='0.0.0.0')
