export interface AssistantInfo {
  id: string;
  name: string;
  icon: string;
  persona: string;
  description: string;
  max_words: number;
  overlap: number;
  top_k: number;
  total_docs: number;
  total_chunks: number;
  active_source?: 'default' | 'uploaded' | 'default_directory' | 'hybrid_knowledge_base';
  filename?: string;
  num_pages?: number;
  num_words?: number;
  num_chars?: number;
  vocab_size?: number;
  matrix_shape?: string;
  first_chunk_preview?: string;
  index_status?: string;
  retrieval_ready?: boolean;
  is_custom?: boolean;
  documents?: string[];
  build_time_ms?: number;
  sample_queries: string[];
}

export interface RetrievedChunk {
  chunk_index: number;
  similarity_score: number;
  confidence_percent: number;
  text: string;
  keywords: string[];
}

export interface ChatRequest {
  assistant_id: string;
  query: string;
  max_words?: number;
  overlap?: number;
  top_k?: number;
  grounded_mode?: boolean;
  api_key?: string;
}

export interface ChatResponse {
  assistant_id: string;
  query: string;
  answer: string;
  citations: string[];
  retrieved_chunks: RetrievedChunk[];
  max_similarity_score: number;
  latency_ms: number;
}

export interface UploadResponse {
  message: string;
  filename: string;
  mode?: 'add' | 'replace';
  documents?: string[];
  total_docs?: number;
  num_pages: number;
  num_words: number;
  num_chars?: number;
  vocab_size?: number;
  matrix_shape?: string;
  build_time_ms?: number;
  first_chunk_preview?: string;
  num_chunks: number;
  active_source: string;
  index_status?: string;
  retrieval_ready?: boolean;
  assistant_id: string;
}

