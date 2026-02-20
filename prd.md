# Product Requirements Document (PRD)

## Project Title

**Admin-Controlled Document-Based AI Chatbot for University Students**

---

## 1. Introduction

Universities generate a large volume of academic documents such as syllabi, lecture notes, regulations, timetables, and internal guidelines. Students often rely on informal sources or general-purpose AI chatbots, which may provide incorrect or unofficial information.

This project aims to develop an **AI-powered chatbot that answers student queries strictly based on administrator-uploaded academic documents**, ensuring accuracy, reliability, and institutional control.

The system follows a **privacy-aware, cost-free, and open-source-first approach**, making it suitable for academic deployment and evaluation.

---

## 2. Problem Statement

Students lack a centralized, reliable system to query official university documents. Existing AI tools:

* Hallucinate answers
* Use external internet knowledge
* Cannot be controlled by the institution

This leads to misinformation, confusion, and reduced trust in academic guidance systems.

---

## 3. Proposed Solution

A **web-based AI chatbot** that:

* Answers questions **only from documents uploaded by an administrator**
* Uses **Retrieval Augmented Generation (RAG)** to restrict responses
* Prevents hallucination by denying answers outside document scope
* Provides a **responsive student interface** and a **secure admin panel**

The system does **not store AI models or vector embeddings persistently**, ensuring ethical AI usage and data minimization.

---

## 4. User Roles & Permissions

### Admin

* Secure login
* Upload academic documents (PDF, DOCX, PPT)
* Trigger document re-indexing
* Manage document availability

### Student

* Login access
* Ask academic questions
* Receive answers based only on uploaded documents

---

## 5. Functional Requirements

### 5.1 Student Interface Module

* Responsive chat interface (mobile, tablet, desktop)
* Question submission via text input
* Display of AI-generated answers
* Fallback message if answer is unavailable

### 5.2 Admin Management Module (/admin)

* Secure authentication
* Document upload and management interface
* Supported formats: PDF, DOCX, PPT
* Trigger document re-indexing

### 5.3 Document Processing Module

* Text extraction from uploaded documents
* Chunking of documents for efficient retrieval
* Metadata association with documents

### 5.4 AI & Vector Search Module

* Question embedding using hosted API
* Similarity search using FAISS (in-memory)
* Retrieval of relevant document chunks

### 5.5 Answer Generation & Control Module

* Context-restricted answer generation using hosted LLM
* Prevention of responses outside document scope
* Standard fallback response for unavailable information

---

## 6. Non-Functional Requirements

* **No local AI model storage**
* **No persistent vector storage**
* High availability during runtime
* Privacy-preserving design
* Free and open-source technologies
* Simple deployment on cloud platforms

---

## 7. System Architecture Overview

### Architecture Pattern

**Retrieval Augmented Generation (RAG)**

Flow:

1. User submits a question
2. Question is converted to embedding
3. FAISS performs in-memory similarity search
4. Relevant document chunks are retrieved
5. Hosted LLM generates a context-restricted answer

---

## 8. Vector Search Design (Key Requirement)

* FAISS index exists **only in memory (RAM)**
* Index is rebuilt automatically on application startup
* No `.index` or embedding files are saved to disk
* On container restart, all embeddings are destroyed

This design ensures:

* Zero long-term AI data retention
* Compliance with data minimization principles
* Academic and ethical AI usage

---

## 9. Technology Stack

### Frontend

* HTML5
* Vanilla JavaScript
* Tailwind CSS (CDN)
* Fully responsive UI

### Backend

* Python 3
* Flask

### AI Services (Hosted)

* Hugging Face Inference API (LLM)
* Hugging Face Embedding API

### Vector Search

* FAISS (in-memory only)

### Database & Storage

* **Supabase**

  * PostgreSQL (users, roles, document metadata)
  * Supabase Storage (uploaded documents)

---

## 10. Hallucination Prevention Strategy

* No internet context provided to LLM
* Strict system prompt enforcement
* Answers generated only from retrieved document chunks
* Fallback response:

  > "Not available in uploaded documents"

---

## 12. Limitations

* Startup delay during re-indexing
* Free API rate limits
* Not designed for very large document sets

These limitations are acceptable for academic demonstration and evaluation.

---

## 13. Future Enhancements

* Multilingual support
* Voice-based queries
* Department-wise chatbots
* Analytics dashboard for admins
* Role-based access expansion

---

## 14. Conclusion

This project delivers a **secure, ethical, and academically robust AI chatbot** tailored for university environments. By combining hosted AI models with in-memory vector search and strict admin control, the system eliminates hallucination, preserves privacy, and ensures institutional trust.

The design is cost-free, open-source, and suitable for real-world academic deployment as well as MCA-level project evaluation.
