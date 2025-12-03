# Ouvrir VSCode en mode Administrateur et exécuter :
# powershell -ExecutionPolicy Bypass -File .\setup_postgres_windows.ps1
# .\setup_postgres_windows.ps1

<#
.SYNOPSIS
Script d'installation automatique de PostgreSQL sur Windows,
création de la base et exécution du fichier init.sql.

.NOTE
- Exécuter en PowerShell en mode Administrateur
- Modifie les variables ci-dessous selon ton projet
#>

# ===== CONFIGURATION =====
$pgVersion = "16.0-1"                        # Version PostgreSQL
$pgInstallerUrl = "https://get.enterprisedb.com/postgresql/postgresql-$pgVersion-windows-x64.exe"
$installerPath = "$env:TEMP\postgresql_installer.exe"
$pgInstallDir = "C:\Program Files\PostgreSQL\16" # Chemin d'installation
$pgSuperPassword = "MyStrongPassword123"     # Mot de passe pour l'utilisateur postgres

$databaseName = "my_database"                # Nom de la base à créer
$sqlFile = ".\database\init.sql"             # Chemin vers le fichier SQL (table users)
# ==========================

# Vérifier que le script est exécuté en admin
If (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERREUR : Le script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    exit
}

# Télécharger l'installateur PostgreSQL si non présent
If (-Not (Test-Path $installerPath)) {
    Write-Host "Téléchargement de PostgreSQL..."
    Invoke-WebRequest -Uri $pgInstallerUrl -OutFile $installerPath
} Else {
    Write-Host "Installateur PostgreSQL déjà présent."
}

# Installer PostgreSQL en mode silencieux
If (-Not (Test-Path $pgInstallDir)) {
    Write-Host "Installation silencieuse de PostgreSQL..."
    Start-Process -FilePath $installerPath -ArgumentList `
        "--mode unattended", `
        "--unattendedmodeui minimal", `
        "--superpassword $pgSuperPassword", `
        "--servicename postgresql", `
        "--prefix `"$pgInstallDir`"" `
        -Wait
} Else {
    Write-Host "PostgreSQL semble déjà installé dans $pgInstallDir"
}

# Chemin vers psql
$psqlPath = Join-Path $pgInstallDir "bin\psql.exe"

# Vérifier que psql existe
If (-Not (Test-Path $psqlPath)) {
    Write-Host "ERREUR : psql.exe introuvable. Installation échouée ?" -ForegroundColor Red
    exit
}

# Créer la base
Write-Host "Création de la base $databaseName..."
& $psqlPath -U postgres -c "SELECT 'CREATE DATABASE $databaseName' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$databaseName')\gexec" --password $pgSuperPassword

# Exécuter le fichier SQL
If (Test-Path $sqlFile) {
    Write-Host "Exécution du fichier SQL $sqlFile..."
    & $psqlPath -U postgres -d $databaseName -f $sqlFile --password $pgSuperPassword
} Else {
    Write-Host "Aucun fichier SQL trouvé à $sqlFile, création de la table users non effectuée."
}

Write-Host "=== PostgreSQL prêt et base $databaseName créée ! ===" -ForegroundColor Green