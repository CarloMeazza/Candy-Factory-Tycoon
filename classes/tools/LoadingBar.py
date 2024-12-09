import pygame
import time


class LoadingBar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, max_time, color=(156, 74, 33)):
        """
        Inizializza una barra di caricamento come Sprite.

        :param x: Coordinata X della barra
        :param y: Coordinata Y della barra
        :param width: Larghezza della barra
        :param height: Altezza della barra
        :param max_time: Tempo massimo per completare il caricamento
        :param color: Colore della barra di caricamento
        """
        super().__init__()

        # Rettangolo e dimensioni
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.color = color

        # Stato temporale
        self.max_time = max_time
        self.current_time = 0
        self.last_update_time = time.time()

    def update(self):
        """
        Aggiorna lo stato della barra di caricamento in base al tempo trascorso.
        """
        if self.max_time == 0:
            return  # Se max_time è 0, non aggiornare

        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now

        self.current_time += dt
        if self.current_time > self.max_time:
            self.current_time = 0

        # Aggiorna l'immagine della barra di caricamento
        self._update_image()

    def _update_image(self):
        """
        Aggiorna la superficie che rappresenta la barra di caricamento.
        """
        self.image.fill((82, 39, 28))
        if self.max_time > 0:
            # Calcola la larghezza del riempimento
            fill_width = int(self.rect.width * self.current_time / self.max_time)
            fill_rect = pygame.Rect(0, 0, fill_width, self.rect.height)

            # Disegna la parte riempita
            self.image.fill(self.color, fill_rect)

        # Disegna il contorno
        pygame.draw.rect(self.image, (45, 20, 22), self.image.get_rect(), 2)

    def set_max_time(self, new_max_time):
        """
        Imposta un nuovo tempo massimo per il caricamento.

        :param new_max_time: Nuovo tempo massimo.
        """
        if self.max_time != new_max_time:
            self.max_time = new_max_time
            self.current_time = 0
