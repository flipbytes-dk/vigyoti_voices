# Vigyoti Voice Demo Generator

Automated system to generate AI receptionist demo conversations for 89 different industries using ElevenLabs voice AI and GPT-4o.

## 🎯 Overview

This tool creates realistic, industry-specific phone conversations between customers and an AI receptionist. Each demo showcases how Vigyoti's AI receptionist handles:
- Inbound call answering
- Customer greetings and inquiries
- Service information
- Appointment booking
- Confirmation and follow-up

## ✨ Features

- **GPT-4o Powered**: Natural conversations with filler words, pauses, and realistic flow
- **10 Diverse Voices**: Multiple accents for both customer and receptionist (American, British, etc.)
- **89 Industries**: Complete coverage of all Vigyoti target markets
- **Batch Processing**: Generate demos in batches of 10 for easy management
- **Automated Setup**: One-command installation and configuration
- **Virtual Environment**: Clean dependency isolation

## 📋 Prerequisites

- Python 3.8+
- ElevenLabs API Key ([Get yours here](https://elevenlabs.io/app/settings/api-keys))
- OpenAI API Key ([Get yours here](https://platform.openai.com/api-keys))

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/flipbytes-dk/vigyoti_voices.git
cd vigyoti_voices
```

### 2. Run Setup

```bash
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Set up your `.env` file

### 3. Configure API Keys

Edit `.env` and add your API keys:

```bash
ELEVENLABS_API_KEY=your_elevenlabs_key_here
OPENAI_API_KEY=your_openai_key_here
```

### 4. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 5. Test with Samples

```bash
python3 generate_conversations.py --test-mode
```

This generates 3 sample demos (Hair Salons, Dentists, Law Firms).

## 📖 Usage

### Generate All 89 Industries

```bash
python3 generate_conversations.py --all
```

**Time**: ~40-45 minutes  
**Cost**: ~$12-15 in API credits

### Generate in Batches of 10

```bash
# Batch 1 (industries 1-10)
python3 batch_generate.py 1

# Batch 2 (industries 11-20)
python3 batch_generate.py 2

# Continue through batch 9 (industries 81-89)
python3 batch_generate.py 9
```

### Generate Specific Industries

```bash
python3 generate_conversations.py --industries "Gyms,Yoga Studios,Personal Trainers"
```

### Generate First N Industries

```bash
python3 generate_conversations.py --limit 20
```

## 🎙️ Voice Variety

**Customer Voices (10 Male):**
- American (Charlie, Brian, Adam, Arnold, Josh, Sam, Patrick)
- British (Daniel, Antoni)
- British-American (Dave)

**Receptionist Voices (10 Female):**
- American (Rachel, Bella, Elli, Matilda, Freya, Gigi)
- British (Lily, Dorothy)
- American-Southern (Grace)
- British-Swedish (Charlotte)

Each conversation randomly selects from these voices for maximum variety!

## 📁 Output Structure

```
output/
├── accountants_ai_receptionist_demo.mp3
├── accountants_script.txt
├── hair_salons_ai_receptionist_demo.mp3
├── hair_salons_script.txt
├── ...
└── generation_report.json
```

## 🔧 Configuration

Edit `config.yaml` to customize:

- **Voice settings**: Stability, similarity, style
- **Conversation length**: Target duration (default: 90 seconds)
- **Customer names**: Pool of names to randomly select from
- **Natural speech**: Filler words, pauses, greetings

## 💰 Cost Estimation

- **GPT-4o**: ~$0.01-0.02 per conversation
- **ElevenLabs**: ~$0.12 per conversation (90 seconds @ $0.08/min)
- **Total per demo**: ~$0.13-0.14
- **All 89 demos**: ~$12-15

## 📊 All 89 Industries

<details>
<summary>Click to expand full list</summary>

1. Accountants
2. Alternative Medicine
3. Appliance Repair
4. Architects
5. Bed and Breakfast
6. Boxing Clubs
7. Car Dealerships
8. Car Repair Shops
9. Car Wash
10. Carpenters
11. Catering Services
12. Chiropractors
13. Cleaning Companies
14. Coffee Shops
15. Construction Companies
16. Couriers and Delivery
17. Cybersecurity
18. DJs and Musicians
19. Dance Studios
20. Daycare and Pre Schools
21. Dentists
22. Driving Schools
23. Ecommerce
24. Electricians
25. Event Planners
26. Financial Advisors
27. Flooring Installers
28. Florists
29. Funeral Homes
30. Gyms
31. HVAC Services
32. Hair Salons
33. Handyman Services
34. Home Inspectors
35. Hotels and Resorts
36. IT Services
37. Insurance Brokers
38. Interior Designers
39. Landscaping Services
40. Laser Clinics
41. Law Firms
42. Locksmith Services
43. Makeup Artists
44. Managed Services Providers
45. Marketing Agencies
46. Martial Arts Schools
47. Massage and Spas
48. Media and entertainment
49. Medical Clinics
50. Medical and Wellness
51. Mortgage Brokers
52. Movers and Packers
53. Music Teachers
54. Nail Salons
55. Nanny and Childcare
56. Notary Public
57. Nutritionists and Dietitians
58. Painters
59. Party Supplies and Rentals
60. Personal Trainers
61. Pest Control
62. Pet Boarding and Daycare
63. Pet Groomers
64. Pet Supply Stores
65. Pharmacies
66. Photographers
67. Physiotherapy
68. Plumbing Services
69. Pool Services
70. Print Shops
71. Property Management
72. Real Estate Agents
73. Resturant
74. Roofing Companies
75. Schools
76. Software and SaaS Services
77. Solar Energy
78. Staffing Agencies
79. Tattoo and Piercing Shops
80. Taxi Services
81. Therapists
82. Travel Agencies
83. Trucking Companies
84. Tutoring Centers
85. Vacation Rentals
86. Veterinary Clinics
87. Videographers
88. Wedding Planners
89. Yoga Studios

</details>

## 🛠️ Troubleshooting

### "ELEVENLABS_API_KEY not found"
Make sure `.env` file exists and contains your API key.

### "OPENAI_API_KEY not found"
Add your OpenAI API key to the `.env` file.

### httpx compatibility error
Run: `pip install --upgrade httpx==0.27.2`

### Rate limiting errors
Increase `rate_limit_delay` in `config.yaml`.

## 📝 Project Structure

```
vigyoti_voices/
├── generate_conversations.py    # Main generation script
├── batch_generate.py           # Batch processing helper
├── config.yaml                 # Configuration file
├── conversation_templates.json # Conversation templates
├── industries.json             # List of 89 industries
├── requirements.txt            # Python dependencies
├── setup.sh                    # Automated setup script
├── .env.example               # Environment variables template
├── README.md                  # This file
├── QUICKSTART.md             # Quick start guide
└── GPT4O_INTEGRATION.md      # GPT-4o integration details
```

## 🤝 Contributing

This is an internal Vigyoti project. For questions or issues, contact the development team.

## 📄 License

Internal use only - Vigyoti AI

---

**Built with ❤️ for Vigyoti AI**
