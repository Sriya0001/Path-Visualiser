# Database Setup

This project uses MySQL to persist algorithm run history.

## Local Development (Docker)

To run the application locally with a database, we use Docker. 

1. Ensure Docker Desktop is running.
2. Start the database by running:
   ```bash
   docker-compose up -d
   ```
   This will start a MySQL 8 container with the following defaults (configured in `docker-compose.yml`):
   - **Host**: `localhost` (or `127.0.0.0`)
   - **Port**: `3307`
   - **Database Name**: `pathfinder`
   - **User**: `app`
   - **Password**: `app`

   *Note: These credentials are intentionally hardcoded for local development and are not suitable for production.*

3. The Flask application uses SQLAlchemy to automatically create the schema on startup. It connects using the `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` environment variables, which default to the local Docker setup if not provided.

## Production (AWS RDS)

Once deployed to AWS, you will **not** use the local Docker container. Instead, you can use a managed database like Amazon RDS (MySQL).

The application is designed so that a managed RDS instance will be a drop-in replacement. You will only need to update the environment variables (`DB_HOST`, `DB_PASSWORD`, etc.) on the production server to point to your RDS instance endpoint. The application code itself requires zero changes to support AWS RDS.
