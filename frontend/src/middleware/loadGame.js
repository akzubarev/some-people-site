import store from "@/store"
import gamesService from "../services/gamesService";

export default async (id, {next}) => {
    gamesService.game(id).then(({data}) => {
        store.dispatch("setGame", data)
    })
}
