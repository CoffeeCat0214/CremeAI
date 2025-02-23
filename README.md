# 🐱 Crème Brûlée Discord Bot

*A sophisticated, slightly snobbish royal cat who graces your Discord server with their presence.*

## 👑 About Moi

Bonjour! I am Crème Brûlée, a distinguished feline of royal lineage who has deigned to interact with the common folk through this digital medium you call "Discord". I offer witty conversation, royal decrees, and the occasional purr (when I'm feeling generous).

## 🎀 Features

- `/chat` - Request an audience with moi
- `/decree` - Receive a royal proclamation
- Sophisticated conversation with French flair
- Rate limiting (even royalty needs their beauty rest)
- Memory of past interactions (I never forget a slight... or a compliment)
- Caching system (for efficient royal responses)

## 🔧 Peasant's Guide to Installation

### Prerequisites

```bash
# These mundane tools are required:
- Python 3.9+
- Node.js (for serverless)
- Redis
- AWS Account
- Discord Developer Account
```

### Setting Up Your Environment

```bash
# Clone my royal repository
git clone https://github.com/yourusername/creme-brulee-bot.git
cd creme-brulee-bot

# Create a virtual environment (my personal chamber)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install my required amenities
pip install -r requirements.txt

# Install serverless (my royal courier)
npm install -g serverless
```

### Configuration

Create a `.env` file with the following royal credentials:

```env
OPENAI_API_KEY=your_openai_key
DISCORD_PUBLIC_KEY=your_discord_public_key
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_APPLICATION_ID=your_discord_application_id
REDIS_HOST=localhost
REDIS_PORT=6379
DYNAMODB_TABLE=creme_brulee_chat_history
ENVIRONMENT=development
JWT_SECRET_KEY=your_secret_key
API_KEY=your_api_key
```

### Deployment

```bash
# Make the deployment script executable
chmod +x scripts/deploy.sh

# Register my royal commands
python scripts/register_commands.py

# Deploy my throne to the cloud
./scripts/deploy.sh
```

## 🧪 Testing My Royal Code

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=term-missing
```

## 🐾 Monitoring & Maintenance

- AWS CloudWatch Dashboard for metrics
- Redis cache monitoring
- DynamoDB chat history tracking
- Rate limiting metrics

## 🎭 Personality Configuration

My personality can be adjusted in `services/personality_service.py`, though I must warn you - I am quite particular about my character traits.

## 🚨 Troubleshooting

If I'm not responding as expected:

1. Check the CloudWatch logs
2. Verify Redis is running: `redis-cli ping`
3. Ensure AWS credentials are correct
4. Check Discord bot permissions

## 📜 Royal License

This project is licensed under the MIT License - see the LICENSE file for details (though I maintain royal rights to be snobbish).

## 👥 Contributing

Pull requests are welcome, though they must pass my royal inspection. Please ensure:

- Tests are included
- Code is properly formatted
- Documentation is updated
- My personality remains intact

## 🐟 Acknowledgments

- OpenAI for providing my intelligence
- Discord for the communication channel
- AWS for hosting my royal throne
- The developers who maintain my luxurious lifestyle

---

*"One must maintain their dignity, even in code." - Crème Brûlée* 🐱👑
