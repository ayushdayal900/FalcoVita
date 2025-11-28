# Google Chat Webhook Setup Guide

## How to Create a Google Chat Webhook

### Step 1: Create or Open a Google Chat Space

1. Open **Google Chat** (https://chat.google.com)
2. Create a new space or open an existing one where you want to receive appointment reminders
3. Name it something like "FalcoVita Appointment Reminders"

### Step 2: Create a Webhook

1. In your Google Chat space, click the space name at the top
2. Select **"Manage webhooks"** from the dropdown menu
3. Click **"Add webhook"**
4. Give it a name: `FalcoVita Appointment Reminders`
5. Optionally add an avatar URL: `https://img.icons8.com/color/96/000000/hospital-2.png`
6. Click **"Save"**
7. **Copy the webhook URL** - it will look like:
   ```
   https://chat.googleapis.com/v1/spaces/AAAAA/messages?key=XXXXX&token=XXXXX
   ```

### Step 3: Add Webhook to Your Environment

1. Open or create `d:\Projects\FalcoVita\backend\.env`
2. Add this line with your actual webhook URL:
   ```bash
   GOOGLE_CHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/AAAAA/messages?key=XXXXX&token=XXXXX
   ```

### Step 4: Test the Integration

Run the test script:
```bash
cd /mnt/d/Projects/FalcoVita
python backend/test_daily_reminders.py
```

You should see appointment reminders appear in your Google Chat space!

## Message Format

The reminders will appear as rich cards with:
- 🏥 Hospital icon and header
- Patient name
- Doctor name
- Appointment time
- Department
- Reminder message

## Fallback Behavior

- If `GOOGLE_CHAT_WEBHOOK_URL` is set → sends to Google Chat
- If not set or fails → falls back to email (MailHog)

## Security Notes

⚠️ **Important**: Keep your webhook URL secret!
- Don't commit it to version control
- The `.env` file is already in `.gitignore`
- Anyone with the webhook URL can send messages to your space
