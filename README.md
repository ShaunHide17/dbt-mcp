
In the root directory, you need to create a .env file which contains 
the required elements depending on whether you are doing a local
or remote deployment

# Local Deployment
```bash
# Python Settings
export PYTHONUNBUFFERED=1

# dbt & MCP Settings
export DBT_PROJECT_DIR=/Users/shaunhide/projects/data/transforms
export DBT_PATH=/Users/shaunhide/projects/data/.venv/bin/dbt
export DISABLE_SEMANTIC_LAYER=true
export DISABLE_DISCOVERY=true
export DISABLE_SQL=true
export DISABLE_ADMIN_API=true

# AI Model Settings
export OPENAI_API_KEY=<key>
export OPENAI_MODEL=openai:gpt-4o-mini

# Database Settings (in this case Postgres)
export DBT_POSTGRES_HOST=hostname_goes_here
export DBT_POSTGRES_USER=username_goes_here
export DBT_POSTGRES_PASSWORD=password_goes_here
export DBT_POSTGRES_PORT=port_goes_here
export DBT_POSTGRES_DB=database_goes_here
export DBT_POSTGRES_SCHEMA=schema_goes_here
```