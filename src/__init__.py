from requests import get, post, Session
from json import dumps, loads
from os import system
from bs4 import BeautifulSoup
from typing import Union, Optional
from datetime import datetime
system('')


# Bvn dans mon API Wrapper OneCube!
# by BlueRed

# TikTok: @bluered.pyx
# Discord (ID): 699359734427549736



__title__ = 'OneCube'
__description__ = 'A OneCube API wrapper'
__author__ = 'BlueRed'
__version__ = '1.01'

__all__ = [
    'APIError', 'Rank', 'Message',
    'Topic', 'Thread', 'Activity',
    'MessageCreated', 'ThreadCreated', 'ActivityType',
    'Player', 'ShopProduct', 'Shop',
    'Client', 'NotFound', 'Categories'
]

BASE = 'https://www.onecube.com'
API_BASE = BASE + '/api'
USER_AGENT = 'OneCubePythonAPIWrapper'
ANSI_RESET = '\u001b[0m'

COLORS = {
    'gray': 39,
    'green': 32,
    'red': 31,
    'yellow': 33
}

class APIError(Exception):
    r"""
    Raised when an API request responds with the wrong status code that is expected
    """
    pass

class NotFound(APIError):
    r"""
    Raised when something is not found by the API.
    e.g: a wrong player name
    """
    pass



class Categories:
    r"""
    All the categories that are on OneCube.
    """

    ANNOUNCES_AND_RULES: 'Category'
    NEWS: 'Category'
    GENERAL_DISCUSSION: 'Category'
    SUGGGESTIONS: 'Category'
    REPORT_AND_BUGS: 'Category'
    TIPS_AND_HELP: 'Category'
    OFF_TOPIC: 'Category'
    CREATION: 'Category'



class Topics:
    r"""
    All the topics that are on OneCube.
    """

    PVP_SWAP: 'Topic'
    BEDWARS: 'Topic'
    UHC: 'Topic'
    UHC_RUN: 'Topic'
    BLOCK_RUN: 'Topic'
    DE_A_COUDRE: 'Topic'
    GRAPHICS: 'Topic'
    RESOURCE_PACK: 'Topic'
    BUILD: 'Topic'
    WEBSITE: 'Topic'
    FORUM: 'Topic'
    HUB: 'Topic'



def to_message_payload(message: str) -> str:
    return dumps({
        'root': {
            'children': [
                {
                    'children': [
                        {
                            'detail': 0,
                            'format': 0,
                            'mode': 'normal',
                            'style': '',
                            'text': message,
                            'type': 'text',
                            'version': 1
                        }
                    ],
                    'direction': 'ltr',
                    'format': '',
                    'indent': 0,
                    'type': 'paragraph',
                    'version': 1
                }
            ],
            'direction': 'ltr',
            'format': '',
            'indent': 0,
            'type': 'root',
            'version': 1
        }
    })



class Rank:
    r"""
    Represent the OneCube rank of a player.

    > name: the name of the rank
    > color: the color of the rank
    > ansi: the ansi color of the rank
    """

    name: str
    color: str
    ansi: str

    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color
        self.ansi = '\u001b[' + str(COLORS.get(color)) + 'm'


    def __str__(self) -> str:
        return self.name


    def __repr__(self) -> str:
        return f'<Rank {self.name} {self.ansi}~{ANSI_RESET}>'



class Message:
    r"""
    Represent a forum message sent from a thread.

    > id: the id of the message
    > content: the content of the message
    > author: the author of the message
    """

    id: int
    content: str
    author: 'Player'

    def __init__(self, id: int, content: str, author: Union['Player', 'Client', dict[str]], thread: 'Thread') -> None:
        self.id = id
        self.content = loads(content)
        self.author = Player(author['id'], author) if isinstance(author, dict) else author
        self.thread = thread


    def __str__(self) -> str:
        return repr(self.content)


    def __repr__(self) -> str:
        return '<Message from thread {!r} by {!r}: {!r}>'.format(str(self.thread), str(self.author), str(self))



