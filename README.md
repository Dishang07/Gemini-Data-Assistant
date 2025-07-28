# Gemini Data Assistant

A powerful AI-powered query assistant that combines document analysis with dataset querying capabilities using Google's Gemini AI model.

## 🚀 Features

- **Intelligent Query Routing**: Automatically determines whether to execute SQL queries or provide general responses
- **Document-Aware**: Can analyze and answer questions about documents and datasets
- **Interactive Web Interface**: Clean Streamlit frontend for easy interaction
- **Tool Calling**: Advanced function calling with Gemini AI for SQL execution and static responses
- **Error Handling**: Robust error handling for API calls and database operations

## 🏗️ Project Structure

```
doc-aware-fixed/
├── backend/
│   ├── main.py                 # FastAPI backend server
│   ├── query_router.py         # Gemini AI query routing logic
│   ├── personality_datasert.xlsx # Dataset file
│   ├── models/
│   │   ├── metadata.py         # Data models and metadata
│   │   └── prompt_templates.py # AI prompt templates
│   └── tools/
│       ├── semantic_answer.py  # Semantic response handling
│       ├── sql_executor.py     # SQL query execution
│       └── utils.py           # Utility functions
├── frontend/
│   └── app.py                 # Streamlit web interface
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Google Gemini API key
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dishang07/Gemini-Data-Assistant.git
   cd Gemini-Data-Assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

   To get a Gemini API key:
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create an API key
   - Copy it to your `.env` file

## 🚀 Usage

### Starting the Application

1. **Start the Backend Server**
   ```bash
   # Navigate to the project root
   cd doc-aware-fixed
   
   # Start the FastAPI server
   python -m uvicorn backend.main:app --reload --port 8000
   ```

2. **Start the Frontend (in a new terminal)**
   ```bash
   # Navigate to the frontend directory
   cd frontend
   
   # Start the Streamlit app
   streamlit run app.py
   ```

3. **Access the Application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Using the Query Interface

1. Open your browser to http://localhost:8501
2. Enter your question in the text input field
3. Click "Submit" to get AI-powered responses
4. The system will automatically:
   - Route SQL-related queries to the database
   - Provide general answers for other questions
   - Display results in JSON format

## 🔧 API Endpoints

### POST `/query`
Process user queries and return intelligent responses.

**Request Body:**
```json
{
  "query": "Your question here"
}
```

**Response Examples:**

SQL Query Response:
```json
{
  "type": "sql",
  "query": "SELECT * FROM dataset WHERE condition",
  "result": [...]
}
```

Static Response:
```json
{
  "type": "static",
  "response": "General answer to your question"
}
```

Error Response:
```json
{
  "type": "error",
  "message": "Error description"
}
```

## 🤖 AI Features

### Query Routing
The system uses Google Gemini's function calling capabilities to intelligently route queries:

- **SQL Queries**: Automatically detected and executed against the dataset
- **General Questions**: Handled with natural language responses
- **Error Handling**: Graceful fallbacks for parsing issues

### Tool Functions
- `execute_sql_query`: Executes SQL queries on the dataset
- `get_static_response`: Returns natural language answers

## 📊 Dataset

The application includes a personality dataset (`personality_datasert.xlsx`) that can be queried using natural language. Ask questions like:
- "Show me all records"
- "What personality types are in the dataset?"
- "Find people with specific traits"

## 🔒 Security

- Environment variables stored in `.env` (not tracked in Git)
- API keys properly secured
- Input validation and error handling
- CORS configuration for secure frontend-backend communication

## 🧪 Development

### Running in Development Mode

Backend with auto-reload:
```bash
uvicorn backend.main:app --reload --port 8000
```

Frontend with auto-reload:
```bash
streamlit run frontend/app.py
```

### Adding New Features

1. **Backend**: Add new endpoints in `backend/main.py`
2. **AI Logic**: Modify query routing in `backend/query_router.py`
3. **Frontend**: Update the Streamlit interface in `frontend/app.py`
4. **Tools**: Add new tool functions in `backend/tools/`

## 📝 Requirements

See `requirements.txt` for the complete list of dependencies. Key packages include:

- `fastapi` - Backend web framework
- `streamlit` - Frontend web interface
- `google-generativeai` - Gemini AI integration
- `pandas` - Data manipulation
- `python-dotenv` - Environment variable management
- `uvicorn` - ASGI server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

