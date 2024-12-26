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
  "Which scent do you find the most soothing?",
  "What is a language you love to listen to even if you don’t understand it?",
  "Oceans or mountains? Why?",
  "What color would you choose to describe yourself?",
  "What’s something you’ve accomplished as an adult that your younger self would be proud of?",
  "What tasks make you feel like your best self?",
  "What’s your Enneagram number, and how does it influence your self-care practices?",
  "What do you love most about your personality?",
  "What do you look for and need in your friendships?",
  "How do you feel best supported in hard times?",
  "What small joys bring light to your day?",
  "What do you love most about our relationship?",
  "What’s your earliest memory?",
  "What’s one thing you’d tell yourself at my age?",
  "What’s a favorite memory of your parents?",
  "Which characteristics do you think you inherited from our parents?",
  "Do you have any tattoos?",
  "What Netflix show or movie are you watching?",
  "What are you currently reading?",
  "What do you do for enjoyment?",
  "What projects are you working on that bring you joy?",
  "How do you unwind after work?",
        "Experts raise the alarm about incoming massive volcanic eruption",
        "New study explains how gold reaches Earth’s surface",
        "Stunning James Webb images reveal the birth of a Milky Way twin",
        "Chinese scientists' major discovery innovating pesticide industry",
        "US researchers to study viability of carbon capture in fish farms",
        "Oldest saber-toothed creature found, rewriting the story of mammal evolution",
        "Scientists discover a 'Goldilocks' zone for DNA organization, opening new doors for drug development",
        "Fly adopts wasp defense to foil predator",
        "Uplift underway in Finland’s Kvarken Archipelago",
        "Astronomers spot an enormous explosion from the 1st black hole ever photographed",
        "Saturn’s rings might be much older than had been thought",
        "Astronauts send Christmas message to Earth from International Space Station",
        "James Webb telescope's big year for cosmology",
        "Webb observes protoplanetary disks that contradict models of planet formation",
        "Christmas night lights: Geomagnetic storm to dazzle 10 US states with Northern Lights",
        "Two populations of dark comets in the solar system could explain where Earth got its oceans",
        "Distant quasar found with 140 trillion times Earth's ocean water",
        "Marmosets call each other by 'names' with distinct vocalizations",
        "Scientists explore negative time in quantum experiments",
        "NASA's Perseverance rover captures oddball rock on Mars",
        "When will we know if NASA’s Parker Solar Probe survived ‘touching’ the sun?",
        "Earth's orbit is crowded with over 1,000 collision warnings per day",
        "Mars orbiter captures a winter wonderland on summertime Mars",
        "500-million-year-old Ecdysozoan fossil embryos found in China",
        "James Webb Space Telescope catches monster black hole napping after 'overeating'",
        "Giant sloths and mastodons coexisted with humans for millennia in the Americas",
        "Ants outshine humans in teamwork",
        "Mars opposition 2025 — How to see the Red Planet at its biggest and brightest",
        "Fruit flies in space — Chinese astronauts show experiment on Tiangong Station",
        "Scientists take a closer look at rare particles called hypernuclei",
        "Dazzling star cluster creates a cosmic holiday wreath",
        "Milky Way’s fluffiest system found a new planet",
        "Chinese satellite poses no danger but gives US observers a ‘spectacular’ light show",
        "Ocean explorers film enchanting marine snow drifting like a symphony through the deep sea",
        "Scientists create 'twisted light' so robots can see like shrimp",
        "Scientists discover a mysterious new predator living deep in the ocean",
        "Asteroid alert! Giant asteroid narrowly misses Earth this Christmas",
        "In Carl Sagan’s death, an amazing life lesson",
        "Gloria in Excelsis Deo! What was the Star of Bethlehem?",
        "Polymer coating gives electron microscopes enhanced 3D vision",
        "Researchers quantify the speed of human thought",
        "Humans almost went extinct 930,000 years ago",
        "Inside the faraway planet where scientists have found shocking signs of life",
        "Santa’s speed on Christmas Eve calculated",
        "NASA’s X-59 silent supersonic aircraft ready to fly for the first time",
        "New study reveals how leaves’ resilience to raindrops might help in agriculture and renewable energy",
        "Revolutionary maps reveal Earth’s geological secrets",
        "The Moon's significant impact on animals worldwide",
        "The controversy over cannibalism",
        "Home foundations are crumbling due to a mineral",
          "MLBB new hero Kalea: Skills, Abilities, Release Date, & More",
  "FC Tactical announces v2.1 update with Guild vs Guild battles and more",
  "Boom Beach free rewards and how to claim them",
  "Vivo X200 Ultra camera specs leak: 200 MP telephoto and 4K recording",
  "Tongits Go: Strategies for success and holiday rewards",
  "Infinix HOT 50 Pro+ released in 4 new colors",
  "Realme Neo7 SE to feature MediaTek Dimensity 8400 SoC",
  "Mobile Legends: Bang Bang – Best Lukas Build",
  "Apple no longer top smartwatch brand in the world",
  "HUAWEI Mate X6 pre-orders with early bird offers",
  "Naruto Ultimate Ninja Storm series sales milestone",
  "Solo Leveling: ARISE – New Jeju Island Raid Update",
  "Anker unveils high-speed USB-C chargers",
  "PUBG Mobile A11 Royale Pass leaks: Upcoming skins and rewards",
  "OPPO Find X8 Mini: Compact design with impressive battery life",
  "HONOR Magic7 RSR Porsche Design unveiled",
  "Samsung Galaxy M16 design and specs revealed",
  "AI phones could sustain chip sector amid slowed data center spending",
  "Samsung to reduce 2025 foldable phone targets due to weak sales",
  "Sony celebrates 30 years of PlayStation",
  "Micron advances HBM4 development, mass production in 2026",
  "Nothing Phone 3a series to get major performance upgrades",
  "Best After Christmas Sales 2024: Top deals",
  "Microsoft leads passkey adoption, aims to eliminate passwords",
  "Samsung Galaxy S25 family's rumored release date",
  "Best Boxing Day deals on games, consoles, and tech",
  "Google launches Android XR platform for extended reality",
  "Xiaomi unveils Cross Door Mijia refrigerator",
  "AMD’s CES 2025 press conference: How to watch",
  "Nobara Linux introduces custom KDE Plasma desktop",
  "ChatGPT hidden content rewrite highlights risks",
  "JBL Xtreme 3 discounted for Christmas",
  "Sony XM5 headphones hit lowest-ever price",
  "Qwen's QVQ rivals top AI models in visual reasoning",
  "Lifetime Microsoft Office subscription deals",
  "50,000-year-old baby mammoth remains found in Siberia",
  "Ruijie Networks' cloud platform flaws expose devices to attacks",
  "Zero-bezel iPhone unlikely before 2026",
  "Escape From Tarkov wipe and patch date confirmed",
  "Chinese OEMs to increase battery capacity by 2025",
  "Google Maps integration in Hyundai vehicles",
  "Instagram testing expired story highlights feature",
  "Pokémon Go Mega Abomasnow counters and moveset explained",
  "Nvidia RTX 5090 spotlight at CES 2025",
  "Evangelion's Rei and Asuka new PVC Nendoroid figures",
  "Lenovo ThinkVision M14t Gen2 review",
  "2024 winners and losers: Samsung and Apple",
         "Dozens dead as passenger plane crashes in Kazakhstan",
  "Russian missile likely cause of Azerbaijan Airlines crash",
  "38 dead and 29 survivors in Azerbaijani airliner crash in Kazakhstan",
  "Passenger captures moments before and after plane crash in Kazakhstan",
  "Biden slams Russia’s Christmas Day assault on Ukraine",
  "Putin 'inhumane,' Zelensky says, as Russia attacks Ukrainian power grid",
  "Ukraine: Zelensky condemns Russia's Christmas Day attack",
  "Russia carried out massive strike on Ukrainian energy system",
  "Pope launches 2025 Jubilee Year with opening of Holy Doors",
  "Pope Francis inaugurates 2025 Jubilee with Holy Door opening",
  "Celebrating Jubilee 2025",
  "Pope Francis opens Holy Door to kick off jubilee year",
  "Pope calls for 'arms to be silenced' in Christmas appeal",
  "Man finds bear in living room as Japan readies license to kill",
  "Bear found under heated table in Fukushima home is captured",
  "South Korean president Yoon defies Christmas summons",
  "South Korea's Yoon defies agency summons over martial law",
  "Chinese embassy demands release of Huawei CFO arrested in Canada",
  "Gemini's Deep Research AI feature expands globally",
  "Ford Ranger Raptor Diesel drag races Toyota Hilux Revo GR Sport",
        "Philippines logs over 4,000 measles, rubella cases",
        "Community action to curb dengue crisis in PH",
        "Food sharing practices in Caribbean countries using intergenerational interviews",
        "Determinants of gender-equitable attitudes among adult men in Malawi",
        "Bird flu kills 20 big cats at Washington animal sanctuary",
        "Bird flu concerns lead LA County officials to warn against feeding pets raw food",
        "AI-designed 'nanocages' mimic viral behavior for gene therapy",
        "Study: Exercise boosts brain function for 24 hours",
        "17-year-old from Jerusalem contracts polio",
        "Effects of smokeless tobacco on cancer incidence: meta-analysis",
        "Linking genetics of dyslexia to brain structure",
        "Heart attack deaths spike during winter holidays",
        "Teabags release billions of microplastics",
        "Study links coffee to lower head and neck cancer risk",
        "H5N1 detected in dairy cattle for the first time",
        "Mongolia confirms outbreak of meningococcal disease",
        "Tips for managing Seasonal Affective Disorder",
        "Hospital wards 'full to bursting' with respiratory patients",
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
    prompt = random.choice(prompts)
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
        sender_email = "edwardlorilla2013@gmail.com"
        sender_password = "giax bwty esxw dquw"

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
