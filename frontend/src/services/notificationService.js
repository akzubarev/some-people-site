import request from "@/services/request"

export default {
    async viewed() {
        return await request.post(`/api/notifications/viewed/`)
    },
    async list() {
        return await request.get(`/api/notifications/`)
    },
    async saveSettings(payload) {
        return await request.post(`/api/notifications/save_settings/`, payload)
    },
    async sendMailing(payload) {
        return await request.put(`/api/mailing/`, payload)
    },
    async telegram() {
        return await request.get(`/api/telegram/`)
    }
}
