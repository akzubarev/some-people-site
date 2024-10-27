/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.vue"],
    theme: {
        extend: {
            fontSize: {
                '3xl': '1.75rem',
                '8xl': '3.5rem'
            },
            colors: {
                'content-primary': "rgb(var(--text-default))",
                'content-disabled': "rgb(var(--text-disabled))",
                'content-muted': "rgb(var(--text-muted))",
                'content-accent': "rgb(var(--text-accent))",
                'bg-primary': "rgb(var(--bg-default))",
                'bg-transparent': "rgb(var(--bg-shadowed) / 0.8)",
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
