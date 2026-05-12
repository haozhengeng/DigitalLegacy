import api from './index'

export interface VaultItem {
  id: string
  user_id: string
  title: string
  category: string
  sub_category: string
  encrypted_content: string
  encrypted_note: string
  platform_name: string
  platform_url: string
  account_name: string
  importance: number
  is_legacy: boolean
  created_at: string
  updated_at: string
}

export const vaultApi = {
  list(category?: string) {
    const params = category ? { category } : {}
    return api.get<VaultItem[]>('/vault/', { params })
  },
  get(id: string) {
    return api.get<VaultItem>(`/vault/${id}`)
  },
  create(data: Partial<VaultItem>) {
    return api.post<VaultItem>('/vault/', data)
  },
  update(id: string, data: Partial<VaultItem>) {
    return api.put<VaultItem>(`/vault/${id}`, data)
  },
  delete(id: string) {
    return api.delete(`/vault/${id}`)
  },
}
