import request from "@/services/request"

export default {
  async list(date) {
    const response = await request.get(
      `/api/events/` + (date ? `?date=${date}` : "")
    )
    return response
  },
  async schedule() {
    const response = await request.get(`/api/events/schedule/`)
    return response
  },
  async checkIn(eventId) {
    return await request.get(`/api/events/checkin/?event_id=${eventId}`);
  },
  async checkOut(eventId) {
    return await request.get(`/api/events/checkout/?event_id=${eventId}`);
  },
}
