# LLM Orchestration – LangChain

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/4380/4380939.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6231/6231228.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/4380/4380939.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/9431/9431523.png" width="80"/></td>
    </tr>
  </table>
</div>

LangChain is a framework for **LLM orchestration**, allowing you to compose prompts, models, chains, tools, and agents into reliable and reusable AI-powered applications.

## Instructions

For the project examples, I set up with Ollama (Local & Free):

- Runs LLMs locally on your machine.
- No API key is required.
- Recommended for learning and experimentation.

>However, you can adapt to use your preferred LLM

## Install a local LLM runtime, such as Ollama

  <img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/blue-ollama.png?ref_type=heads" width="60"/>
  
  Ollama is a free Large Language Model (LLM) with reduced capacity
compared to commercial models, but it works very well for **practice,
studies, and prototypes**.

It can be installed on: 
- Personal computers
- Servers
- On-premise environments

--- 

### 1. Ollama Download

Access the official download page:
https://ollama.com/download

--- 

### 2. Installation by Operating System

#### Linux

Run the following command in the terminal:

``` bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows or macOS

Download the installer directly from the official website and follow the
installation steps.

--- 

### 3. Choosing a Model (LLM)

After installation, browse the model library to select the version that
best fits your use case (text, code, multimodal, etc.):
https://ollama.com/library

When choosing a model, consider: - Model size (1B, 3B, 7B, etc.) - Task
type (text generation, chat, code, etc.) - Hardware and resource usage

--- 

### 4. Downloading the Model (Pull)

Once you have selected a model, download it using the `pull` command.

Example: using **llama 3.2**, a moderate model with options ranging from
**1B to 3B** parameters:

``` bash
ollama pull llama3.2
```

--- 

### 5. Running the Model

After downloading the model, run it with:

``` bash
ollama run llama3.2
```

---

### 6. Important Notes

-   Always ensure the Ollama service is running before using it in a
    project
    
-   In some systems, Ollama may start automatically when the computer
    boots
    
--- 

### 7. Project Dependencies

In your project dependency file (`requirements.txt`, `environment.yml`,
etc.), include the required library to integrate with Ollama.

**For example**, If your project uses **LangChain** and consumes the locally installed
Ollama, add the following dependency:

``` txt
langchain-ollama
```

--- 

### 8. Select Your Model

When configuring your project, import the required libraries and specify the model name:

```python
model_name = "llama3.2"
```
