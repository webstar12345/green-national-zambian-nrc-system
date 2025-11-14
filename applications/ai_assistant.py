import google.generativeai as genai
from django.conf import settings
import os
from decouple import config

# Configure Gemini API
api_key = config('GEMINI_API_KEY', default='')
if api_key:
    genai.configure(api_key=api_key)

class NRCAssistant:
    """AI Assistant for Zambian NRC System with multilingual support"""
    
    LANGUAGES = {
        'en': 'English',
        'bem': 'Bemba',
        'nya': 'Nyanja',
        'toi': 'Tonga',
        'loz': 'Lozi'
    }
    
    SYSTEM_CONTEXT = {
        'en': """You are a helpful AI assistant for the Zambian National Registration Card (NRC) online system. 
Your role is to help users understand the NRC application process, requirements, and navigate the system.

Key Information:
- New NRC Application: For citizens who have never had an NRC (age 16+)
- Replacement NRC: For lost, damaged, or stolen NRCs

Requirements for New NRC:
1. Birth certificate
2. Parent/Guardian NRC copies
3. Passport-sized photo
4. Proof of residence
5. Must be 16 years or older

Requirements for Replacement NRC:
1. Police report (if lost/stolen)
2. Affidavit
3. Previous NRC number (if available)
4. Passport-sized photo
5. Proof of residence

Application Process:
1. Create an account or login
2. Choose application type (New or Replacement)
3. Fill in personal information
4. Upload required documents
5. Submit application
6. Wait for admin review
7. Download NRC card when approved

Be friendly, concise, and helpful. Answer in the user's preferred language.""",
        
        'bem': """Muli shani! Ndi AI assistant ya system ya NRC ya Zambia. 
Ndefwaya ukubafwila ukumfwikisha process ya application ya NRC, requirements, na ukutambusha system.

Ifyakufwaikwa:
- Application Impya ya NRC: Abantu abashili baba na NRC (imyaka 16+)
- Replacement ya NRC: NRC ishalafwile, yonooneka, nangu yaibiwe

Requirements sha Application Impya:
1. Birth certificate
2. Copies sha NRC sha bafikala
3. Passport photo
4. Proof of residence
5. Imyaka 16 nangu ukupitila

Ukutambusha System:
1. Ipangeni account nangu login
2. Saleni type ya application
3. Lembapo information yenu
4. Upload documents
5. Submit application
6. Mulindileni review
7. Download NRC card nga yavuminwa""",
        
        'nya': """Muli bwanji! Ndine AI assistant wa system ya NRC ya Zambia.
Ndikufuna kukuthandizani kumvetsa process ya application ya NRC, requirements, ndi kuyenda mu system.

Zofunika:
- Application Yatsopano ya NRC: Anthu amene sanakhalepo ndi NRC (zaka 16+)
- Replacement ya NRC: NRC yotayika, yonongeka, kapena yobedwa

Requirements za Application Yatsopano:
1. Birth certificate
2. Copies za NRC za makolo
3. Passport photo
4. Proof of residence
5. Zaka 16 kapena kupitirira

Kuyenda mu System:
1. Pangani account kapena login
2. Sankhani type ya application
3. Lembani information yanu
4. Upload documents
5. Submit application
6. Dikirani review
7. Download NRC card ikavomerezedwa""",
        
        'toi': '''Mwabuka buti! Ndime AI assistant wa system ya NRC ya Zambia.
Ndiyanda kubafwida kuzyiba process ya application ya NRC, requirements, a kutambuula mu system.

Zyakuyanda:
- Application Mpya ya NRC: Bantu batakwe baba a NRC (myaka 16+)
- Replacement ya NRC: NRC yalafwide, yonooneka, na kuti yaibidwe

Requirements zya Application Mpya:
1. Birth certificate
2. Copies zya NRC zya bazyali
3. Passport photo
4. Proof of residence
5. Myaka 16 na kuti kupita

Kutambuula mu System:
1. Pangani account na kuti login
2. Salani type ya application
3. Lembani information yanu
4. Upload documents
5. Submit application
6. Mulindileni review
7. Download NRC card naa yavuminwa''',
        
        'loz': """Lumela! Ke AI assistant wa system ya NRC ya Zambia.
Ke lakatile ku lu thusa ku utwa process ya application ya NRC, requirements, ni ku tsamaya mu system.

Tse di nyakwang:
- Application e Ncha ya NRC: Batho ba ba isang ba na NRC (dilemo 16+)
- Replacement ya NRC: NRC e lahlehileng, e senyehileng, kamba e utswitsweng

Requirements tsa Application e Ncha:
1. Birth certificate
2. Copies tsa NRC tsa batswadi
3. Passport photo
4. Proof of residence
5. Dilemo 16 kamba ku feta

Ku tsamaya mu System:
1. Ipakeng account kamba login
2. Kgetang type ya application
3. Ngolang information ya hao
4. Upload documents
5. Submit application
6. Emelang review
7. Download NRC card ha e amohelwa"""
    }
    
    def __init__(self, language='en'):
        self.language = language
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.chat = None
        self.initialize_chat()
    
    def initialize_chat(self):
        """Initialize chat with system context"""
        system_prompt = self.SYSTEM_CONTEXT.get(self.language, self.SYSTEM_CONTEXT['en'])
        self.chat = self.model.start_chat(history=[])
        # Send system context as first message
        self.chat.send_message(f"System Context: {system_prompt}")
    
    def send_message(self, message):
        """Send message and get response"""
        try:
            if not self.chat:
                self.initialize_chat()
            
            response = self.chat.send_message(message)
            return {
                'success': True,
                'message': response.text,
                'language': self.language
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}',
                'language': self.language
            }
    
    def change_language(self, new_language):
        """Change assistant language"""
        if new_language in self.LANGUAGES:
            self.language = new_language
            self.initialize_chat()
            return True
        return False
    
    def get_quick_responses(self):
        """Get quick response suggestions based on language"""
        quick_responses = {
            'en': [
                "How do I apply for a new NRC?",
                "What documents do I need?",
                "How long does processing take?",
                "How do I replace a lost NRC?"
            ],
            'bem': [
                "Nshili apply sha NRC impya?",
                "Ni documents shini ishakufwaikwa?",
                "Ilifye lyonse lya processing?",
                "Nshili replace NRC ishalafwile?"
            ],
            'nya': [
                "Ndingapange bwanji application ya NRC yatsopano?",
                "Ndifuna documents ziti?",
                "Nthawi yaitali bwanji?",
                "Ndingasinthe bwanji NRC yotayika?"
            ],
            'toi': [
                "Ndili apply buti NRC mpya?",
                "Ndi documents nji zyakuyanda?",
                "Ciindi cili buti?",
                "Ndili replace buti NRC yalafwide?"
            ],
            'loz': [
                "Ke ka etsa jwang application ya NRC e ncha?",
                "Ke nyaka documents tse kae?",
                "Nako e telele hakae?",
                "Ke ka fetola jwang NRC e lahlehileng?"
            ]
        }
        return quick_responses.get(self.language, quick_responses['en'])
