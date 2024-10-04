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

**Troubleshooting:**

In order for this to work, you'll need the Python Reddit API Wrapper, or "Praw", and a way to send email from your host machine. I use Postfix. In your Postfix configuration, make sure to setup TLS configuration, and your app password in a 'sasl_passwd' file.

For example

```
relayhost = [smtp.gmail.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_tls_security_level = encrypt
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
```
Your app password in the sasl file would look like this

```
[smtp.gmail.com]:587 your_email@gmail.com:your_app_password
```

and then make sure permissions are set correctly

```
sudo chmod 600 /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db
```

An example configuration setup would look like this

```
smtpd_relay_restrictions = permit_mynetworks permit_sasl_authenticated defer_unauth_destination
myhostname = your_os.router.home
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
myorigin = /etc/mailname
mydestination = $myhostname, localhost, localhost.localdomain
relayhost = [smtp.gmail.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_sasl_mechanism_filter = plain, login
smtp_tls_security_level = encrypt
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
mailbox_size_limit = 0
recipient_delimiter = +
inet_interfaces = all
inet_protocols = ipv4
```

Note: I did some troubleshooting and it seems you need to set protocols to ipv4, or it may not work.

After you've made changes to Postfix, make sure you run

```
sudo systemctl restart postfix
```

If it's still not working for you, you may need to install the SASL Authentication Library, do this

```
sudo apt-get install libsasl2-modules sasl2-bin
```

Then

```
sudo nano /etc/postfix/sasl/smtpd.conf
```

And add these lines to the configuration file you've just opened

```
pwcheck_method: saslauthd
mech_list: plain login
```

After making these changes (if you needed them), run these commands

```
sudo systemctl restart postfix
sudo systemctl restart saslauthd
```

Send yourself a test e-mail to ensure all of this is working, by runmning this command

```
echo "Test email" | mail -s "SASL Test" your_mail@example.com
```

Watch logs with the command

```
sudo tail -f /var/log/mail.log
```

If you're not getting any logs, or terminal is throwing a 'not found' command, do this

```
sudo nano /etc/rsyslog.d/50-default.conf
```

Ensure this line is there

```
mail.*                        -/var/log/mail.log
```

If it isn't, add it.

Then, run this command

```
sudo systemctl restart rsyslog
```

Now, open the Postfix config again. If you've forgotten how to do that, run

```
nano /etc/postfix/main.cf
```

Ensure this line exists

```
maillog_file = /var/log/mail.log
```

If it doesn't, add it, then save, and restart Postfix again, and give a test e-mail a shot.

If you had to run through all of these steps, and you want to confirm that the_daily_report is working, open crontab and adjust the time at which the e-mail should be sent, and then check your e-mail.

Here's what mine looks like

![the_report_example](https://github.com/user-attachments/assets/1c0b223a-ef3b-4dcb-9054-b40195610fd9)

