import avatar from '../assets/images/default_avatar.png'
import brand from '../assets/images/logo/mg.svg'
import whaleLogo from '../assets/images/logo/whales.svg'
import whaleBackground from '../assets/images/games/whales/background.png'
import whaleHeader from '../assets/images/games/whales/header.png'
import whaleCharacter from '../assets/images/games/whales/character.png'
import whaleGroup from '../assets/images/games/whales/group.png'
import frostBackground from '../assets/images/games/frostpunk/background.png'
import frostHeader from '../assets/images/games/frostpunk/header.png'
import frostCharacter from '../assets/images/games/frostpunk/characters/default.png'

const icons = import.meta.glob<string>('../assets/images/games/frostpunk/groups/*.png',
  { eager: true, query: '?url', import: 'default' })
const groupNames: Record<string, string> = {
  'Администрация': 'admin', 'Порядок': 'order', 'Вера': 'faith', 'Ассамблея': 'ass',
  'Профсоюз': 'prof', 'ИИК': 'iik', 'Ноябристы': 'november', 'Диверсанты': 'diver',
  'Путь Вендиго': 'cannibal', 'Военные': 'war', 'Преступность': 'crime',
  'Черный Рынок': 'black_market', 'Агитаторы': 'agit', 'Дети': 'children',
}
export { avatar, brand, whaleLogo }
export function gameImages(alias: string) {
  return alias === 'frostpunk'
    ? { background: frostBackground, header: frostHeader, character: frostCharacter }
    : { background: whaleBackground, header: whaleHeader, character: whaleCharacter }
}
export function groupImage(alias: string, name: string) {
  return alias === 'frostpunk'
    ? icons['../assets/images/games/frostpunk/groups/' + groupNames[name] + '.png']
    : whaleGroup
}
