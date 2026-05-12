import api from './index'

export interface EmotionalFile {
  id: string
  user_id: string
  title: string
  file_type: string
  file_path: string
  encrypted_content: string
  mime_type: string
  recipient_beneficiary_id: string | null
  is_delivered: boolean
  delivered_at: string | null
  created_at: string
  updated_at: string
}

export const emotionalApi = {
  list(fileType?: string) {
    const params = fileType ? { file_type: fileType } : {}
    return api.get<EmotionalFile[]>('/emotional/', { params })
  },
  get(id: string) {
    return api.get<EmotionalFile>(`/emotional/${id}`)
  },
  create(data: Partial<EmotionalFile>) {
    return api.post<EmotionalFile>('/emotional/', data)
  },
  update(id: string, data: Partial<EmotionalFile>) {
    return api.put<EmotionalFile>(`/emotional/${id}`, data)
  },
  delete(id: string) {
    return api.delete(`/emotional/${id}`)
  },
}
