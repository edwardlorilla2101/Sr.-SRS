import random
import subprocess

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
            print(f"Model {model_name} not found. Pulling the model...")
            pull_result = subprocess.run(
                ["ollama", "pull", model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if pull_result.returncode != 0:
                raise Exception(f"Error pulling model: {pull_result.stderr}")
            print(f"Model {model_name} pulled successfully.")
    except Exception as e:
        raise Exception(f"Error ensuring model availability: {e}")

def generate_random_inputs():
    topics = [
        "Future of Renewable Energy",
        "Impact of AI on Job Markets",
        "Benefits of Meditation",
        "Space Exploration: Challenges and Opportunities",
        "The Rise of Electric Vehicles",
        "Data Privacy in the Digital Age",
        "Climate Change and Its Global Effects",
        "Mental Health Awareness in the Workplace",
        "Blockchain Technology and Its Applications",
        "The Role of Robotics in Modern Industry"
    ]
    styles = ["Researchers", "Data Scientists", "Common People"]
    input_text = random.choice(topics)
    no_words = 1500
    blog_style = random.choice(styles)
    return input_text, no_words, blog_style

def get_ollama_response(input_text, no_words, blog_style):
    prompt = f"""
        Write a blog for {blog_style} job profile about the topic "{input_text}"
        within {no_words} words.
    """
    try:
        ensure_model_available("llama-2-7b")
        result = subprocess.run(
            ["ollama", "run", "llama-2-7b", prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Error: {result.stderr}")
        return result.stdout.strip()
    except Exception as e:
        return f"Error during query: {e}"

if __name__ == "__main__":
    topic, word_count, audience = generate_random_inputs()
    print(f"Random Topic: {topic}")
    print(f"Word Count: {word_count}")
    print(f"Blog Style: {audience}\n")
    blog_content = get_ollama_response(topic, word_count, audience)
    print("Generated Blog Content:\n")
    print(blog_content)
