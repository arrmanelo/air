.PHONY: help build up down logs clean restart simulator

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build all Docker containers
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs for all services
	docker-compose logs -f

clean: ## Remove all containers, volumes, and images
	docker-compose down -v --rmi all

restart: ## Restart all services
	docker-compose restart

simulator: ## Run IoT sensor simulator
	cd simulator && python sensor_simulator.py

status: ## Show status of all services
	docker-compose ps

db-shell: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U eco_monitor -d environmental_monitoring

backend-shell: ## Open bash shell in IoT service
	docker-compose exec iot_service bash

test: ## Run tests (TODO)
	@echo "Running tests..."
	# cd backend/iot_service && pytest

dev-setup: ## Setup development environment
	@echo "Setting up development environment..."
	cp .env.example .env
	@echo "Please edit .env file with your API keys"
	@echo "Then run: make build && make up"

prod-deploy: ## Deploy to production (TODO)
	@echo "Deploying to production..."
	# Add production deployment steps