class Category:
    r"""
    Represent the category that is used for a forum thread to differentiate it subject.

    > id: the id of the category
    > backend_id: the backend id of the category
    > name: the name of the category
    > slug: the slug of the category (like the name)
    > color: the color of the category card
    > ansi: the ansi color of the category card
    """

    id: int
    backend_id: str
    name: str
    slug: str
    color: str
    ansi: str

    def __init__(self, id: int, infos: dict[str]):
        self.__session = Session()
        self.__session.headers['User-Agent'] = USER_AGENT

        self.id = id
        infos = infos or self.load()

        self.backend_id = infos['@id']
        self.name = infos['name']
        self.slug = infos['slug']
        self.color = infos['color']
        self.ansi = '\u001b[' + str(COLORS.get(self.color)) + 'm'


    def __str__(self) -> str:
        return self.name


    def __repr__(self) -> str:
        return f'<Topic {self.name} {self.ansi}~{ANSI_RESET}>'



class Topic:
    r"""
    Represent the topic that is used like categories but more precise.

    > id: the id of the topic
    > backend_id: the backend id of the topic
    > name: the name of the topic
    > color: the color of the topic card
    > ansi: the ansi color of the topic card
    > views: the total views of all threads that contains the topic
    > threads_count: the total threads that contains the topic
    > messages_count: the total messages of all threads that contains the topic
    > last_view_update: TODO
    > created_at: when the thread has been created
    > updated_at: when the thread has been updated
    """

    id: int
    backend_id: str
    name: str
    color: str
    ansi: str
    views: int
    threads_count: int
    messages_count: int
    last_view_update: datetime
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: int, infos: dict[str]):
        self.id = id
        self.name = infos['name']

        self.backend_id = infos['@id']
        self.color = infos['color']
        self.views = infos['views']

        self.threads_count = infos['threadsCount']
        self.messages_count = infos['messagesCount']

        self.last_view_update = datetime.fromisoformat(infos['lastViewUpdate'])
        self.created_at = datetime.fromisoformat(infos['createdAt'])
        self.updated_at = datetime.fromisoformat(infos['updatedAt'])


    def __str__(self) -> str:
        return self.name


    def __repr__(self) -> str:
        return f'<Topic {self.name} {self.ansi}~{ANSI_RESET}>'



