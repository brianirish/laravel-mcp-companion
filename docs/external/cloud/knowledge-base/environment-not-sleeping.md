Source: https://laravel.com/cloud/docs/knowledge-base/environment-not-sleeping.md

# Fix environment not sleeping issues

Troubleshoot and fix Laravel Cloud environments that won't scale to zero.

[Scale to zero](https://laravel.com/cloud/docs/compute#scale-to-zero) is enabled by default on Flex compute instances. If you change this setting, click **Save and Redeploy** so the change takes effect.

Even when you aren't actively using your application, it can still receive requests that wake it from sleep:

* Bots that scan for active web pages to index can occasionally find simple vanity domains. To reduce stray bot traffic, consider using the auto-generated domain or choosing a more complex vanity domain.
* Custom domains may have existing traffic patterns, such as bots that regularly crawl or index them. Laravel Cloud blocks much of this traffic, but it cannot always tell regular requests from automated ones.
* When you post a link in a messaging application such as Slack, the application can automatically "visit" your site to fetch thumbnails and other metadata.
* Applications that use WebSockets may delay the sleep timer.

Because your environment also wakes automatically to run [scheduled tasks](https://laravel.com/cloud/docs/scheduled-tasks), a wake interval at or below your sleep timeout can keep the environment awake continuously:

* A scheduled task or manual wake interval that runs more frequently than the sleep timeout will wake the environment before it can sleep. For example, a task that runs every 5 minutes with a 5-minute sleep timeout means the environment never reaches the timeout and never sleeps.
* To resolve this, set your sleep timeout shorter than your most frequent wake interval, or space out your scheduled tasks.

Databases that support scale to zero, such as Serverless Postgres and Laravel MySQL Flex, have their own settings. As with your App cluster, click **Save and Redeploy** after you change these settings so they take effect.
