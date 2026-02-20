# 🤖 UniBot.ai - Admin-Controlled Academic RAG Chatbot

![Banner Placeholder](<img width="268" height="223" alt="Screenshot 2026-02-20 223431" src="https://github.com/user-attachments/assets/c1212640-997a-47e3-ac88-2ead407be98e" />
)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97-Hugging%20Face-FFD21E?style=for-the-badge)](https://huggingface.co/)
[![Supabase](https://img.shields.io/badge/Supabase-Database-3EC189?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/stebyvarghese1/unibot.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**UniBot.ai** is a state-of-the-art, privacy-focused AI chatbot designed specifically for university environments. By leveraging **Retrieval-Augmented Generation (RAG)** via Hugging Face Inference API, it ensures that students receive accurate, official information strictly based on administrator-uploaded documents, eliminating the risk of AI hallucinations.

---

## ✨ Key Features

### 👨‍🎓 For Students
- **Context-Aware Chat**: Get answers to questions about syllabi, notes, and regulations.
- **Strict Accuracy**: Answers are cross-referenced with official university documents.
- **Modern UI**: Sleek, mobile-responsive chat interface with dark mode support.
- **Support for Images**: Automatic captioning for images using Vision Language Models.

### 🛡️ For Administrators
- **Document Management**: Upload PDF, DOCX, and PPT files seamlessly.
- **Web Scraping**: Auto-index university web pages for dynamic information retrieval.
- **Control Panel**: Manage document availability and trigger manual re-indexing.
- **Secure Access**: Robust authentication and role-based access control.

### 🏗️ Technical Excellence
- **Zero-Persistence Vectors**: FAISS index is rebuilt in-memory on startup for maximum privacy and data minimization.
- **PostgreSQL Optimization**: Custom indexes for lightning-fast retrieval of document chunks and chat logs.
- **Inference Fallbacks**: Multi-model fallback system (Mistral, Zephyr, Flan) ensures high availability for answer generation.

---

## 📸 Screenshots

| Student Chat Interface | Admin Dashboard |
| :---: | :---: |
| ![Chat UI](<img width="1919" height="909" alt="Screenshot 2026-02-20 224008" src="https://github.com/user-attachments/assets/0e5e7c8e-5e8c-4174-afce-5df3b5223793" />
)(<img width="1919" height="908" alt="Screenshot 2026-02-20 224056" src="https://github.com/user-attachments/assets/19cd26a4-9c0d-491e-b577-8eed0cc819b8" />
) | ![![Uploading Screenshot 2026-02-20 224008.png…]()
Admin Dashboard](<img width="1919" height="900" alt="Screenshot 2026-02-20 224416" src="https://github.com/user-attachments/assets/672b98f1-bb55-4406-9191-166141092e80" />
) |
| *Modern Dark Theme* | *Document Management* |

---

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.10 or higher
- [Supabase](https://supabase.com/) Account (PostgreSQL & Storage)
- [Hugging Face API Token](https://huggingface.co/settings/tokens)

### 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/stebyvarghese1/unibot.ai.git
   cd unibot.ai
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   # Supabase Configuration
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   DATABASE_URL=your_postgresql_uri

   # AI Configuration (Hugging Face)
   HUGGINGFACE_API_TOKEN=your_hf_token
   HF_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   HF_LLM_MODEL=mistralai/Mistral-7B-Instruct-v0.2
   
   # Admin Credentials
   ADMIN_EMAIL=admin@university.edu
   ADMIN_PASSWORD=secure_password_here
   ```

5. **Run the Application**
   ```bash
   python run.py
   ```
   The app will be available at `http://localhost:5000`.

---

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Flask (Python), SQLAlchemy |
| **Frontend** | Vanilla JavaScript, Tailwind CSS, HTML5 |
| **Database** | PostgreSQL (Supabase) |
| **Storage** | Supabase Storage (Original Documents) |
| **Vector Search** | FAISS (In-memory) |
| **LLM Inference** | Hugging Face (Mistral-7B, Zephyr-7B) |
| **Embeddings** | Hugging Face (sentence-transformers) |
| **Vision** | Salesforce BLIP (Image Captioning) |

---

## 📐 How It Works (RAG Flow)

1. **Upload**: Admin uploads a document (PDF/DOCX/PPT).
2. **Process**: The system extracts text and splits it into semantic chunks.
3. **Index**: On startup, chunks are converted to embeddings using `sentence-transformers` and stored in an **in-memory FAISS index**.
4. **Query**: When a student asks a question, the system performing a similarity search to find the most relevant chunks.
5. **Generate**: A hosted LLM (Mistral/Zephyr) uses the retrieved chunks as context to generate an accurate answer.
6. **Fallback**: If the primary model fails or no relevant information is found, the system uses a fallback model or politely informs the user.


---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  Built with ❤️ for University Students and Educators.
</p>
