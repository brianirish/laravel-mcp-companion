Source: https://laravel.com/forge/docs/knowledge-base/networks.md

# Networks

> Common issues and solutions for Laravel Forge.

## Deleted SSH firewall rule

If you have deleted the firewall rule (typically port 22) from the Laravel Forge UI or directly on the server, Forge will be unable to connect to the server and will be unable to re-create this rule for you.

To fix this, you will need to access the server directly via your provider and manually add the SSH port again. DigitalOcean allows you to connect remotely through their dashboard.

Laravel Forge uses `ufw` for the firewall, so once you've connected to the server you need to run the following as `root`:

```bash theme={null}
ufw allow 22
```
