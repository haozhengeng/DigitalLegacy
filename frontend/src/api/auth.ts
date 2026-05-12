import api from './index'

export interface LoginData {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  username: string
  password: string
  display_name?: string
}

export const authApi = {
  login(data: LoginData) {
    return api.post('/auth/login', data)
  },
  register(data: RegisterData) {
    return api.post('/auth/register', data)
  },
  getMe() {
    return api.get('/auth/me')
  },
  updateMe(data: any) {
    return api.put('/auth/me', data)
  },
  enableMFA(data: { secret: string; code: string }) {
    return api.post('/auth/mfa/enable', data)
  },
  disableMFA() {
    return api.post('/auth/mfa/disable')
  },
}
