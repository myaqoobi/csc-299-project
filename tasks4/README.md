# Task 4: AI-Powered Task Summarization

**What is this?**  
A standalone experiment that uses OpenAI's Chat Completions API to automatically summarize long task descriptions into short, actionable phrases.

## 🎯 How It Works

### The Flow:
```
Long Paragraph Description → OpenAI API → Short Phrase Summary
```

### Example:
- **Input (paragraph):**
  ```
  "I need to complete my computer science assignment for CSC299. 
  This involves creating a task management system with Python, 
  writing comprehensive tests using pytest, and documenting 
  everything in a README file. The deadline is next week..."
  ```

- **Output (short phrase):**
  ```
  "Complete CSC299 Python assignment with tests"
  ```

## 🚀 Setup

1. **Get an OpenAI API Key:**
   - Go to https://platform.openai.com/api-keys
   - Create a new API key
   - Copy the key

2. **Set the API Key:**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

3. **Run the application:**
   ```bash
   uv run tasks4
   ```

## 📋 What It Does

1. **Takes paragraph-length descriptions** - Long, detailed task descriptions
2. **Sends to OpenAI API** - Uses GPT-3.5-turbo to analyze the text
3. **Gets short summaries** - Returns concise 3-8 word phrases
4. **Processes multiple descriptions** - Loops through all samples independently

## 🔧 Technical Details

- **API:** OpenAI Chat Completions API
- **Model:** `gpt-3.5-turbo` (ChatGPT-3.5-mini equivalent)
- **Function:** `summarize_task()` - Handles the API call
- **Main Loop:** Processes each description independently
- **Sample Data:** 2 paragraph-length task descriptions included

## 📝 Sample Descriptions

The code includes 2 sample paragraph descriptions:
1. A computer science assignment task
2. A job interview preparation task

You can add more by editing the `sample_descriptions` list in `main()`.

## ⚠️ Important Notes

- **API Key Required:** You must set `OPENAI_API_KEY` environment variable
- **API Costs:** Using OpenAI API may incur small costs (check OpenAI pricing)
- **Standalone:** This is separate from tasks1-3 (no task manager code copied)

## 🎓 Assignment Requirements Met

✅ Created tasks4 directory with `uv`  
✅ Standalone experiment (no PKMS/task software copied)  
✅ Uses OpenAI Chat Completions API  
✅ Summarizes paragraph descriptions to short phrases  
✅ Loop processes multiple descriptions independently  
✅ Includes at least 2 sample paragraph descriptions  
✅ Runnable with `uv run tasks4`



