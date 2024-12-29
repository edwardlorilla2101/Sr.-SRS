import random
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
def ensure_model_available(model_name):
    """Ensure the model[
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
    ] is available locally or pull it if missing."""
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
        "Why did Filipinos buy more food additives from sari-sari stores in 2024?",
  "Peso strengthens back to P57 vs dollar level",
  "Google Labs launches Whisk, a new image generation tool",
  "Ellen Adarna covers baby's face in Christmas family photo",
  "WINNER Mino’s military discharge could be revoked",
  "Squid Game Season 2: Character guide and reviews",
  "Filipinos adapt to rising prices with smart spending",
  "Camembert cheese compounds improve memory and learning",
  "Bitcoin loses $2 trillion market cap post-Christmas",
  "MMFF review: 'The Kingdom' imagines alternate reality for PH",
  "IMF urges restoration of LandBank and DBP capital",
  "OpenAI’s ChatGPT experiences post-Christmas outage",
  "Goodbye to the $100 bill: US confirms ban",
  "Denise Julia responds to BJ Pascual controversy",
  "Psychological insights on cultivating mystery with potential partners",
  "Favorite holiday cocktail recipes from around the world",
  "Philippines has 2nd largest share of branded residences in Asia",
  "Rosé and Bruno Mars dominate global charts with 'APT.'",
  "Reuse hacks for old pasta sauce jars",
  "Lee Junho undergoes intensive tax audit investigation",
  "Samsung One UI 7 introduces HDR fine-tuning",
  "Pig Chinese Horoscope 2025: Insights on overnight success",
  "Ruby 3.4 programming language brings performance updates",
  "First-ever solar night panel unveiled: How it works with moonlight",
  "Captain America’s replacement achieves milestones quickly",
  "Crypto donations for tax benefits",
  "Gold prices rise amid holiday trading",
  "Denzel Washington gets baptized and receives minister’s license",
  "Cyberpunk 2077 players question lingering food graphics issues",
  "Floki DAO proposes European ETP launch",
  "ERC caps reserve market price at P25/kWh",
  "Unreal Engine 5.5 shows massive performance improvements",
  "Weird Windows 11 bug prevents security updates",
  "Gold forecast for 2025: Spot price predictions",
  "Yin-yang mindset proposed to heal polarized societies",
  "DA proposes removing brand labels from imported rice",
  "Lab-grown cocoa set to revolutionize the industry",
  "Super veggie rich in calcium and vitamin C gains attention",
  "Meta’s gains for a third straight year: Challenges and factors",
  "Elon Musk’s continued dominance and wealth accumulation in 2024",
  "Tax hike risks amidst economic turmoil in the UK",
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
        "Cold hands are common in winter: When are they a health issue?",
  "DOH: Private hospitals should bare info on charity beds, fees",
  "PhilHealth hikes benefit packages for heart patients",
  "Eye drops recalled nationwide due to fungal contamination",
  "Morgan Stanley sees potential growth in surgical robotic stocks",
  "AI tech gains traction at hospitals",
  "TRENDS Study highlights AI's new healthcare horizons",
  "AI-driven digital health revolution transforming medical decision-making",
  "Preparing healthcare education for an AI-augmented future",
  "The world’s first virtual hospital is here",
  "Amazon’s next big acquisition prediction",
  "A public health emergency is waiting at the bottom of the antibiotic resistance cliff",
  "Stocks in healthcare sector set to surge in 2025",
  "Human error blamed in Ascension data breach affecting 5.6 million patients",
  "Healthcare giant admits over 5 million patients affected by ransomware attack",
  "NHS issues warning as norovirus cases rise",
  "Biden administration proposes new cybersecurity rules for healthcare",
  "NHS to begin world-first trial of AI tool to identify type 2 diabetes risk",
  "Hospitals trial AI to spot type 2 diabetes risk",
  "Groundbreaking AI tool to predict diabetes risk years in advance",
  "Top 7 health stories of 2024",
  "Pig kidney transplants and new schizophrenia drug among 2024 medical breakthroughs",
  "Royal Papworth Hospital’s 'lungs in a box' technology boosts transplants",
  "Lab-grown blood cells created without donors",
  "NHS coping with 'upsurge' in flu cases",
  "Families urged to stay home to stop contagious virus spread",
  "Visiting restrictions imposed on hospitals amid respiratory illness surge",
  "Welsh hospitals reintroduce face masks for visitors and staff",
  "Reliance acquires Karkinos Healthcare for Rs 375 crore",
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
        "Origami Artists",
    "Cartographers",
    "Climate Scientists",
    "Geologists",
    "Volcanologists",
    "Storm Chasers",
    "Hurricane Researchers",
    "Tornado Enthusiasts",
    "Urban Historians",
    "Civic Planners",
    "Transportation Designers",
    "Automotive Engineers",
    "Drone Pilots",
    "Space Engineers",
    "Satellite Designers",
    "Rocket Enthusiasts",
    "AI Trainers",
    "Machine Learning Engineers",
    "Cybersecurity Experts",
    "Penetration Testers",
    "Digital Artists",
    "Motion Graphics Designers",
    "Augmented Reality Developers",
    "Holography Experts",
    "3D Printing Specialists",
    "Prototyping Engineers",
    "Industrial Designers",
    "Material Scientists",
    "Nanotechnologists",
    "Biochemists",
    "Geneticists",
    "Microbiologists",
    "Plant Scientists",
    "Agricultural Technologists",
    "Aquaponics Enthusiasts",
    "Permaculture Designers",
    "Ecotourism Experts",
    "Sustainable Architects",
    "Green Builders",
    "Zero Waste Advocates",
    "Upcycling Artists",
    "Circular Economy Specialists",
    "Clean Energy Researchers",
    "Solar Panel Engineers",
    "Wind Energy Specialists",
    "Hydropower Experts",
    "Battery Technologists",
    "Electric Vehicle Enthusiasts",
    "Energy Storage Innovators",
    "Waste Management Experts",
    "Recycling Advocates",
    "Composting Enthusiasts",
    "Environmental Policy Experts",
    "Biodiversity Advocates",
    "Endangered Species Researchers",
    "Wetland Conservationists",
    "Mountain Climbers",
    "Cave Explorers",
    "Arctic Explorers",
    "Desert Survival Experts",
    "Deep Sea Explorers",
    "Polar Researchers",
    "Adventure Photographers",
    "Cultural Storytellers",
    "Folklore Researchers",
    "Traditional Crafts Enthusiasts",
    "Festivals Organizers",
    "Ethnomusicologists",
    "Traditional Dancers",
    "Calligraphers",
    "Typography Designers",
    "Sign Painters",
    "Street Artists",
    "Muralists",
    "Protest Artists",
    "Activist Designers",
    "Political Cartoonists",
    "Social Documentary Filmmakers",
    "War Photographers",
    "Crisis Management Experts",
    "Humanitarian Workers",
    "Refugee Advocates",
    "Disability Activists",
    "Accessible Technology Designers",
    "Inclusive Educators",
    "Interpreters",
    "Translators",
    "Language Preservationists",
    "Dialect Coaches",
    "Cognitive Scientists",
    "Behavioral Economists",
    "Neuroscientists",
    "Psychiatric Researchers",
    "Addiction Counselors",
    "Rehabilitation Experts",
    "Wellness Coaches",
    "Positive Psychologists",
    "Happiness Researchers",
    "Holistic Healers",
         "Archaeologists",
    "Game Designers",
    "Puzzle Enthusiasts",
    "Mythologists",
    "Paleontologists",
    "Astrobiologists",
    "Metaverse Creators",
    "Blockchain Developers",
    "Web3 Enthusiasts",
    "App Developers",
    "Cryptographers",
    "Zoologists",
    "Epidemiologists",
    "Astrologers",
    "Numismatists",
    "Philatelists",
    "Toy Collectors",
    "Historical Reenactors",
    "Craftsmen",
    "Leatherworkers",
    "Blacksmiths",
    "Woodworkers",
    "Beekeepers",
    "Cheesemakers",
    "Winemakers",
    "Brewmasters",
    "Tea Sommeliers",
    "Whiskey Connoisseurs",
    "Luxury Brand Experts",
    "Sneaker Collectors",
    "Fashion Historians",
    "Tattoo Artists",
    "Bodybuilders",
    "Yoga Instructors",
    "Pilates Trainers",
    "Climbers",
    "Parkour Enthusiasts",
    "Survivalists",
    "Bushcrafters",
    "Stunt Performers",
    "Escape Room Designers",
    "Magic Enthusiasts",
    "Illusionists",
    "Stand-Up Comedians",
    "Screenwriters",
    "Playwrights",
    "Voice Actors",
    "Radio Hosts",
    "Audiobook Narrators",
    "Music Producers",
    "Sound Engineers",
    "Songwriters",
    "Lyricists",
    "DJ Artists",
    "Classical Musicians",
    "Orchestra Conductors",
    "Street Performers",
    "Circus Artists",
    "Jugglers",
    "Acrobats",
    "Equestrians",
    "Cyclists",
    "Runners",
    "Marathon Trainers",
    "Triathletes",
    "Swimmers",
    "Scuba Divers",
    "Freedivers",
    "Surfing Enthusiasts",
    "Skiers",
    "Snowboarders",
    "Skaters",
    "Roller Derby Athletes",
    "Mixed Martial Artists",
    "Fencers",
    "Archers",
    "Chess Players",
    "Board Game Designers",
    "Fantasy Writers",
    "Sci-Fi Enthusiasts",
    "Cosplayers",
    "Fanfiction Writers",
    "Graphic Novel Artists",
    "Comic Collectors",
    "Animators",
    "VFX Artists",
    "3D Modelers",
    "Game Streamers",
    "Urban Explorers",
    "Treasure Hunters",
    "Forensic Scientists",
    "Crime Writers",
    "Private Investigators",
    "Ethnographers",
    "Sociolinguists",
    "Educational Technologists",
    "Knowledge Managers",
    "Information Architects",
    "Museum Technologists",
    "Cultural Preservationists",
    "Ecosystem Restorers",
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
    no_words = 50000
    blog_style = random.choice(styles)
    return input_text, no_words, blog_style

