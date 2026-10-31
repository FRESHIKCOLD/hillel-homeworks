from dataclasses import dataclass, field
import random
import sys


@dataclass(frozen=True)
class Card:
    name: str
    kind: str
    cost: int = 0
    power: int = 0
    toughness: int = 0
    flying: bool = False
    haste: bool = False
    effect: str = ''
    value: int = 0
    text: str = ''
    mana_cost: str = ''
    oracle_text: str = ''
    type_line: str = ''


@dataclass
class Creature:
    card: Card
    uid: int
    tapped: bool = False
    sick: bool = True
    damage: int = 0


@dataclass
class Player:
    name: str
    deck: list
    hand: list = field(default_factory=list)
    board: list = field(default_factory=list)
    grave: list = field(default_factory=list)
    life: int = 20
    lands: int = 0
    used: int = 0
    land_played: bool = False
    color: str = 'R'

    @property
    def mana(self):
        return self.lands - self.used


DRAGONS = [
    Card(name='Raging Goblin', kind='creature', cost=1, power=1, toughness=1, flying=False, haste=True, mana_cost='{R}', oracle_text='Haste (This creature can attack and {T} as soon as it comes under your control.)', type_line='Creature — Goblin Berserker', text='Ускорение'),
    Card(name='Goblin Piker', kind='creature', cost=2, power=2, toughness=1, flying=False, haste=False, mana_cost='{1}{R}', oracle_text='', type_line='Creature — Goblin Warrior', text='Без дополнительных способностей.'),
    Card(name='Goblin Chariot', kind='creature', cost=3, power=2, toughness=2, flying=False, haste=True, mana_cost='{2}{R}', oracle_text='Haste (This creature can attack and {T} as soon as it comes under your control.)', type_line='Creature — Goblin Warrior', text='Ускорение'),
    Card(name='Canyon Minotaur', kind='creature', cost=4, power=3, toughness=3, flying=False, haste=False, mana_cost='{3}{R}', oracle_text='', type_line='Creature — Minotaur Warrior', text='Без дополнительных способностей.'),
    Card(name='Fire Elemental', kind='creature', cost=5, power=5, toughness=4, flying=False, haste=False, mana_cost='{3}{R}{R}', oracle_text='', type_line='Creature — Elemental', text='Без дополнительных способностей.'),
    Card(name='Volcanic Dragon', kind='creature', cost=6, power=4, toughness=4, flying=True, haste=True, mana_cost='{4}{R}{R}', oracle_text='Flying, haste', type_line='Creature — Dragon', text='Полёт; Ускорение'),
    Card(name='Shock', kind='spell', cost=1, power=0, toughness=0, flying=False, haste=False, mana_cost='{R}', oracle_text='Shock deals 2 damage to any target.', type_line='Instant', effect='damage', value=2, text='2 урона любой цели.'),
    Card(name='Lightning Strike', kind='spell', cost=2, power=0, toughness=0, flying=False, haste=False, mana_cost='{1}{R}', oracle_text='Lightning Strike deals 3 damage to any target.', type_line='Instant', effect='damage', value=3, text='3 урона любой цели.'),
    Card(name='Lava Spike', kind='spell', cost=1, power=0, toughness=0, flying=False, haste=False, mana_cost='{R}', oracle_text='Lava Spike deals 3 damage to target player or planeswalker.', type_line='Sorcery — Arcane', effect='player_damage', value=3, text='3 урона целевому игроку или planeswalker.'),
]
UNDEAD = [
    Card(name='Walking Corpse', kind='creature', cost=2, power=2, toughness=2, flying=False, haste=False, mana_cost='{1}{B}', oracle_text='', type_line='Creature — Zombie', text='Без дополнительных способностей.'),
    Card(name='Scathe Zombies', kind='creature', cost=3, power=2, toughness=2, flying=False, haste=False, mana_cost='{2}{B}', oracle_text='', type_line='Creature — Zombie', text='Без дополнительных способностей.'),
    Card(name='Barony Vampire', kind='creature', cost=3, power=3, toughness=2, flying=False, haste=False, mana_cost='{2}{B}', oracle_text='', type_line='Creature — Vampire', text='Без дополнительных способностей.'),
    Card(name='Catacomb Slug', kind='creature', cost=5, power=2, toughness=6, flying=False, haste=False, mana_cost='{4}{B}', oracle_text='', type_line='Creature — Slug', text='Без дополнительных способностей.'),
    Card(name='Zombie Goliath', kind='creature', cost=5, power=4, toughness=3, flying=False, haste=False, mana_cost='{4}{B}', oracle_text='', type_line='Creature — Zombie Giant', text='Без дополнительных способностей.'),
    Card(name='Dross Crocodile', kind='creature', cost=4, power=5, toughness=1, flying=False, haste=False, mana_cost='{3}{B}', oracle_text='', type_line='Creature — Zombie Crocodile', text='Без дополнительных способностей.'),
    Card(name='Murder', kind='spell', cost=3, power=0, toughness=0, flying=False, haste=False, mana_cost='{1}{B}{B}', oracle_text='Destroy target creature.', type_line='Instant', effect='destroy', value=0, text='Уничтожить целевое существо.'),
    Card(name="Sovereign's Bite", kind='spell', cost=2, power=0, toughness=0, flying=False, haste=False, mana_cost='{1}{B}', oracle_text='Target player loses 3 life and you gain 3 life.', type_line='Sorcery', effect='drain', value=3, text='Целевой игрок теряет 3 жизни, ты получаешь 3 жизни.'),
    Card(name="Night's Whisper", kind='spell', cost=2, power=0, toughness=0, flying=False, haste=False, mana_cost='{1}{B}', oracle_text='You draw two cards and lose 2 life.', type_line='Sorcery', effect='draw_lose', value=2, text='Возьми 2 карты и потеряй 2 жизни.'),
]
LANDS = {
    'Mountain': Card(name='Mountain', kind='land', cost=0, power=0, toughness=0, flying=False, haste=False, mana_cost='', oracle_text='({T}: Add {R}.)', type_line='Basic Land — Mountain', text='Даёт красную ману {R}.'),
    'Swamp': Card(name='Swamp', kind='land', cost=0, power=0, toughness=0, flying=False, haste=False, mana_cost='', oracle_text='({T}: Add {B}.)', type_line='Basic Land — Swamp', text='Даёт чёрную ману {B}.'),
}


