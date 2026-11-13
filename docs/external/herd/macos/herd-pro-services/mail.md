Source: https://herd.laravel.com/docs/macos/herd-pro-services/mail.md

# Mail

# Working with emails

When you are working with emails locally, you need to make sure that these emails don't leave your machine and get sent to real users but it's also important to inspect them easily.

Herd Pro provides an SMTP mail server on your local machine that catches all outgoing emails instead of sending them to the world. It displays them in Herds own email client and provides rich debugging capabilities for all types of emails.

This saves you from sending emails to real users and frees you up from paying cloud services for developer email inboxes, not even requiring you to dig through log files when using the log driver. It's also super fast and organizes all emails per site.


## Setup

> [!NOTE]
>
> When using `laravel new` or Herd's site creation wizard, Herd configures the mail server in your `.env` file for you automatically.

The mail server uses the SMTP protocol to accept mails but instead of sending them to their recipient, it saves them to an internal database.

You can use the settings below and add them to your local `.env` file to receive mails in the Herd Pro mail app.

> [tab] Laravel
>
> ```bash .env theme={null}
> MAIL_MAILER=smtp
> MAIL_HOST=127.0.0.1
> MAIL_PORT=2525
> MAIL_USERNAME="${APP_NAME}"
> MAIL_PASSWORD=null
> MAIL_ENCRYPTION=null
> MAIL_FROM_ADDRESS="hello@example.com"
> MAIL_FROM_NAME="${APP_NAME}"
> ```

> [tab] WordPress
>
> ```php functions.php theme={null}
> function herd_mailer($phpmailer) {
>     $phpmailer->isSMTP();
>     $phpmailer->Host = '127.0.0.1';
>     $phpmailer->SMTPAuth = true;
>     $phpmailer->Port = 2525;
>     $phpmailer->Username = 'WordPress';
>     $phpmailer->Password = '';
> }
>
> add_action('phpmailer_init', 'herd_mailer');
> ```

> [tab] Other Frameworks
>
> Please refer to your framework specific documentation on how to configure outgoing emails and use the provided SMTP server host, port and username to connect to Laravel Herd.

The mail client groups incoming mails by the username of the mail sender. This allows you to create a dedicated inbox for each project.
Either specify a unique username manually, or use the `APP_NAME` environment variable to automatically use your application's name as the inbox name. Depending on your application name, you might need to set the username for your mailbox manually before emails show up in Herd.

## Changing the port

By default, the Herd Pro mail server runs on port `2525` but you can customize this configuration in the Mail section of the "Herd Pro" tab in the settings. Run `herd mail:config` to see the current host, port and the `.env` values for your application.


## Inspecting mails

You may inspect the header values of an email by opening the sidebar of the email window at the top right.

The HTML source of the email or the raw email content are available via right-click on the email itself. They open in a new window, and you can open raw or HTML content of multiple mails at the same time.


## Attachments

Herd stores all attachments in your Herd application directory and creates a folder for each email with all attached files. You can either open them from this folder or directly from the email.

```
~/Library/Application Support/Herd/Log/mail
```

## Deleting mails

You can delete single emails by selecting the email and pressing the `Backspace` key but if you want to get rid of a whole inbox, you can use the trash icon in the top bar of the mail window.

## Mails via the CLI

The `herd mail:*` commands give you access to all captured mails from your terminal. They are especially useful for testing flows like sign-ups or password resets, and for AI agents that need to click a verification link.

```bash theme={null}
# List the latest mails
herd mail:list

# Show the newest mail with a specific subject
herd mail:latest --subject="Verify Email Address"

# Wait for a new mail and show it
herd mail:wait --to=taylor@laravel.com

# Print all links of a mail
herd mail:links MAIL_ID
```

See the [CLI reference](https://herd.laravel.com/docs/macos/advanced-usage/herd-cli.md#mail-herd-pro) for all commands and options.

## Troubleshooting

If you accidentally sent thousands of emails to Herd or something is wrong, you can check the SQLite database file where Herd stores all emails. You can find the file at:

```
~/Library/Application Support/Herd/HerdCoreData.sqlite
```

You can truncate all mail related tables in this file without breaking the rest of the application.
