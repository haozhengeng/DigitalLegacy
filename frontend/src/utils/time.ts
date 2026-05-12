import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

dayjs.extend(utc)
dayjs.extend(timezone)

const CN_TZ = 'Asia/Shanghai'

export function formatCN(time: string | null | undefined, fmt = 'YYYY-MM-DD HH:mm'): string {
  if (!time) return ''
  return dayjs(time).tz(CN_TZ).format(fmt)
}

export function formatDateCN(time: string | null | undefined): string {
  return formatCN(time, 'MM-DD HH:mm')
}
