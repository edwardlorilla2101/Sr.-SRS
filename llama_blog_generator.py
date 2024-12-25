def ensure_model_available(model_name):
    """Ensure the model is available locally."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if model_name not in result.stdout:
            print(f"Model {model_name} not found. Attempting to pull the model...")
            pull_result = subprocess.run(
                ["ollama", "pull", model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if pull_result.returncode != 0:
                raise Exception(f"Error pulling model: {pull_result.stderr.strip()}")
            print(f"Model {model_name} pulled successfully.")
    except Exception as e:
        raise Exception(f"Error ensuring model availability: {e}")

def get_ollama_response(input_text, no_words, blog_style):
    prompt = f"""
        Write a blog for {blog_style} job profile about the topic "{input_text}"
        within {no_words} words.
    """
    try:
        ensure_model_available("llama-2-7b")  # Adjust the model name if necessary
        result = subprocess.run(
            ["ollama", "run", "llama-2-7b", prompt],  # Adjust command if needed
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Error: {result.stderr.strip()}")
        return result.stdout.strip()
    except Exception as e:
        return f"Error during query: {e}"
