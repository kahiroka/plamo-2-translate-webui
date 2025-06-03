# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a web-based interface for the PLaMo-2 Translate model, a 9.53B parameter model developed by Preferred Networks for English-Japanese translation.

## Model Information
- **Model**: pfnet/plamo-2-translate (HuggingFace)
- **Size**: 9.53 billion parameters
- **Purpose**: English-Japanese translation
- **Max tokens**: 2000
- **License**: PLaMo community license (commercial use requires contacting Preferred Networks)

## Development Setup
When implementing this project:
1. Create a Python virtual environment
2. Install vllm: `pip install vllm`
3. Choose a web framework (Gradio or Streamlit recommended for ML interfaces)
4. Ensure GPU availability with substantial memory

## Implementation Requirements
The web UI should implement the PLaMo-2 translation format:
```python
prompt = r'''<|plamo:op|>dataset
translation
<|plamo:op|>input lang=English
[User's English text here]
<|plamo:op|>output lang=Japanese
'''
```

Key vllm parameters:
- `trust_remote_code=True`
- `max_model_len=2000`
- `temperature=0` for deterministic translation
- Stop token: `<|plamo:op|>`

## Architecture Considerations
- The model requires GPU memory for inference
- Consider implementing request queuing for multiple users
- Add input validation (max 2000 tokens)
- Support both English→Japanese and Japanese→English translation directions