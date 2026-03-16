#!/bin/bash
# DNS Bot v2 - Project Initialization Script (Shell wrapper)

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BOLD}${BLUE}Starting DNS Bot v2 Project Initialization${NC}\n"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 is available${NC}"

# Run the initialization script
echo -e "${BLUE}Running initialization script...${NC}\n"

python3 init-project.py

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}${BOLD}✓ Initialization completed successfully!${NC}\n"
    echo -e "${BOLD}Next steps:${NC}"
    echo -e "1. Edit backend/.env and add your API keys"
    echo -e "2. Run: ${BOLD}./setup.sh${NC} to start services"
    exit 0
else
    echo -e "\n${RED}✗ Initialization failed${NC}"
    exit 1
fi
