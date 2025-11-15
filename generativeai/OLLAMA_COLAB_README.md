# Ollama on Google Colab with Cloudflare Tunnel

A complete solution for running Ollama (Large Language Models) on Google Colab with public access via Cloudflare Tunnel.

## 🌟 Features

- **Easy Setup**: One-click installation of Ollama on Google Colab
- **Public Access**: Cloudflare Tunnel provides free public URL access
- **Multiple Models**: Support for Llama 3, Mistral, Code Llama, and more
- **Interactive Chat**: Built-in chat interface for testing
- **API Ready**: Full REST API access for integration
- **Free to Use**: Runs on Google Colab's free tier

## 🚀 Quick Start

### Step 1: Open in Google Colab

1. Upload `ollama_colab_setup.ipynb` to Google Colab
2. Or click: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

### Step 2: Enable GPU (Recommended)

1. Click `Runtime` → `Change runtime type`
2. Select `GPU` as Hardware accelerator
3. Choose `T4 GPU` (free tier)
4. Click `Save`

### Step 3: Run the Notebook

Execute the cells in order:

1. **System Check** - Verify resources available
2. **Install Ollama** - Download and install Ollama
3. **Start Server** - Launch Ollama service
4. **Install Cloudflare** - Set up tunnel software
5. **Start Tunnel** - Get your public URL
6. **Download Model** - Pull your chosen model
7. **Test & Chat** - Interact with the model

## 📦 What Gets Installed

### Software Components

- **Ollama**: LLM runtime and server
- **Cloudflared**: Cloudflare Tunnel client
- **Python packages**: requests, json (standard library)

### Models (Your Choice)

You can download any Ollama-compatible model:

| Model | Size | RAM Required | Best For |
|-------|------|--------------|----------|
| llama3:8b | ~4.7GB | 8GB+ | General chat, fast responses |
| llama3:13b | ~7.4GB | 16GB+ | Better quality, slower |
| mistral:7b | ~4.1GB | 8GB+ | Efficient, good quality |
| codellama:13b | ~7.4GB | 16GB+ | Code generation |
| qwen2.5:14b | ~9GB | 16GB+ | Multilingual |

## 🔧 Configuration

### Changing the Model

In cell 6 (Download Models), modify:

```python
MODEL_NAME = "llama3:13b"  # Change this to your preferred model
```

Available options:
- `llama3:8b`
- `llama3:13b`
- `mistral:7b`
- `codellama:13b`
- `qwen2.5:14b`

### Memory Considerations

**Free Colab Resources:**
- Standard: 12-13GB RAM
- With GPU: Additional GPU memory
- Disk: 100GB+ available

**Recommendations:**
- **8GB RAM or less**: Use 7B-8B models
- **16GB RAM**: Can use 13B models
- **32GB+ RAM**: Can use larger models

## 🌐 Using the Public URL

After running the tunnel cell, you'll get a URL like:
```
https://random-name.trycloudflare.com
```

### API Examples

#### Python

```python
import requests
import json

url = "https://your-url.trycloudflare.com/api/chat"
payload = {
    "model": "llama3:13b",
    "messages": [
        {"role": "user", "content": "Hello! How are you?"}
    ],
    "stream": False
}

response = requests.post(url, json=payload)
print(response.json()['message']['content'])
```

#### cURL

```bash
curl https://your-url.trycloudflare.com/api/chat -d '{
  "model": "llama3:13b",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}'
```

#### JavaScript (Node.js)

```javascript
const fetch = require('node-fetch');

async function chat(message) {
  const response = await fetch('https://your-url.trycloudflare.com/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'llama3:13b',
      messages: [{ role: 'user', content: message }],
      stream: false
    })
  });

  const data = await response.json();
  return data.message.content;
}

chat("Hello!").then(console.log);
```

## 📚 API Endpoints

### Chat Completion

```
POST /api/chat
```

**Body:**
```json
{
  "model": "llama3:13b",
  "messages": [
    {"role": "user", "content": "Your message"}
  ],
  "stream": false
}
```

### Generate Completion

```
POST /api/generate
```

**Body:**
```json
{
  "model": "llama3:13b",
  "prompt": "Your prompt here",
  "stream": false
}
```

### List Models

```
GET /api/tags
```

### Pull Model

```
POST /api/pull
```

**Body:**
```json
{
  "name": "llama3:13b"
}
```

## ⚠️ Important Notes

### Session Limitations

