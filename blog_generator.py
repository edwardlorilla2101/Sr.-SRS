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
        # Technology Topics
        "Advancements in Quantum Computing",
        "Cybersecurity Trends in 2024",
        "The Role of Blockchain in Government Systems",
        "The Future of Self-Driving Cars",
        "How AI is Transforming Video Games",
        "Ethical Concerns in Facial Recognition Technology",
        "The Rise of Open Source in Artificial Intelligence",
        "How 5G Technology Impacts Rural Connectivity",
        "The History and Evolution of Cloud Computing",
        "Renewable Energy Storage Innovations",
        "The Role of Big Data in Fighting Climate Change",
        "How Augmented Reality is Redefining Travel",
        "Understanding the Metaverse: Beyond Gaming",
        "Ethical Dilemmas in Biometric Surveillance",
        "Space Mining: Is it Feasible?",
        "Robotics in Everyday Life",
        "The Evolution of Smart Cities",
        "AI in Customer Service: Boon or Bane?",
        "Data Science Trends Shaping the Future",
        "The Impact of IoT on Healthcare Delivery",
    
        # Health Topics
        "The Science Behind Sleep Cycles",
        "How Mental Health Awareness is Changing Society",
        "The Role of Technology in Elderly Care",
        "Preventing Chronic Diseases Through Lifestyle Changes",
        "Exploring the Benefits of Telemedicine",
        "How AI is Transforming Cancer Detection",
        "Genetic Engineering in Modern Medicine",
        "The Role of Gut Health in Mental Wellbeing",
        "Understanding the Rise of Anti-Microbial Resistance",
        "Fitness Trends in 2024",
        "The Future of Preventive Healthcare",
        "How Wearable Devices Revolutionize Personal Fitness",
        "The Impact of Climate Change on Public Health",
        "How Nutrition Affects Brain Function",
        "The Role of Meditation in Chronic Pain Management",
        "Digital Detox and Its Impact on Mental Health",
        "The Benefits of Mindfulness in Stress Management",
        "How Personalized Medicine is Changing Treatment",
        "The Evolution of Vaccine Technology",
        "Yoga: An Ancient Solution to Modern Stress",
    
        # Education Topics
        "The Rise of Online Learning Platforms",
        "How AI is Transforming Personalized Education",
        "The Future of Hybrid Learning Models",
        "The Impact of Gamification in Education",
        "How Technology Helps Overcome Learning Disabilities",
        "The Role of VR in Virtual Classrooms",
        "Why Emotional Intelligence Should Be Taught in Schools",
        "Benefits of Cross-Disciplinary Education",
        "The Future of Coding Bootcamps",
        "Addressing the Digital Divide in Education",
        "How Peer Learning Boosts Engagement",
        "The Role of Open Educational Resources",
        "How Project-Based Learning Improves Retention",
        "STEM Education: Encouraging Girls in Tech",
        "The Evolution of Traditional Libraries in the Digital Age",
        "Why Financial Literacy is Essential for Students",
        "How Online Certifications Are Reshaping Careers",
        "The Role of Podcasts in Self-Learning",
        "Language Learning in a Globalized World",
        "How Parent Involvement Enhances Student Performance",
    
        # Business and Economics Topics
        "How E-Commerce is Shaping Retail",
        "The Future of Subscription-Based Business Models",
        "How AI is Enhancing Employee Productivity",
        "Ethical Challenges in Corporate Data Usage",
        "The Evolution of Customer Loyalty Programs",
        "The Impact of Digital Transformation on Small Businesses",
        "How Startups are Innovating Supply Chains",
        "The Role of Behavioral Economics in Marketing",
        "Remote Work: Productivity Challenges and Benefits"
    ]
    styles = [
        "Researchers", "Data Scientists", "Common People", "Students", "Entrepreneurs",
        "Marketers", "Tech Enthusiasts", "Environmentalists", "Educators", "Healthcare Professionals",
        "Investors", "Content Creators", "Policy Makers", "Journalists", "Travel Enthusiasts",
        "Parents", "Artists", "Fitness Enthusiasts", "Engineers", "Historians",
        "Teachers", "Developers", "Startup Founders", "Writers", "Bloggers",
        "Gamers", "Environmental Activists", "Social Workers", "Consultants", "Small Business Owners",
        "Public Speakers", "Podcasters", "Psychologists", "Sociologists", "Economists",
        "Architects", "Designers", "Photographers", "Lawyers", "Accountants",
        "Athletes", "Personal Trainers", "Chefs", "Food Critics", "Fashion Designers",
        "Musicians", "Film Makers", "Storytellers", "Book Lovers", "Minimalists",
        "Philosophers", "Technologists", "AI Enthusiasts", "Robotics Experts", "Urban Planners",
        "Astronomers", "Mathematicians", "Physicists", "Chemists", "Biologists",
        "Medical Researchers", "Veterinarians", "Farmers", "Futurists", "Cryptocurrency Enthusiasts",
        "HR Professionals", "Recruiters", "Sales Experts", "E-commerce Entrepreneurs", "Digital Nomads",
        "Remote Workers", "Mental Health Advocates", "Mindfulness Coaches", "Public Relations Experts", "Event Planners",
        "Adventure Seekers", "Wildlife Conservationists", "Marine Biologists", "Astronauts", "Space Enthusiasts",
        "DIY Hobbyists", "Car Enthusiasts", "Pet Owners", "Nature Photographers", "Gardeners",
        "Home Decorators", "Interior Designers", "Outdoor Enthusiasts", "Sports Fans", "Social Media Influencers",
        "YouTubers", "Film Critics", "Comedians", "Lifestyle Bloggers", "Relationship Coaches",
        "Spiritual Guides", "Religious Leaders", "Ethicists", "Activists", "Human Rights Advocates",
        "Policy Analysts", "Data Analysts", "Startup Mentors", "Cultural Historians", "Linguists"
    ]

    input_text = random.choice(topics)
    no_words = 3000
    blog_style = random.choice(styles)
    return input_text, no_words, blog_style

