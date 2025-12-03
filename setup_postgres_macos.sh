#!/bin/bash
# Ouvrir VSCode en mode Administrateur et exécuter :
# chmod +x setup_postgres_macos.sh
# ./setup_postgres_macos.sh

set -e

DB_NAME="ma_base"
DB_USER="devuser"
DB_PASSWORD="monmotdepasse"

echo "=== Installation de PostgreSQL (macOS) ==="

# Vérifier Homebrew
if ! command -v brew &> /dev/null; then
    echo "Homebrew n'est pas installé. Installe-le avec :"
    echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    exit 1
fi

brew update
brew install postgresql
brew services start postgresql

echo "=== Configuration PostgreSQL ==="

# Création utilisateur
psql postgres -c "DO \$\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$DB_USER') THEN
      CREATE ROLE $DB_USER LOGIN PASSWORD '$DB_PASSWORD';
   END IF;
END\$\$;"

# Création base
psql postgres -c "SELECT 'CREATE DATABASE $DB_NAME OWNER $DB_USER'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec"

# Exécuter init.sql
if [ -f "./database/init.sql" ]; then
    echo "Exécution de ./database/init.sql..."
    psql -d "$DB_NAME" -f "./database/init.sql"
fi

echo "=== PostgreSQL prêt sur macOS ! ==="