def get_ollama_response(input_text, no_words, blog_style, word_of_the_day, model_name="llama3"):
    """Generate a blog using Ollama with the provided inputs."""
    today_year = datetime.now().year
    prompts = [
        # Conversational Prompt
        f"""
            Write a blog for {blog_style} professionals about the topic "{input_text}". Make it engaging and easy to read, with approximately {no_words} words. 
            Use the word "{word_of_the_day}" creatively and naturally. Include:
            - Practical examples or relatable anecdotes to illustrate key points.
            - Synonyms and alternative phrases for "{input_text}" to improve SEO.
            - Eye-catching headings and bullet points for better readability.
            - A concluding call-to-action to inspire further thought or action.with seo optimize
        """,

        # Research-Oriented Prompt
        f"""
            Develop an in-depth, SEO-optimized blog for {blog_style} professionals on the topic "{input_text}". The blog should:
            - Be around {no_words} words.
            - Use "{word_of_the_day}" thoughtfully in a relevant context.
            - Include statistics, references, or data-driven insights to support the content.
            - Highlight challenges, solutions, or innovations related to the topic.
            - Use structured formatting, with headings, subheadings, and lists to organize the information.with seo optimize
        """,

        # Storytelling Prompt
        f"""
            Create a narrative-style blog for {blog_style} professionals that focuses on the topic "{input_text}". The blog should:
            - Be {no_words} words long.
            - Include the word "{word_of_the_day}" in a meaningful and creative way.
            - Start with a captivating story or anecdote to draw readers in.
            - Include a moral, takeaway, or lesson that ties back to the topic.
            - Use vivid language and relatable examples to make the content engaging.with seo optimize
        """,

        # Listicle Prompt
        f"""
            Write a blog for {blog_style} professionals in the form of a listicle about "{input_text}". The blog should:
            - Contain {no_words} words and use the word "{word_of_the_day}" naturally.
            - Include at least 5 main points or items, each with a brief explanation or example.
            - Use headings and bullet points to make the content scannable.
            - End with a summary or call-to-action to encourage further engagement. with seo optimize
        """,

        # Opinion Piece Prompt
        f"""
            Write an opinion-based blog for {blog_style} professionals about the topic "{input_text}". The blog should:
            - Be {no_words} words long.
            - Use "{word_of_the_day}" in a bold and creative way to emphasize your perspective.
            - Present a clear stance on the topic and support it with logical arguments.
            - Address potential counterarguments and provide rebuttals.
            - Conclude with a strong and memorable statement to leave an impact.with seo optimize
        """,

        # How-To Guide Prompt
        f"""
            Create a detailed how-to guide for {blog_style} professionals about "{input_text}". The blog should:
            - Be {no_words} words in length and include "{word_of_the_day}" in a practical context.
            - Outline clear, step-by-step instructions with examples or tips.
            - Use headings, subheadings, and numbered lists for easy navigation.
            - Address common challenges and provide solutions for each step.with seo optimize
        """,

        # FAQ-Style Prompt
        f"""
            Write a blog for {blog_style} professionals in a FAQ format about the topic "{input_text}". The blog should:
            - Be around {no_words} words long and include "{word_of_the_day}" in a creative way.
            - Address at least 5 common questions or concerns related to the topic.
            - Provide concise and informative answers with actionable advice.
            - Use headings or bold text for each question to improve readability.with seo optimize
        """,

        # Problem-Solution Prompt
        f"""
            Write a blog for {blog_style} professionals focused on solving a specific problem related to "{input_text}". The blog should:
            - Be {no_words} words long.
            - Use "{word_of_the_day}" in the context of addressing or overcoming the problem.
            - Clearly define the problem and explain why it matters.
            - Offer practical solutions or strategies to tackle the issue.
            - Conclude with a summary or call-to-action encouraging readers to act.with seo optimize
        """,

        # Analytical Prompt
        f"""
            Create an analytical blog for {blog_style} professionals that examines "{input_text}". The blog should:
            - Be approximately {no_words} words in length.
            - Include "{word_of_the_day}" to emphasize key points or findings.
            - Break down the topic into smaller components or trends for analysis.
            - Use data, graphs, or references to support arguments.
            - Conclude with insights or predictions based on the analysis.with seo optimize
        """,

        # Creative Prompt
        f"""
            Write a creative blog for {blog_style} professionals about the topic "{input_text}". The blog should:
            - Be around {no_words} words and incorporate "{word_of_the_day}" in an imaginative way.
            - Use storytelling, metaphors, or fictional scenarios to explore the topic.
            - Focus on originality and unique perspectives to captivate readers.
            - Provide a meaningful takeaway or lesson at the end.with seo optimize
        """,
        f"Write a blog {blog_style}: Why {input_text} No Longer Works in {today_year} and What to Do Instead. Be around {no_words} words and include '{word_of_the_day}'.",
        f"Write a blog How {blog_style} Professionals Can Benefit from {input_text} in {today_year}. Write {no_words} words and creatively use '{word_of_the_day}'.",
        f"Write a blog 5 Underrated Tools for {blog_style} Professionals to Master {input_text} in {today_year}. Cover this in {no_words} words with '{word_of_the_day}' included.",
        f"Write a blog What {input_text} Means for {blog_style} Professionals in {today_year}. Analyze in {no_words} words while emphasizing '{word_of_the_day}'.",
        f"Write a blog How {blog_style} Professionals Can Master {input_text} in {today_year}. Provide actionable tips in {no_words} words and include '{word_of_the_day}'.",
        f"Write a blog Why {input_text} Is Critical for {blog_style} Success in {today_year}. Dive into the topic in {no_words} words, using '{word_of_the_day}' naturally.",
        f"Write a blog Lessons on {input_text} for {blog_style} Professionals in {today_year}. Share insights in {no_words} words, creatively using '{word_of_the_day}'.",
        f"Write a blog The Evolution of {input_text} for {blog_style} Professionals in {today_year}. Cover its journey in {no_words} words and include '{word_of_the_day}'.",
        f"Write a blog How {blog_style} Professionals Can Overcome Challenges with {input_text} in {today_year}. Offer solutions in {no_words} words, using '{word_of_the_day}'.",
        f"Write a blog Behind the Scenes: {input_text} for {blog_style} in {today_year}. Unveil insights in {no_words} words with a focus on '{word_of_the_day}'.",
        f"Write a blog Top Strategies for {blog_style} Professionals to Excel in {input_text} in {today_year}. Outline in {no_words} words while incorporating '{word_of_the_day}'.",
        f"Write a blog 5 Ways {blog_style} Professionals Can Leverage {input_text} in {today_year}. Highlight approaches in {no_words} words, using '{word_of_the_day}' creatively.",
        f"Write a blog The Role of {input_text} in {blog_style} Growth in {today_year}. Explain in {no_words} words while weaving in '{word_of_the_day}'.",
        f"Write a blog Why {input_text} Matters for {blog_style} in {today_year}. Discuss its significance in {no_words} words and incorporate '{word_of_the_day}'.",
        f"Write a blog The Future of {input_text} for {blog_style} Professionals Beyond {today_year}. Speculate in {no_words} words, making '{word_of_the_day}' central to the narrative.",
        f"Write a blog 5 Key Insights on {input_text} for {blog_style} in {today_year}. Provide them in {no_words} words and include '{word_of_the_day}' creatively.",
        f"Write a blog How {input_text} Is Shaping the Future of {blog_style} in {today_year}. Write {no_words} words and make '{word_of_the_day}' a focus point.",
        f"Write a blog The Importance of {input_text} for {blog_style} Professionals in {today_year}. Highlight why in {no_words} words, incorporating '{word_of_the_day}' naturally.",
        f"Write a blog How to Use {input_text} Effectively as a {blog_style} Professional in {today_year}. Cover this in {no_words} words, using '{word_of_the_day}' practically.",
        f"The Challenges of {input_text} in {blog_style} and How to Overcome Them in {today_year}. Write {no_words} words and creatively use '{word_of_the_day}'.",
        f"How {blog_style} Professionals Can Navigate {input_text} in {today_year}. Provide guidance in {no_words} words and include '{word_of_the_day}'.",
        f"Write a blog 5 Lessons Learned from {input_text} for {blog_style} Professionals in {today_year}. Share these in {no_words} words while incorporating '{word_of_the_day}'.",
        f"Write a blog The Power of {input_text} for {blog_style} in {today_year}. Explain its influence in {no_words} words, ensuring '{word_of_the_day}' is highlighted.",
        f"Write a blog Why {input_text} Should Be a Priority for {blog_style} in {today_year}. Discuss in {no_words} words while weaving '{word_of_the_day}' into the narrative.",
        f"Write a blog How {blog_style} Professionals Can Improve Their Work Through {input_text} in {today_year}. Cover this in {no_words} words and use '{word_of_the_day}'.",
        f"Write a blog The Impact of {input_text} on {blog_style} Success in {today_year}. Analyze in {no_words} words while making '{word_of_the_day}' central to the discussion.",
        f"Write a blog The Role of {input_text} in Transforming {blog_style} in {today_year}. Write about this in {no_words} words, ensuring '{word_of_the_day}' is included.",
        f"Write a blog How {input_text} Can Revolutionize {blog_style} in {today_year}. Explore the potential in {no_words} words with '{word_of_the_day}' creatively used.",
        f"Write a blog The Ultimate Guide to {input_text} for {blog_style} Professionals in {today_year}. Write this in {no_words} words, incorporating '{word_of_the_day}' throughout."


    ]

                                  
    prompt = random.choice(prompts) + " well structured blog with adsense approve article and seo optimize article"
    promptTitle =  """
    Generates an SEO-optimized title for a blog.

    Parameters:
        input_text (str): The topic or main subject of the blog.
        blog_style (str): The target audience or style of the blog.
        word_of_the_day (str): A keyword or phrase to be included in the title.

    Returns:
        str: A dynamically generated, SEO-optimized title.

    Mastering {input_text}: A Comprehensive Guide for {blog_style} Professionals Featuring {word_of_the_day}
    """

    try:
        ensure_model_available(model_name)
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        resultTitle = subprocess.run(
            ["ollama", "run", model_name, promptTitle],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Error running model: {result.stderr.strip()}")
        print("Ollama Response Retrieved Successfully.")
        return {
            "blog": result.stdout.strip(),
            "title": resultTitle.stdout.strip()
        }
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
        message["Subject"] = subject.replace("\n", " ").strip()

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
        recipient = "edwardlorilla2048.edwardlancelorilla1@blogger.com"  # Replace with the actual recipient's email
        send_email(
            recipient_email=recipient,
            subject=blog_content["title"],
            content=blog_content["blog"]
        )
    else:
        print("Blog content generation failed. Email will not be sent.")