def get_ollama_response(input_text, no_words, blog_style, word_of_the_day, model_name="llama2:chat"):
    """Generate a blog using Ollama with the provided inputs."""
    prompts = [
        # Conversational Prompt
        f"""
            Write a blog for {blog_style} professionals about the topic "{input_text}". Make it engaging and easy to read, with approximately {no_words} words. 
            Use the word "{word_of_the_day}" creatively and naturally. Include:
            - Practical examples or relatable anecdotes to illustrate key points.
            - Synonyms and alternative phrases for "{input_text}" to improve SEO.
            - Eye-catching headings and bullet points for better readability.
            - A concluding call-to-action to inspire further thought or action.
        """,

        # Research-Oriented Prompt
        f"""
            Develop an in-depth, SEO-optimized blog for {blog_style} professionals on the topic "{input_text}". The blog should:
            - Be around {no_words} words.
            - Use "{word_of_the_day}" thoughtfully in a relevant context.
            - Include statistics, references, or data-driven insights to support the content.
            - Highlight challenges, solutions, or innovations related to the topic.
            - Use structured formatting, with headings, subheadings, and lists to organize the information.
        """,

        # Storytelling Prompt
        f"""
            Create a narrative-style blog for {blog_style} professionals that focuses on the topic "{input_text}". The blog should:
            - Be {no_words} words long.
            - Include the word "{word_of_the_day}" in a meaningful and creative way.
            - Start with a captivating story or anecdote to draw readers in.
            - Include a moral, takeaway, or lesson that ties back to the topic.
            - Use vivid language and relatable examples to make the content engaging.
        """,

        # Listicle Prompt
        f"""
            Write a blog for {blog_style} professionals in the form of a listicle about "{input_text}". The blog should:
            - Contain {no_words} words and use the word "{word_of_the_day}" naturally.
            - Include at least 5 main points or items, each with a brief explanation or example.
            - Use headings and bullet points to make the content scannable.
            - End with a summary or call-to-action to encourage further engagement.
        """,

        # Opinion Piece Prompt
        f"""
            Write an opinion-based blog for {blog_style} professionals about the topic "{input_text}". The blog should:
            - Be {no_words} words long.
            - Use "{word_of_the_day}" in a bold and creative way to emphasize your perspective.
            - Present a clear stance on the topic and support it with logical arguments.
            - Address potential counterarguments and provide rebuttals.
            - Conclude with a strong and memorable statement to leave an impact.
        """,

        # How-To Guide Prompt
        f"""
            Create a detailed how-to guide for {blog_style} professionals about "{input_text}". The blog should:
            - Be {no_words} words in length and include "{word_of_the_day}" in a practical context.
            - Outline clear, step-by-step instructions with examples or tips.
            - Use headings, subheadings, and numbered lists for easy navigation.
            - Address common challenges and provide solutions for each step.
        """,

        # FAQ-Style Prompt
        f"""
            Write a blog for {blog_style} professionals in a FAQ format about the topic "{input_text}". The blog should:
            - Be around {no_words} words long and include "{word_of_the_day}" in a creative way.
            - Address at least 5 common questions or concerns related to the topic.
            - Provide concise and informative answers with actionable advice.
            - Use headings or bold text for each question to improve readability.
        """,

        # Problem-Solution Prompt
        f"""
            Write a blog for {blog_style} professionals focused on solving a specific problem related to "{input_text}". The blog should:
            - Be {no_words} words long.
            - Use "{word_of_the_day}" in the context of addressing or overcoming the problem.
            - Clearly define the problem and explain why it matters.
            - Offer practical solutions or strategies to tackle the issue.
            - Conclude with a summary or call-to-action encouraging readers to act.
        """,

        # Analytical Prompt
        f"""
            Create an analytical blog for {blog_style} professionals that examines "{input_text}". The blog should:
            - Be approximately {no_words} words in length.
            - Include "{word_of_the_day}" to emphasize key points or findings.
            - Break down the topic into smaller components or trends for analysis.
            - Use data, graphs, or references to support arguments.
            - Conclude with insights or predictions based on the analysis.
        """,

        # Creative Prompt
        f"""
            Write a creative blog for {blog_style} professionals about the topic "{input_text}". The blog should:
            - Be around {no_words} words and incorporate "{word_of_the_day}" in an imaginative way.
            - Use storytelling, metaphors, or fictional scenarios to explore the topic.
            - Focus on originality and unique perspectives to captivate readers.
            - Provide a meaningful takeaway or lesson at the end.
        """
    ]
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