class Thread:
    r"""
    A forum thread created by a player.

    > id: the id of the thread
    > name: the name of the thread
    > views: the view count
    > upvotes: the upvotes count
    > topics: the list of the thread topics
    > category: the thread category
    > pinned: if the thread is pinned
    > author: the author of the thread
    > first_message: the first message
    > last_message: the last message
    > vote_id: the id of the vote if you voted (does'nt save it)
    > messages: all the messages of the thread
    """

    id: int
    name: int
    views: int
    upvotes: int
    topics: list[Topic]
    category: Category
    pinned: bool
    author: 'Player'
    first_message: Message
    last_message: Message
    vote_id: Optional[int]
    messages: list[Message]

    def __init__(self, id: int, infos: dict[str] = {}) -> None:
        self.__session = Session()
        self.__session.headers['User-Agent'] = USER_AGENT

        self.id = id
        infos = infos or self.load()

        self.name = infos['name']
        self.views = infos['views']
        self.upvotes = infos['upVoteCount']
        self.topics = [Topic(topic['id'], topic) for topic in infos['topics']]
        self.__category = infos['category']
        self.pinned = infos['pinned']

        self.author = Player(infos['user']['id'], infos['user'])
        self.first_message = Message(infos['firstMessage']['id'], infos['firstMessage']['content'], infos['firstMessage']['user'], self)
        self.last_message = Message(infos['lastMessage']['id'], infos['lastMessage']['content'], infos['lastMessage']['user'], self)

        self.vote_id = None


    def __str__(self) -> str:
        return self.name


    def __repr__(self) -> str:
        return '<Thread {!r} by {!r}>'.format(self.name, self.author.username)


    @property
    def category(self) -> Category:
        if isinstance(self.__category, Category):
            return self.__category

        infos = self.load()
        self.__category = Category(infos['category']['id'], infos['category'])
        return self.__category


    @property
    def messages(self) -> list[Message]:
        endpoint = API_BASE + '/threads/{}/messages'.format(self.id)
        req = self.__session.get(endpoint)

        if req.status_code != 200:
            raise APIError(f'API returned {req.status_code}')

        resp = req.json()
        return [Message(message['id'], message['content'], message['user'], self) for message in resp['hydra:member']]


    def load(self) -> dict:
        endpoint = API_BASE + '/threads/' + str(self.id)
        req = self.__session.get(endpoint)

        if req.status_code == 400:
            raise NotFound(f'Cannot find thread {self.id!r}')

        elif req.status_code != 200:
            raise APIError(f'API returned {req.status_code}')

        resp = req.json()
        return resp


    def send(self, client: 'Client', message: str) -> Message:
        endpoint = API_BASE + '/messages'
        message_data = to_message_payload(message)

        req = client._session.post(endpoint, json = {
            'content': message_data,
            'thread': '/threads/' + str(self.id),
            'user': '/users/' + client.id,
            'medias': []
        })

        if req.status_code != 201:
            raise APIError(f'API returned {req.status_code}')

        resp = req.json()
        return Message(resp['id'], message_data, client, self)


    def vote(self, client: 'Client', up: bool = True) -> None:
        endpoint = API_BASE + '/votes'
        req = client._session.post(endpoint, json = {
            'up': up,
            'thread': '/threads/' + str(self.id),
            'user': '/users/' + client.id,
        })

        if req.status_code != 201:
            raise APIError(f'API returned {req.status_code}')


    def remove_vote(self, client: 'Client') -> None:
        if self.vote_id is None:
            return

        endpoint = API_BASE + '/votes/' + str(self.vote_id)
        req = client._session.delete(endpoint, json = {})

        if req.status_code != 204:
            raise APIError(f'API returned {req.status_code}')


    def save(self, client: 'Client') -> None:
        endpoint = API_BASE + '/thread_bookmarks'
        req = client._session.post(endpoint, json = {
            'thread': '/threads/' + str(self.id),
            'user': '/users/' + client.id,
        })

        if req.status_code != 201:
            raise APIError(f'API returned {req.status_code}')


    @staticmethod
    def get_trend(items_per_page: int = 5) -> list['Thread']:
        endpoint = API_BASE + '/threads/trending'
        req = get(endpoint, headers = {'User-Agent': USER_AGENT}, params = {'itemsPerPage': items_per_page})

        resp = req.json()
        return [Thread(thread['id'],thread) for thread in resp['hydra:member']]


    @staticmethod
    def search(search: str, page: int = 1) -> list['Thread']:
        endpoint = API_BASE + '/threads/search'
        req = get(endpoint, headers = {'User-Agent': USER_AGENT}, params = {'page': page, 'search': search})

        resp = req.json()
        return [Thread(thread['id'],thread) for thread in resp['hydra:member']]


    @staticmethod
    def search_by_category(category: Union[Category, str], topic: Optional[Union[Topic, str]] = None) -> list['Thread']:
        category_id = category.id if isinstance(category, Category) else category
        topic_id = topic.id if isinstance(topic, Topic) else topic

        endpoint = API_BASE + '/categories/{}/threads'.format(category_id)
        endpoint += '?order[pinned]=DESC&order[trendingScore]=DESC'

        req = get(
            endpoint,
            headers = {'User-Agent': USER_AGENT},
            params = {'topics.id': topic_id} if topic is not None else None
        )

        resp = req.json()
        return [Thread(thread['id'],thread) for thread in resp['hydra:member']]



class Activity:
    r"""
    The part of the activity of a player.

    > id: the id of the activity part
    > type: the string backend type of the activity part
    """

    id: str
    type: str

    def __init__(self, id: str, type: str, count: int) -> None:
        self.id = id
        self.type = type
        self.count = count



