class Fila:
    def __init__(self):
        self._itens = []
    
    def enqueue(self, item) -> None:
        self._itens.append(item)
    
    def vazia(self) -> bool:
        return len(self._itens) == 0
    
    def tamanho(self) -> int:
        return len(self._itens)
    
    def listar(self) -> list:
        return list(self._itens)
    
    def dequeue(self) -> int:
        if self.vazia():
            return None
        
        return self._itens.pop(0)
    
    