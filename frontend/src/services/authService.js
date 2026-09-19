import request from "@/services/request"
import requestNoauth from "@/services/request_noauth"

export default {
    async me(payload = undefined) {
        return await request.get(`/api/users/me/`)
    },
    async update_me(payload) {
        return await request.put(`/api/users/update_me/`, payload)
    },
    async telegramLink() {
        return await request.post('/api/users/telegram_link/')
    },
    async register(payload) {
        return await request.post(`/api/users/register/`, payload)
    },
    async delete(uuid, data) {
        return await request.delete(`/api/users/${uuid}/`, {data})
    },
    async changePassword(payload) {
        return await request.post(`/api/users/set_password/`, payload)
    },
    async requestEmailChange(payload) {
        return await request.post(`/api/users/request_change_email/`, payload)
    },
    async changeEmail(payload) {
        return await request.post(`/api/users/change_email/`, payload)
    },
    async login(payload) {
        return await requestNoauth.post(`/api/token/login/`, payload)
    },
    async logout(token) {
        return await request.post(`/api/token/logout/`, {}, {
            skipSessionGuard: true,
            headers: {Authorization: `Token ${token}`}
        })
    },
}
