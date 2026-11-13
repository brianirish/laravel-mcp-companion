Source: https://herd.laravel.com/docs/windows/troubleshooting/path.md

# PATH Configuration

## CLI commands are not recognized

If you receive errors like `'herd' is not recognized as an internal or external command` or `'php' is not recognized` when trying to run Herd commands in your terminal, the Herd bin folder is likely missing from your system's PATH environment variable.

You can check if Herd is in your PATH by running this command in PowerShell:

```ps1 theme={null}
$env:PATH -split ';' | Where-Object { $_ -like '*herd*' }
```

If Herd is correctly configured, you should see something like `C:\Users\YourUsername\.config\herd\bin`. If there's no output, you need to add the Herd bin folder to your PATH manually.

## Adding Herd to your PATH via Windows Settings

Press `Win + R`, type `sysdm.cpl`, and press Enter. Go to the **Advanced** tab and click **Environment Variables**. Under **User variables**, select **Path** and click **Edit**. Click **New** and add:

```
%USERPROFILE%\.config\herd\bin
```

Click **OK** on all dialogs to save the changes.

## Adding Herd to your PATH via PowerShell

Alternatively, you can run this command in an elevated PowerShell (Run as Administrator):

```ps1 theme={null}
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "User") + ";%USERPROFILE%\.config\herd\bin",
    "User"
)
```

## Applying the changes

After modifying the PATH, you need to reload the environment variables. You can apply the changes without restarting your terminal by running:

```ps1 theme={null}
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

Alternatively, close all terminal windows and open a new one. You can verify the fix by running `herd --version` or `php --version`.

## The bin folder doesn't exist

If the Herd bin folder at `%USERPROFILE%\.config\herd\bin` doesn't exist or is empty, reinstalling Herd will recreate it and set up the PATH correctly.
