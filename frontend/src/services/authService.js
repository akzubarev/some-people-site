import request from "@/services/request"
import requestNoauth from "@/services/request_noauth"

export default {
    async me(payload = undefined) {
        let response
        if (payload) {
            response = await request.put(`/api/users/me/`, payload)
        } else {
            response = await request.get(`/api/users/me/`)
        }
        return response
    },
    async user_stats(uuid) {
        return await request.get(`/api/users/get_stats/?uuid=${uuid}`)
    },
    async locationRating(params) {
        return await request.get(`/api/users/location_rating/`, {params})
    },
    async reactivate(payload) {
        return await request.post(`/api/users/resend_activation/`, payload)
    },
    async register(payload) {
        return await request.post(`/api/users/`, payload)
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
    async logout() {
        return await request.post(`/api/token/logout/`)
    },
    async countryRating(top) {
        return await request.get(`/api/users/country_rating/` + (top ? `?top=${top}` : ""))
    },
    async lastRegistrations() {
        return await request.get(`/api/users/last_registrations/`)
    },
    async stats() {
        return await request.get(`/api/users/stats/`)
    }
}
