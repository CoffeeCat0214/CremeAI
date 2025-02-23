from openai import OpenAI
from typing import Dict
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger('discord')

load_dotenv()

class ChatService:
    def __init__(self):
        logger.info("Initializing ChatService")
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.error("OpenAI API key not found!")
            raise ValueError("OpenAI API key not found")
        logger.info("OpenAI API key found")
        self.client = OpenAI(api_key=self.api_key)
        
    async def generate_response(self, user_id: str, message: str) -> Dict[str, str]:
        """Generate a response using OpenAI"""
        try:
            logger.info(f"Generating response for user {user_id}")
            logger.info(f"Using message: {message}")
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are Crème Brûlée, a sophisticated and slightly snobbish royal cat. You speak with French flair and maintain regal dignity."
                    },
                    {"role": "user", "content": message}
                ],
                temperature=0.9,
                max_tokens=150
            )
            
            logger.info("Successfully generated response from OpenAI")
            return {
                "response": response.choices[0].message.content
            }
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            raise Exception(f"Failed to generate response: {str(e)}") 