class Game:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.players = [Player('Ты · Красная колода', self.make_deck(DRAGONS, 'Mountain')),
                        Player('Бот · Чёрная колода', self.make_deck(UNDEAD, 'Swamp'), color='B')]
        self.active = 0
        self.phase = 'main'
        self.turn = 1
        self.winner = None
        self.uid = 0
        self.attacked = False
        self.attackers = []
        self.blocks = {}
        self.log = []
        self.mulligan_used = False
        self.acted = False
        for i in (0, 1):
            self.draw(i, 7)
        self.say('Твой первый ход. Сыграй землю, затем существ или заклинания.')

    def make_deck(self, cards, land):
        deck = [LANDS[land]] * 24
        deck += [card for card in cards for _ in range(4)]
        self.rng.shuffle(deck)
        return deck

    def say(self, message):
        self.log.append(message)
        self.log = self.log[-60:]

    def draw(self, who, count=1):
        for _ in range(count):
            if self.winner is not None:
                return
            p = self.players[who]
            if not p.deck:
                self.winner = 1 - who
                self.phase = 'over'
                self.say(f'{p.name}: колода закончилась при попытке добора.')
                return
            p.hand.append(p.deck.pop())

    def mulligan(self):
        if self.active != 0 or self.turn != 1 or self.acted or self.mulligan_used:
            raise ValueError('Новая рука доступна один раз до первого действия.')
        p = self.players[0]
        p.deck.extend(p.hand)
        p.hand.clear()
        self.rng.shuffle(p.deck)
        self.draw(0, 7)
        self.mulligan_used = True
        self.say('Бесплатная пересдача: получены новые 7 карт.')

    def creature(self, who, uid):
        return next((c for c in self.players[who].board if c.uid == uid), None)

    def check(self):
        for p in self.players:
            for c in p.board[:]:
                if c.damage >= c.card.toughness:
                    p.board.remove(c)
                    p.grave.append(c.card)
                    self.say(f'{c.card.name} погибает.')
        dead = [i for i, p in enumerate(self.players) if p.life <= 0]
        if dead:
            self.winner = -1 if len(dead) == 2 else 1 - dead[0]
            self.phase = 'over'

    def play(self, who, index, target=None):
        if self.winner is not None or who != self.active or self.phase != 'main':
            raise ValueError('Сейчас нельзя разыгрывать карты.')
        p = self.players[who]
        if not 0 <= index < len(p.hand):
            raise ValueError('Выбери карту из руки.')
        card = p.hand[index]
        enemy = 1 - who
        if card.kind == 'land':
            if p.land_played:
                raise ValueError('Земля в этом ходу уже сыграна.')
            p.hand.pop(index)
            p.lands += 1
            p.land_played = True
            self.acted = True
            self.say(f'{p.name}: {card.name}.')
            return
        if any(c in card.mana_cost for c in 'WUBRG' if c != p.color):
            raise ValueError('Нет маны нужного цвета.')
        if card.cost > p.mana:
            raise ValueError(f'Нужно {card.cost} маны; доступно {p.mana}. Сыграй землю или закончи ход.')
        victim = None
        target_owner = enemy
        if target == 'selfhero':
            target_owner = who
        elif isinstance(target, tuple) and len(target) == 2 and target[0] == 'self':
            target_owner = who
            victim = self.creature(who, target[1])
        elif target not in ('hero', 'selfhero'):
            victim = self.creature(enemy, target)
        if card.effect in ('damage', 'destroy', 'player_damage', 'drain'):
            legal = (victim is not None if card.effect == 'destroy' else
                     target in ('hero', 'selfhero') if card.effect in ('player_damage', 'drain') else
                     victim is not None or target in ('hero', 'selfhero'))
            if not legal:
                raise ValueError('Выбери допустимую цель по тексту карты.')
        p.hand.pop(index)
        p.used += card.cost
        self.acted = True
        self.say(f'{p.name}: {card.name}.')
        if card.kind == 'creature':
            self.uid += 1
            p.board.append(Creature(card, self.uid, sick=not card.haste))
        else:
            p.grave.append(card)
            if card.effect in ('damage', 'player_damage'):
                if victim is None:
                    self.players[target_owner].life -= card.value
                else:
                    victim.damage += card.value
            elif card.effect == 'destroy':
                self.players[target_owner].board.remove(victim)
                self.players[target_owner].grave.append(victim.card)
            elif card.effect == 'heal':
                p.life += card.value
            elif card.effect == 'draw':
                self.draw(who, card.value)
            elif card.effect == 'draw_lose':
                self.draw(who, card.value)
                p.life -= 2
            elif card.effect == 'drain':
                self.players[target_owner].life -= card.value
                p.life += card.value
        self.check()

    def can_attack(self, c):
        return not c.tapped and not c.sick

    def declare_attack(self, ids):
        if self.phase != 'main' or self.attacked or self.winner is not None:
            raise ValueError('Атаковать можно один раз за ход.')
        ids = list(dict.fromkeys(ids))
        chosen = [self.creature(self.active, uid) for uid in ids]
        if not chosen or any(c is None or not self.can_attack(c) for c in chosen):
            raise ValueError('Выбери готовых существ для атаки.')
        self.attacked = True
        self.attackers = ids
        self.blocks = {}
        for c in chosen:
            c.tapped = True
        self.phase = 'block'
        self.say(f'{self.players[self.active].name}: атака ({len(ids)} существ).')

    def can_block(self, attacker, blocker):
        return not blocker.tapped and (not attacker.card.flying or blocker.card.flying)

    def assign_block(self, attacker_id, blocker_id):
        if self.phase != 'block' or attacker_id not in self.attackers:
            raise ValueError('Сначала выбери атакующего.')
        attacker = self.creature(self.active, attacker_id)
        blocker = self.creature(1 - self.active, blocker_id)
        if not attacker or not blocker or not self.can_block(attacker, blocker):
            raise ValueError('Этот боец не может блокировать: он повёрнут или не имеет полёта.')
        if self.blocks.get(attacker_id) == blocker_id:
            del self.blocks[attacker_id]
            return
        for key in list(self.blocks):
            if self.blocks[key] == blocker_id:
                del self.blocks[key]
        self.blocks[attacker_id] = blocker_id

    def auto_block(self):
        defender = self.players[1 - self.active]
        for uid in sorted(self.attackers, key=lambda x: self.creature(self.active, x).card.power, reverse=True):
            a = self.creature(self.active, uid)
            candidates = [b for b in defender.board if self.can_block(a, b) and b.uid not in self.blocks.values()]
            if candidates:
                # Prefer a surviving blocker; otherwise trade the weakest creature.
                candidates.sort(key=lambda b: (b.card.toughness - b.damage <= a.card.power,
                                                b.card.power < a.card.toughness - a.damage,
                                                b.card.cost))
                self.assign_block(uid, candidates[0].uid)

    def resolve_combat(self):
        if self.phase != 'block':
            raise ValueError('Сейчас нет боя.')
        defender = self.players[1 - self.active]
        for uid in self.attackers:
            a = self.creature(self.active, uid)
            b = self.creature(1 - self.active, self.blocks.get(uid))
            if b:
                a.damage += b.card.power
                b.damage += a.card.power
                self.say(f'{a.card.name} против {b.card.name}.')
            else:
                defender.life -= a.card.power
                self.say(f'{a.card.name}: {a.card.power} урона игроку.')
        self.attackers = []
        self.blocks = {}
        self.phase = 'main'
        self.check()

    def end_turn(self):
        if self.phase != 'main' or self.winner is not None:
            raise ValueError('Сначала заверши бой.')
        for p in self.players:
            for c in p.board:
                c.damage = 0
        self.active = 1 - self.active
        self.turn += 1
        self.attacked = False
        self.acted = False
        p = self.players[self.active]
        p.used = 0
        p.land_played = False
        for c in p.board:
            c.tapped = False
            c.sick = False
        self.draw(self.active)
        self.say(f'Ход {self.turn}: {p.name}.')

    def ai_main(self):
        if self.winner is not None:
            return
        p = self.players[self.active]
        for index, card in enumerate(p.hand):
            if card.kind == 'land' and not p.land_played:
                self.play(self.active, index)
                break
        while self.winner is None:
            options = []
            enemies = self.players[1 - self.active].board
            for i, card in enumerate(p.hand):
                if card.kind == 'land' or card.cost > p.mana:
                    continue
                target = None
                priority = 2 + card.cost if card.kind == 'creature' else 1
                if card.effect == 'destroy':
                    if not enemies:
                        continue
                    target = max(enemies, key=lambda c: c.card.cost).uid
                    priority = 9
                elif card.effect == 'damage':
                    killable = [c for c in enemies if c.card.toughness - c.damage <= card.value]
                    if self.players[1 - self.active].life <= card.value:
                        target, priority = 'hero', 100
                    elif killable:
                        target, priority = max(killable, key=lambda c: c.card.cost).uid, 8
                    else:
                        target = 'hero'
                elif card.effect in ('player_damage', 'drain'):
                    target = 'hero'
                    priority = 100 if self.players[1-self.active].life <= card.value else 4
                elif card.effect == 'draw_lose' and (p.life <= 2 or len(p.deck) < 2):
                    continue
                elif card.effect == 'heal' and p.life >= 20:
                    continue
                elif card.effect == 'draw' and len(p.deck) < card.value:
                    continue
                options.append((priority, i, target))
            if not options:
                break
            _, index, target = max(options, key=lambda x: x[0])
            self.play(self.active, index, target)


