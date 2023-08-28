# Fact-Checker-WhatsApp-Bot

**Description:**
The Fact-Check Chatbot is a web application built using Flask, Twilio, Web Search, and backed by OpenAI API. It serves as an SMS-based fact-checking tool that evaluates the authenticity of information provided in user queries. The chatbot performs web searches, extracts relevant article text, and then generates responses backed with AI to user inquiries.

**Installation Instructions:**
1. Clone the repository: `git clone `
2. Navigate to the project directory: `cd fact-check-chatbot`
3. Create a virtual environment (optional but recommended): `python -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install the required dependencies: `pip install -r requirements.txt`
6. Set up environment variables:
- Obtain an OpenAI API key and set it as `OPENAI_API_KEY` in your environment.
7. Run the application: `python app.py`

**Use Instructions:**
1. The application listens for incoming SMS messages containing queries.
2. Send an SMS message to the specified endpoint with your query.
3. The chatbot will process the query, fact-check the information, and reply with a response indicating the authenticity of the information along with relevant sources.

**Contribution Instructions:**
Contributions to the project are welcome. To contribute:

1. Fork the repository on GitHub.
2. Clone your forked repository: `git clone `
3. Create a new branch for your feature: `git checkout -b feature-name`
4. Make necessary changes and commit them: `git commit -m "Add your message"`
5. Push your changes to your fork: `git push origin feature-name`
6. Create a pull request to the main repository's `main` branch.

**Project Contents and File Structure:**
- `app.py`: Main Python script containing the Flask application, GPT-3 interactions, and routing logic.
- `requirements.txt`: List of required Python packages and their versions.
- `venv/`: Virtual environment directory (optional but recommended).
- `README.md`: Project's README file providing an overview, installation instructions, usage guidelines, and contribution details.

This project showcases the integration of the GPT-3.5 Turbo model into a Flask application for real-time fact-checking via SMS. The codebase is modular and easily extensible for further improvements and features.
