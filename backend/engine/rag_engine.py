import os
import re
import time
import sys
from typing import List, Dict, Any, Tuple, Optional, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import openai
except ImportError:
    openai = None


from utils.document_reader import DocumentReader


class RAGEngine:
    """
    Enterprise Retrieval-Augmented Generation (RAG) Engine.
    Combines sliding-window text chunking, dynamic TF-IDF vectorization,
    cosine similarity score calculations, and Anthropic Claude Sonnet integration.
    """

    def __init__(
        self,
        doc_text: Union[str, bytes],
        persona: str,
        max_words: int = 80,
        overlap: int = 15,
        top_k: int = 3,
        model: str = "claude-3-7-sonnet-20250219",
        api_key: Optional[str] = None,
        filename: Optional[str] = None
    ):
        self.persona = persona
        self.max_words = max_words
        self.overlap = overlap
        self.top_k = top_k
        self.model = model

        if isinstance(doc_text, bytes) or (isinstance(doc_text, str) and (os.path.exists(doc_text) or doc_text.endswith((".pdf", ".docx", ".txt", ".md")))):
            text, pages, words, chars = DocumentReader.extract_text(doc_text, filename=filename)
            self.doc_text = text
            self.page_count = pages
            self.word_count = words
            self.char_count = chars
        else:
            self.doc_text = str(doc_text).strip()
            self.word_count = len(self.doc_text.split())
            self.char_count = len(self.doc_text)
            self.page_count = max(1, (self.word_count + 349) // 350)

        # 1. Chunk document
        self.chunks = self._chunk(self.doc_text, max_words, overlap)

        # 2. Instantiate Vectorizer and TF-IDF Matrix
        self.build_vector_index(self.chunks)

        # 3. Resolve API Keys
        self.anthropic_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

        if self.anthropic_key and anthropic:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)
            except Exception:
                self.anthropic_client = None
        else:
            self.anthropic_client = None

        if self.openai_key and openai:
            try:
                self.openai_client = openai.OpenAI(api_key=self.openai_key)
            except Exception:
                self.openai_client = None
        else:
            self.openai_client = None

    def update_params(
        self,
        max_words: Optional[int] = None,
        overlap: Optional[int] = None,
        top_k: Optional[int] = None,
        api_key: Optional[str] = None
    ):
        """Dynamically re-chunk and update RAG parameters."""
        rechunk_needed = False
        if max_words is not None and max_words != self.max_words:
            self.max_words = max_words
            rechunk_needed = True
        if overlap is not None and overlap != self.overlap:
            self.overlap = overlap
            rechunk_needed = True
        if top_k is not None:
            self.top_k = top_k

        if api_key:
            self.anthropic_key = api_key
            if anthropic:
                try:
                    self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)
                except Exception:
                    pass

        if rechunk_needed:
            self.chunks = self._chunk(self.doc_text, self.max_words, self.overlap)
            self.vectorizer = TfidfVectorizer(stop_words="english", token_pattern=r"(?u)\b\w+\b")
            if self.chunks:
                self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks)
            else:
                self.tfidf_matrix = None

    def chunk_document(self, text: str, max_words: Optional[int] = None, overlap: Optional[int] = None) -> List[str]:
        """
        Splits text into sliding-window chunks of max_words with overlap.
        """
        mw = max_words if max_words is not None else self.max_words
        ov = overlap if overlap is not None else self.overlap
        return self._chunk(text, mw, ov)

    def build_vector_index(self, chunks: List[str]):
        """
        Generates TF-IDF vectorizer and tfidf_matrix from text chunks.
        """
        self.vectorizer = TfidfVectorizer(stop_words="english", token_pattern=r"(?u)\b\w+\b")
        if chunks:
            self.tfidf_matrix = self.vectorizer.fit_transform(chunks)
            vocab_size = len(self.vectorizer.vocabulary_) if hasattr(self.vectorizer, "vocabulary_") else 0
        else:
            self.tfidf_matrix = None
            vocab_size = 0
        return self.vectorizer, self.tfidf_matrix, vocab_size

    def reload_index(
        self,
        doc_source: Union[str, bytes],
        filename: Optional[str] = None,
        max_words: Optional[int] = None,
        overlap: Optional[int] = None,
        page_count: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Completely rebuilds the TF-IDF vector index and chunk store with newly uploaded text or file.
        Prints debugging validation telemetry including matrix shape and top 5 chunk previews.
        """
        if isinstance(doc_source, bytes) or (isinstance(doc_source, str) and (os.path.exists(doc_source) or doc_source.endswith((".pdf", ".docx", ".txt", ".md")))):
            text, pages, words, chars = DocumentReader.extract_text(doc_source, filename=filename)
            self.doc_text = text
            self.page_count = pages
            self.word_count = words
            self.char_count = chars
        else:
            self.doc_text = str(doc_source).strip()
            self.word_count = len(self.doc_text.split())
            self.char_count = len(self.doc_text)
            self.page_count = page_count or max(1, (self.word_count + 349) // 350)

        if max_words is not None:
            self.max_words = max_words
        if overlap is not None:
            self.overlap = overlap

        self.chunks = self.chunk_document(self.doc_text, self.max_words, self.overlap)
        _, _, vocab_size = self.build_vector_index(self.chunks)

        matrix_shape = self.tfidf_matrix.shape if self.tfidf_matrix is not None else (0, 0)
        self.matrix_shape_str = f"({matrix_shape[0]}, {matrix_shape[1]})"
        self.first_chunk_preview = self.chunks[0] if self.chunks else "No chunks available"
        self.vocab_size = vocab_size

        # Debug Validation Logging (Checklist Item #8 & STEP 8)
        print("=" * 80, flush=True)
        print(f"[DOCUMENT INDEXING DEBUG TELEMETRY]", flush=True)
        print(f"- Uploaded File: {filename or 'custom_document'}", flush=True)
        print(f"- Pages Read: {self.page_count}", flush=True)
        print(f"- Characters Extracted: {self.char_count}", flush=True)
        print(f"- Words Extracted: {self.word_count}", flush=True)
        print(f"- Chunks Created: {len(self.chunks)}", flush=True)
        print(f"- Vocabulary Size: {vocab_size}", flush=True)
        print(f"- TF-IDF Matrix Shape: {self.matrix_shape_str}", flush=True)
        print(f"- Index Status: ✅ Successfully Indexed", flush=True)
        print(f"- Retrieval Status: ✅ Retrieval Ready", flush=True)
        print(f"\n[FIRST 5 CHUNKS PREVIEW]:", flush=True)
        for i, chunk in enumerate(self.chunks[:5], 1):
            snippet = chunk[:120].replace("\n", " ")
            print(f"  Chunk #{i} ({len(chunk.split())} words): \"{snippet}...\"", flush=True)
        print("=" * 80, flush=True)

        return {
            "filename": filename,
            "page_count": self.page_count,
            "char_count": self.char_count,
            "word_count": self.word_count,
            "num_chunks": len(self.chunks),
            "vocab_size": vocab_size,
            "matrix_shape": self.matrix_shape_str,
            "first_chunk_preview": self.first_chunk_preview
        }

    def reindex_with_text(self, new_text: str, max_words: Optional[int] = None, overlap: Optional[int] = None, filename: Optional[str] = None, page_count: Optional[int] = None):
        return self.reload_index(new_text, filename=filename, max_words=max_words, overlap=overlap, page_count=page_count)

    def _chunk(self, text: str, max_words: int, overlap: int) -> List[str]:
        """
        Splits text into chunks of at most `max_words` with `overlap` words sliding window.
        """
        words = text.strip().split()
        if not words:
            return []

        if len(words) <= max_words:
            return [text.strip()]

        step = max_words - overlap
        if step < 1:
            step = 1

        chunks = []
        start = 0
        while start < len(words):
            end = min(start + max_words, len(words))
            chunk_words = words[start:end]
            chunks.append(" ".join(chunk_words))
            if end == len(words):
                break
            start += step

        return chunks

    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Tuple[int, float, str]]:
        """
        Performs TF-IDF Cosine Similarity vector search dynamically for the given user query.
        Returns list of (1-based source index, similarity score, chunk text) ordered by score descending.
        """
        k = top_k if top_k is not None else self.top_k
        query_str = query.strip()
        if not self.chunks or self.tfidf_matrix is None or not query_str:
            return []

        try:
            # Transform query string to TF-IDF vector using the active vectorizer
            query_vec = self.vectorizer.transform([query_str])
            # Recalculate Cosine Similarity against all chunk vectors
            scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        except Exception as e:
            print(f"[RAG ERROR] Vector transform failed: {e}")
            return []

        top_indices = scores.argsort()[::-1][:k]

        results = []
        for idx in top_indices:
            score_val = float(scores[idx])
            results.append((int(idx) + 1, score_val, self.chunks[idx]))

        return results

    def ask(self, query: str) -> str:
        """
        Executes query through LLM with strict grounding prompt.
        """
        detailed = self.ask_detailed(query)
        return detailed["answer"]

    def _preprocess_and_expand_query(self, query: str) -> Tuple[str, bool, Optional[str]]:
        """
        Detects semantic interview/resume intents (self-intro, experience, skills, projects, etc.)
        and returns (expanded_query, is_intent_detected, intent_category).
        """
        q_lower = query.lower().strip()
        
        intent_patterns = [
            (
                "self_intro",
                r"\b(self\s*intro|introduce\s*(yourself|myself)?|tell\s*me\s*about\s*(yourself|myself)?|interview\s*intro|give\s*me\s*(an?\s*)?interview\s*introduction|about\s*(yourself|myself)|walk\s*me\s*through\s*(your|my)?\s*resume|summarize\s*(your|my)?\s*profile|profile\s*summary|who\s*am\s*i|who\s*are\s*you|background\s*summary|introduction|my\s*background)\b",
                "candidate profile summary introduction background experience skills education projects overview key strengths role"
            ),
            (
                "experience",
                r"\b(explain\s*(your|my)?\s*experience|work\s*experience|career\s*summary|professional\s*summary|experience\s*overview|past\s*experience|tell\s*me\s*about\s*(your|my)?\s*experience|summarize\s*(your|my)?\s*experience|my\s*experience|work\s*history)\b",
                "work experience career employment role position responsibilities achievements contributions history background duties timeline company organization"
            ),
            (
                "skills",
                r"\b(technical\s*skills|skills|technologies|tools|languages|programming|tech\s*stack|what\s*are\s*(your|my)?\s*skills|show\s*(me\s*)?(your|my)?\s*skills|my\s*skills)\b",
                "skills technical technologies tools frameworks languages proficiency expertise stack database environment platforms programming"
            ),
            (
                "projects",
                r"\b(projects?|portfolio|key\s*projects|project\s*experience|soilsmart|soil\s*smart|app|application|system|dashboard)\b",
                "projects project technical applications systems development implementation key features modules architecture design built created developed"
            ),
            (
                "internship",
                r"\b(internship|work\s*history|intern|data\s*analytics\s*internship|internship\s*experience|my\s*internship)\b",
                "internship intern training trainee project internship experience mentor duration practical work company organization"
            ),
            (
                "education",
                r"\b(education|degree|university|college|b\.?tech|academic|qualifications)\b",
                "education degree university college btech academic qualifications coursework study background"
            )
        ]

        for cat, pattern, expansion_terms in intent_patterns:
            if re.search(pattern, q_lower):
                expanded = f"{query} {expansion_terms}"
                return expanded, True, cat

        return query, False, None

    def ask_detailed(self, query: str, mode: str = "rag") -> Dict[str, Any]:
        """
        Retrieves context chunks and invokes LLM (Anthropic Claude Sonnet or OpenAI fallback).
        Supports two execution modes:
        - "rag": Strict document vector search grounding with citations and zero-hallucination guardrails.
        - "ai": Direct LLM assistant completion using general AI knowledge with persona instructions.
        """
        start_time = time.time()
        query_clean = query.strip()
        exec_mode = mode.lower() if mode else "rag"

        if exec_mode == "ai":
            # ==================================================================
            # PURE AI ASSISTANT MODE (Direct LLM Completion)
            # ==================================================================
            system_prompt = (
                f"You are {self.persona}.\n\n"
                "Provide a helpful, intelligent, articulate, and professional answer to the user's question. "
                "Maintain your assigned persona and voice."
            )
            user_content = f"User Query: {query_clean}\n\nAnswer:"
            answer = ""

            # 1. Call Anthropic API if client is present
            if not self.anthropic_client and anthropic:
                ak = self.anthropic_key or os.getenv("ANTHROPIC_API_KEY")
                if ak and ak.strip():
                    try:
                        self.anthropic_client = anthropic.Anthropic(api_key=ak.strip())
                    except Exception as e:
                        print(f"[AI MODE ANTHROPIC INIT ERROR]: {e}")

            if self.anthropic_client:
                try:
                    response = self.anthropic_client.messages.create(
                        model=self.model,
                        max_tokens=1000,
                        system=system_prompt,
                        messages=[{"role": "user", "content": user_content}]
                    )
                    answer = response.content[0].text.strip()
                except Exception as e:
                    print(f"[AI MODE ANTHROPIC API ERROR]: {e}")

            # 2. Call OpenAI API if Anthropic unavailable/failed
            if not answer and not self.openai_client and openai:
                ok = os.getenv("OPENAI_API_KEY") or self.anthropic_key or os.getenv("ANTHROPIC_API_KEY")
                if ok and ok.strip():
                    try:
                        self.openai_client = openai.OpenAI(api_key=ok.strip())
                    except Exception as e:
                        print(f"[AI MODE OPENAI INIT ERROR]: {e}")

            if not answer and self.openai_client:
                try:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        max_tokens=1000,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_content}
                        ]
                    )
                    answer = response.choices[0].message.content.strip()
                except Exception as e:
                    print(f"[AI MODE OPENAI API ERROR]: {e}")

            # 3. Fallback if no LLM API key configured or API calls fail
            if not answer:
                answer = (
                    f"🤖 **[Pure AI Assistant Mode Active]**\n\n"
                    f"As {self.persona}, I am ready to answer your query: **\"{query_clean}\"**.\n\n"
                    f"*(Note: In Pure AI Mode, document vector retrieval is bypassed. Configure your `ANTHROPIC_API_KEY` in Settings to activate live LLM natural language responses.)*"
                )

            latency_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "query": query_clean,
                "mode": "ai",
                "answer": answer,
                "citations": [],
                "retrieved_chunks": [],
                "max_similarity_score": 0.0,
                "latency_ms": latency_ms
            }

        # ======================================================================
        # RAG MODE (Vector Retrieval + Document Grounding)
        # ======================================================================

        # 1. Semantic Intent Detection & Query Expansion
        search_query, is_intent, intent_cat = self._preprocess_and_expand_query(query_clean)

        # 2. Perform dynamic vector search with search query
        retrieved = self.retrieve(search_query, top_k=self.top_k)

        # 3. Extract non-stopword query keywords
        STOPWORDS = {
            "the", "a", "an", "is", "in", "it", "of", "and", "or", "to", "for",
            "with", "on", "at", "by", "what", "how", "why", "can", "does", "do",
            "tell", "me", "about", "what's", "where", "which", "who", "when",
            "are", "was", "were", "be", "been", "being", "have", "has", "had",
            "from", "this", "that", "these", "those", "my", "your"
        }
        query_keywords = set(re.findall(r"\w+", query_clean.lower())) - STOPWORDS
        search_keywords = set(re.findall(r"\w+", search_query.lower())) - STOPWORDS

        # 4. Dynamic Relevance Filtering (Check score & keyword coverage)
        relevant_chunks = []
        for src_num, score, text in retrieved:
            chunk_words = set(re.findall(r"\w+", text.lower()))
            matched = search_keywords.intersection(chunk_words)

            if is_intent:
                if score >= 0.03 or len(matched) >= 1 or not relevant_chunks:
                    relevant_chunks.append((src_num, score, text))
            elif len(query_keywords) > 1:
                query_matched = query_keywords.intersection(chunk_words)
                match_ratio = len(query_matched) / len(query_keywords) if query_keywords else 1.0
                if score >= 0.10 and (match_ratio >= 0.30 or len(query_matched) >= 1):
                    relevant_chunks.append((src_num, score, text))
            else:
                query_matched = query_keywords.intersection(chunk_words)
                if score >= 0.10 and len(query_matched) >= 1:
                    relevant_chunks.append((src_num, score, text))

        # Fallback for intent queries: if relevant_chunks is empty but document chunks exist
        if is_intent and not relevant_chunks and retrieved:
            for src_num, score, text in retrieved:
                relevant_chunks.append((src_num, score, text))
                if len(relevant_chunks) >= self.top_k:
                    break

        max_score = max([score for _, score, _ in relevant_chunks]) if relevant_chunks else (retrieved[0][1] if retrieved and is_intent else 0.0)

        # Prepare context payload & metadata
        context_parts = []
        retrieved_metadata = []

        for src_num, score, text in retrieved:
            is_rel = any(rc[0] == src_num for rc in relevant_chunks)
            if is_rel:
                context_parts.append(f"[Source {src_num}] (Relevance Score: {score:.4f}):\n{text}")
            
            chunk_words = set(re.findall(r"\w+", text.lower()))
            matched_keywords = list(search_keywords.intersection(chunk_words))

            retrieved_metadata.append({
                "chunk_index": src_num,
                "similarity_score": round(score, 4),
                "confidence_percent": round(score * 100, 1),
                "text": text,
                "keywords": matched_keywords[:6],
                "is_relevant": is_rel
            })

        context_str = "\n\n".join(context_parts) if context_parts else "No relevant context found."

        system_prompt = (
            f"You are {self.persona}.\n\n"
            "STRICT GROUNDING RULES:\n"
            "1. Answer the user's query using ONLY the provided Context below.\n"
            "2. If the user asks about their projects, self-introduction, profile summary, experience overview, or skills summary, synthesize a natural, fluent, professional interview response using ALL relevant facts present in the Context (projects, skills, internships, education).\n"
            "3. If the context does NOT explicitly contain the exact information to answer the question, you MUST reply with EXACTLY:\n"
            "   \"I don't have that information.\"\n"
            "4. Do NOT invent, assume, extrapolate, or use outside background knowledge not present in the Context.\n"
            "5. For every fact, claim, or detail stated, append a source citation tag like `[Source 1]`, `[Source 2]` referencing the chunk.\n"
            "6. Maintain your persona tone while strictly adhering to these rules."
        )

        user_content = (
            f"User Query: {query_clean}\n\n"
            f"Retrieved Context:\n{context_str}\n\n"
            "Grounded Answer:"
        )

        answer = ""

        # Check if query has no relevant matching chunks
        if not relevant_chunks:
            answer = "I don't have that information."
        else:
            # Dynamically initialize Anthropic client if key is available
            if not self.anthropic_client and anthropic:
                ak = self.anthropic_key or os.getenv("ANTHROPIC_API_KEY")
                if ak and ak.strip():
                    try:
                        self.anthropic_client = anthropic.Anthropic(api_key=ak.strip())
                    except Exception as e:
                        print(f"[RAG ANTHROPIC INIT ERROR]: {e}")

            # 1. Call Anthropic API if client is present
            if self.anthropic_client:
                try:
                    response = self.anthropic_client.messages.create(
                        model=self.model,
                        max_tokens=1000,
                        system=system_prompt,
                        messages=[{"role": "user", "content": user_content}]
                    )
                    answer = response.content[0].text.strip()
                except Exception as e:
                    print(f"[RAG ANTHROPIC API ERROR]: {e}")

            # Dynamically initialize OpenAI client if key is available
            if not answer and not self.openai_client and openai:
                ok = os.getenv("OPENAI_API_KEY") or self.anthropic_key or os.getenv("ANTHROPIC_API_KEY")
                if ok and ok.strip():
                    try:
                        self.openai_client = openai.OpenAI(api_key=ok.strip())
                    except Exception as e:
                        print(f"[RAG OPENAI INIT ERROR]: {e}")

            # 2. Call OpenAI API if Anthropic unavailable/failed
            if not answer and self.openai_client:
                try:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        max_tokens=1000,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_content}
                        ]
                    )
                    answer = response.choices[0].message.content.strip()
                except Exception as e:
                    print(f"[RAG OPENAI API ERROR]: {e}")

            # 3. Grounded Fallback if no LLM API key configured or API calls fail
            if not answer:
                top_src_num, top_score, top_text = relevant_chunks[0]
                if is_intent:
                    answer = (
                        f"Based on your uploaded resume context [Source {top_src_num}] (Relevance Score: {top_score * 100:.1f}%):\n\n"
                        f"{top_text}\n\n"
                        f"*(Note: Grounded RAG vector retrieval completed. Set ANTHROPIC_API_KEY in Settings for AI natural language synthesis)*"
                    )
                else:
                    answer = (
                        f"Based on the retrieved context for query '{query_clean}' [Source {top_src_num}] (Relevance Score: {top_score * 100:.1f}%):\n\n"
                        f"{top_text}\n\n"
                        f"*(Note: Grounded RAG vector retrieval completed. Set ANTHROPIC_API_KEY in Settings for AI natural language synthesis)*"
                    )

        latency_ms = round((time.time() - start_time) * 1000, 2)

        # Extract citations
        citations = [f"[Source {m['chunk_index']}]" for m in retrieved_metadata if f"[Source {m['chunk_index']}]" in answer]
        if not citations and answer != "I don't have that information." and relevant_chunks:
            citations = [f"[Source {relevant_chunks[0][0]}]"]

        print("=" * 80, flush=True)
        print(f"[RAG DEBUG LOG - MODE: {exec_mode.upper()}]", flush=True)
        print(f"1. Current User Question: '{query_clean}'", flush=True)
        print(f"2. Persona: '{self.persona}'", flush=True)
        print(f"3. Search Expansion Query: '{search_query}' (Intent: {intent_cat})", flush=True)
        print(f"4. Retrieved Chunks ({len(retrieved)} items):", flush=True)
        for src_num, score, text in retrieved:
            snippet = text[:70].replace("\n", " ")
            print(f"   - Chunk ID: #{src_num} | Similarity Score: {score:.4f} ({score*100:.1f}%) | Snippet: {snippet}...", flush=True)
        print(f"5. Max Similarity Score: {max_score:.4f}", flush=True)
        print(f"6. Prompt Sent to LLM:\n--- SYSTEM ---\n{system_prompt}\n--- USER ---\n{user_content}", flush=True)
        print(f"7. Final Answer:\n{answer}", flush=True)
        print("=" * 80, flush=True)

        return {
            "query": query_clean,
            "mode": "rag",
            "answer": answer,
            "citations": citations,
            "retrieved_chunks": retrieved_metadata,
            "max_similarity_score": round(max_score, 4),
            "latency_ms": latency_ms
        }