BG = '#0d1514'
PANEL = '#16211e'
TEXT = '#edf3ff'
MUTED = '#a1b0a5'
GOLD = '#e8b96f'
RED = '#ed7868'
BLUE = '#78b7ed'


# Real card names are used for Scryfall lookup.
ART_NAMES = {c.name: c.name for c in DRAGONS + UNDEAD + list(LANDS.values())}


class ArtStore:
    """Worker only downloads bytes. Tk images are created on the main thread."""
    def __init__(self, directory=None):
        import os
        import queue
        import threading
        from pathlib import Path
        self.directory = Path(directory or Path(os.environ.get('LOCALAPPDATA', Path.home())) / 'AshAndBones' / 'art-v1')
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.download, daemon=True)

    def start(self):
        self.thread.start()

    def download(self):
        import hashlib
        import json
        import time
        from urllib.request import Request, urlopen
        from urllib.parse import urlencode, urlparse
        def get(url, accept):
            request = Request(url, headers={'User-Agent': 'AshAndBonesStudyGame/1.1', 'Accept': accept})
            with urlopen(request, timeout=12) as response:
                data = response.read(12_000_001)
                if len(data) > 12_000_000:
                    raise ValueError('Image too large')
                return data
        try:
            self.directory.mkdir(parents=True, exist_ok=True)
        except OSError:
            self.queue.put(('done', 'Не удалось создать кэш. Игра доступна без артов.'))
            return
        failures = 0
        for local_name, source_name in ART_NAMES.items():
            key = hashlib.sha256(source_name.encode()).hexdigest()[:20]
            path = self.directory / (key + '.png')
            info = self.directory / (key + '.json')
            try:
                metadata = json.loads(info.read_text('utf-8')) if info.exists() else None
                valid = path.exists() and path.stat().st_size > 8 and path.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n'
                if not valid or not metadata:
                    time.sleep(0.12)
                    metadata = json.loads(get('https://api.scryfall.com/cards/named?' + urlencode({'exact': source_name}), 'application/json'))
                    image_url = metadata['image_uris']['png']
                    if urlparse(image_url).hostname != 'cards.scryfall.io':
                        raise ValueError('Unexpected image host')
                    data = get(image_url, 'image/png')
                    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
                        raise ValueError('Invalid PNG')
                    temporary = path.with_suffix('.tmp')
                    temporary.write_bytes(data)
                    temporary.replace(path)
                    info.write_text(json.dumps(metadata), 'utf-8')
                self.queue.put(('image', local_name, str(path), metadata))
            except Exception:
                failures += 1
                self.queue.put(('failed', local_name))
        self.queue.put(('done', 'Арты загружены и сохранены.' if not failures else f'Не загружено артов: {failures}. Игра работает; повтор загрузки — при следующем запуске.'))


