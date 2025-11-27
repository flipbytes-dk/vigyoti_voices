# 🚀 Quick Start Guide

Get your AI receptionist demos up and running in 5 minutes!

## Step 1: Run Setup

```bash
cd /Users/dk2/Documents/vigyoti_voices
./setup.sh
```

This will:
- ✅ Check Python installation
- ✅ Create virtual environment (`venv/`)
- ✅ Install all dependencies
- ✅ Create `.env` file
- ✅ Set up output directory

## Step 2: Activate Virtual Environment

Every time you work on this project, activate the virtual environment:

```bash
source venv/bin/activate
```

You'll see `(venv)` in your terminal prompt when activated.

## Step 3: Add Your API Key

1. Get your ElevenLabs API key from: https://elevenlabs.io/app/settings/api-keys
2. Open `.env` file
3. Replace `your_api_key_here` with your actual API key

```bash
# Edit .env
ELEVENLABS_API_KEY=sk_your_actual_key_here
```

## Step 4: Test with 3 Samples

```bash
python3 generate_conversations.py --test-mode
```

This generates demos for:
- Hair Salons
- Dentists  
- Law Firms

**Cost**: ~$0.30

## Step 5: Review Output

Check the `output/` directory:
```
output/
├── hair_salons_ai_receptionist_demo.mp3  ← Listen to this!
├── hair_salons_script.txt                ← Read the script
├── dentists_ai_receptionist_demo.mp3
├── dentists_script.txt
├── law_firms_ai_receptionist_demo.mp3
└── law_firms_script.txt
```

## Step 6: Generate All 89 Industries

Once you're happy with the samples:

```bash
python3 generate_conversations.py --all
```

**Time**: ~15-20 minutes  
**Cost**: ~$9-15

---

## 🎯 Common Commands

### Generate specific industries
```bash
python3 generate_conversations.py --industries "Gyms,Yoga Studios,Personal Trainers"
```

### Generate first 10 only
```bash
python3 generate_conversations.py --limit 10
```

### Regenerate failed ones
```bash
# Check generation_report.json for failed industries
python3 generate_conversations.py --industries "Failed Industry 1,Failed Industry 2"
```

---

## 🔧 Troubleshooting

### "ELEVENLABS_API_KEY not found"
→ Make sure `.env` file exists and contains your API key

### Audio sounds robotic
→ Edit `config.yaml` and adjust voice settings:
```yaml
voices:
  receptionist:
    stability: 0.7  # Increase for more consistent voice
```

### Rate limit errors
→ Increase delay in `config.yaml`:
```yaml
processing:
  rate_limit_delay: 5  # Increase from 2 to 5 seconds
```

---

## 📊 What You'll Get

- **89 MP3 files**: One for each industry (60-90 seconds each)
- **89 Script files**: Text version of each conversation
- **Generation report**: JSON summary of success/failures
- **Log file**: Detailed processing logs

---

## 💡 Tips

1. **Start small**: Always test with `--test-mode` first
2. **Check credits**: Make sure you have ~$15 in ElevenLabs credits
3. **Listen to samples**: Review quality before generating all 89
4. **Customize voices**: Try different voice IDs in `config.yaml`
5. **Adjust length**: Modify `target_duration_seconds` for longer/shorter demos

---

## 📞 Need Help?

1. Check `generation.log` for errors
2. Review `README.md` for detailed documentation
3. Verify your API key is correct
4. Ensure you have sufficient API credits

---

**Ready to go? Run `./setup.sh` to get started! 🎙️**
