# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project, please report it by creating a **private security advisory** on GitHub:

1. Go to the [Security tab](https://github.com/brianirish/laravel-mcp-companion/security) of this repository
2. Click "Report a vulnerability" 
3. Provide details about the vulnerability

This will create a private discussion that only you and I can see until we decide how to handle it.

For non-security bugs, please use the regular [issue tracker](https://github.com/brianirish/laravel-mcp-companion/issues).

## Which versions get fixes

[VERSIONING.md](VERSIONING.md#which-versions-get-fixes) says which versions receive security fixes.

## Scope

This project is a Model Context Protocol (MCP) server for Laravel documentation. Security concerns mainly involve:
- Documentation parsing and serving
- Network communication
- Dependency vulnerabilities

## Trusted and untrusted input

**The documentation is other people's text.** The server holds pages written by Laravel, by the
maintainers of the packages it covers and by Laracasts, and hands them to your assistant as they
were published. A nightly job refetches them and the result is merged without a person reading
it. The server removes images and, from pages fetched as HTML, links, but it does not look for
text written to steer a model. Treat what the tools return the way you would treat a web page
your assistant has read: it can contain text written to instruct a model.

**A client is trusted over stdio and not over HTTP.** Over stdio the client is the program that
started the server. Over HTTP it is anyone who can reach the port, and authentication is off until
you configure it, so:

- the server binds `127.0.0.1` unless told otherwise, and checks the `Host` and `Origin` headers;
- `update_laravel_docs` answers with an error unless authentication is on or the server was
  started with `--allow-updates`;
- a string argument longer than 1,000 characters is refused.

`/healthz` and `/.well-known/mcp/server.json` answer without a token by design, and `/healthz`
reports the server's version. [OPERATIONS.md](OPERATIONS.md#running-over-http) has the details.

**The sites documentation is fetched from are trusted for content only.** An update follows a
redirect only over https and only to one of those sites or to GitHub, refuses a page over 20 MB
and an archive over 100 MB, and writes nothing outside the documentation directory.

## What to Expect

As this is a personal project maintained in my spare time, please expect:
- Response within 1-2 weeks for initial acknowledgment
- Best-effort fixes depending on severity and complexity
- Open communication about timeline and feasibility