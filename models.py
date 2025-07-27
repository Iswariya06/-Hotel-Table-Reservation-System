class ReservationManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.tables = {i: Table(i) for i in range(1, 11)}  # Default 10 tables
            cls._instance.observers = []
        return cls._instance

    def get_all_tables(self):
        return self.tables

    def add_table(self, table_id):
        if table_id not in self.tables:
            self.tables[table_id] = Table(table_id)

    def reserve_table(self, table_id, user, time_slot):
        if table_id in self.tables:
            success = self.tables[table_id].reserve(user, time_slot)
            if success:
                self.notify_observers(f"Table {table_id} reserved by {user.name} at {time_slot}.")
            return success
        return False

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.notify(message)


class User:
    def __init__(self, name):
        self.name = name
        self.notifications = []

    def notify(self, message):
        self.notifications.append(message)


class Table:
    def __init__(self, table_id):
        self.table_id = table_id
        self.state = AvailableState()

    def reserve(self, user, time_slot):
        return self.state.reserve(self, user, time_slot)

    def cancel(self):
        return self.state.cancel(self)


class TableState:
    def reserve(self, table, user, time_slot):
        raise NotImplementedError

    def cancel(self, table):
        raise NotImplementedError


class AvailableState(TableState):
    def reserve(self, table, user, time_slot):
        table.state = ReservedState()
        table.reservation_details = {"user": user, "time_slot": time_slot}
        return True


class ReservedState(TableState):
    def reserve(self, table, user, time_slot):
        return False

    def cancel(self, table):
        table.state = AvailableState()
        table.reservation_details = None
        return True
