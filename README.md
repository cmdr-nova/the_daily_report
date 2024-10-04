# the_daily_report

A python app for e-mailing yourself the top 5 trending posts in subreddits of your choice.

This is a very simple Python script for sending yourself something interesting to read in the morning. If you're not sure where or how to create a Reddit app in order to get this working, please follow this link: https://www.reddit.com/prefs/apps

In order to create an app password via Google, simply click-through into your security settings, and find the App Password option.

Presto!

Now, assuming you're on Mac or Linux, open a terminal and type 

``` 
crontab -e
``` 

Use Nano, it's the best, and easiest Linux text editor. No, I won't accept any criticism for saying that.

Now, once you're inside, type in this

```
0 9 * * * /usr/bin/python3 /path/to/your_script.py
```

And, of course, you can change this to your liking, and add whatever you want!
