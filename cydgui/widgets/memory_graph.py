import gc
import framebuf
from .async_canvas import AsyncCanvas
from cydgui.utils.colors import Colors


class MemoryGraphWidget(AsyncCanvas):
    """
    Gráfico de memória livre fatiado em bandas horizontais para consumo mínimo de RAM.
    """

    def __init__(self, max_samples=60, interval_ms=1000, **kwargs):
        super().__init__(interval_ms=interval_ms, **kwargs)

        self.max_samples = max_samples
        self.samples = []
        
        # Altura de cada fatia (banda). 16 é um excelente equilíbrio de performance/RAM
        self.BAND_H = 16
        self.buf = None
        self.fbuf = None

    # ---------------------------------------------------------
    # UPDATE (async state)
    # ---------------------------------------------------------

    async def update_async(self):
        free = gc.mem_free()
        self.samples.append(free)

        if len(self.samples) > self.max_samples:
            self.samples.pop(0)

    # ---------------------------------------------------------
    # DRAW (Fatiado em bandas horizontais)
    # ---------------------------------------------------------

    def on_draw(self):
        if not self.samples:
            return

        w = self.width
        h = self.height

        # ---------------------------------------------------------
        # Mini Buffer Estático (Ex: 240 x 16 x 2 = ~7.6 KB)
        # ---------------------------------------------------------
        if self.buf is None:
            self.buf = bytearray(w * self.BAND_H * 2)
            self.fbuf = framebuf.FrameBuffer(self.buf, w, self.BAND_H, framebuf.RGB565)

        max_val = max(self.samples)
        min_val = min(self.samples)
        rng = max(max_val - min_val, 1)

        n = len(self.samples)
        step_x = w / max(n - 1, 1)

        # Passo 1: Pré-calcula os pontos globais do gráfico para evitar reprocessamento
        points = []
        for i, value in enumerate(self.samples):
            x = int(i * step_x)
            norm = (value - min_val) / rng
            y = int((h - 2) - norm * (h - 3)) + 1
            points.append((x, y))

        ax = self.absolute_x
        ay = self.absolute_y
        COR_BORDA = Colors.GRAY if hasattr(Colors, 'GRAY') else 0x7BEF

        # ---------------------------------------------------------
        # LOOP DE RENDERIZAÇÃO POR BANDAS HORIZONTAIS
        # ---------------------------------------------------------
        for y_start in range(0, h, self.BAND_H):
            y_end = min(y_start + self.BAND_H, h)
            current_bh = y_end - y_start  # Altura real desta banda (a última pode ser menor)

            # Limpa a fatia atual na RAM
            self.fbuf.fill(0)

            # Desenha as bordas (apenas se caírem dentro desta fatia de Y)
            if y_start == 0:
                self.fbuf.line(0, 0, w - 1, 0, COR_BORDA)  # Borda Superior
            if y_end == h:
                self.fbuf.line(0, h - 1 - y_start, w - 1, h - 1 - y_start, COR_BORDA)  # Borda Inferior
            
            # Bordas Laterais (sempre desenhadas na altura da fatia corrente)
            self.fbuf.line(0, 0, 0, current_bh - 1, COR_BORDA)
            self.fbuf.line(w - 1, 0, w - 1, current_bh - 1, COR_BORDA)

            # Desenha o gráfico transladado para a coordenada local da fatia
            for i in range(1, len(points)):
                prev_x, prev_y = points[i - 1]
                x, y = points[i]

                # Subtraímos y_start para mapear o Y global para o Y local do mini buffer.
                # O framebuf em C descarta automaticamente o que estiver fora de [0, BAND_H-1]
                self.fbuf.line(prev_x, prev_y - y_start, x, y - y_start, Colors.CYAN)

            # Despeja APENAS esta fatia na tela
            self.renderer.block(
                ax,
                ay + y_start,
                ax + w - 1,
                ay + y_end - 1,
                self.buf  # Enviará apenas os bytes necessários baseados na altura informada acima
            )

        # ---------------------------------------------------------
        # Passo 3: Texto por cima de tudo no final
        # ---------------------------------------------------------
        text = "Mem.: {:.2f} kB".format(self.samples[-1] / 1024)
        self.draw_text(4, 4, text, Colors.WHITE)
