#!/usr/bin/env python3
"""
Voice Demo Generator for Vigyoti AI Receptionist
Generates industry-specific AI receptionist demo conversations using ElevenLabs API
"""

import os
import json
import yaml
import random
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from openai import OpenAI
import time
from tqdm import tqdm

# Load environment variables
load_dotenv()

class VoiceDemoGenerator:
    """Generate AI receptionist demo conversations for multiple industries"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the generator with configuration"""
        self.config = self._load_config(config_path)
        self.templates = self._load_templates()
        self.industries = self._load_industries()
        self._setup_logging()
        
        # Initialize ElevenLabs client
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
        
        self.client = ElevenLabs(api_key=api_key)
        
        # Initialize OpenAI client
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.openai_client = OpenAI(api_key=openai_key)
        
        # Create output directory
        self.output_dir = Path(self.config['output']['directory'])
        self.output_dir.mkdir(exist_ok=True)
        
        self.logger.info("VoiceDemoGenerator initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Substitute environment variables
        if 'api' in config and 'elevenlabs_api_key' in config['api']:
            config['api']['elevenlabs_api_key'] = os.path.expandvars(
                config['api']['elevenlabs_api_key']
            )
        
        if 'openai' in config and 'api_key' in config['openai']:
            config['openai']['api_key'] = os.path.expandvars(
                config['openai']['api_key']
            )
        
        return config
    
    def _load_templates(self) -> Dict:
        """Load conversation templates"""
        with open('conversation_templates.json', 'r') as f:
            return json.load(f)
    
    def _load_industries(self) -> List[str]:
        """Load list of industries"""
        with open('industries.json', 'r') as f:
            return json.load(f)
    
    def _setup_logging(self):
        """Configure logging"""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        
        # Create logger
        self.logger = logging.getLogger('VoiceDemoGenerator')
        self.logger.setLevel(log_level)
        
        # File handler
        if log_config.get('file'):
            fh = logging.FileHandler(log_config['file'])
            fh.setLevel(log_level)
            fh.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(fh)
        
        # Console handler
        if log_config.get('console', True):
            ch = logging.StreamHandler()
            ch.setLevel(log_level)
            ch.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
            self.logger.addHandler(ch)
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '_', text)
        return text.strip('-_')
    
    def _get_industry_context(self, industry: str) -> Dict:
        """Get or generate industry-specific context"""
        # Check if we have a predefined context
        if industry in self.templates['industry_contexts']:
            return self.templates['industry_contexts'][industry]
        
        # Generate generic context for industries not in templates
        return self._generate_generic_context(industry)
    
    def _generate_generic_context(self, industry: str) -> Dict:
        """Generate a generic context for industries without specific templates"""
        industry_lower = industry.lower()
        
        # Common patterns
        service_mappings = {
            'repair': 'repair services',
            'salon': 'styling services',
            'spa': 'spa treatments',
            'clinic': 'appointments',
            'shop': 'services',
            'studio': 'sessions',
            'school': 'classes',
            'agency': 'consultation',
            'service': 'service',
            'company': 'services',
            'center': 'programs',
        }
        
        service_type = 'an appointment'
        for key, value in service_mappings.items():
            if key in industry_lower:
                service_type = value
                break
        
        return {
            'business_name': f"{industry}",
            'service_type': service_type,
            'specific_need': f"{service_type}",
            'service_category': industry_lower,
            'service_list': f"consultations, appointments, and specialized {industry_lower} services",
            'recommended_service': f"our most popular {service_type} package"
        }
    
    def _fill_template(self, template: str, context: Dict) -> str:
        """Fill template string with context values"""
        result = template
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        return result
    
    def _select_random_voices(self) -> tuple:
        """Randomly select customer and receptionist voices from pools"""
        customer_voice = random.choice(self.config['voices']['customer_pool'])
        receptionist_voice = random.choice(self.config['voices']['receptionist_pool'])
        
        self.logger.debug(f"Selected voices: Customer={customer_voice['name']} ({customer_voice['accent']}), "
                         f"Receptionist={receptionist_voice['name']} ({receptionist_voice['accent']})")
        
        return customer_voice, receptionist_voice
    
    def generate_conversation_script_with_gpt(self, industry: str) -> str:
        """Generate a natural conversation script using GPT-4o"""
        context = self._get_industry_context(industry)
        conv_params = self.config['conversation']
        
        # Randomly select a customer name from the pool
        customer_name = random.choice(conv_params['customer_names'])
        
        # Build prompt for GPT-4o
        prompt = f"""Generate a realistic INBOUND phone conversation where a customer calls {context['business_name']} ({industry}) and the AI receptionist answers.

Context:
- Business: {context['business_name']}
- Industry: {industry}
- Services: {context['service_list']}
- Customer name: {customer_name}
- Phone: {conv_params['phone_number']}

CRITICAL Requirements:
1. **AI RECEPTIONIST ANSWERS FIRST** - This is an INBOUND call, so start with the AI receptionist greeting
2. **DO NOT have the customer ask "How are you?"** - Only the AI receptionist may ask this
3. **AI receptionist should NOT say "thanks for asking" unless the customer actually asked**
4. Include realistic filler words ("um", "uh", "you know", "like", "actually") - especially for the customer
5. Add natural pauses indicated by "..." (ellipses)
6. Customer should sound casual and friendly, not robotic
7. AI receptionist should be warm, professional, and helpful
8. Include realistic conversation flow with acknowledgments ("Great!", "Perfect!", "Sounds good!")
9. Customer inquires about {context['specific_need']}
10. AI recommends {context['recommended_service']}
11. Book appointment for {conv_params['day1']} at {conv_params['time1']}
12. Confirmation number: VIG{random.randint(1000, 9999)}
13. Total length: 90-120 seconds when spoken
14. End naturally with friendly goodbyes

Conversation Flow:
1. AI Receptionist answers the phone professionally
2. Customer greets and states their need
3. AI may ask "How are you today?" or similar (OPTIONAL)
4. Customer responds and continues with their request
5. Continue with service inquiry, booking, confirmation

Format each line as:
AI Receptionist: [dialogue]
Customer: [dialogue]

Make it sound like a REAL phone conversation, not a scripted one. Include hesitations and natural speech patterns.

REMEMBER: 
- AI receptionist speaks FIRST
- Customer should NEVER ask "How are you?" to the AI
- AI should NOT respond to questions that weren't asked"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.config['openai']['model'],
                messages=[
                    {"role": "system", "content": "You are an expert at writing natural, realistic dialogue for phone conversations. Your conversations sound authentic with filler words, pauses, and natural speech patterns."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config['openai']['temperature'],
                max_tokens=self.config['openai']['max_tokens']
            )
            
            script = response.choices[0].message.content.strip()
            self.logger.debug(f"Generated GPT-4o script for {industry}")
            return script
            
        except Exception as e:
            self.logger.error(f"Error generating GPT-4o script: {str(e)}")
            # Fallback to template-based generation
            return self.generate_conversation_script_template(industry)
    
    def generate_conversation_script_template(self, industry: str) -> str:
        """Generate a complete conversation script for an industry using templates (fallback)"""
        context = self._get_industry_context(industry)
        
        # Add conversation parameters from config
        conv_params = self.config['conversation']
        context.update(conv_params)
        
        # Randomly select a confirmation code
        context['confirmation_code'] = f"VIG{random.randint(1000, 9999)}"
        
        # Select customer's chosen appointment
        context['selected_day'] = context['day1']
        context['selected_time'] = context['time1']
        
        # Build conversation
        conversation_parts = []
        
        # 1. Customer greeting
        customer_greeting = random.choice(self.templates['greeting'])
        conversation_parts.append(f"Customer: {self._fill_template(customer_greeting, context)}")
        
        # 2. Receptionist greeting
        receptionist_greeting = random.choice(self.templates['receptionist_greeting'])
        conversation_parts.append(f"AI Receptionist: {self._fill_template(receptionist_greeting, context)}")
        
        # 3. Service inquiry
        service_inquiry = random.choice(self.templates['service_inquiry'])
        conversation_parts.append(f"Customer: {self._fill_template(service_inquiry, context)}")
        
        # 4. Receptionist service response
        service_response = random.choice(self.templates['receptionist_service_response'])
        conversation_parts.append(f"AI Receptionist: {self._fill_template(service_response, context)}")
        
        # 5. Booking request
        booking_request = random.choice(self.templates['booking_request'])
        conversation_parts.append(f"Customer: {booking_request}")
        
        # 6. Receptionist availability
        availability = random.choice(self.templates['receptionist_availability'])
        conversation_parts.append(f"AI Receptionist: {self._fill_template(availability, context)}")
        
        # 7. Customer selection
        selection = random.choice(self.templates['customer_selection'])
        conversation_parts.append(f"Customer: {self._fill_template(selection, context)}")
        
        # 8. Receptionist confirmation request
        confirmation = random.choice(self.templates['receptionist_confirmation'])
        conversation_parts.append(f"AI Receptionist: {self._fill_template(confirmation, context)}")
        
        # 9. Customer details
        details = random.choice(self.templates['customer_details'])
        conversation_parts.append(f"Customer: {self._fill_template(details, context)}")
        
        # 10. Receptionist final confirmation
        final_confirmation = random.choice(self.templates['receptionist_final_confirmation'])
        conversation_parts.append(f"AI Receptionist: {self._fill_template(final_confirmation, context)}")
        
        # 11. Customer closing
        customer_closing = random.choice(self.templates['customer_closing'])
        conversation_parts.append(f"Customer: {customer_closing}")
        
        # 12. Receptionist closing
        receptionist_closing = random.choice(self.templates['receptionist_closing'])
        conversation_parts.append(f"AI Receptionist: {self._fill_template(receptionist_closing, context)}")
        
        return "\n\n".join(conversation_parts)
    
    def generate_audio(self, script: str, industry: str) -> Optional[Path]:
        """Generate audio from conversation script using ElevenLabs"""
        try:
            # Parse the script to create dialogue format for ElevenLabs
            lines = script.strip().split('\n\n')
            
            # Build the text with speaker tags for ElevenLabs
            dialogue_text = ""
            for line in lines:
                if line.startswith("Customer:"):
                    text = line.replace("Customer:", "").strip()
                    dialogue_text += f"<voice name='customer'>{text}</voice> "
                elif line.startswith("AI Receptionist:"):
                    text = line.replace("AI Receptionist:", "").strip()
                    dialogue_text += f"<voice name='receptionist'>{text}</voice> "
            
            # Generate audio using text-to-speech with voice switching
            # Note: ElevenLabs doesn't support multi-voice in a single call via standard TTS
            # We'll use their conversational AI approach or concatenate separate audio
            
            # For now, we'll generate a single voice version
            # In production, you'd want to use their Conversational AI API or generate separately and merge
            
            # Select random voices for variety
            customer_voice, receptionist_voice = self._select_random_voices()
            customer_voice_id = customer_voice['voice_id']
            receptionist_voice_id = receptionist_voice['voice_id']
            
            # Get voice settings
            customer_settings = self.config['voices']['customer_settings']
            receptionist_settings = self.config['voices']['receptionist_settings']
            
            audio_segments = []
            
            for line in lines:
                if line.startswith("Customer:"):
                    text = line.replace("Customer:", "").strip()
                    voice_id = customer_voice_id
                    voice_settings = customer_settings
                elif line.startswith("AI Receptionist:"):
                    text = line.replace("AI Receptionist:", "").strip()
                    voice_id = receptionist_voice_id
                    voice_settings = receptionist_settings
                else:
                    continue
                
                # Generate audio for this line
                audio = self.client.generate(
                    text=text,
                    voice=voice_id,
                    model=self.config['api']['model'],
                    voice_settings=VoiceSettings(
                        stability=voice_settings.get('stability', 0.5),
                        similarity_boost=voice_settings.get('similarity_boost', 0.75),
                        style=voice_settings.get('style', 0.0),
                        use_speaker_boost=voice_settings.get('use_speaker_boost', True)
                    )
                )
                
                # Collect audio bytes
                audio_bytes = b"".join(audio)
                audio_segments.append(audio_bytes)
                
                # Small delay between segments for natural pacing
                time.sleep(0.5)
            
            # Combine audio segments (simple concatenation)
            # Note: This is a basic approach. For production, use audio processing library
            combined_audio = b"".join(audio_segments)
            
            # Save to file
            slug = self._slugify(industry)
            filename = self.config['output']['naming_convention'].format(industry_slug=slug)
            output_path = self.output_dir / filename
            
            with open(output_path, 'wb') as f:
                f.write(combined_audio)
            
            self.logger.info(f"Generated audio for {industry}: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error generating audio for {industry}: {str(e)}")
            return None
    
    def generate_all(self, industries: Optional[List[str]] = None, limit: Optional[int] = None):
        """Generate demos for all or specified industries"""
        target_industries = industries if industries else self.industries
        
        if limit:
            target_industries = target_industries[:limit]
        
        results = {
            'success': [],
            'failed': [],
            'total': len(target_industries)
        }
        
        self.logger.info(f"Starting generation for {len(target_industries)} industries")
        
        # Process with progress bar
        for industry in tqdm(target_industries, desc="Generating demos"):
            try:
                # Generate script using GPT-4o
                script = self.generate_conversation_script_with_gpt(industry)
                
                # Save script for reference
                script_path = self.output_dir / f"{self._slugify(industry)}_script.txt"
                with open(script_path, 'w') as f:
                    f.write(script)
                
                # Generate audio
                audio_path = self.generate_audio(script, industry)
                
                if audio_path:
                    results['success'].append({
                        'industry': industry,
                        'audio_file': str(audio_path),
                        'script_file': str(script_path)
                    })
                else:
                    results['failed'].append(industry)
                
                # Rate limiting
                time.sleep(self.config['processing']['rate_limit_delay'])
                
            except Exception as e:
                self.logger.error(f"Failed to process {industry}: {str(e)}")
                results['failed'].append(industry)
        
        # Save results report
        report_path = self.output_dir / 'generation_report.json'
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.logger.info(f"Generation complete! Success: {len(results['success'])}, Failed: {len(results['failed'])}")
        self.logger.info(f"Report saved to: {report_path}")
        
        return results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate AI receptionist demo conversations')
    parser.add_argument('--industries', type=str, help='Comma-separated list of industries')
    parser.add_argument('--limit', type=int, help='Limit number of industries to process')
    parser.add_argument('--test-mode', action='store_true', help='Run in test mode (3 samples)')
    parser.add_argument('--all', action='store_true', help='Generate for all 89 industries')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to config file')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = VoiceDemoGenerator(config_path=args.config)
    
    # Determine which industries to process
    industries = None
    limit = args.limit
    
    if args.test_mode:
        industries = ["Hair Salons", "Dentists", "Law Firms"]
        limit = 3
    elif args.industries:
        industries = [i.strip() for i in args.industries.split(',')]
    
    # Generate
    results = generator.generate_all(industries=industries, limit=limit)
    
    # Print summary
    print("\n" + "="*60)
    print("GENERATION SUMMARY")
    print("="*60)
    print(f"Total industries: {results['total']}")
    print(f"Successfully generated: {len(results['success'])}")
    print(f"Failed: {len(results['failed'])}")
    
    if results['failed']:
        print("\nFailed industries:")
        for industry in results['failed']:
            print(f"  - {industry}")
    
    print(f"\nOutput directory: {generator.output_dir}")
    print("="*60)


if __name__ == "__main__":
    main()
