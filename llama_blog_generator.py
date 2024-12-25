import random
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

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

# Function to get response from LLaMA model
def get_llama_response(input_text, no_words, blog_style):
    # Initialize LLaMA model
    llm = CTransformers(
        model='models/llama-2-7b-chat.ggmlv3.q8_0.bin',
        model_type='llama',
        config={'max_new_tokens': 256, 'temperature': 0.01}
    )
    
    # Prompt template
    template = """
        Write a blog for {blog_style} job profile for a topic {input_text}
        within {no_words} words.
    """
    prompt = PromptTemplate(
        input_variables=["blog_style", "input_text", "no_words"],
        template=template
    )
    
    # Generate response
    response = llm(prompt.format(
        blog_style=blog_style,
        input_text=input_text,
        no_words=no_words
    ))
    return response

# Main script
if __name__ == "__main__":
    topic, word_count, audience = generate_random_inputs()
    print(f"Random Topic: {topic}")
    print(f"Word Count: {word_count}")
    print(f"Blog Style: {audience}\n")
    
    blog_content = get_llama_response(topic, word_count, audience)
    print("Generated Blog Content:\n")
    print(blog_content)