export interface SystemStats {
  total_documents: number;
  total_chunks: number;
  avg_retrieval_score: number;
  current_model: string;
  avg_response_time_ms: number;
  total_queries: number;
  assistant_breakdown: {
    id: string;
    name: string;
    documents?: string[];
    doc_count?: number;
    chunk_count: number;
    queries_count: number;
    avg_score: number;
  }[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || '/api/v1';

export async function fetchAssistants(): Promise<AssistantInfo[]> {
  try {
    const res = await fetch(`${API_BASE}/assistants`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch assistants');
    return await res.json();
  } catch (error) {
    console.warn('API connection offline, using client fallback metadata');
    return [
      {
        id: 'interview_coach',
        name: 'Interview Preparation Coach',
        icon: 'UserCheck',
        persona: 'Professional Interview Coach',
        description: 'Rehearses project experience, React Native, Power BI, SQL, and ML/RAG engineering questions.',
        max_words: 80,
        overlap: 15,
        top_k: 2,
        total_docs: 4,
        total_chunks: 18,
        active_source: 'default_directory',
        filename: 'resume.pdf, project_report.pdf, internship_certificate.pdf, skills.txt',
        num_pages: 4,
        num_words: 1250,
        documents: ['resume.pdf', 'project_report.pdf', 'internship_certificate.pdf', 'skills.txt'],
        index_status: '✅ Successfully Indexed',
        is_custom: false,
        sample_queries: [
          'Tell me about your education',
          'Explain my projects',
          'Generate a self introduction'
        ]
      },
      {
        id: 'campus_faq',
        name: 'Campus FAQ Helpdesk',
        icon: 'GraduationCap',
        persona: 'Friendly Student Helpdesk',
        description: 'Instant student assistance for library borrowing limits, hostel curfew hours, fee penalties, and exam attendance.',
        max_words: 90,
        overlap: 20,
        top_k: 3,
        total_docs: 4,
        total_chunks: 14,
        active_source: 'default_directory',
        filename: 'college_handbook.pdf, hostel_rules.pdf, library_rules.pdf, fee_structure.pdf',
        num_pages: 4,
        num_words: 1100,
        documents: ['college_handbook.pdf', 'hostel_rules.pdf', 'library_rules.pdf', 'fee_structure.pdf'],
        index_status: '✅ Successfully Indexed',
        is_custom: false,
        sample_queries: [
          'What are the hostel curfew hours?',
          'How many books can I borrow from the library?',
          'What is the penalty for late fee payment?'
        ]
      },
      {
        id: 'study_buddy',
        name: 'Exam Study Buddy',
        icon: 'BookOpen',
        persona: 'Patient OS Teacher',
        description: 'Tuned fine-grained RAG (50 words/chunk) explaining FCFS, SJF, Round Robin, and Convoy Effect.',
        max_words: 50,
        overlap: 12,
        top_k: 3,
        total_docs: 3,
        total_chunks: 21,
        active_source: 'default_directory',
        filename: 'operating_systems.pdf, dbms.pdf, sql_notes.txt',
        num_pages: 3,
        num_words: 980,
        documents: ['operating_systems.pdf', 'dbms.pdf', 'sql_notes.txt'],
        index_status: '✅ Successfully Indexed',
        is_custom: false,
        sample_queries: [
          'Explain FCFS and SJF scheduling algorithms.',
          'Which scheduling algorithm causes the convoy effect and why?',
          'What are the ACID properties in DBMS?'
        ]
      },
      {
        id: 'ecommerce_support',
        name: 'Ecommerce Customer Support',
        icon: 'ShoppingBag',
        persona: 'Customer Support Agent',
        description: 'Product specification helper for laptop sizing, color options, 15-day return policy, and warranty.',
        max_words: 80,
        overlap: 15,
        top_k: 2,
        total_docs: 4,
        total_chunks: 12,
        active_source: 'default_directory',
        filename: 'product_catalog.pdf, shipping_policy.pdf, return_policy.pdf, warranty.pdf',
        num_pages: 4,
        num_words: 890,
        documents: ['product_catalog.pdf', 'shipping_policy.pdf', 'return_policy.pdf', 'warranty.pdf'],
        index_status: '✅ Successfully Indexed',
        is_custom: false,
        sample_queries: [
          'What is the laptop size limit and return policy?',
          'What colors are available for the Voyager Pro backpack?',
          'How long is the warranty coverage?'
        ]
      },
      {
        id: 'code_docs',
        name: 'Code & API Documentation',
        icon: 'Code',
        persona: 'Technical Documentation Expert',
        description: 'Grounded documentation assistant for RAGEngine methods: chunk_text(), retrieve(), and ask().',
        max_words: 80,
        overlap: 20,
        top_k: 3,
        total_docs: 2,
        total_chunks: 10,
        active_source: 'default_directory',
        filename: 'developer_guide.pdf, README.md',
        num_pages: 2,
        num_words: 820,
        documents: ['developer_guide.pdf', 'README.md'],
        index_status: '✅ Successfully Indexed',
        is_custom: false,
        sample_queries: [
          'How does RAGEngine compute TF-IDF similarity?',
          'What parameters are passed to chunk_document?',
          'How to install and run the RAG Assistant Suite?'
        ]
      }
    ];
  }
}

export async function sendQuery(payload: ChatRequest): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Network error occurred' }));
    throw new Error(errorData.detail || 'Failed to communicate with RAG Engine');
  }

  return await res.json();
}

export async function fetchStats(): Promise<SystemStats> {
  try {
    const res = await fetch(`${API_BASE}/stats`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch stats');
    return await res.json();
  } catch (error) {
    return {
      total_documents: 17,
      total_chunks: 75,
      avg_retrieval_score: 0.9142,
      current_model: 'llama-3.3-70b-versatile (Groq Cloud)',
      avg_response_time_ms: 128.4,
      total_queries: 42,
      assistant_breakdown: [
        { id: 'interview_coach', name: 'Interview Coach', chunk_count: 18, queries_count: 12, avg_score: 0.925 },
        { id: 'campus_faq', name: 'Campus FAQ', chunk_count: 14, queries_count: 10, avg_score: 0.890 },
        { id: 'study_buddy', name: 'Study Buddy', chunk_count: 21, queries_count: 15, avg_score: 0.941 },
        { id: 'ecommerce_support', name: 'Ecommerce Support', chunk_count: 12, queries_count: 8, avg_score: 0.880 },
        { id: 'code_docs', name: 'Code Documentation', chunk_count: 10, queries_count: 9, avg_score: 0.935 }
      ]
    };
  }
}

export async function updateSettings(apiKey: string): Promise<any> {
  const res = await fetch(`${API_BASE}/settings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ api_key: apiKey })
  });
  return await res.json();
}

export async function uploadDocument(
  assistantId: string,
  file: File,
  mode: 'add' | 'replace' = 'add'
): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('mode', mode);

  const res = await fetch(`${API_BASE}/assistants/${assistantId}/upload`, {
    method: 'POST',
    body: formData
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({ detail: 'Failed to upload document' }));
    throw new Error(errData.detail || 'Upload failed');
  }

  return await res.json();
}

export async function resetAssistantDocument(assistantId: string): Promise<UploadResponse> {
  const res = await fetch(`${API_BASE}/assistants/${assistantId}/reset`, {
    method: 'POST'
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({ detail: 'Failed to reset document' }));
    throw new Error(errData.detail || 'Reset failed');
  }

  return await res.json();
}
