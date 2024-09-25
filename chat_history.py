class ChatHistory:
    def __init__(self, max_entries=10):
        """
        Inisialisasi ChatHistory dengan kapasitas maksimum.

        :param max_entries: Jumlah maksimum riwayat obrolan yang dapat disimpan.
        """
        self.max_entries = max_entries
        self.context = []

    def add_context(self, user_input, ai_response):
        """
        Menambahkan riwayat obrolan baru.

        :param user_input: Input pengguna.
        :param ai_response: Respon AI.
        """
        self.context.append(
            {"user_input": user_input, "ai_response": ai_response})
        if len(self.context) > self.max_entries:
            self.context = self.context[-self.max_entries:]

    def get_context(self):
        """
        Mengambil riwayat obrolan.

        :return: Daftar riwayat obrolan.
        """
        return self.context
