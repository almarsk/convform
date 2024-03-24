from posixpath import join


class ProofException(Exception):
    def __init__(self, issues):
        newline = '\n'
        self.message = f"{newline.join(str(issue) for issue in issues)}"
        super().__init__(self.message)