- **Free Colab**: ~12 hours max runtime
- **Colab Pro**: ~24 hours max runtime
- **Tunnel URL**: Changes each time you restart

### Security Considerations

- Public URL is accessible to **anyone**
- Don't share sensitive data through the model
- Consider implementing authentication for production use
- Monitor usage to prevent abuse

### Resource Management

- Models consume significant disk space
- Download times: 10-30 minutes depending on model size
- First run downloads models; subsequent runs use cache
- Cache location: `~/.cache/huggingface/`

## 🐛 Troubleshooting

### Common Issues

#### 1. Out of Memory Error

**Problem**: `CUDA out of memory` or `Killed`

**Solutions:**
- Use a smaller model (8B instead of 13B)
- Restart runtime and try again
- Enable High-RAM runtime (Colab Pro)

#### 2. Model Download Fails

**Problem**: Timeout or network error

**Solutions:**
- Check internet connection
- Try downloading again
- Use a smaller model first
- Check Colab's connection status

#### 3. Tunnel Not Working

**Problem**: Can't access public URL

**Solutions:**
- Restart the tunnel cell
- Check if cloudflared process is running
- Verify Ollama server is active
- Try accessing local URL first

#### 4. Slow Responses

**Problem**: Model takes too long to respond

**Solutions:**
- Enable GPU acceleration
- Use a smaller model
- Reduce response length parameters
- Check if other processes are using resources

### Verification Commands

Run these in a code cell to check status:

```python
# Check Ollama server
!curl http://localhost:11434/api/tags

# Check running processes
!ps aux | grep ollama

# Check GPU status
!nvidia-smi

# Check disk space
!df -h

# Check memory
!free -h
```

## 🎯 Use Cases

### Development & Testing

- Test LLM integrations locally
- Prototype AI applications
- Experiment with different models
- API development and testing

### Education & Learning

- Learn about LLMs and APIs
- Understand model behavior
- Practice prompt engineering
- Study model comparisons

### Personal Projects

- Build chatbots
- Create content generators
- Develop code assistants
- Text analysis tools

## 📖 Additional Resources

### Documentation

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Cloudflare Tunnel Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps)
- [Google Colab Guide](https://colab.research.google.com/)

### Model Libraries

- [Ollama Model Library](https://ollama.com/library)
- [Hugging Face Models](https://huggingface.co/models)

### Community

- [Ollama GitHub](https://github.com/ollama/ollama)
- [Ollama Discord](https://discord.gg/ollama)

## 🤝 Contributing

Found an issue or want to improve the notebook? Contributions welcome!

1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## ⚡ Tips & Best Practices

### Optimize Performance

1. **Use GPU**: Always enable GPU for better performance
2. **Right-size Models**: Choose model based on available RAM
3. **Cache Models**: Download once, reuse in future sessions
4. **Stream Responses**: Use `stream: true` for better UX

### Manage Costs

1. **Free Tier**: Use Google Colab free tier for testing
2. **Colab Pro**: Consider for longer sessions ($10/month)
3. **Model Size**: Smaller models = less resource usage
4. **Session Management**: Stop runtime when not in use

### Production Considerations

1. **Authentication**: Add API keys for public deployment
2. **Rate Limiting**: Implement to prevent abuse
3. **Monitoring**: Track usage and performance
4. **Backups**: Save important configurations
5. **Scaling**: Consider dedicated hosting for production

## 🔄 Updates & Maintenance

The notebook is regularly updated to include:

- Latest Ollama versions
- New model support
- Performance improvements
- Bug fixes
- Security patches

Check back regularly for updates!

## 💡 FAQ

**Q: How long does setup take?**
A: Initial setup: 5-10 minutes. Model download: 10-30 minutes.

**Q: Can I use this for production?**
A: Not recommended. Use dedicated hosting for production workloads.

**Q: Is my data private?**
A: Models run locally in your Colab session. However, the public URL is accessible to anyone.

**Q: Can I use multiple models simultaneously?**
A: Yes! Download multiple models and switch between them.

**Q: Does this cost money?**
A: Free on Google Colab free tier. Colab Pro offers better resources for $10/month.

**Q: How do I save my session?**
A: Models are cached automatically. Code and configurations need to be saved manually.

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) - Amazing LLM runtime
- [Cloudflare](https://www.cloudflare.com/) - Free tunnel service
- [Google Colab](https://colab.research.google.com/) - Free compute resources
- The open-source AI community

---

**Happy Coding! 🚀**

For questions or support, please open an issue on GitHub.
