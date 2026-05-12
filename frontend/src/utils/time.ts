import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'

dayjs.extend(utc)

const CN_OFFSET = 8

export function formatCN(time: string | null | undefined, fmt = 'YYYY-MM-DD HH:mm'): string {
  if (!time) return ''
  return dayjs.utc(time).add(CN_OFFSET, 'hour').format(fmt)
}

export function formatDateCN(time: string | null | undefined): string {
  return formatCN(time, 'MM-DD HH:mm')
}
