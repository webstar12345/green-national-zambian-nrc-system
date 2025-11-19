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
        self.model = None
        self.chat = None
        
        # Only initialize model if API key is available
        if api_key:
            try:
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                self.initialize_chat()
            except Exception as e:
                print(f"Failed to initialize Gemini model: {e}")
                self.model = None
    
    def initialize_chat(self):
        """Initialize chat with system context"""
        if not self.model:
            return
        
        try:
            system_prompt = self.SYSTEM_CONTEXT.get(self.language, self.SYSTEM_CONTEXT['en'])
            self.chat = self.model.start_chat(history=[])
            # Send system context as first message
            self.chat.send_message(f"System Context: {system_prompt}")
        except Exception as e:
            print(f"Failed to initialize chat: {e}")
            self.chat = None
    
    def send_message(self, message):
        """Send message and get response"""
        # Check if API key is configured and model is initialized
        if not api_key or not self.model or not self.chat:
            return self.get_fallback_response(message)
        
        try:
            response = self.chat.send_message(message)
            return {
                'success': True,
                'message': response.text,
                'language': self.language
            }
        except Exception as e:
            # Fallback to predefined responses if API fails
            print(f"Gemini API error: {e}")
            return self.get_fallback_response(message)
    
    def change_language(self, new_language):
        """Change assistant language"""
        if new_language in self.LANGUAGES:
            self.language = new_language
            self.initialize_chat()
            return True
        return False
    
    def get_fallback_response(self, message):
        """Provide fallback responses when API is not available"""
        message_lower = message.lower()
        
        # Define responses for common questions
        responses = {
            'en': {
                'apply': "To apply for a new NRC:\n1. Click 'Apply' in the menu\n2. Choose 'New NRC Application'\n3. Fill in your personal details\n4. Upload required documents (birth certificate, parent's NRC, photo, proof of residence)\n5. Submit your application\n\nProcessing takes 14-30 days.",
                'documents': "Required documents:\n• Birth certificate\n• Parent/Guardian NRC copies\n• Passport-sized photo\n• Proof of residence\n• You must be 16 years or older",
                'time': "Application processing typically takes 14-30 days from submission. You can track your application status in 'My Applications'.",
                'replace': "To replace a lost/damaged NRC:\n1. Click 'Apply' → 'Replacement'\n2. Provide police report (if lost/stolen)\n3. Fill in details and upload documents\n4. Submit application\n\nYou'll receive your replacement within 14-30 days.",
                'track': "To track your application:\n1. Go to 'My Applications' in the menu\n2. View all your submitted applications\n3. Check the status (Pending, Under Review, Approved, Rejected)\n4. Download your NRC card when approved",
                'default': "I'm here to help with NRC applications! You can ask me about:\n• How to apply for a new NRC\n• Required documents\n• Processing time\n• Replacing a lost NRC\n• Tracking your application\n\nWhat would you like to know?"
            },
            'bem': {
                'apply': "Ukwapply sha NRC impya:\n1. Pindani 'Apply' mu menu\n2. Saleni 'New NRC Application'\n3. Lembapo details yenu\n4. Upload documents (birth certificate, NRC sha bafikala, photo, proof of residence)\n5. Submit application\n\nProcessing itola amasiku 14-30.",
                'documents': "Documents ishakufwaikwa:\n• Birth certificate\n• Copies sha NRC sha bafikala\n• Passport photo\n• Proof of residence\n• Imyaka 16 nangu ukupitila",
                'time': "Processing ya application itola amasiku 14-30. Mwingalanga status mu 'My Applications'.",
                'replace': "Ukureplace NRC ishalafwile:\n1. Pindani 'Apply' → 'Replacement'\n2. Leteni police report\n3. Lembapo details\n4. Submit application",
                'track': "Ukulanga application:\n1. Yani ku 'My Applications'\n2. Moneni applications yonse\n3. Chekeni status\n4. Download NRC card nga yavuminwa",
                'default': "Ndefwaya ukubafwila na NRC applications! Mwingabushapo:\n• Ukwapply sha NRC impya\n• Documents ishakufwaikwa\n• Processing time\n• Ukureplace NRC\n• Ukulanga application"
            },
            'nya': {
                'apply': "Kupanga application ya NRC yatsopano:\n1. Dinani 'Apply' mu menu\n2. Sankhani 'New NRC Application'\n3. Lembani zambiri zanu\n4. Upload documents (birth certificate, NRC ya makolo, chithunzi, proof of residence)\n5. Submit application\n\nProcessing imatenga masiku 14-30.",
                'documents': "Documents zofunika:\n• Birth certificate\n• Copies za NRC za makolo\n• Passport photo\n• Proof of residence\n• Zaka 16 kapena kupitirira",
                'time': "Processing ya application imatenga masiku 14-30. Mutha kuyang'ana status mu 'My Applications'.",
                'replace': "Kusintha NRC yotayika:\n1. Dinani 'Apply' → 'Replacement'\n2. Perekani police report\n3. Lembani zambiri\n4. Submit application\n\nMulandira NRC yanu m'masiku 14-30.",
                'track': "Kuyang'ana application:\n1. Pitani ku 'My Applications'\n2. Onani applications zonse\n3. Yang'anani status\n4. Download NRC card ikavomerezedwa",
                'default': "Ndili pano kuthandiza ndi NRC applications! Mutha kufunsa za:\n• Kupanga application ya NRC yatsopano\n• Documents zofunika\n• Nthawi yaitali\n• Kusintha NRC yotayika\n• Kuyang'ana application yanu"
            },
            'toi': {
                'apply': "Kupanga application ya NRC mpya:\n1. Kankani 'Apply' mu menu\n2. Salani 'New NRC Application'\n3. Lembani zyanu\n4. Upload documents (birth certificate, NRC ya bazyali, chifwaniso, proof of residence)\n5. Submit application\n\nProcessing itola masiku 14-30.",
                'documents': "Documents zyakuyanda:\n• Birth certificate\n• Copies zya NRC zya bazyali\n• Passport photo\n• Proof of residence\n• Myaka 16 na kuti kupita",
                'time': "Processing ya application itola masiku 14-30. Mulanga status mu 'My Applications'.",
                'replace': "Kusandula NRC yalafwide:\n1. Kankani 'Apply' → 'Replacement'\n2. Letani police report\n3. Lembani zyanu\n4. Submit application\n\nMuyotambula NRC yanu mu masiku 14-30.",
                'track': "Kulanga application:\n1. Yani ku 'My Applications'\n2. Mubone applications zyoonse\n3. Langani status\n4. Download NRC card naa yavuminwa",
                'default': "Ndili ano kubafwida a NRC applications! Mulabuzya:\n• Kupanga application ya NRC mpya\n• Documents zyakuyanda\n• Ciindi citola\n• Kusandula NRC yalafwide\n• Kulanga application yanu"
            },
            'loz': {
                'apply': "Ho etsa application ya NRC e ncha:\n1. Tobela 'Apply' mo menu\n2. Kgetha 'New NRC Application'\n3. Ngola lintlha tsa hao\n4. Upload documents (birth certificate, NRC ya batswadi, setshwantsho, proof of residence)\n5. Submit application\n\nProcessing e nka matsatsi 14-30.",
                'documents': "Documents tse di nyakwang:\n• Birth certificate\n• Copies tsa NRC tsa batswadi\n• Passport photo\n• Proof of residence\n• Dilemo 16 kamba ku feta",
                'time': "Processing ya application e nka matsatsi 14-30. U ka bona status mo 'My Applications'.",
                'replace': "Ho fetola NRC e lahlehileng:\n1. Tobela 'Apply' → 'Replacement'\n2. Fana ka police report\n3. Ngola lintlha\n4. Submit application\n\nU tla fumana NRC ya hao ka matsatsi 14-30.",
                'track': "Ho sheba application:\n1. Eya ho 'My Applications'\n2. Bona applications tsohle\n3. Sheba status\n4. Download NRC card ha e amohelwa",
                'default': "Ke teng ho thusa ka NRC applications! U ka botsa ka:\n• Ho etsa application ya NRC e ncha\n• Documents tse di nyakwang\n• Nako e telele hakae\n• Ho fetola NRC e lahlehileng\n• Ho sheba application ya hao"
            }
        }
        
        lang_responses = responses.get(self.language, responses['en'])
        
        # Match keywords to responses
        if any(word in message_lower for word in ['apply', 'application', 'new', 'first']):
            response_text = lang_responses['apply']
        elif any(word in message_lower for word in ['document', 'need', 'require', 'what']):
            response_text = lang_responses['documents']
        elif any(word in message_lower for word in ['time', 'long', 'how long', 'when', 'days']):
            response_text = lang_responses['time']
        elif any(word in message_lower for word in ['replace', 'lost', 'stolen', 'damage']):
            response_text = lang_responses['replace']
        elif any(word in message_lower for word in ['track', 'status', 'check', 'where']):
            response_text = lang_responses['track']
        else:
            response_text = lang_responses['default']
        
        return {
            'success': True,
            'message': response_text,
            'language': self.language
        }
    
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