class MessageCreated(Activity):
    r"""
    The part of the activity of a player when he replied to one or multiples threads.

    > threads: the threads where the messages was sent
    """

    threads: list[Thread]

    def __init__(self, *args, threads: list[dict[str]]) -> None:
        super().__init__(*args)
        self.threads = [Thread(thread['id'], thread) for thread in threads]



class ThreadCreated(Activity):
    r"""
    The part of the activity of a player when he created one or multiples threads.

    > threads: the created threads
    """

    threads: list[Thread]

    def __init__(self, *args, threads: list[dict[str]]) -> None:
        super().__init__(*args)
        self.threads = [Thread(thread['id'], thread) for thread in threads]

ActivityType = Union[Activity, MessageCreated, ThreadCreated]



class Player:
    r"""
    An account of the OneCube website. (a Minecraft player too)

    > id: the id of the player
    > ingame_id: the id of the player that is used ingame
    > username: the Minecraft username of the player
    > uuid: the unique identifier of the computer linked to the player account
    > rank: the rank of the player
    > threads: the threads where the player sent a message
    """

    id: str
    ingame_id: int
    username: str
    uuid: str
    rank: Rank
    threads: list[Thread]

    def __init__(self, id: str, infos: dict[str] = {}) -> None:
        self._session = Session()
        self._session.headers['User-Agent'] = USER_AGENT

        self.id = id
        infos = infos or self.load()

        self.id = infos['id']
        self.ingame_id = infos['playerId']
        self.username = infos['username']
        self.uuid = infos['uuid']
        self.rank = Rank(infos['rankName'], infos['rankColor'])


    def __str__(self) -> str:
        return self.username


    def __repr__(self) -> str:
        return '<{}~{} {} {}>'.format(self.rank.ansi, ANSI_RESET, self.rank.name, self)


    @property
    def icon_uri(self) -> str:
        endpoint = BASE + '/player/' + self.username
        req = self._session.get(endpoint)

        soup = BeautifulSoup(req.text, 'html.parser')
        elements = soup.find_all('img', {'alt': f'{self} avatar'})
        return BASE + next(elem.attrs.get('src') for elem in elements if '/_next/image' in elem.attrs.get('src'))


    @property
    def threads(self) -> list[Thread]:
        endpoint = API_BASE + '/users/{}/thread_subscriptions'.format(self.id)
        req = self._session.get(endpoint)

        resp = req.json()
        return [
            Thread(thread_subs['thread']['id'])
            for thread_subs in resp['hydra:member']
        ]


    @property
    def thread_bookmarks(self) -> list[Thread]:
        endpoint = API_BASE + '/users/{}/thread_bookmarks'.format(self.id)
        req = self._session.get(endpoint)

        resp = req.json()
        return [
            Thread(thread_bookmark['thread']['id'])
            for thread_bookmark in resp['hydra:member']
        ]


    @property
    def activity(self) -> list[ActivityType]:
        endpoint = API_BASE + '/game/players/{}/activity'.format(self.username)
        req = self._session.get(endpoint)

        if req.status_code != 200:
            raise APIError(f'API returned {req.status_code}')

        resp = req.json()
        activities = []

        for activity in resp['hydra:member']:
            args = (activity['id'], activity['type'], activity['count'])

            if activity['type'] == 'message_created':
                activities.append(MessageCreated(*args, threads = activity['threads']))

            elif activity['type'] == 'thread_created':
                activities.append(ThreadCreated(*args, threads = activity['threads']))

            else:
                activities.append(Activity(*args))

        return activities


    def load(self) -> dict:
        endpoint = API_BASE + '/game/players/' + self.id
        req = self._session.get(endpoint)

        if req.status_code == 400:
            raise NotFound(f'Cannot find player {self.id!r}')

        elif req.status_code != 200:
            raise APIError(f'API returned {req.status_code}')

        resp = req.json()
        return resp['user']



