import katya from '../../assets/images/mg/katya.png'
import liza from '../../assets/images/mg/liza.png'
import anya from '../../assets/images/mg/anya.png'
import lesha from '../../assets/images/mg/lesha.png'
import nastya from '../../assets/images/mg/nastya.png'
export const mgData: Record<string, { idx: number; name: string; status: string; description: string; image: string }> = {
    'cath_johns': {
        'idx': 1,
        'name': "Катя",
        'status': "Половина ГМа",
        'description': "Половина ГМа",
        'image': katya,
    },
    'lizakudl': {
        'idx': 2,
        'name': "Лиза",
        'status': "Вторая половина ГМа",
        'description': "Вторая половина ГМа",
        'image': liza,
    },
    'vakhannka': {
        'idx': 3,
        'name': "Аня",
        'status': "Биба",
        'description': "Биба",
        'image': anya,
    },
    'Томат': {
        'idx': 4,
        'name': "Леша",
        'status': "Боба",
        'description': "Почему мальчик с хуями вместо рук не сгорел в пожаре? Потому что рукописи не горят",
        'image': lesha,
    },
    'vash_ded': {
        'idx': 5,
        'name': "Настя",
        'status': "Джек",
        'description': "Я ебу гусей",
        'image': nastya,
    },

}