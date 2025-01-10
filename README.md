# ComplimentAiBot

ComplimentAiBot is a Telegram bot that provides various interactive features such as sending compliments, flirts, photos, and quizzes. The bot also logs user interactions and can send scheduled messages.

## Features

- **Start Command**: `/start` - Starts the bot and sends a welcome message with a photo.
- **End Quiz Command**: `/cancel` - Ends the quiz and sends a message indicating the quiz has ended.
- **Send Photo**: Sends a random photo of a girl.
- **Send Flirt**: Sends a random flirt message with a photo.
- **Send Compliment**: Sends a random compliment with a photo.
- **Start Quiz**: Starts a quiz with multiple questions.
- **First Question**: Sends the first question of the quiz.
- **Next Question**: Sends the next question of the quiz based on the user's answer.
- **Losing Quiz**: Handles the scenario when the user answers incorrectly.
- **Get Logs Command**: `/get_logs` - Retrieves and displays the logs of user interactions (admin only).
- **Get User ID Command**: `/get_user_id` - Retrieves and displays the user's Telegram ID.
- **Scheduled Message**: Sends a daily message to a specified user at 9 a.m. Moscow time.

## Customization

### Environment Variables

- `API_TOKEN`: Your Telegram bot API token.
- `ADMIN_ID`: The Telegram user ID of the admin.
- `DATABASE_URL`: The URL of your PostgreSQL database.
- `YOUR_LOVE_ID`: The Telegram user ID of the user who will receive the daily message.

### Handlers

- **cmd_start**: Handles the `/start` command.
- **end_quiz**: Handles the `/cancel` command and ends the quiz.
- **send_photo**: Sends a random photo of a girl.
- **send_flirt**: Sends a random flirt message with a photo.
- **send_compliment**: Sends a random compliment with a photo.
- **start_quiz**: Starts the quiz.
- **first_question**: Sends the first question of the quiz.
- **next_question**: Sends the next question of the quiz.
- **losing_quiz**: Handles incorrect answers in the quiz.
- **get_logs**: Retrieves and displays the logs of user interactions (admin only).
- **log_user_id**: Retrieves and displays the user's Telegram ID.

### Scheduler

The bot uses `APScheduler` to schedule a daily message at 9 a.m. Moscow time. The message is sent to the user specified by the `YOUR_LOVE_ID` environment variable.

### Logging

User interactions are logged in a PostgreSQL database. The logs include the timestamp, user ID, username, and action.

## Setup

1. Clone the repository:
   git clone https://github.com/nkonshin/ComplimentAiBot
   cd ComplimentAiBot

2. Install the required dependencies:
   pip3 install -r requirements.txt

3. Set up your environment variables in a .env file:
   API_TOKEN=your_api_token
   ADMIN_ID=your_admin_id
   DATABASE_URL=your_database_url
   YOUR_LOVE_ID=your_love_id

4. Initialize the PostgreSQL database:
   psql -U your_username -h your_host -d bot_logs -f init_db.sql

5. Run the bot
   python3 bot.py

## Usage
   - **Start the bot by sending the /start command.**
   - **Use the /cancel command to end the quiz.**
   - **Use the /get_logs command to retrieve logs (admin only).**
   - **Use the /get_user_id command to get your Telegram user ID.**