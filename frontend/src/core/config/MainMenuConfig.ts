import {useI18n} from "vue-i18n"

const DocMenuConfig = () => {
    const {t} = useI18n()
    return [
        {
            pages: [
                [
                    {
                        heading: t("menu.dashboard"),
                        route: "/dashboard",
                        svgIcon: require("@/assets/images/menu/home.svg")
                    },
                    {
                        heading: "Игры",
                        route: "/games",
                        svgIcon: require("@/assets/images/menu/about.svg")
                    }
                ]
            ]
        }
    ]
}

export default DocMenuConfig
