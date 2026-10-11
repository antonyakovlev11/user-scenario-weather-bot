"""Новая учебная демонстрация состояний диалога. Погодный API не подключён."""
from enum import Enum, auto

PLACES = {
    "москва": [("moscow", "Москва")],
    "киров": [("kirov_43", "Киров, Кировская область"), ("kirov_40", "Киров, Калужская область")],
}
PERIODS = {"сегодня": "today", "завтра": "tomorrow"}


class State(Enum):
    PLACE = auto()
    CHOICE = auto()
    PERIOD = auto()
    READY = auto()


class Dialog:
    def __init__(self):
        self.state = State.PLACE
        self.options = []
        self.place = None
        self.request = None

    def handle(self, message):
        message = message.strip().casefold()
        if self.state == State.PLACE:
            if not message:
                return "Укажите населённый пункт."
            self.options = PLACES.get(message, [])
            if not self.options:
                return "Место не найдено в учебном справочнике. Уточните название."
            if len(self.options) > 1:
                self.state = State.CHOICE
                return "Выберите номер: " + "; ".join(f"{i+1}. {place[1]}" for i,place in enumerate(self.options))
            self.place = self.options[0]
            self.state = State.PERIOD
            return "Выберите период: сегодня или завтра."
        if self.state == State.CHOICE:
            if not message.isdecimal() or not 1 <= int(message) <= len(self.options):
                return "Укажите номер из списка."
            self.place = self.options[int(message)-1]
            self.state = State.PERIOD
            return "Выберите период: сегодня или завтра."
        if self.state == State.PERIOD:
            if message not in PERIODS:
                return "Доступны периоды: сегодня или завтра."
            self.request = {"place_id": self.place[0], "period": PERIODS[message]}
            self.state = State.READY
            return f"Параметры запроса готовы: {self.request}. В демонстрации API не подключён."
        return "Сценарий завершён. Для нового запроса создайте новый Dialog."


if __name__ == "__main__":
    dialog = Dialog()
    for text in ["", "Неизвестное место", "Киров", "9", "1", "неделя", "сегодня"]:
        print(f"> {text!r}\n{dialog.handle(text)}")
