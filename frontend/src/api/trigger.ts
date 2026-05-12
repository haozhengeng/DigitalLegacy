import api from './index'

export interface TriggerConfig {
  id: string
  user_id: string
  is_enabled: boolean
  inactivity_days: number
  check_in_interval_days: number
  alert_t0_push: boolean
  alert_t3_sms: boolean
  alert_t7_contact: boolean
  last_check_in: string | null
  trigger_started_at: string | null
  trigger_completed_at: string | null
  is_triggered: boolean
  is_emergency_recalled: boolean
  created_at: string
  updated_at: string
}

export interface TriggerStatus {
  is_triggered: boolean
  is_emergency_recalled: boolean
  days_since_last_checkin: number
  inactivity_days: number
  trigger_stage: string
  next_alert_at: string | null
}

export interface TriggerLog {
  id: string
  user_id: string
  event_type: string
  description: string
  metadata_json: string
  created_at: string
}

export const triggerApi = {
  getConfig() {
    return api.get<TriggerConfig>('/trigger/config')
  },
  updateConfig(data: Partial<TriggerConfig>) {
    return api.put<TriggerConfig>('/trigger/config', data)
  },
  checkIn() {
    return api.post<{ message: string; last_check_in: string }>('/trigger/check-in')
  },
  getStatus() {
    return api.get<TriggerStatus>('/trigger/status')
  },
  emergencyRecall() {
    return api.post<{ message: string; is_emergency_recalled: boolean }>('/trigger/emergency-recall')
  },
  getLogs() {
    return api.get<TriggerLog[]>('/trigger/logs')
  },
}
