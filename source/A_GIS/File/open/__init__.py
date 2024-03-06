def open(*, path: type["pathlib.Path"], binary=False, chunk_size=1024):
    import requests
    import builtins
    import zlib
    import A_GIS.File.is_url

    class _HttpFile:
        # Assuming other parts of your class remain the same

        def __init__(self, url, chunk_size=1024, binary=False):
            self.response = requests.get(url, stream=True)
            self.response.raise_for_status()  # Ensure we got a successful response
            self.chunk_size = chunk_size
            self.buffer = b""  # Use bytes for buffer
            self.binary = binary
            self.decompressor = None

            # Check if content is compressed and prepare decompressor if
            # necessary
            content_encoding = self.response.headers.get(
                "Content-Encoding", ""
            )
            if content_encoding == "gzip":
                self.decompressor = zlib.decompressobj(
                    16 + zlib.MAX_WBITS
                )  # gzip decompression

        def readline0(self):
            if self.binary:
                raise NotImplementedError(
                    "readline is not implemented for binary mode."
                )

            newline_pos = self.buffer.find(b"\n")
            while newline_pos == -1:
                chunk = self.response.raw.read(self.chunk_size)
                if self.decompressor:
                    chunk = self.decompressor.decompress(chunk)
                if not chunk:
                    result, self.buffer = self.buffer, b""
                    return result
                self.buffer += chunk
                newline_pos = self.buffer.find(b"\n")

            result, self.buffer = (
                self.buffer[: newline_pos + 1],
                self.buffer[newline_pos + 1 :],
            )
            return result

        def readline(self):
            result = self.readline0()
            if self.binary:
                return result
            else:
                return result.decode("utf-8")

        def read0(self, size=-1):
            # Handle as binary data
            if size == -1:
                if self.buffer:
                    result = self.buffer + self.response.raw.read()
                    if self.decompressor:
                        result = self.decompressor.decompress(result)
                    self.buffer = b""
                    return result
                else:
                    result = self.response.raw.read()
                    if self.decompressor:
                        result = self.decompressor.decompress(result)
                    return result

            else:
                while len(self.buffer) < size:
                    chunk = self.response.raw.read(self.chunk_size)
                    if self.decompressor:
                        chunk = self.decompressor.decompress(chunk)
                    if not chunk:
                        break
                    self.buffer += chunk
                result, self.buffer = self.buffer[:size], self.buffer[size:]
                return result

        def read(self):
            result = self.read0()
            if self.binary:
                return result
            else:
                return result.decode("utf-8")

        def __iter__(self):
            return self

        def __next__(self):
            line = self.readline()
            if line:
                return line
            else:
                raise StopIteration

    mode = "r"
    if binary:
        mode += "b"

    if A_GIS.File.is_url(path):
        return _HttpFile(path, chunk_size=chunk_size, binary=binary)
    else:
        return builtins.open(path, mode)