class Client(Player):
    r"""
    A logged OneCube account.

    > email:  the email of the account
    > password: the password of the account
    > cookie: the cookie used by cloudflare to protect attacks
    > token: the access token or session id (called same)
    > metadata: the metadata of the account
    """

    email: str
    password: str
    cookie: str
    token: str
    metadata: dict[str]

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password

        self.cookie = self.get_cookie()
        infos = self.login()
        self.update(infos)


    @property
    def unread_notifications(self) -> int:
        endpoint = API_BASE + '/users/{}/unreadNotifications'.format(self.id)
        req = self._session.get(endpoint)

        resp = req.json()
        return resp['unreadNotifications']


    @property
    def total_subscriptions(self) -> int:
        endpoint = API_BASE + '/users/{}/subscriptions'.format(self.id)
        req = self._session.get(endpoint, headers = {'X-Auth-Token': self.token})

        resp = req.json()
        return resp['hydra:totalItems']


    def update(self, infos: dict[str]) -> None:
        self.token = infos['sessionId']
        self.metadata = infos['user']['metadata']

        super().__init__(infos['user']['username'])
        self._session.headers.update({'User-Agent': USER_AGENT, 'X-Auth-Token': self.token, 'Content-Type': 'application/ld+json; charset=utf-8'})


    def get_cookie(self) -> str:
        endpoint = BASE + '/cdn-cgi/challenge-platform/h/g/cv/result/77c835e91e85d251'
        req = post(endpoint)
        return req.headers['Set-Cookie'].split(';')[0]


    def login(self) -> dict[str]:
        endpoint = API_BASE + '/security/login'
        req = post(
            endpoint,
            headers = {'Cookie': self.cookie, 'User-Agent': USER_AGENT},
            json = {'email': self.email, 'password': self.password, 'rememberMe': False}
        )
        
        if req.status_code != 200:
            raise APIError(f'API returned {req.status_code}')

        resp = req.json()
        return resp


    def create_thread(self, name: str, content: str, category: Union[Category, str], topics: list[Union[Topic, str]] = []) -> Thread:
        endpoint = API_BASE + '/threads'
        req = self._session.post(endpoint, json = {
            'name': name,
            'category': category.backend_id if isinstance(category, Category) else category,
            'topics': [topic.backend_id if isinstance(topic, Topic) else topic for topic in topics],
            'user': '/users/' + str(self.id),
            'pinned': False,
            'open': True,
            'visible': True,
            'trendingUntilDate': None,
            'allowNotifications': True,
            'firstMessage': {
                'content': to_message_payload(content),
                'user': '/users/' + str(self.id),
                'medias': []
            }
        })
        
        print(req.status_code)
        print(req.text)


    def send_password_reset_token(self, email: Optional[str] = None) -> None:
        endpoint = API_BASE + '/security/password/token'
        req = self._session.post(endpoint, json = {'email': email or self.email})

        if req.status_code != 200:
            raise APIError(f'API returned {req.status_code}')


    def reset_password(self, reset_token: str, new_password: str, reconnect: bool = True) -> None:
        endpoint = API_BASE + '/security/password/reset'
        req = self._session.post(endpoint, json = {
            'token': reset_token,
            'password': new_password,
            'rememberMe': False
        })

        if req.status_code != 200:
            raise APIError(f'API returned {req.status_code}')

        if reconnect:
            self.password = new_password
            infos = req.json()
            self.update(infos)



