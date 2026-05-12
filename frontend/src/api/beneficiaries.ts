import api from './index'

export interface Beneficiary {
  id: string
  user_id: string
  name: string
  email: string
  phone: string
  relation: string
  id_number: string
  is_identity_verified: boolean
  permission_vault: boolean
  permission_emotional: boolean
  permission_key_fragments: boolean
  is_notified: boolean
  notified_at: string | null
  notes: string
  created_at: string
}

export const beneficiariesApi = {
  list() {
    return api.get<Beneficiary[]>('/beneficiaries/')
  },
  create(data: Partial<Beneficiary>) {
    return api.post<Beneficiary>('/beneficiaries/', data)
  },
  update(id: string, data: Partial<Beneficiary>) {
    return api.put<Beneficiary>(`/beneficiaries/${id}`, data)
  },
  verify(id: string, data: { id_number: string }) {
    return api.post<Beneficiary>(`/beneficiaries/${id}/verify`, data)
  },
  delete(id: string) {
    return api.delete(`/beneficiaries/${id}`)
  },
}
