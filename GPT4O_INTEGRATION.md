# GPT-4o Integration - Natural Conversation Enhancement

## 🎯 What Changed

### 1. Voice Updates
- **Customer**: Changed to **Charlie** (IKne3meq5aSn9XLyUdCD) - casual, friendly male voice
- **Receptionist**: Changed to **Lily** (pFZP5JQG7iQjIQuC4Bku) - warm, professional female voice
- **Customer Name**: Updated to **James Martinez** (matches male voice)

### 2. GPT-4o Integration
- Added OpenAI API client for natural conversation generation
- Conversations now include:
  - ✅ Natural greetings and small talk
  - ✅ Filler words ("um", "uh", "you know", "like", "actually")
  - ✅ Natural pauses (indicated by "...")
  - ✅ Realistic conversation flow
  - ✅ Casual, friendly customer tone
  - ✅ Warm, professional AI receptionist

### 3. Configuration Updates
- Added OpenAI settings in `config.yaml`
- Increased conversation duration to 90 seconds for more natural flow
- Added natural speech parameters (filler words, pauses, greetings)
- Lower stability settings for more voice variation

## 📦 Files Modified

1. **config.yaml** - New voice IDs, OpenAI settings, natural speech parameters
2. **generate_conversations.py** - GPT-4o integration for conversation generation
3. **requirements.txt** - Added `openai==1.54.0`
4. **.env.example** - Added OPENAI_API_KEY template

## 🚀 How to Use

### Step 1: Install New Dependency

```bash
# Activate virtual environment
source venv/bin/activate

# Install OpenAI package
pip install openai==1.54.0
```

### Step 2: Verify API Keys

Make sure your `.env` file has both keys:

```bash
ELEVENLABS_API_KEY=your_elevenlabs_key_here
OPENAI_API_KEY=your_openai_key_here
```

### Step 3: Generate Test Samples

```bash
python3 generate_conversations.py --test-mode
```

## 🎙️ What to Expect

The new conversations will sound much more natural:

**Before** (Template-based):
```
Customer: Hi, I'm calling about a haircut and color.
AI Receptionist: Hello! Thank you for calling Luxe Hair Studio. How can I help you today?
```

**After** (GPT-4o generated):
```
Customer: Hi there! How are you doing today?
AI Receptionist: I'm doing great, thanks for asking! How can I help you?
Customer: Well, um... I was actually hoping to book an appointment for, like, a haircut and maybe some highlights?
AI Receptionist: Oh perfect! We'd love to help you with that. Let me just... yeah, we have some great options for highlights and cuts.
```

## 🔧 Technical Details

### GPT-4o Prompt Engineering

The system generates conversations using a detailed prompt that includes:
- Industry-specific context
- Natural speech requirements
- Conversation flow guidelines
- Realistic dialogue patterns

### Fallback Mechanism

If GPT-4o fails for any reason, the system automatically falls back to the template-based generation to ensure reliability.

### Voice Settings

- **Lower stability** (0.4 for customer, 0.5 for receptionist) = more natural variation
- **Style variation** (0.3 for customer, 0.2 for receptionist) = more expressive delivery
- **Longer duration** (90 seconds) = room for natural pauses and flow

## 💰 Cost Impact

- **GPT-4o cost**: ~$0.01-0.02 per conversation (very low)
- **ElevenLabs cost**: ~$0.12 per conversation (90 seconds @ $0.08/min)
- **Total per demo**: ~$0.13-0.14
- **All 89 demos**: ~$12-13

The GPT-4o cost is minimal compared to voice generation.

## ✅ Next Steps

1. Install the `openai` package
2. Ensure OPENAI_API_KEY is in `.env`
3. Run test mode to hear the difference
4. Generate all 89 demos with natural conversations!
