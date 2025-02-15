/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.vue"],
    theme: {
        extend: {
            fontFamily: {
                primary: ["Montserrat"],
                'nanum-brush': ['"Nanum Brush Script"', 'cursive'],
            },
            colors: {
                'content-primary': "rgb(var(--content-primary))",
                'content-secondary': "rgb(var(--content-secondary))",
                'content-secondary-shadowed': "rgb(var(--content-secondary-shadowed))",
                'content-disabled': "rgb(var(--content-disabled))",
                'content-disabled-transparent': "rgb(var(--content-disabled) / 0.3)",
                'content-muted': "rgb(var(--content-muted))",
                'content-accent': "rgb(var(--content-accent))",
                'content-accent-1': "rgb(var(--content-accent-1))",
                'bg-primary': "rgb(var(--bg-default))",
                'bg-transparent': "rgb(0 0 0 / 0.75)",
                'bg-transparent-2': "rgb(0 0 0 / 0.4)",
                'bg-transparent-white': "rgb(255 255 255 / 0.2)",
                'whales-bg': "rgb(224 229 228)",
                'gradient-start': "rgb(var(--gradient-start))",
                'gradient-middle': "rgb(var(--gradient-end))",
                'gradient-end': "rgb(var(--gradient-end))",
                gray: {
                    400: '#8A9099',
                    700: '#262C33',
                    800: '#1D2126',
                    900: '#13161A',
                    1000: '#101114',
                },
            },
        },
    },
    plugins: []
}
