import praw
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Reddit API credentials
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID', # This will be e-mailed to you upon app creation
    client_secret='YOUR_CLIENT_SECRET', # This is listed within the Reddit app you've created
    user_agent='YOUR_APP_NAME', # Self explanatory
)

# List of your favorite subreddits
subreddits = ['Python', 'learnprogramming', 'technology']  # Add your favorite subreddits here

# Get top trending posts for the day
def get_trending_posts(subreddit):
    subreddit_obj = reddit.subreddit(subreddit)
    trending_posts = []

    for post in subreddit_obj.top('day', limit=5):  # Get top 5 posts of the day
        trending_posts.append(f"{post.title} ({post.score} upvotes)\n{post.url}\n")
        
    return trending_posts

# Compose the email content
def compose_email_content():
    email_content = ""
    for subreddit in subreddits:
        email_content += f"\nTrending in r/{subreddit}:\n"
        trending_posts = get_trending_posts(subreddit)
        email_content += "\n".join(trending_posts)
        email_content += "\n" + "-"*50 + "\n"
    return email_content

# Send the email
def send_email(report_content):
    from_email = 'your_email@example.com'
    to_email = 'recipient_email@example.com'
    subject = f'Daily Reddit Report - {datetime.now().strftime("%Y-%m-%d")}'
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(report_content, 'plain'))
    
    # Configure your SMTP server (example: Gmail)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, 'your_email_password')  # Use app-specific passwords for Gmail, never use your ACTUAL password, even if you're running this locally
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    report_content = compose_email_content()
    send_email(report_content)