class App:
    def __init__(self):
        import tkinter as tk
        from tkinter import messagebox, ttk
        self.tk, self.messagebox = tk, messagebox
        self.root = tk.Tk()
        self.root.title('Пепел и кости — MTG Duel')
        self.root.geometry('1440x900')
        self.root.minsize(1080, 700)
        self.root.configure(bg=BG)
        self.game = Game()
        self.selected = self.target = self.block_selection = None
        self.attack_selection = set()
        self.notice = 'Начни с Mountain: выбери карту в руке и нажми «Сыграть карту».'
        self.hand_page = 0
        self.busy = False
        self.art_images, self.art_sources, self.scaled_art, self.art_meta = {}, {}, {}, {}
        self.preview_card = None
        self.hovered_hand = None
        self.resize_job = None
        self.fullscreen = False
        self.art_store = ArtStore()
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill='x', padx=18, pady=8)
        tk.Label(top, text='ПЕПЕЛ И КОСТИ', font=('Segoe UI', 16, 'bold'), fg=GOLD, bg=BG).pack(side='left')
        tk.Label(top, text='  /  MTG DUEL', font=('Segoe UI', 10), fg=MUTED, bg=BG).pack(side='left')
        self.button(top, 'Новая дуэль', self.restart).pack(side='right', padx=(6, 0))
        self.button(top, 'Полный экран · F11', self.toggle_fullscreen).pack(side='right', padx=6)
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('Duel.TNotebook', background=BG, borderwidth=0)
        style.configure('Duel.TNotebook.Tab', padding=(20, 6), font=('Segoe UI', 10, 'bold'), background=PANEL, foreground=MUTED)
        style.map('Duel.TNotebook.Tab', background=[('selected', '#28423d')], foreground=[('selected', GOLD)])
        self.tabs = ttk.Notebook(self.root, style='Duel.TNotebook')
        self.tabs.pack(fill='both', expand=True, padx=12, pady=(0, 10))
        arena = tk.Frame(self.tabs, bg=BG)
        self.rules_tab = tk.Frame(self.tabs, bg=BG)
        self.tabs.add(arena, text='Игровой стол')
        self.tabs.add(self.rules_tab, text='Правила и управление')
        self.actions = tk.Frame(arena, bg='#151c20', highlightbackground='#45514b', highlightthickness=1)
        self.actions.pack(side='bottom', fill='x', pady=(8, 0))
        self.guide = tk.Label(self.actions, bg='#151c20', fg=TEXT, font=('Segoe UI', 10),
                              anchor='w', justify='left', padx=12, pady=4, height=2, wraplength=1000)
        self.guide.pack(fill='x')
        controls = tk.Frame(self.actions, bg='#151c20')
        controls.pack(fill='x', padx=10, pady=(0, 8))
        self.play_button = self.button(controls, 'Сыграть карту', self.play, accent=True)
        self.play_button.pack(side='left', padx=(0, 8))
        self.all_button = self.button(controls, 'Выбрать всех', self.select_all)
        self.all_button.pack(side='left', padx=(0, 8))
        self.attack_button = self.button(controls, 'Атаковать выбранными', self.attack)
        self.attack_button.pack(side='left')
        self.end_button = self.button(controls, 'Закончить ход', self.end, accent=True)
        self.end_button.pack(side='right')
        self.mulligan_button = self.button(controls, 'Пересдать руку', self.mulligan)
        self.mulligan_button.pack(side='right', padx=8)
        side = tk.Frame(arena, bg=PANEL, width=250, highlightbackground='#34423d', highlightthickness=1)
        side.pack(side='left', fill='y', padx=(0, 8))
        side.pack_propagate(False)
        self.side = side
        tk.Label(side, text='ВЫБРАННАЯ КАРТА', bg=PANEL, fg=GOLD, font=('Segoe UI', 10, 'bold')).pack(pady=(10, 3))
        self.preview = tk.Canvas(side, width=245, height=335, bg=PANEL, highlightthickness=0)
        self.preview.pack()
        self.credit = tk.Label(side, text='Наведи курсор на карту', bg=PANEL, fg=TEXT, font=('Segoe UI', 9), wraplength=222, justify='left', anchor='w')
        self.credit.pack(fill='x', padx=12, pady=5)
        self.button(side, 'Карта на Scryfall ↗', self.open_art).pack(fill='x', padx=12, pady=4)
        self.art_status = tk.Label(side, text='Загрузка карт…', bg=PANEL, fg=MUTED, font=('Segoe UI', 8), wraplength=222, justify='left')
        self.art_status.pack(fill='x', padx=12, pady=3)
        tk.Label(side, text='ЖУРНАЛ ДУЭЛИ', bg=PANEL, fg=GOLD, font=('Segoe UI', 9, 'bold')).pack(anchor='w', padx=12, pady=(6, 2))
        self.history = tk.Label(side, bg=PANEL, fg=MUTED, wraplength=222, anchor='nw', justify='left', font=('Segoe UI', 9))
        self.history.pack(fill='both', expand=True, padx=12, pady=(0, 6))
        self.game_tab = tk.Frame(arena, bg='#1b2c28', highlightbackground='#546052', highlightthickness=1)
        self.game_tab.pack(side='left', fill='both', expand=True)
        self.game_tab.columnconfigure(0, weight=1)
        self.game_tab.rowconfigure(1, weight=1, minsize=86)
        self.game_tab.rowconfigure(3, weight=1, minsize=86)
        self.enemy_info, self.enemy_life, self.enemy_resources, self.enemy_piles = self.hero_bar(0, True)
        self.enemy_canvas = self.board_canvas(1)
        self.enemy_canvas.bind('<Button-1>', lambda e: self.board_click(1, e))
        self.status = tk.Label(self.game_tab, bg='#14241f', fg=GOLD, font=('Segoe UI', 10, 'bold'), pady=6)
        self.status.grid(row=2, column=0, sticky='ew')
        self.player_canvas = self.board_canvas(3)
        self.player_canvas.bind('<Button-1>', lambda e: self.board_click(0, e))
        self.player_info, self.player_life, self.player_resources, self.player_piles = self.hero_bar(4, False)
        handbar = tk.Frame(self.game_tab, bg='#111e1b')
        handbar.grid(row=5, column=0, sticky='ew')
        self.hand_title = tk.Label(handbar, bg='#111e1b', fg=MUTED, font=('Segoe UI', 9), padx=12)
        self.hand_title.pack(side='left')
        self.button(handbar, '›', lambda: self.page(1)).pack(side='right')
        self.button(handbar, '‹', lambda: self.page(-1)).pack(side='right')
        self.hand_canvas = tk.Canvas(self.game_tab, bg='#111e1b', height=180, highlightthickness=0)
        self.hand_canvas.grid(row=6, column=0, sticky='ew')
        self.hand_canvas.bind('<Button-1>', self.hand_click)
        self.message = tk.Label(self.actions, bg='#151c20', fg=GOLD, font=('Segoe UI', 9), anchor='w', padx=12, pady=2)
        self.message.pack(fill='x', before=self.guide)
        self.detail = tk.Label(self.game_tab)  # Description is displayed in the inspection panel.
        self.build_rules()
        self.root.bind('<Configure>', self.schedule_resize)
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self.leave_fullscreen())
        self.hand_canvas.bind('<Motion>', lambda e: self.hover(self.hand_canvas, e, 'hand:', 0))
        self.hand_canvas.bind('<Leave>', lambda e: self.leave_hand())
        self.enemy_canvas.bind('<Motion>', lambda e: self.hover(self.enemy_canvas, e, 'unit:', 1))
        self.player_canvas.bind('<Motion>', lambda e: self.hover(self.player_canvas, e, 'unit:', 0))
        for surface in (self.hand_canvas, self.enemy_canvas, self.player_canvas, self.preview):
            surface.bind('<Configure>', lambda e: self.render())
        self.art_store.start()
        self.root.after(150, self.poll_art)
        self.root.after_idle(self.render)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)

    def leave_fullscreen(self):
        self.fullscreen = False
        self.root.attributes('-fullscreen', False)
        self.selected = self.target = None
        self.attack_selection.clear()
        self.render()

    def schedule_resize(self, event):
        if event.widget != self.root:
            return
        if self.resize_job:
            self.root.after_cancel(self.resize_job)
        self.resize_job = self.root.after(80, self.resize)

    def resize(self):
        self.resize_job = None
        height = self.root.winfo_height()
        self.hand_canvas.config(height=max(135, min(205, int(height*.2))))
        self.preview.config(height=335 if height >= 820 else 270)
        self.guide.config(wraplength=max(900, self.root.winfo_width()-60))
        self.render()

    def hero_bar(self, row, enemy):
        tk = self.tk
        bar = tk.Frame(self.game_tab, bg='#192621', height=64)
        bar.grid(row=row, column=0, sticky='ew')
        bar.pack_propagate(False)
        resources = tk.Canvas(bar, width=235, height=62, bg='#192621', highlightthickness=0)
        resources.pack(side='left', padx=8)
        piles = tk.Canvas(bar, width=150, height=62, bg='#192621', highlightthickness=0)
        piles.pack(side='right', padx=8)
        center = tk.Frame(bar, bg='#192621')
        center.pack(expand=True)
        life = tk.Label(center, text='20', bg='#2b242a' if enemy else '#38271f', fg=TEXT,
                        font=('Segoe UI', 28, 'bold'), width=3, cursor='hand2')
        life.pack(side='left', padx=6)
        label = tk.Label(center, bg='#192621', fg=TEXT, font=('Segoe UI', 10, 'bold'), justify='left', cursor='hand2')
        label.pack(side='left')
        for widget in (life, label):
            widget.bind('<Button-1>', lambda e, own=not enemy: self.hero_target(own))
        return label, life, resources, piles

    def button(self, parent, text, command, accent=False):
        return self.tk.Button(parent, text=text, command=command, bg=GOLD if accent else '#2b3a34',
                              fg=BG if accent else TEXT, activebackground='#c98d45', activeforeground=BG,
                              relief='flat', font=('Segoe UI', 10, 'bold'), padx=12, pady=6, cursor='hand2')

    def board_canvas(self, row):
        holder = self.tk.Frame(self.game_tab, bg='#1b2c28')
        holder.grid(row=row, column=0, sticky='nsew')
        canvas = self.tk.Canvas(holder, bg='#1b2c28', height=140, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        # Shift + wheel pans crowded battlefields without permanent scrollbars.
        canvas.bind('<Shift-MouseWheel>', lambda e: canvas.xview_scroll(-1 if e.delta>0 else 1, 'units'))
        canvas.bind('<MouseWheel>', lambda e: canvas.xview_scroll(-1 if e.delta>0 else 1, 'units'))
        return canvas

    def card_image(self, card, width, height):
        import math
        source = self.art_sources.get(card.name)
        if not source:
            return None
        step = max(1, math.ceil(source.width()/width), math.ceil(source.height()/height))
        key = (card.name, step)
        if key not in self.scaled_art:
            self.scaled_art[key] = source.subsample(step)
        return self.scaled_art[key]

    def card_box(self, canvas, x, y, card, tag, selected=False, unit=None, extra='', large=False, size=None, playable=False):
        w, h = size or ((230, 325) if large else (112, 156))
        border = GOLD if selected else '#7dd5cf' if playable else '#6f6957'
        canvas.create_rectangle(x+4, y+5, x+w+4, y+h+5, fill='#101713', outline='', tags=tag)
        if selected or playable:
            canvas.create_rectangle(x-2, y-2, x+w+2, y+h+2, outline='#635640' if selected else '#365b53', width=3, tags=tag)
        canvas.create_rectangle(x, y, x+w, y+h, fill='#111512', outline=border, width=2 if selected or playable else 1, tags=tag)
        picture = self.card_image(card, w-4, h-4)
        if picture:
            canvas.create_image(x+w/2, y+h/2, image=picture, tags=tag)
        else:
            fill = '#684334' if card in DRAGONS else '#41404a' if card.kind!='land' else '#45563a'
            canvas.create_rectangle(x+4, y+4, x+w-4, y+h-4, fill=fill, outline='', tags=tag)
            canvas.create_text(x+8, y+8, text=card.name, fill=TEXT, anchor='nw', width=w-16, font=('Segoe UI', 12 if large else 9, 'bold'), tags=tag)
            canvas.create_text(x+w/2, y+h*.44, text=card.mana_cost or 'LAND', fill=GOLD, font=('Segoe UI', 13 if large else 10, 'bold'), tags=tag)
            canvas.create_text(x+8, y+h*.6, text=card.text if large else card.type_line.split(' — ')[0], fill=TEXT, anchor='nw', width=w-16, font=('Segoe UI', 10 if large else 8), tags=tag)
        if unit:
            state = extra or ('Отдыхает' if unit.tapped else 'Ждёт хода' if unit.sick else 'Готов')
            color = '#b76443' if extra=='Атакует' else '#468b88' if extra=='Блокирует' else '#272b28'
            canvas.create_rectangle(x+1, y+h-19, x+w-1, y+h-1, fill=color, outline='', tags=tag)
            canvas.create_text(x+w/2, y+h-10, text=state, fill=TEXT, font=('Segoe UI', 8), tags=tag)
        if card.kind=='creature':
            stats=f'{card.power}/{card.toughness}'
            if unit and unit.damage:stats+=f' −{unit.damage}'
            canvas.create_rectangle(x+w-55, y+h-(39 if unit else 20), x+w-2, y+h-(20 if unit else 2), fill='#131a18', outline='#716c56', tags=tag)
            canvas.create_text(x+w-28, y+h-(30 if unit else 11), text=stats, fill=TEXT, font=('Segoe UI', 10, 'bold'), tags=tag)

    def draw_resources(self, canvas, player, enemy):
        canvas.delete('all')
        color = '#967eb4' if enemy else '#ec9257'
        canvas.create_text(4, 9, text=f'МАНА  {player.mana} / {player.lands}', fill=TEXT, anchor='nw', font=('Segoe UI', 10, 'bold'))
        for i in range(min(10, player.lands)):
            x=5+i*20
            canvas.create_oval(x, 32, x+14, 46, fill=color if i<player.mana else '#303b34', outline=color if i<player.mana else '#50584f')
        if not player.lands:
            canvas.create_text(4, 38, text='Земли ещё не сыграны', anchor='w', fill=MUTED, font=('Segoe UI', 8))
        if player.lands>10:
            canvas.create_text(214, 39, text=f'+{player.lands-10}', fill=MUTED, font=('Segoe UI', 8))

    def draw_piles(self, canvas, player):
        canvas.delete('all')
        for x, title, count, fill in [(8,'Колода',len(player.deck),'#3c3738'),(78,'Кладбище',len(player.grave),'#242f29')]:
            canvas.create_rectangle(x+3, 7, x+48, 48, fill='#0c1411', outline='#625848')
            canvas.create_rectangle(x, 4, x+45, 45, fill=fill, outline='#8a785d')
            canvas.create_text(x+22, 24, text=str(count), fill=TEXT, font=('Segoe UI', 15, 'bold'))
            canvas.create_text(x+22, 55, text=title, fill=MUTED, font=('Segoe UI', 8))

    def draw_field(self, who, canvas):
        g=self.game
        width,height=max(300,canvas.winfo_width()),max(85,canvas.winfo_height())
        canvas.delete('all')
        # A subdued table surface and inlaid border keep the cards prominent.
        for i in range(12):
            inset=i*5
            if width>2*inset and height>2*inset:
                canvas.create_rectangle(inset,inset,width-inset,height-inset,outline='#1d302a')
        canvas.create_line(24,height/2,width-24,height/2,fill='#2a3c32')
        canvas.create_polygon(width/2-35,height/2,width/2,height/2-24,width/2+35,height/2,width/2,height/2+24,outline='#344538',fill='#21352d')
        board=g.players[who].board
        if not board:
            canvas.create_text(width/2,height/2,text='ПОЛЕ ПРОТИВНИКА' if who else 'ТВОЁ ПОЛЕ',fill='#718375',font=('Segoe UI',11,'bold'))
        h=min(169,height-20);w=max(55,int(h*.72));gap=14
        total=len(board)*(w+gap)-gap
        start=max(16,(width-total)/2)
        for i,c in enumerate(board):
            chosen=c.uid in self.attack_selection or (c.uid==self.target if who else ('self',c.uid)==self.target) or c.uid==self.block_selection
            extra=''
            if g.phase=='block':
                if c.uid in g.attackers:extra='Заблокирован' if c.uid in g.blocks else 'Атакует'
                if c.uid in g.blocks.values():extra='Блокирует'
            self.card_box(canvas,start+i*(w+gap),(height-h)/2,c.card,f'unit:{c.uid}',chosen,c,extra,size=(w,h))
        extent=max(width,total+32)
        canvas.config(scrollregion=(0,0,extent,height))
        if extent>width:
            canvas.create_text(canvas.canvasx(10),height-5,text='Колесо мыши: прокрутка поля',anchor='sw',fill=MUTED,font=('Segoe UI',8))

    def draw_hand(self):
        canvas=self.hand_canvas;p=self.game.players[0]
        width=max(300,canvas.winfo_width());height=max(130,canvas.winfo_height())
        canvas.delete('all')
        h=height-22;w=int(h*.72)
        per_page=max(1,int((width-30)//max(65,w*.75)))
        pages=max(1,(len(p.hand)+per_page-1)//per_page)
        self.hand_page=max(0,min(self.hand_page,pages-1))
        indices=list(range(self.hand_page*per_page,min(len(p.hand),(self.hand_page+1)*per_page)))
        gap=min(w+8,(width-w-30)/max(1,len(indices)-1))
        total=w+gap*max(0,len(indices)-1)
        start=(width-total)/2
        self.hand_title.config(text=f'ТВОЯ РУКА · {len(p.hand)} карт   /   {self.hand_page+1} из {pages}   ·   Наведи для просмотра')
        main=self.game.active==0 and self.game.phase=='main' and self.game.winner is None and not self.busy
        # Raised card is painted last and wins hit testing over its neighbours.
        raised=self.hovered_hand if self.hovered_hand in indices else self.selected
        order=[i for i in indices if i!=raised]+([raised] if raised in indices else [])
        for index in order:
            c=p.hand[index];slot=indices.index(index)
            playable=main and (not p.land_played if c.kind=='land' else c.cost<=p.mana)
            self.card_box(canvas,start+slot*gap,2 if index==raised else 16,c,f'hand:{index}',index==self.selected,size=(w,h),playable=playable)

    def leave_hand(self):
        self.hovered_hand=None
        self.draw_hand()

    def hover(self, canvas, event, prefix, who):
        index = self.hit(canvas, event, prefix)
        if index is None:
            return
        card = (self.game.players[0].hand[index] if prefix == 'hand:' and index < len(self.game.players[0].hand)
                else next((c.card for c in self.game.players[who].board if c.uid == index), None))
        if prefix == 'hand:' and index != self.hovered_hand:
            self.hovered_hand = index
            self.draw_hand()
        if card and card != self.preview_card:
            self.preview_card = card
            self.render_preview()

    def render_preview(self):
        self.preview.delete('all')
        card = self.preview_card
        if not card:
            self.preview.create_text(120, 150, text='Наведи курсор на карту\nв руке или на поле', fill=MUTED, font=('Segoe UI', 12), justify='center')
            return
        height=max(250,self.preview.winfo_height())
        h=min(325,height-12);w=int(h*.707)
        self.card_box(self.preview,(245-w)/2,6,card,'preview',large=True,size=(w,h))
        info = self.art_meta.get(card.name, {})
        self.credit.config(text=card.name + ' ' + card.mana_cost + '\n' + card.text + '\nХудожник: ' + info.get('artist', 'загружается…'))

    def open_art(self):
        import webbrowser
        from urllib.parse import urlparse
        info = self.art_meta.get(self.preview_card.name, {}) if self.preview_card else {}
        url = info.get('scryfall_uri', 'https://scryfall.com')
        if urlparse(url).scheme == 'https' and urlparse(url).hostname == 'scryfall.com':
            webbrowser.open(url)

    def poll_art(self):
        import queue
        import math
        changed = False
        finished = False
        while True:
            try:
                event = self.art_store.queue.get_nowait()
            except queue.Empty:
                break
            if event[0] == 'done':
                self.art_status.config(text=event[1])
                finished = True
            elif event[0] == 'image':
                _, name, path, metadata = event
                try:
                    source = self.tk.PhotoImage(file=path)
                    self.art_sources[name] = source
                    for large, maxw, maxh in [(False, 130, 158), (True, 224, 313)]:
                        step = max(1, math.ceil(source.width()/maxw), math.ceil(source.height()/maxh))
                        self.art_images[name, large] = source.subsample(step, step)
                    self.art_meta[name] = metadata
                    changed = True
                    self.art_status.config(text=f'Иллюстрации: {len(self.art_meta)}/{len(ART_NAMES)}')
                except self.tk.TclError:
                    self.art_status.config(text='Один из артов не открылся. Остальные карты доступны.')
        if changed:
            self.render()
            self.render_preview()
        if not finished:
            self.root.after(150, self.poll_art)

    def render(self):
        g = self.game
        p, enemy = g.players
        if not hasattr(self, 'history'):
            return
        phase = 'ТВОЙ ХОД' if g.active == 0 else 'ХОД БОТА'
        if g.phase == 'block' and g.active == 1:
            phase = 'ЗАЩИТА · выбери атакующего, затем своего блокирующего'
        if g.winner is not None:
            phase = 'ПОБЕДА! Ты выиграл дуэль.' if g.winner == 0 else ('НИЧЬЯ' if g.winner == -1 else 'ПОРАЖЕНИЕ · попробуй новую игру')
        self.status.config(text=f'Ход {g.turn}   /   {phase}')
        self.enemy_info.config(text=f'ПРОТИВНИК\nЧёрная колода · {len(enemy.hand)} карт', fg=GOLD if self.target=='hero' else TEXT)
        self.player_info.config(text='ТЫ · КРАСНАЯ\n' + ('Земля сыграна' if p.land_played else 'Можно сыграть землю'), fg=GOLD if self.target=='selfhero' else TEXT)
        self.enemy_life.config(text=str(max(0,enemy.life)),fg=GOLD if self.target=='hero' else TEXT)
        self.player_life.config(text=str(max(0,p.life)),fg=GOLD if self.target=='selfhero' else TEXT)
        for player,resources,piles,is_enemy in [(enemy,self.enemy_resources,self.enemy_piles,True),(p,self.player_resources,self.player_piles,False)]:
            self.draw_resources(resources,player,is_enemy)
            self.draw_piles(piles,player)
        self.draw_field(1,self.enemy_canvas)
        self.draw_field(0,self.player_canvas)
        self.draw_hand()
        card = p.hand[self.selected] if self.selected is not None and self.selected < len(p.hand) else None
        if card:
            self.preview_card = card
        self.render_preview()
        self.detail.config(text=f'{card.name}: {card.text}' if card else 'Клик по карте в руке — выбрать. Клик по своему готовому существу — добавить в атаку.')
        self.message.config(text=self.notice[:125])
        self.history.config(text='\n\n'.join(g.log[-3:]))
        main = g.active == 0 and g.phase == 'main' and g.winner is None and not self.busy
        blocking = g.active == 1 and g.phase == 'block' and g.winner is None
        playable = main and card is not None and (not p.land_played if card.kind == 'land' else card.cost <= p.mana)
        self.play_button.config(state='normal' if playable else 'disabled')
        if g.winner is not None:
            hint = 'Дуэль завершена. Кнопка «Новая игра» начинает новую партию.'
        elif blocking:
            hint = 'ЗАЩИТА: нажми атакующее существо сверху → своего защитника снизу → «Завершить бой». Без блока урон получишь ты.'
        elif not main:
            hint = 'Противник делает ход. Дождись атаки или начала своего хода.'
        elif card:
            if card.kind == 'land':
                hint = 'Земля уже сыграна в этом ходу. Выбери другую карту.' if p.land_played else 'Нажми «Сыграть карту»: земля добавит 1 ману. За ход можно сыграть одну землю.'
            elif card.cost > p.mana:
                hint = f'Не хватает маны: нужно {card.cost}, доступно {p.mana}. Сыграй землю или выбери более дешёвую карту.'
            elif card.effect in ('damage', 'destroy', 'player_damage', 'drain'):
                hint = 'Выбери цель: ' + ('строку игрока' if card.effect in ('player_damage', 'drain') else 'существо' if card.effect == 'destroy' else 'существо или строку игрока') + ', затем нажми «Сыграть карту». Можно выбрать свою цель.'
            else:
                hint = f'Нажми «Сыграть карту». Будет потрачено {card.cost} маны.'
        elif self.attack_selection:
            hint = f'В атаку выбрано {len(self.attack_selection)}. Нажми «Атаковать выбранными». Повторный клик снимает выбор.'
        elif not p.land_played and any(c.kind == 'land' for c in p.hand):
            hint = '1. Выбери «Mountain» в руке → «Сыграть карту».  2. Сыграй существо за ману.  3. Атакуй или закончи ход.'
        else:
            hint = 'Выбери карту в руке или готовых существ для атаки. Если действий нет — «Закончить ход». Правила — в соседней вкладке.'
        self.guide.config(text=hint)
        self.attack_button.config(state='normal' if (main and not g.attacked) or blocking else 'disabled',
                                  text='Завершить бой' if blocking else 'Атаковать выбранными')
        self.all_button.config(state='normal' if main and not g.attacked else 'disabled')
        self.end_button.config(state='normal' if main else 'disabled')
        self.mulligan_button.config(state='normal' if main and g.turn == 1 and not g.acted and not g.mulligan_used else 'disabled')

    def hit(self, canvas, event, prefix):
        items = canvas.find_overlapping(canvas.canvasx(event.x), canvas.canvasy(event.y), canvas.canvasx(event.x), canvas.canvasy(event.y))
        for item in reversed(items):
            for tag in canvas.gettags(item):
                if tag.startswith(prefix):
                    return int(tag.split(':')[1])
        return None

    def hand_click(self, event):
        if self.busy or self.game.active != 0 or self.game.phase != 'main':
            return
        self.selected = self.hit(self.hand_canvas, event, 'hand:')
        self.target = None
        if self.selected is not None:
            card = self.game.players[0].hand[self.selected]
            self.notice = 'Выбери цель согласно тексту карты, затем нажми «Сыграть карту».' if card.effect in ('damage', 'destroy', 'player_damage', 'drain') else 'Нажми «Сыграть карту».'
        self.render()

    def board_click(self, who, event):
        if self.busy or self.game.winner is not None:
            return
        g = self.game
        uid = self.hit(self.player_canvas if who == 0 else self.enemy_canvas, event, 'unit:')
        if uid is None:
            return
        try:
            if g.active == 1 and g.phase == 'block':
                if who == 1 and uid in g.attackers:
                    self.block_selection = uid
                    self.notice = 'Теперь выбери своё неповёрнутое существо. Повторный выбор снимает блок.'
                elif who == 0:
                    g.assign_block(self.block_selection, uid)
                    self.notice = 'Блок назначен. Можно назначить другие или нажать «Завершить бой».'
            elif g.active == 0 and g.phase == 'main':
                chosen = g.players[0].hand[self.selected] if self.selected is not None and self.selected < len(g.players[0].hand) else None
                if who == 1 or chosen and chosen.effect in ('damage', 'destroy', 'player_damage', 'drain'):
                    self.target = uid if who == 1 else ('self', uid)
                    self.notice = 'Цель выбрана. Нажми «Сыграть карту».'
                elif not g.attacked:
                    c = g.creature(0, uid)
                    if not g.can_attack(c):
                        raise ValueError('Этот боец повёрнут или только что вызван.')
                    if uid in self.attack_selection:
                        self.attack_selection.remove(uid)
                    else:
                        self.attack_selection.add(uid)
                    self.notice = f'Для атаки выбрано: {len(self.attack_selection)}.'
        except ValueError as error:
            self.notice = str(error)
        self.render()

    def hero_target(self, own=False):
        if self.game.active == 0 and not self.busy:
            self.target = 'selfhero' if own else 'hero'
            self.notice = ('Цель: ты.' if own else 'Цель: бот.') + ' Нажми «Сыграть карту».'
            self.render()

    def play(self):
        try:
            self.game.play(0, self.selected if self.selected is not None else -1, self.target)
            self.selected = self.target = None
            self.notice = 'Карта сыграна. Можно продолжить или закончить ход.'
        except ValueError as error:
            self.notice = str(error)
        self.render()

    def select_all(self):
        self.attack_selection = {c.uid for c in self.game.players[0].board if self.game.can_attack(c)}
        self.notice = f'Для атаки выбрано: {len(self.attack_selection)}.'
        self.render()

    def attack(self):
        try:
            g = self.game
            if g.active == 1 and g.phase == 'block':
                g.resolve_combat()
                if g.winner is None:
                    g.end_turn()
                self.block_selection = None
                self.notice = 'Твой ход. Мана восстановлена, карта взята.'
            else:
                g.declare_attack(sorted(self.attack_selection))
                g.auto_block()
                g.resolve_combat()
                self.attack_selection.clear()
                self.notice = 'Бой завершён. Можно сыграть карты или закончить ход.'
        except ValueError as error:
            self.notice = str(error)
        self.render()

    def end(self):
        try:
            self.game.end_turn()
        except ValueError as error:
            self.notice = str(error)
            return
        self.selected = self.target = None
        self.attack_selection.clear()
        self.busy = True
        self.notice = 'Бот разыгрывает карты…'
        self.render()
        self.root.after(600, self.bot_turn)

    def bot_turn(self):
        g = self.game
        g.ai_main()
        if g.winner is None:
            ready = [c.uid for c in g.players[1].board if g.can_attack(c)]
            if ready:
                g.declare_attack(ready)
                self.notice = 'Защита: кликни по атакующему боту, затем по своему существу. После выбора блоков нажми «Завершить бой».'
            else:
                g.end_turn()
                self.notice = 'Твой ход: сыграй землю, затем карты.'
        self.busy = False
        self.render()

    def mulligan(self):
        try:
            self.game.mulligan()
            self.selected = None
            self.notice = 'Получена новая стартовая рука. Пересдача доступна только один раз.'
        except ValueError as error:
            self.notice = str(error)
        self.render()

    def page(self, delta):
        self.hand_page = max(0, self.hand_page+delta)
        self.render()

    def restart(self):
        if self.busy:
            return
        if self.messagebox.askyesno('Новая дуэль', 'Начать новую игру?'):
            self.game = Game()
            self.selected = self.target = self.block_selection = None
            self.attack_selection.clear()
            self.hand_page = 0
            self.hovered_hand = None
            self.preview_card = None
            self.notice = 'Сыграй землю из руки. Цель — снизить жизни бота до нуля.'
            self.render()

    def build_rules(self):
        tk = self.tk
        self.button(self.rules_tab, 'Вернуться к игре', lambda: self.tabs.select(0), accent=True).pack(anchor='w', padx=20, pady=12)
        body = tk.Frame(self.rules_tab, bg=BG)
        body.pack(fill='both', expand=True, padx=20, pady=(0, 16))
        text = tk.Text(body, bg=PANEL, fg=TEXT, relief='flat', wrap='word', padx=24, pady=18,
                       font=('Segoe UI', 12), spacing3=8, cursor='arrow')
        scroll = tk.Scrollbar(body, command=text.yview)
        scroll.pack(side='right', fill='y')
        text.pack(side='left', fill='both', expand=True)
        text.configure(yscrollcommand=scroll.set)
        text.tag_configure('title', font=('Segoe UI', 21, 'bold'), foreground=GOLD, spacing3=16)
        text.tag_configure('heading', font=('Segoe UI', 14, 'bold'), foreground=GOLD, spacing1=14)
        text.insert('end', 'Как играть в «Пепел и кости»\n', 'title')
        sections = [
            ('Цель игры', 'Ты играешь красной колодой против чёрной колоды бота. У каждого 20 жизней. Снизь жизни противника до 0. Если нужно взять карту, а колода пуста, игрок также проигрывает.'),
            ('Первый ход — по шагам', '1. В нижнем ряду (рука) нажми карту «Mountain».\n2. Нажми «Сыграть карту». Теперь у тебя 1 мана.\n3. Выбери существо стоимостью 1 ману, если оно есть, и сыграй его.\n4. Нажми «Закончить ход». Обычно новое существо сможет атаковать только на следующем твоём ходу.\nДо первого действия можно один раз бесплатно заменить все 7 стартовых карт.'),
            ('Что где находится', 'Сверху — противник, в центре — два поля существ, снизу — твои жизни и рука. Большие числа — жизни: по ним можно выбрать цель заклинания. Кружки слева показывают доступную ману, стопки справа — колоду и кладбище. Внизу закреплены кнопки действий. Золотая рамка показывает выбор. Подсказка над кнопками объясняет следующий шаг. Бирюзовая рамка в руке означает, что маны хватает. При наведении карта приподнимается, а слева появляется её крупный просмотр. Слева под просмотром карты — последние события. Карты на поле расположены по центру; если существ много, прокручивай поле колесом мыши. F11 включает полный экран, Esc возвращает оконный режим и снимает выбор.'),
            ('Земли и мана', 'Mountain — земля: её можно сыграть бесплатно, но только одну за ход. Каждая земля даёт 1 ману. Мана 2/3 означает: осталось 2 из 3. Стоимость карты написана на ней; при розыгрыше мана тратится автоматически. В начале своего хода мана полностью восстанавливается.'),
            ('Как атаковать', 'Нажми своих существ со статусом «Готов к бою» или «Выбрать всех». Затем нажми «Атаковать выбранными». Бот выбирает блокирующих. Атаковать можно один раз за ход. Атакующие отдыхают до твоего следующего хода и не смогут защищать тебя во время хода бота. После боя можно ещё сыграть карты.'),
            ('Как защищаться', 'Когда бот атакует: сначала нажми его атакующее существо, затем своего защитника. Повтори для других атакующих. Надписи на картах покажут назначенные блоки. Повторный выбор той же пары снимает блок. Нажми «Завершить бой», когда готов. Можно ничего не блокировать — тогда весь незаблокированный урон получишь ты. Один защитник блокирует одного атакующего; отдыхающий защищать не может.'),
            ('Числа и способности существ', '3/2 означает: 3 силы (наносит 3 урона), 2 выносливости (погибает от 2 урона). При блоке оба существа наносят урон одновременно; лишний урон игроку не проходит. Урон существам очищается в конце хода.\n«Ждёт хода» — только что призвано, пока не атакует, но может блокировать.\n«Ускорение» — может атаковать сразу.\n«Полёт» — заблокировать может только другое летающее существо.\n«Отдыхает» — уже атаковало, пока не атакует и не блокирует.'),
            ('Заклинания и выбор цели', 'Shock и Lightning Strike: выбери карту → существо или строку игрока → «Сыграть карту». Можно выбрать свою цель. Lava Spike нацеливается на игрока (planeswalker здесь нет). Murder уничтожает выбранное существо. Sovereign’s Bite требует выбрать игрока: он теряет 3 жизни, а ты получаешь 3. Night’s Whisper берёт 2 карты и отнимает 2 жизни. Если маны не хватает, кнопка розыгрыша отключена, а подсказка объяснит причину.'),
            ('Иллюстрации и источник', 'При первом запуске игра скачивает изображения с Scryfall и сохраняет их в папке AshAndBones/art-v1 в LOCALAPPDATA (на Windows). Для первого скачивания нужен интернет; сохранённые арты работают без сети. Художник и ссылка указаны слева при наведении. Показываются полные изображения настоящих карт MTG. Стоимость, характеристики и Oracle-текст сверены с Scryfall. Под просмотром есть пояснение на русском. Иллюстрации принадлежат их правообладателям; эта игра не является официальным продуктом Wizards of the Coast или Forge.'),
            ('Колода и ограничения этой версии', 'Две готовые колоды по 60 карт: 24 земли и 36 других карт. В начале у каждого 7 карт. Первый игрок пропускает первый добор. Настоящие карты MTG, но упрощённый движок: без стека, ответов на заклинания, planeswalker, лимита руки и нескольких блокирующих. Даже Instant разыгрывается только в свою главную фазу. Колоды одноцветные, земли оплачивают карты автоматически. Бесплатная пересдача — учебное упрощение. Партия не сохраняется после закрытия окна. Переключение вкладок не сбрасывает игру.'),
        ]
        for heading, paragraph in sections:
            text.insert('end', heading + '\n', 'heading')
            text.insert('end', paragraph + '\n')
        text.configure(state='disabled')

    def help(self):
        self.tabs.select(self.rules_tab)

    def run(self):
        self.root.mainloop()


def tests():
    import unittest

    class RulesTest(unittest.TestCase):
        def fresh(self):
            g = Game(42)
            for p in g.players:
                p.hand.clear()
                p.board.clear()
                p.lands = 10
            return g

        def test_decks(self):
            g = Game(1)
            for p in g.players:
                self.assertEqual(len(p.deck)+len(p.hand), 60)
                self.assertEqual(len(p.hand), 7)
                self.assertEqual(sum(c.kind == 'land' for c in p.deck+p.hand), 24)

        def test_one_land(self):
            g = self.fresh()
            g.players[0].hand = [LANDS['Mountain']]*2
            g.play(0, 0)
            with self.assertRaises(ValueError): g.play(0, 0)

        def test_mana_and_sickness(self):
            g = self.fresh()
            g.players[0].hand = [DRAGONS[1]]
            g.play(0, 0)
            self.assertEqual(g.players[0].mana, 8)
            self.assertFalse(g.can_attack(g.players[0].board[0]))
            g.end_turn(); g.end_turn()
            self.assertEqual(g.players[0].mana, 10)
            self.assertTrue(g.can_attack(g.players[0].board[0]))

        def test_bad_target_no_payment(self):
            g = self.fresh()
            g.players[0].hand = [DRAGONS[6]]
            with self.assertRaises(ValueError): g.play(0, 0)
            self.assertEqual(g.players[0].mana, 10)
            self.assertEqual(len(g.players[0].hand), 1)

        def test_insufficient_mana(self):
            g = self.fresh();g.players[0].lands = 0;g.players[0].hand = [DRAGONS[4]]
            with self.assertRaises(ValueError): g.play(0, 0)
            self.assertEqual(len(g.players[0].hand), 1)

        def test_haste_and_direct_damage(self):
            g = self.fresh();g.players[0].hand = [DRAGONS[2]];g.play(0, 0)
            g.declare_attack([g.players[0].board[0].uid]);g.resolve_combat()
            self.assertEqual(g.players[1].life, 18)
            with self.assertRaises(ValueError):g.declare_attack([1])

        def test_simultaneous_combat(self):
            g = self.fresh()
            g.players[0].board = [Creature(DRAGONS[1], 1, sick=False)]
            g.players[1].board = [Creature(DRAGONS[1], 2)]
            g.declare_attack([1]);g.assign_block(1, 2);g.resolve_combat()
            self.assertFalse(g.players[0].board);self.assertFalse(g.players[1].board)
            self.assertEqual(g.players[1].life, 20)

        def test_flying_and_tapped_blocker(self):
            g = self.fresh()
            g.players[0].board = [Creature(DRAGONS[5], 1, sick=False)]
            g.players[1].board = [Creature(UNDEAD[1], 2), Creature(UNDEAD[2], 3, tapped=True)]
            g.declare_attack([1])
            with self.assertRaises(ValueError):g.assign_block(1, 2)
            with self.assertRaises(ValueError):g.assign_block(1, 3)

        def test_reassign_blocker(self):
            g = self.fresh()
            g.players[0].board = [Creature(DRAGONS[1], i, sick=False) for i in (1, 2)]
            g.players[1].board = [Creature(UNDEAD[1], 3)]
            g.declare_attack([1, 2]);g.assign_block(1, 3);g.assign_block(2, 3)
            self.assertEqual(g.blocks, {2: 3})

        def test_spells(self):
            g = self.fresh();g.players[0].color = 'B'
            g.players[0].hand = [UNDEAD[7], UNDEAD[8]]
            g.play(0, 0, 'hero');self.assertEqual(g.players[1].life, 17)
            self.assertEqual(g.players[0].life, 23)
            g.play(0, 0);self.assertEqual(g.players[0].life, 21)
            self.assertEqual(len(g.players[0].hand), 2)

        def test_lava_spike_targets(self):
            g = self.fresh();g.players[0].hand = [DRAGONS[8]]
            g.players[1].board = [Creature(UNDEAD[0], 1)]
            with self.assertRaises(ValueError):g.play(0, 0, 1)
            self.assertEqual(g.players[0].used, 0)
            g.play(0, 0, 'hero');self.assertEqual(g.players[1].life, 17)

        def test_self_targets_and_color(self):
            g = self.fresh();g.players[0].hand = [DRAGONS[6], UNDEAD[6]]
            g.play(0, 0, 'selfhero');self.assertEqual(g.players[0].life, 18)
            with self.assertRaises(ValueError):g.play(0, 0, 1)
            g.players[0].color='B';g.players[0].board=[Creature(UNDEAD[0], 1)]
            g.play(0, 0, ('self', 1));self.assertFalse(g.players[0].board)

        def test_sovereigns_bite_self(self):
            g = self.fresh();g.players[0].color='B';g.players[0].life=2
            g.players[0].hand=[UNDEAD[7]]
            with self.assertRaises(ValueError):g.play(0,0)
            g.play(0,0,'selfhero')
            self.assertEqual(g.players[0].life,2)
            self.assertIsNone(g.winner)

        def test_nights_whisper_can_kill_caster(self):
            g = self.fresh();g.players[0].color='B';g.players[0].life=2
            g.players[0].hand=[UNDEAD[8]];g.play(0,0)
            self.assertEqual(g.winner,1)

        def test_kill_and_cleanup(self):
            g = self.fresh();g.players[1].board = [Creature(UNDEAD[1], 5)]
            g.players[0].hand = [DRAGONS[6]];g.play(0, 0, 5)
            self.assertEqual(len(g.players[1].grave), 1)
            g.players[1].board = [Creature(UNDEAD[3], 6, damage=1)]
            g.end_turn();self.assertEqual(g.players[1].board[0].damage, 0)

        def test_deck_loss_and_life_loss(self):
            g = self.fresh();g.players[0].deck = [];g.draw(0)
            self.assertEqual(g.winner, 1)
            g = self.fresh();g.players[1].life = 2;g.players[0].hand = [DRAGONS[6]]
            g.play(0, 0, 'hero');self.assertEqual(g.winner, 0)

        def test_full_games(self):
            for seed in range(50):
                g = Game(seed)
                for _ in range(180):
                    if g.winner is not None:break
                    g.ai_main()
                    if g.winner is not None:break
                    ready = [c.uid for c in g.players[g.active].board if g.can_attack(c)]
                    if ready:
                        g.declare_attack(ready);g.auto_block();g.resolve_combat()
                    if g.winner is not None:break
                    g.end_turn()
                self.assertIsNotNone(g.winner)
                for p in g.players:
                    self.assertGreaterEqual(p.mana, 0)
                    self.assertEqual(len(p.deck)+len(p.hand)+len(p.board)+len(p.grave)+p.lands, 60)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RulesTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    if '--test' in sys.argv:
        raise SystemExit(tests())
    App().run()
