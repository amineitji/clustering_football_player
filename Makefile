# Définitions des variables
PYTHON = python3
MAIN_SCRIPT = src/main.py
TEAM_NAME = Lyon  # Tu peux changer ce nom d'équipe par défaut

# Cible pour lancer le script avec un argument
run: $(MAIN_SCRIPT)
	$(PYTHON) $(MAIN_SCRIPT) --team_name $(TEAM_NAME)

# Cible pour nettoyer le dossier /viz_data
clean:
	rm -rf viz_data/*

# Cible pour spécifier le nom de l'équipe à la volée
run_team:
	@read -p "Enter team name: " TEAM_NAME; \
	$(PYTHON) $(MAIN_SCRIPT) --team_name $$TEAM_NAME

# Instructions d'aide
help:
	@echo "Usage:"
	@echo "  make run TEAM_NAME=<team_name>    # Exécute le script avec le nom d'équipe spécifié"
	@echo "  make clean                       # Supprime le contenu du dossier /viz_data"
	@echo "  make run_team                    # Exécute le script en demandant le nom de l'équipe"

