#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== DNS Bot v2 - Local Setup Script ===${NC}\n"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed${NC}"
    echo "Install from: https://www.docker.com/products/docker-desktop"
    exit 1
fi
echo -e "${GREEN}✓ Docker is installed${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose is installed${NC}\n"

# Create .env file
echo "Creating backend .env file..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓ Created backend/.env${NC}"
else
    echo -e "${YELLOW}! backend/.env already exists${NC}"
fi

# Create frontend .env file
echo "Creating frontend .env file..."
if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    echo -e "${GREEN}✓ Created frontend/.env${NC}"
else
    echo -e "${YELLOW}! frontend/.env already exists${NC}"
fi

echo -e "\n${GREEN}Starting services...${NC}\n"

# Start Docker Compose services
docker-compose up -d

# Wait for services to be healthy
echo -e "\n${YELLOW}Waiting for services to start...${NC}"
sleep 10

# Check if services are running
echo -e "\n${GREEN}=== Service Status ===${NC}"
docker-compose ps

echo -e "\n${GREEN}=== URLs ===${NC}"
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "PostgreSQL: localhost:5432"
echo "Redis: localhost:6379"

echo -e "\n${GREEN}=== Next Steps ===${NC}"
echo "1. Set your API keys in backend/.env"
echo "2. Access the application at http://localhost:5173"
echo "3. View logs: docker-compose logs -f"
echo "4. Stop services: docker-compose down"

echo -e "\n${GREEN}Setup complete!${NC}\n"
