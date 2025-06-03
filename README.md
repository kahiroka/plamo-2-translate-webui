# plamo-2-translate-webui
PLaMo Translation Model with Web UI

A web-based interface for the PLaMo-2 Translate model, providing English-Japanese translation capabilities through an easy-to-use Gradio interface.

## Features

- 🌐 Web-based translation interface using Gradio
- 🔄 Bidirectional translation (English ↔ Japanese)
- 🚀 Powered by PLaMo-2 Translate (9.53B parameters)
- 💾 GPU-accelerated inference with vLLM
- 🎯 Zero-temperature translation for consistent results

## Requirements

- Python 3.8+
- CUDA-capable GPU with sufficient memory (~20GB+ recommended)
- NVIDIA drivers and CUDA toolkit

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/plamo-2-translate-webui.git
cd plamo-2-translate-webui
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the web UI:
```bash
python app.py
```

2. Optional arguments:
```bash
# Create a public shareable link
python app.py --share

# Run on a specific port
python app.py --port 8080
```

3. Open your browser and navigate to `http://localhost:7860`

4. Click "Load Model" to initialize the PLaMo-2 model (this may take a few minutes)

5. Enter text to translate and click "Translate"

## Model Information

- **Model**: [pfnet/plamo-2-translate](https://huggingface.co/pfnet/plamo-2-translate)
- **Parameters**: 9.53 billion
- **License**: PLaMo community license (commercial use requires contacting Preferred Networks)
- **Max tokens**: 2000

## Tips for Best Results

- Keep translations under ~500 words for optimal performance
- The model is specifically trained for English-Japanese translation
- First model load will download ~20GB of model weights
- Subsequent loads will be faster using cached weights

## Project Structure

```
plamo-2-translate-webui/
├── app.py              # Main application entry point
├── src/
│   ├── translator.py   # PLaMo-2 translation service
│   └── web_ui.py       # Gradio interface
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Troubleshooting

- **CUDA out of memory**: The model requires significant GPU memory. Try using a GPU with at least 24GB VRAM.
- **Model loading fails**: Ensure you have proper internet connection for downloading model weights.
- **Slow performance**: Translation speed depends on GPU performance and text length.

## Acknowledgments

- PLaMo-2 model by Preferred Networks
- Built with [Gradio](https://gradio.app/) and [vLLM](https://github.com/vllm-project/vllm)
