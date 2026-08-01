# Forge - Recipes

*Source: https://forge.laravel.com/docs/recipes*

---

## On this page
- [Introduction](#introduction)
- [Managing recipes](#managing-recipes)
  - [Creating recipes](#creating-recipes)
  - [Editing recipes](#editing-recipes)
  - [Deleting recipes](#deleting-recipes)
  - [Running recipes](#running-recipes)
- [Variables](#variables)
- [Laravel Forge recipes](#laravel-forge-recipes)
Basics
# Recipes
Copy pageCopy page
Save and run common Bash scripts across your servers.
Copy pageCopy page
## [​](#introduction) Introduction
Recipes allow you to save common Bash scripts and run them across any of your servers. For example, you could save a recipe to install MongoDB so you can conveniently run it on future servers.
## [​](#managing-recipes) Managing recipes
### [​](#creating-recipes) Creating recipes
To create a recipe, navigate to the “Recipes” page. Then, click the “New recipe” button. After providing a name, user and script, click the “Create recipe” button.
When your organization is using [teams](/docs/teams), you will also be able to choose who to share the recipe with. By default, this is everyone in your organization, but you may also share recipes with teams.
### [​](#editing-recipes) Editing recipes
To edit a recipe, navigate to the “Recipes” page. Then, click on the dropdown next to the recipe you want to edit. Click the “Edit” dropdown item and modify the recipe as required.
### [​](#deleting-recipes) Deleting recipes
To delete a recipe, navigate to the “Recipes” page. Then, click on the dropdown next to the recipe you want to delete. Click the “Delete” dropdown item and confirm that you do want to delete the recipe.
### [​](#running-recipes) Running recipes
To run a recipe, navigate to the “Recipes” page. Then, click on the dropdown next to the recipe you want to run. Click the “Run” dropdown item and select the servers you want to run the recipe on. You may also choose to send the recipe output via email.
Recipes will also create run logs which you can access by clicking on the recipe item. From here you may click on a run to see the full output.
## [​](#variables) Variables
Laravel Forge provides a few variables that can be used to make your recipe more dynamic. You are free to use any of these variables within your recipe’s script:
- `{{server_id}}` - The ID of the server that the recipe is running on
- `{{server_name}}` - The name of the server that the recipe is running on
- `{{ip_address}}` - The public IP address of the server
- `{{private_ip_address}}` - The private IP address of the server
- `{{username}}` - The server user who is running the script
- `{{db_password}}` - The database password for the server the script is running on
- `{{server_type}}` - The type of the server that the recipe is running on, i.e. one of the following…
  - `"app"`
  - `"cache"`
  - `"database"`
  - `"loadbalancer"`
  - `"meilisearch"`
  - `"web"`
  - `"worker"`
When using these variables, you should ensure that they exactly match the syntax shown above.
## [​](#laravel-forge-recipes) Laravel Forge recipes
Occasionally, Laravel Forge may provide recipes to perform adhoc fixes to your servers. These recipes may not be modified, but can be ran in the same way as typical recipes.
Was this page helpful?
YesNo
[SSH Keys](/docs/ssh)[API](/docs/api)
⌘I