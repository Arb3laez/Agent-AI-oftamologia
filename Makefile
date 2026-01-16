.PHONY: setup validate-groq up test deploy-staging deploy-production clean

setup:
	@echo "Setting up environment..."
	python -m venv venv
	@echo "Activate venv with: source venv/bin/activate (Linux/Mac) or .\\venv\\Scripts\\activate (Windows)"
	@echo "Then run: pip install -r orchestrator/requirements.txt -r agents/requirements.txt"

validate-groq:
	python scripts/validate_groq.py

up:
	docker-compose up --build

test:
	pytest tests/

deploy-staging:
	@echo "Deploying to staging..."
	kubectl apply -f infrastructure/k8s/orchestrator/
	kubectl apply -f infrastructure/k8s/agents/

deploy-production:
	@echo "Deploying to production..."
	# kubectl config use-context production
	kubectl apply -f infrastructure/k8s/orchestrator/
	kubectl apply -f infrastructure/k8s/agents/

clean:
	docker-compose down
	rm -rf __pycache__ venv
