from dataclasses import dataclass


@dataclass
class UndoOperation:
    target_object: object
    handler: object
    args: tuple


class UndoManager:
    __undo_operations = []

    @staticmethod
    def register_operation(target_object, handler, *args):
        UndoManager.__undo_operations.append(UndoOperation(target_object, handler, args))

    # args=(1,"p1",100)
    # add_product(args) -> add_product((1,"p1",100))
    # add_product(*args) -> add_product(1,"p1",100)
    @staticmethod
    def undo():
        # todo: check empty list
        undo_operation = UndoManager.__undo_operations.pop()
        undo_operation.handler(undo_operation.target_object, *undo_operation.args)