class ShopProduct:
    r"""
    An item of the OneCube shop.

    > id: the id of the product
    > name: the name of the product
    > amount: the amount of the product unit
    > subscription: TODO
    > stripe_product_id: the id of the product from stripe
    > method_payments: the id of the product from stripe
    > eur_price: the price of the product in EURO
    > usd_price: the price of the product in DOLLAR
    > gbp_price: the price of the product in POUND
    > chf_price: the price of the product in CHF
    > cad_price: the price of the product in CAD
    """

    id: int
    name: str
    amount: int
    subscription: bool
    stripe_product_id: str
    method_payments: list[str]
    eur_price: float
    usd_price: float
    gbp_price: float
    chf_price: float
    cad_price: float

    def __init__(self, infos: dict[str]) -> None:
        self.id = infos['id']
        self.name = infos['name']
        self.amount = infos['amount']
        self.subscription = infos['subscription']
        self.stripe_product_id = infos['stripeProductId']

        self.method_payments = [
            method for method in (
                'CreditCard', 'PaysafeCard', 'Paypal',
                'Dedipass', 'Mollie', 'Stripe'
            ) if infos['allow' + method]
        ]

        self.eur_price = infos['priceEUR']
        self.usd_price = infos['priceUSD']
        self.gbp_price = infos['priceGBP']
        self.chf_price = infos['priceCHF']
        self.cad_price = infos['priceCAD']


    def __str__(self) -> str:
        return self.name


    def __repr__(self) -> str:
        return '<Product {} ()>'




class ShopMeta(type):

    @property
    def items(self) -> list[ShopProduct]:
        endpoint = API_BASE + '/shop_products'
        req = get(endpoint, headers = {'User-Agent': USER_AGENT})

        if req.status_code != 200:
            raise APIError(f'API returned {req.status_code}')

        resp = req.json()
        items = resp['hydra:member']
        return [ShopProduct(item) for item in items]


    def __repr__(self) -> str:
        return '<OneCube Shop>'



class Shop(metaclass = ShopMeta):
    r"""
    The shop of the OneCube website.

    > items: the list of the shop products
    """


    items: list[ShopProduct]



# why did I do that, I could have just made a .get system :(

Categories.ANNOUNCES_AND_RULES = Category(1, {'@id': '/categories/1', 'name': 'Annonces et règles', 'slug': 'annonces-et-regles', 'color': 'red'})
Categories.NEWS = Category(2, {'@id': '/categories/2', 'name': 'Actualités', 'slug': 'actualites', 'color': 'red'})
Categories.GENERAL_DISCUSSION = Category(3, {'@id': '/categories/3', 'name': 'Discussions générales', 'slug': 'discussions-generales', 'color': 'sky'})
Categories.SUGGGESTIONS = Category(4, {'@id': '/categories/4', 'name': 'Suggestions', 'slug': 'suggestions', 'color': 'sky'})
Categories.REPORT_AND_BUGS = Category(5, {'@id': '/categories/5', 'name': 'Signalement bugs', 'slug': 'bugs', 'color': 'sky'})
Categories.TIPS_AND_HELP = Category(6, {'@id': '/categories/6', 'name': 'Astuces et entraide', 'slug': 'astuces-et-entraide', 'color': 'sky'})
Categories.OFF_TOPIC = Category(7, {'@id': '/categories/7', 'name': 'Hors sujet', 'slug': 'hors-sujet', 'color': 'sky'})
Categories.CREATION = Category(8, {'@id': '/categories/8', 'name': 'Créations', 'slug': 'creations', 'color': 'sky'})

