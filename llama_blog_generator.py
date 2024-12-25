import random
from ollama import Ollama

def generate_random_inputs():
    # List of random topics
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
    
    # List of blog styles
    styles = ["Researchers", "Data Scientists", "Common People"]
    
    # Generate random values
    input_text = random.choice(topics)
    no_words = 1500  # Fixed word count
    blog_style = random.choice(styles)
    
    return input_text, no_words, blog_style

# Function to get response from Ollama
def get_ollama_response(input_text, no_words, blog_style):
    # Initialize Ollama
    model = Ollama(model_name="llama-2-7b")  # Adjust model name if necessary
    
    # Prompt template
    prompt = f"""
        Write a blog for {blog_style} job profile about the topic "{input_text}"
        within {no_words} words.
    """
    
    # Generate response
    response = model.query(prompt)
    return response["response"]  # Extract the response text

# Main script
if __name__ == "__main__":
    topic, word_count, audience = generate_random_inputs()
    print(f"Random Topic: {topic}")
    print(f"Word Count: {word_count}")
    print(f"Blog Style: {audience}\n")
    
    blog_content = get_ollama_response(topic, word_count, audience)
    print("Generated Blog Content:\n")
    print(blog_content)
