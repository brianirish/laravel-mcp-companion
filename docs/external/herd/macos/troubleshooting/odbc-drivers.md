Source: https://herd.laravel.com/docs/macos/troubleshooting/odbc-drivers.md

# ODBC Drivers

# Using Microsoft ODBC Drivers on macOS

You might encounter the following error message when trying to use the Microsoft ODBC Driver for SQL Server on macOS:

> "This extension requires the Microsoft ODBC Driver for SQL Server to communicate with SQL Server."

In order to install the missing ODBC driver, please take a alook at the latest official [ODBC Driver installation guide](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16#microsoft-odbc-18) from Microsoft.

After installing the driver, you will need to manually symlink the Homebrew installed driver to the default location where the Microsoft ODBC Driver for SQL Server expects it to be. This can be done by running the following command:

```bash theme={null}
sudo ln -s /opt/homebrew/etc/odbcinst.ini /etc/odbcinst.ini
sudo ln -s /opt/homebrew/etc/odbc.ini /etc/odbc.ini
```
