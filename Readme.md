# SQLite Chat Assistant

A Python-based chat assistant that interacts with an SQLite database to answer natural language queries about employees and departments.
Visit [Chat Bot](https://sqlite-chatbot-tndq.onrender.com/) from here.

## Overview

This application provides a conversational interface to query company data stored in an SQLite database. Users can ask questions in plain English and receive formatted responses based on the database content.

## How It Works

### Architecture Components
1. **SQLite Database**: 
   - Stores employee and department data in two tables
   - Pre-populated with sample data (can be extended)

2. **Query Processing Engine**:
   - Uses regex patterns to map natural language to SQL queries
   - Supports 4 core query types:
     - List employees by department
     - Find department managers
     - Show employees hired after specific dates
     - Calculate department salary totals

3. **Web Interface**:
   - Simple Flask-based UI for interaction
   - Error handling for invalid inputs
   - Clean response formatting

## Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation & Running Locally

1. **Clone the repository**
```bash
git clone https://github.com/Gautam-bhatt-901/sqlite-chatbot.git
cd sqlite-chat-assistant