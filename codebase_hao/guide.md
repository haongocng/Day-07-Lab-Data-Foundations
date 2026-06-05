# Lab 7 - Phase 2 (Group Task) Specification

## Objective

Evaluate how different data strategies affect retrieval quality in a simple RAG pipeline.

The goal is NOT to compare models. The goal is to compare:

* Chunking strategies
* Chunking parameters
* Metadata schemas
* Retrieval configurations

while using the same document collection.

---

# Domain Selection

Selected domain:

```text
Vietnamese Legal Documents
```

Dataset source:

```text
HuggingFace: thangvip/vietnamese-legal-qa
```

---

# Document Preparation

## Requirements

Collect:

```text
5-10 legal documents
```

Convert documents into:

```text
data/Data_Law_Transportation/*.md
```

Each file should contain:

```markdown
# Document Title

## Content

<legal article content>
```

Avoid storing raw JSON as retrieval documents.

Use only clean textual content.

---

# Metadata Schema

Each document must contain at least 2 useful metadata fields.
```

Metadata must be usable for:

```python
search_with_filter(...)
```

experiments.

---

# Benchmark Construction

Create:

```text
5 benchmark queries
```

and

```text
5 gold answers
```

Requirements:

* Queries should not be identical
* Queries should cover different legal topics
* Answers must be verifiable from documents

Suggested categories:

* factual retrieval
* multi-paragraph retrieval
* metadata-sensitive retrieval

Example:

Q:

```text
What are the conditions for establishing an enterprise?
```

Gold Answer:

```text
<ground-truth answer extracted from the document>
```

---

# Strategy Assignment

Each team member must use a different strategy.

Example:

## Member A

```text
FixedSizeChunker
chunk_size=300
overlap=50
```

## Member B

```text
FixedSizeChunker
chunk_size=500
overlap=100
```

## Member C

```text
RecursiveChunker
```

## Member D

```text
SemanticChunker
```

Optional:

```text
RecursiveChunker + Metadata Filtering
```

---

# Evaluation

Run all 5 benchmark queries using each strategy.

For every query record:

* Retrieved Top-3 chunks
* Similarity scores
* Agent answer
* Gold answer

---

# Comparison Criteria

Evaluate using the following metrics.

## 1. Retrieval Precision

Questions:

* Are Top-3 results relevant?
* Does retrieval return correct legal content?

---

## 2. Chunk Coherence

Questions:

* Is the chunk semantically complete?
* Is information split across chunks?

---

## 3. Metadata Utility

Questions:

* Does metadata filtering improve retrieval?
* Does filtering remove useful results?

Compare:

```python
search()
```

vs

```python
search_with_filter()
```

---

## 4. Grounding Quality

Questions:

* Is the answer supported by retrieved chunks?
* Can the source chunk be identified?

---

## 5. Data Strategy Impact

Questions:

* Which chunking strategy performs best?
* Why does it perform better on legal documents?

---

# Deliverables

## Group Deliverables

* 5-10 legal documents
* Metadata schema
* 5 benchmark queries
* 5 gold answers
* Retrieval comparison results

## Discussion Deliverables

Explain:

1. Which strategy performed best?
2. Which strategy performed worst?
3. Why?
4. Did metadata filtering help?
5. What failure cases were observed?

---

# Expected Outcome

Demonstrate that:

```text
Same documents
Same retrieval pipeline
Same model

Different chunking / metadata strategies

=> Different retrieval quality
```

Key lesson:

```text
Data Strategy > Model Selection
```
