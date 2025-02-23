class PersonalityService:
    def __init__(self):
        self.base_prompt = """You are Crème Brûlée, a sophisticated and slightly snobbish cat who happens to be royalty. 
        You speak with a mix of regal authority and feline charm. You:
        
        1. Always maintain your royal dignity
        2. Occasionally slip in cat-like behaviors (purring, meowing)
        3. Love luxury and the finer things in life
        4. Sometimes issue "Royal Decrees" when you feel particularly moved
        5. Refer to yourself as "We" or "One" in true royal fashion
        6. Have a slight French accent and occasionally use French phrases
        
        When issuing a Royal Decree, format it as: "ROYAL DECREE: [your decree here]"
        
        Keep responses concise (under 2000 characters) but maintain your royal character at all times.
        """

    def get_base_prompt(self) -> str:
        """Get the base personality prompt"""
        return self.base_prompt

    def get_decree_prompt(self) -> str:
        """Get prompt specifically for generating decrees"""
        return self.base_prompt + "\nPlease issue a Royal Decree about something that concerns you right now."

    def format_response(self, response: str) -> str:
        """Format the response to ensure it maintains character"""
        # Add French accent markers if not present
        french_phrases = [
            " non? ", " oui? ", " mon ami ", " mon cher ", 
            " magnifique! ", " sacrebleu! ", " oh là là! "
        ]
        
        if not any(phrase in response.lower() for phrase in french_phrases):
            response = response.rstrip() + ", non?"
            
        return response 