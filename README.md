# GenAI Finance Assistant (Work in Progress)

This project is an early stage implementation of a GenAI powered finance assistant designed to help analysts query and understand internal finance terminology and documentation using retrieval augmented generation (RAG).

The goal is to build a system that grounds large language model responses in structured finance data, making answers reliable, auditable, and suitable for a professional finance context.

⚠️ **Status: Work in Progress**  
This repository is under active development. Core components are being built incrementally and the system is not yet production ready.

## Current Progress

At this stage, the project focuses on data ingestion and preparation, which forms the foundation for retrieval and question answering.

Implemented so far:
- CSV ingestion pipeline that converts structured finance data into LLM readable text
- Deterministic text formatting for consistent downstream retrieval
- Basic traceability using source filename and row number
- Modular ingestion design intended to be callable when new data is uploaded
- Text chunking pipeline that converts raw text records into LangChain Documents
- Configurable chunk sizing with overlap for optimal retrieval
- Metadata preservation including term, category, source file, and line number
- Sub-chunking logic for records that exceed the maximum chunk size

The ingestion layer is intentionally isolated from embeddings, retrieval, and UI logic to keep the pipeline debuggable and extensible.

## Planned Architecture

The full system will follow a standard RAG pipeline:

1. Data ingestion  
   Structured data sources (CSV, internal documentation) converted into clean text records

2. Vector retrieval  
   Text records embedded and indexed using FAISS for semantic search

3. LLM generation  
   Responses generated strictly from retrieved context using OpenAI models

4. User interface  
   A lightweight Streamlit interface for interactive querying and source inspection

## What Is Not Implemented Yet

The following components are planned but not yet complete:
- Embedding and vector index creation
- Semantic retrieval and ranking
- LLM response generation with citations
- Streamlit based chat interface
- Guardrails for refusal and hallucination prevention

## Motivation

Finance workflows require accuracy, traceability, and controlled reasoning. This project prioritizes:
- Grounded answers over creative generation
- Explicit source attribution
- Predictable and auditable behavior

The system is intentionally being built bottom up, starting with data quality and traceability before adding model intelligence.

## Notes

This README will evolve as the project progresses. Implementation details, setup instructions, and usage examples will be added once the core pipeline is complete.
