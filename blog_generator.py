import random
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def ensure_model_available(model_name):
    """Ensure the model is available locally or pull it if missing."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if model_name not in result.stdout:
            print(f"Model {model_name} not found locally. Attempting to pull...")
            pull_result = subprocess.run(
                ["ollama", "pull", model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if pull_result.returncode != 0:
                raise Exception(f"Error pulling model: {pull_result.stderr.strip()}")
            print(f"Model {model_name} pulled successfully.")
        else:
            print(f"Model {model_name} is already available locally.")
    except Exception as e:
        raise Exception(f"Error ensuring model availability: {e}")

def fetch_word_of_the_day():
    """Fetch the Word of the Day from Merriam-Webster."""
    try:
        url = "https://www.merriam-webster.com/word-of-the-day"
        response = subprocess.run(
            ["curl", "-s", "-o", "/tmp/response.html", "-w", "%{http_code}", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if response.stdout.strip() != "200":
            print(f"Failed to fetch Word of the Day. HTTP Status: {response.stdout.strip()}")
            return None
        with open("/tmp/response.html", "r") as file:
            html_content = file.read()
        word = subprocess.run(
            ["grep", "-oP", '(?<=<h2 class="word-header-txt">)[^<]+', "/tmp/response.html"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        ).stdout.strip()
        if word:
            print(f"Fetched Word of the Day: {word}")
            return word
        print("Word of the Day not found in the response.")
        return None
    except Exception as e:
        print(f"Error fetching Word of the Day: {e}")
        return None

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
    no_words = 3000
    blog_style = random.choice(styles)
    return input_text, no_words, blog_style

def get_ollama_response(input_text, no_words, blog_style, word_of_the_day, model_name="llama2:chat"):
    """Generate a blog using Ollama with the provided inputs."""
    prompt = f"""
        Write a blog for {blog_style} job profile about the topic "{input_text}" 
        within {no_words} words. Include the word "{word_of_the_day}" creatively.
    """
    try:
        ensure_model_available(model_name)
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Error running model: {result.stderr.strip()}")
        print("Ollama Response Retrieved Successfully.")
        return result.stdout.strip()
    except Exception as e:
        return f"Error during query: {e}"

def send_email(recipient_email, subject, content):
    """Send the generated blog content via email."""
    try:
        sender_email = "elancelorilla@gmail.com"
        sender_password = "your_password"

        # Set up the MIME message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        # Attach the blog content
        message.attach(MIMEText(content, "plain"))

        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent successfully to {recipient_email}.")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    # Generate random inputs
    topic, word_count, audience = generate_random_inputs()
    word_of_the_day = fetch_word_of_the_day() or "innovation"  # Default if WOTD fetch fails
    
    # Display inputs
    print(f"Random Topic: {topic}")
    print(f"Word Count: {word_count}")
    print(f"Blog Style: {audience}")
    print(f"Word of the Day: {word_of_the_day}\n")
    
    # Generate the blog content
    blog_content = get_ollama_response(topic, word_count, audience, word_of_the_day)
    print("Generated Blog Content:\n")
    print(blog_content)

    # Send the blog content via email
    if "Error" not in blog_content:
        recipient = "edwardlorilla2048.edwardlancelorilla@blogger.com"  # Replace with the actual recipient's email
        send_email(
            recipient_email=recipient,
            subject=f"{topic}",
            content=blog_content
        )
    else:
        print("Blog content generation failed. Email will not be sent.")
