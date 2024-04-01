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
    async byId(id) {
        return await request.get(`/api/users/by_id/?id=` + id + "")
    },
    async user_stats(uuid) {
        return await request.get(`/api/users/get_stats/?uuid=` + uuid + "")
    },
    async byIds(ids) {
        return await request.get(
            `/api/users/by_ids/?id[]=` + ids.join("&id[]=") + ""
        )
    },
    async getActiveCountries() {
        return await request.get(`/api/users/get_active_countries/`)
    },
    async getGlobeData(params) {
        return await request.get(`/api/users/country_map/`, {params})
    },
    async locationRating(params) {
        return await request.get(`/api/users/location_rating/`, {params})
    },
    async activate(payload) {
        return await requestNoauth.post(`/api/users/activation/`, payload)
    },
    async reactivate(payload) {
        return await request.post(`/api/users/resend_activation/`, payload)
    },
    async register(payload) {
        return await request.post(`/api/users/`, payload)
    },
    async sendPassReset(payload) {
        return await request.post(`/api/users/reset_password/`, payload)
    },
    async passReset(payload) {
        return await request.post(`/api/users/reset_password_confirm/`, payload)
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
    async setViziEmail(payload) {
        return await request.post(`/api/users/set_vizi/`, payload)
    },
    async login(payload) {
        return await requestNoauth.post(`/api/token/login/`, payload)
    },
    async logout() {
        return await request.post(`/api/token/logout/`)
    },
    async topEarned(params) {
        const response = await request.get(`/api/users/top_earned/`, {params})
        return response
    },
    async countryRating(top) {
        const response = await request.get(
            `/api/users/country_rating/` + (top ? `?top=${top}` : "")
        )
        return response
    },
    async lastRegistrations() {
        const response = await request.get(`/api/users/last_registrations/`)
        return response
    },
    async stats() {
        const response = await request.get(`/api/users/stats/`)
        return response
    }
}
