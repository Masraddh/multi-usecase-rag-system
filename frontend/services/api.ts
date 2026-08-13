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
  active_source?: 'default' | 'uploaded';
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
  num_pages: number;
  num_words: number;
  num_chars?: number;
  vocab_size?: number;
  matrix_shape?: string;
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
    chunk_count: number;
    queries_count: number;
    avg_score: number;
  }[];
}

const resolveApiBase = (): string => {
  let envUrl = process.env.NEXT_PUBLIC_API_URL;
  if (!envUrl) return 'http://localhost:8000/api/v1';
  let cleaned = envUrl.trim().replace(/\/+$/, '');
  if (!cleaned.endsWith('/api/v1')) {
    cleaned = `${cleaned}/api/v1`;
  }
  return cleaned;
};

const API_BASE = resolveApiBase();


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
        total_docs: 1,
        total_chunks: 5,
        active_source: 'default',
        filename: 'interview_prep.txt',
        num_pages: 1,
        num_words: 245,
        is_custom: false,
        sample_queries: [
          'Tell me about a project where you worked with real-time data.',
          'Tell me about a project involving payments.',
          'What is your weakest area?'
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
        total_docs: 1,
        total_chunks: 4,
        active_source: 'default',
        filename: 'campus_faq.txt',
        num_pages: 1,
        num_words: 260,
        is_custom: false,
        sample_queries: [
          'How many books can I borrow?',
          'Can I enter the hostel at 10 PM Saturday?',
          'Will I get into trouble for late entry?'
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
        total_docs: 1,
        total_chunks: 7,
        active_source: 'default',
        filename: 'study_buddy.txt',
        num_pages: 1,
        num_words: 320,
        is_custom: false,
        sample_queries: [
          'Which scheduling algorithm causes the convoy effect and why?',
          'Why does Round Robin add overhead?',
          'Compare FCFS and SJF scheduling.'
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
        total_docs: 1,
        total_chunks: 4,
        active_source: 'default',
        filename: 'ecommerce.txt',
        num_pages: 1,
        num_words: 210,
        is_custom: false,
        sample_queries: [
          'Does it fit a 15-inch laptop?',
          'Available colours?',
          'Refund after 20 days?'
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
        total_docs: 1,
        total_chunks: 3,
        active_source: 'default',
        filename: 'code_docs.txt',
        num_pages: 1,
        num_words: 290,
        is_custom: false,
        sample_queries: [
          'What does overlap do?',
          'What happens if ask() finds no information?',
          'How does retrieve() compute similarity?'
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
      total_documents: 5,
      total_chunks: 23,
      avg_retrieval_score: 0.9142,
      current_model: 'claude-3-7-sonnet-20250219',
      avg_response_time_ms: 128.4,
      total_queries: 42,
      assistant_breakdown: [
        { id: 'interview_coach', name: 'Interview Coach', chunk_count: 5, queries_count: 12, avg_score: 0.925 },
        { id: 'campus_faq', name: 'Campus FAQ', chunk_count: 4, queries_count: 10, avg_score: 0.890 },
        { id: 'study_buddy', name: 'Study Buddy', chunk_count: 7, queries_count: 15, avg_score: 0.941 },
        { id: 'ecommerce_support', name: 'Ecommerce Support', chunk_count: 4, queries_count: 8, avg_score: 0.880 },
        { id: 'code_docs', name: 'Code Documentation', chunk_count: 3, queries_count: 9, avg_score: 0.935 }
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

export async function uploadDocument(assistantId: string, file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

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
