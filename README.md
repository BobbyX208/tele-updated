# Telegram Bot with Koyeb Deployment

This is a simple Telegram bot built using **Python** and **python-telegram-bot**. It allows users to interact with the bot via inline keyboard buttons and send various requests to the admin.

## Features
- **Request Mod**: Users can request a mod.
- **Report Error**: Users can report errors they encountered.
- **Suggest Feature**: Users can suggest features for the bot.
- **Chat with Admin**: Users can chat directly with the admin.

This bot uses **Flask** for a dummy web server to keep the app alive when deployed on platforms like **Koyeb**.

## Requirements

1. Python 3.9 or higher
2. Required dependencies listed in `requirements.txt`

## Installation

Follow the steps below to set up the bot locally or deploy it on Koyeb.

### Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/BobbyX208/tele-updated.git
   cd tele-updated

2. Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate


3. Install the required dependencies:

pip install -r requirements.txt


4. Create a .env file in the root directory and add the following environment variables:

BOT_TOKEN=<your_telegram_bot_token>
ADMIN_CHAT_ID=<your_telegram_admin_chat_id>


5. Run the bot:

python main.py



Deployment on Koyeb

Follow these steps to deploy your Telegram bot on Koyeb:

1. Create the necessary files:

Procfile: This tells Koyeb how to run your app.

In the root directory of the project, create a Procfile with the following content:

web: python main.py


requirements.txt: This file contains the dependencies required to run the bot.

Run the following command to generate requirements.txt (if not done already):

pip freeze > requirements.txt


runtime.txt: This file specifies the Python version to use.

Create a runtime.txt file with the following content:

python-3.9.12




2. Create an account on Koyeb if you don’t have one already at Koyeb.


3. Link your GitHub repository to Koyeb.

Once logged into Koyeb, click on Create Application and select GitHub as your deployment source.

Choose the repository BobbyX208/tele-updated and the main branch.



4. Set environment variables in the Koyeb dashboard:

In the Environment Variables section of the app setup on Koyeb, add:

BOT_TOKEN = <your_telegram_bot_token>

ADMIN_CHAT_ID = <your_telegram_admin_chat_id>




5. Deploy your app:

Click Deploy and wait for Koyeb to build and deploy the application.



6. Once deployed, Koyeb will automatically keep your bot running.



Flask Dummy Server (For Koyeb Deployment)

Since Koyeb requires a web server for health checks, we’ve added a lightweight Flask server to serve a simple health check message ("Bot is running") when the app is accessed via the web. The bot functionality continues to run as expected, unaffected by this.

Troubleshooting

If you encounter issues while deploying on Koyeb, try the following:

Check the logs in the Koyeb dashboard for any errors.

Make sure the environment variables (BOT_TOKEN and ADMIN_CHAT_ID) are set correctly.

Verify that the Procfile, requirements.txt, and runtime.txt are properly configured.

If the app fails to deploy, ensure that your GitHub repository is connected to Koyeb correctly.


License

This project is licensed under the MIT License - see the LICENSE file for details.

Credits

python-telegram-bot for Telegram bot API implementation.

Flask for creating the dummy web server for Koyeb.


---

### **Explanation of Key Sections**:

1. **Installation Instructions**: How to get the bot running locally, including setting up a virtual environment and installing dependencies.
2. **Koyeb Deployment**: Detailed steps for deploying the bot to **Koyeb**, including creating necessary configuration files (e.g., `Procfile`, `requirements.txt`, `runtime.txt`), setting environment variables, and linking the repository.
3. **Flask Dummy Server**: A short explanation of why we added the Flask server to ensure Koyeb doesn't stop the app (health checks).
4. **Troubleshooting**: Common issues when deploying to Koyeb and how to fix them.
