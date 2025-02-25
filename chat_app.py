import streamlit as st
from pinecone.grpc import PineconeGRPC as Pinecone
from sentence_transformers import SentenceTransformer
from google import genai

# Set page configuration
st.set_page_config(page_title="RAG Chatbot Demo", layout="wide")

# Initialize Pinecone
pc = Pinecone(api_key='pcsk_49H1KG_LWe5PjAUyYUQzsosFHuZMSqQhVRdKmXVVkncZXgfztXKqhPnVtndPD8SnTZ277F')
index = pc.Index("sunway-demo")  # Make sure this matches your index name in the notebook

# Initialize Google Genai client
client = genai.Client(api_key="AIzaSyBU6KkDTG6-71FC2raqVswQgotX_rIGRkg")

# Load the embedding model
@st.cache_resource
def load_model():
    return SentenceTransformer('all-mpnet-base-v2')

model = load_model()

def generate_embedding(text):
    """Generate embeddings for text using SentenceTransformer"""
    return model.encode(text).tolist()

def query_pinecone(query_text, top_k=5):
    """Query Pinecone index for similar documents"""
    query_embedding = generate_embedding(query_text)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return results

def generate_response(prompt, context):
    """Generate response using Google's Gemini model"""
    # client = genai.GenerativeModel(model_name="gemini-2.0-flash")
    response = client.models.generate_content(contents = f"Context: {context}\n\nPrompt: {prompt}", model = "gemini-2.0-flash")
    return response.text

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat header
st.title("📚 RAG Chatbot Demo")
st.markdown("Ask questions about the Transformer paper!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("What would you like to know about the Transformer architecture?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Show a spinner while processing
        with st.spinner("Thinking..."):
            # Retrieve similar chunks from Pinecone
            results = query_pinecone(prompt)
            
            # Format the context from retrieved documents
            context = ""
            for match in results['matches']:
                context += f"{match['metadata']['text']}\n\n"
            
            # Generate a response using the Gemini model
            response_text = generate_response(prompt, context)
            
            # Display the response
            message_placeholder.markdown(response_text)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})

# Add info about the system
with st.sidebar:
    st.title("About")
    st.markdown("""
    This is a RAG (Retrieval-Augmented Generation) chatbot demo that:
    
    1. Takes your question
    2. Finds relevant passages from the Transformer paper
    3. Uses Google's Gemini model to generate a response based on the retrieved context
    
    The system uses:
    - Pinecone for vector storage
    - SentenceTransformer for embeddings
    - Google Gemini for text generation
    """)