Topics.PVP_SWAP = Topic(1, {'@id': '/topics/1', 'id': 1, 'name': 'PvpSwap', 'color': 'purple', 'views': 0, 'threadsCount': 150, 'messagesCount': 316, 'lastViewUpdate': '2022-11-22T17:25:27+00:00', 'createdAt': '2022-11-22T17:25:27+00:00', 'updatedAt': '2022-12-20T15:48:27+00:00'})
Topics.BEDWARS = Topic(2, {'@id': '/topics/2', 'id': 2, 'name': 'Bedwars', 'color': 'rose', 'views': 0, 'threadsCount': 169, 'messagesCount': 327, 'lastViewUpdate': '2022-11-22T17:28:11+00:00', 'createdAt': '2022-11-22T17:28:11+00:00', 'updatedAt': '2022-12-20T15:48:27+00:00'})
Topics.UHC = Topic(3, {'@id': '/topics/3', 'id': 3, 'name': 'UHC', 'color': 'yellow', 'views': 0, 'threadsCount': 126, 'messagesCount': 273, 'lastViewUpdate': '2022-11-22T17:28:11+00:00', 'createdAt': '2022-11-22T17:28:11+00:00', 'updatedAt': '2022-12-20T15:48:27+00:00'})
Topics.UHC_RUN = Topic(4, {'@id': '/topics/4', 'id': 4, 'name': 'UHC Run', 'color': 'orange', 'views': 0, 'threadsCount': 155, 'messagesCount': 295, 'lastViewUpdate': '2022-11-22T17:28:11+00:00', 'createdAt': '2022-11-22T17:28:11+00:00', 'updatedAt': '2022-12-20T15:48:27+00:00'})
Topics.BLOCK_RUN = Topic(5, {'@id': '/topics/5', 'id': 5, 'name': 'BlockRun', 'color': 'green', 'views': 0, 'threadsCount': 58, 'messagesCount': 181, 'lastViewUpdate': '2022-11-22T17:28:11+00:00', 'createdAt': '2022-11-22T17:28:11+00:00', 'updatedAt': '2022-12-20T15:48:27+00:00'})
Topics.DE_A_COUDRE = Topic(6, {'@id': '/topics/6', 'id': 6, 'name': 'Dé à coudre', 'color': 'sky', 'views': 0, 'threadsCount': 68, 'messagesCount': 199, 'lastViewUpdate': '2022-11-22T17:28:11+00:00', 'createdAt': '2022-11-22T17:28:11+00:00', 'updatedAt': '2022-12-20T15:48:27+00:00'})
Topics.GRAPHICS = Topic(7, {'@id': '/topics/7', 'id': 7, 'name': 'Graphisme', 'color': 'amber', 'views': 0, 'threadsCount': 12, 'messagesCount': 43, 'lastViewUpdate': '2022-11-22T17:28:11+00:00', 'createdAt': '2022-11-22T17:28:11+00:00', 'updatedAt': '2022-12-16T17:13:52+00:00'})
Topics.RESOURCE_PACK = Topic(8, {'@id': '/topics/8', 'id': 8, 'name': 'Resource pack', 'color': 'amber', 'views': 0, 'threadsCount': 7, 'messagesCount': 21, 'lastViewUpdate': '2022-11-22T17:28:11+00:00', 'createdAt': '2022-11-22T17:28:11+00:00', 'updatedAt': '2022-12-06T08:32:46+00:00'})
Topics.BUILD = Topic(9, {'@id': '/topics/9', 'id': 9, 'name': 'Build', 'color': 'amber', 'views': 0, 'threadsCount': 8, 'messagesCount': 15, 'lastViewUpdate': '2022-11-22T17:28:11+00:00', 'createdAt': '2022-11-22T17:28:11+00:00', 'updatedAt': '2022-12-20T00:43:22+00:00'})
Topics.WEBSITE = Topic(10, {'@id': '/topics/10', 'id': 10, 'name': 'Site', 'color': 'amber', 'views': 0, 'threadsCount': 64, 'messagesCount': 139, 'lastViewUpdate': '2022-11-22T17:28:11+00:00', 'createdAt': '2022-11-22T17:28:11+00:00', 'updatedAt': '2022-12-20T13:09:38+00:00'})
Topics.FORUM = Topic(11, {'@id': '/topics/11', 'id': 11, 'name': 'Forum', 'color': 'amber', 'views': 0, 'threadsCount': 70, 'messagesCount': 171, 'lastViewUpdate': '2022-11-22T17:28:11+00:00', 'createdAt': '2022-11-22T17:28:11+00:00', 'updatedAt': '2022-12-20T13:09:38+00:00'})
Topics.HUB = Topic(12, {'@id': '/topics/12', 'id': 12, 'name': 'Hub', 'color': 'lime', 'views': 0, 'threadsCount': 149, 'messagesCount': 275, 'lastViewUpdate': '2022-11-22T17:28:11+00:00', 'createdAt': '2022-11-22T17:28:11+00:00', 'updatedAt': '2022-12-20T15:48:23+00:00'})