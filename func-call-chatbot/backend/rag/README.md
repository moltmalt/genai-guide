# RAG (Retrieval-Augmented Generation) System

This directory contains the RAG system implementation for the T-shirt chatbot, which provides enhanced knowledge retrieval capabilities using vector embeddings stored in JSON files.

## Overview

The RAG system enhances the chatbot's ability to provide detailed, accurate information about:
- Product descriptions and details
- Frequently Asked Questions (FAQ)
- Store policies (shipping, returns, privacy)

## Architecture

### Components

1. **`embedding_generator.py`** - Handles OpenAI embedding generation
2. **`vector_store.py`** - Manages vector storage and similarity search
3. **`knowledge_base.py`** - Contains structured knowledge content
4. **`rag_function.py`** - Main RAG system integration
5. **`__init__.py`** - Module initialization

### Data Structure

Vectors are stored in JSON files in the `data/knowledge_base/` directory:
- `product_vectors.json` - Product descriptions and details
- `faq_vectors.json` - FAQ content
- `policy_vectors.json` - Policy information

## Usage

### Integration with Chatbot

The RAG system is automatically integrated into the chatbot through the `search_knowledge_base` function call. The chatbot will automatically use RAG when users ask about:

- Product information and details
- Shipping and delivery questions
- Return and exchange policies
- Sizing and fit questions
- General store information

### Function Call

```python

search_knowledge_base(
    query="What are your shipping options?",
    top_k=3,
    content_type="faq_vectors"  
)
```

## Setup

1. **Install Dependencies**
   ```bash
   pip install numpy openai python-dotenv
   ```

2. **Set Environment Variables**
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **Build Knowledge Base** (First time only)
   ```bash
   cd backend
   python scripts/build_knowledge_base.py
   ```

4. **Test the System**
   ```bash
   python test_rag.py
   ```

## Features

### Smart Content Detection
- Automatically detects query type (product, FAQ, policy)
- Routes to appropriate knowledge base sections
- Combines multiple sources when relevant

### Vector Storage
- Uses JSON files (no database required)
- Efficient cosine similarity search
- Supports multiple content types

### Enhanced Responses
- Formatted, readable responses
- Context-aware information
- Relevant metadata included

## Content Types

### Products
- Detailed product descriptions
- Available sizes and colors
- Material and care information
- Category and tag information

### FAQ
- Common customer questions
- Detailed answers
- Categorized by topic

### Policies
- Shipping information
- Return and refund policies
- Privacy and security policies

## Performance

- Fast similarity search using numpy
- Efficient vector storage in JSON
- Automatic caching of loaded vectors
- Batch processing for initial setup

## Extending the System

### Adding New Content

1. Update the content in `knowledge_base.py`
2. Run the build script to regenerate vectors
3. The system will automatically include new content

### Adding New Content Types

1. Create new content loading method in `KnowledgeBase`
2. Add vector creation method
3. Update the RAG system to handle new type
4. Regenerate vectors

## Troubleshooting

### Common Issues

1. **Missing OpenAI API Key**
   - Ensure `OPENAI_API_KEY` is set in environment
   - Check `.env` file configuration

2. **Vector Files Not Found**
   - Run `python scripts/build_knowledge_base.py`
   - Check `data/knowledge_base/` directory exists

3. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python path includes backend directory

### Testing

Use the test script to verify functionality:
```bash
python test_rag.py
```

This will test various query types and show the system's responses. 